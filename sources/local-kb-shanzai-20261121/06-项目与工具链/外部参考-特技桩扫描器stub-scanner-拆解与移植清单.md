# 外部参考 `stub-scanner-reference`：特技桩扫描器拆解与移植清单

> 建立 2026-10-15｜对象：`大鲸鱼产生专用\_外部源码\caocao-mod-public-knowledge-base\...\07-工具参考\stub-scanner-reference\`
> （上游自述：识别规则由 **一个 6.5pl 样本**提炼；**不捆绑任何引擎地址**）
> 核查对象样本：`Ekd5.exe`，SHA `25DB2211FE8F495DE4993BAB296C23C180E18679F00A0E43B47B1FD2034B7EAF`（339 备份 / 46 补丁）。

## 结论速览

1. 它是**纯只读**的 PE32 桩候选扫描器：`pe.py`（节表/VA→偏移）+ `stub_scan.py`（扫 E8 + 反汇编桩参数）+ `arg_stub.py`（调用方循环区间）+ `scan_engine.py`（CLI）。
2. **目标地址不写在代码里，全部来自 `--profile` JSON**：`dispatch_ranges`（**被调用者**地址区间，不是扫描区间！）+ `inline_core_targets`（内联核心地址）。⇒ 移植成本主要在"填 profile"，其次是替换 4 处指令形态假设。
3. 扫描范围 = **除 `.rsrc` 外的所有节、整节 `raw_size`、逐字节找 `E8`**；**没有** `IMAGE_SCN_MEM_EXECUTE`/`CNT_CODE` 判定 ⇒ 数据区会参与误报。
4. 参数还原是**基于位置的启发式**（假设压栈顺序 = eff, stack, equip, per），只认 `push imm8/imm32`、`push eax`（个人号）、`push ecx`（装备号）、`add al/eax,base`（参数化桩）、`push dword ptr [ebp+正偏移]`（包装桩）。**负偏移 `[ebp-XX]` 一律不识别**。
5. ★ **对 `Ekd5.exe` 的实测适配风险**：当前样本 `0x43F1E8` 处是 `push [ebp-0x2C]; push [ebp+8]; push [ebp-4]; call 0x43C31D` —— 3 个实参里 2 个是负偏移，**包装桩识别（`arg_pushes>=3`）与 `_collect_pushes` 都会漏/中断** ⇒ 直接跑会大面积落到"异常/mov桩"分支。
6. `0x43F27F` 现为 `E9 F7 8A 01 00`（跳到 `0x458D7B`）= **已打过补丁**，不再是原生链尾；任何地址结论须按当前 SHA 现读（`_样本时间线.py`）。

## 适用版本

- 参考实现来源：6.5pl 样本经验（其 README/`stub_scan.py:1-6` 自述）。
- 本次核查：复刻版 6.6山贼 `Ekd5.exe` SHA `25DB2211…4B7EAF`（PE32 / x86 / ImageBase `0x00400000` / 6 节）。
- 6.5 结论不得直接套 6.6；本页只做「可移植性核查」，未做任何实机验证。

## 已确认事实

### A. PE 侧（`core/pe.py`）

- `load_pe()`：`MZ` → `e_lfanew@0x3C` → `PE\0\0`；校验 `Machine==0x14C`(pe.py:23)、opt magic `0x10B`(pe.py:25)、`ImageBase@opt+28`(pe.py:27)；节表项 40 字节，取 `Name/+12 VirtualAddress/+16 SizeOfRawData/+20 PointerToRawData`(pe.py:35-38)。
- `va2off()`(pe.py:49-57)：`rva = va - ImageBase`，线性找 `sec.va <= rva < sec.va + sec.raw_size`，`off = sec.raw + (rva - sec.va)`。
- **对齐处理 = 不做**：直接把 `raw_size` 当虚拟大小用（未读 `VirtualSize`），因此不处理 `FileAlignment`/`SectionAlignment`。
- 扫描范围由 `_scan_e8()` 自己界定（stub_scan.py:14-19）：逐节 `data[s.raw:s.raw+s.raw_size]`，`base = ImageBase + s.va`，**只跳过名为 `.rsrc` 的节**。
- `Ekd5.exe` 实测节表（虚拟大小 vs 原始大小）：`.code 0x85000/0x84E00`、`.text1 0x5000/0x4800`、`.text2 0x33000/0x6800`、`.api 0x10000/0xF600`、`.text3 0x64000/0x64000`、`.rsrc 0x15000/0x15000`。⇒ ①`.text2` 有 `0x2C800` 字节"仅有虚拟大小"的尾部，按本实现视为**不可映射**；②`.api` 节名是**非 ASCII**（`latin1` 解码才不会抛异常，pe.py:35）；③原始布局连续无缝隙，无对齐空洞。

### B. 扫描与排序（`core/stub_scan.py`）

- 命中条件（stub_scan.py:28）：`E8 rel32` 的**目标** `tgt` 落在 `dispatch_ranges` 任一区间内，**或** `tgt ∈ inline_core_targets ∪ wrappers`。命中后 `i += 5`；未命中 `i += 1`（stub_scan.py:30-33，注释明确"假 E8 后仍逐字节找下一处"）。
- 序言定位：`_find_prologue_va()`(stub_scan.py:214-227) 在 `call_va-0x800` 内**反向逐字节**找 `55 8B EC` / `55 89 E5`。
- 包装桩：`_find_wrapper_cores()`(stub_scan.py:90-118) 找"内部 ≥3 个 `push dword ptr [ebp + X]` 后 call 内联核心"的函数，且要求 `pro` 不在 `dispatch_ranges`、`call_va - pro <= 0x40`。
- 参数解析：`_collect_pushes()`(stub_scan.py:37-87) 从 call 向前收集；`_parse()`(stub_scan.py:164-190) 按立即数个数分类：`4→标准桩`、`3→3参桩`、`≥5→多推桩`、含 `add al/eax`→`参数化桩`、含 `push eax`→`动态桩`、否则`异常`。
- `mov al` 桩：`_moval_nums()`(stub_scan.py:121-161)，要求 call 前 `0x10` 字节内有 `push eax`，取 `push eax` 之前本函数内所有 `mov al, imm`。
- **去重/排序/打分**：`found` 按 `sorted(hits)`（即 `(call_va, tgt)` 地址升序）输出；`wrappers` 用 `set` 去重；**没有置信度评分、没有 per 去重、没有跨节同址合并**。

### C. 参数/循环还原（`core/arg_stub.py`）

- `find_arg_stub_cores()`(arg_stub.py:21-50)：识别 `push 0; push 1; push eq-imm; push [ebp+8]; call 核心` 形态（`[ebp+8]` 字符串精确匹配 arg_stub.py:35，`imm_n>=3`，`call-pro<=0x40`）。
- `arg_stub_range()`(arg_stub.py:73-116)：在其调用者里找 `push imm32`(首字节 `0x68`，arg_stub.py:98) 取 `start`，找 `cmp dword ptr [ebp - X], N`(arg_stub.py:106) 取 `max_n`，返回**闭区间** `(start, start+max_n-1)`(arg_stub.py:115)。
- `_callers_of()`(arg_stub.py:53-70) 是**第二份独立 E8 扫描器**（与 `_scan_e8` 实现不同）。

### D. 命令行（`scan_engine.py`）

```
python -m pip install -r requirements.txt        # 仅 capstone==5.0.9
python scan_engine.py <engine.exe> --profile <profile.json> [--output out.json]
```
输出 JSON：`stubs[]`（`call/tgt/kind/type/eff/stack/equip/per/per_expr/moval_nums/start/push_vas` + 可选 `name`）、`arg_stub_ranges[]`、`notes[]`。profile 缺省为 `profile.example.json` 的四个空字段（`dispatch_ranges`/`inline_core_targets` 两者不能同时为空，否则 CLI 报错，scan_engine.py:34-35）。

### E. 移植到 `Ekd5.exe` 的实测证据（静态复读）

- `VA 0x43F1E8 -> off 0x03E5E8`：`FF 75 D4 FF 75 08 FF 75 FC E8 27 D1 FF FF` =
  `push dword ptr [ebp-0x2C]; push dword ptr [ebp+8]; push dword ptr [ebp-4]; call 0x43C31D`。
- `VA 0x43F27F -> off 0x03E67F`：`E9 F7 8A 01 00 90 90 90` ⇒ 跳到 `0x458D7B`（**已占用/已打补丁**）。

## 实现·使用方法（若要真跑）

1. 复制 `profile.example.json` → 填 `dispatch_ranges`（**被调用者**地址区间，左闭右开）+ `inline_core_targets`（内联核心 VA）；可填 `dispatch_body` 排除调度体内的调用记录。
2. `python scan_engine.py "…\Ekd5.exe" --profile 你的.json --output 结果.json`（`--output` 不得等于被扫文件，scan_engine.py:78-79）。
3. 结果一律当**候选**：回反汇编器核对 `call` 前后控制流，按目标文件原始字节复核地址与字段（README「维护和限制」）。

## 风险与边界

### 需替换的样本硬编码（常量名 + 文件:行）

| # | 常量/假设 | 位置 | 说明 |
|---|---|---|---|
| 1 | `machine != 0x14C`（PE32 x86 校验） | pe.py:23 | 换非 x86 或 PE32+ 直接抛错 |
| 2 | opt magic `!= 0x10B` | pe.py:25 | PE32+ 的 `0x20B` 被拒 |
| 3 | `ImageBase@opt+28`、节项 `+12/+16/+20` | pe.py:27,36-38 | PE32 布局硬编码 |
| 4 | 用 `raw_size` 当虚拟大小 | pe.py:54,65-67 | 未读 `VirtualSize`；`vsize>rawsize` 的节有"不可映射尾部" |
| 5 | 跳过节名 `.rsrc` | stub_scan.py:16、arg_stub.py:56 | 只认这一个名字（Ekd5 恰好有 `.rsrc`，但 `.api` 名非 ASCII） |
| 6 | 只认 `E8`（rel32 直接调用） | stub_scan.py:23,27；arg_stub.py:62-64 | 漏 `FF 15`/`FF D7` 间接调用、`E9` 尾跳、thunk |
| 7 | `call_va - pro > 0x800` 阈值 | stub_scan.py:132,242；stub_scan.py:214(`max_back=0x800`) | 远距离桩漏检 |
| 8 | `call_va - pro <= 0x40`（"桩很短"阈值） | stub_scan.py:115；arg_stub.py:48 | 桩体 >0x40 字节即漏（Ekd5 特技代码普遍更长） |
| 9 | `push eax` = 个人号、`push ecx` = 装备号 | stub_scan.py:50,59 | 寄存器语义是**该样本的约定**，非通用 |
| 10 | `sum(imm) >= 4` 后停止收集更早 `push eax` | stub_scan.py:55 | "标准桩/3参桩已齐"的样本假设 |
| 11 | `calc_skip > 6` 算术指令上限 | stub_scan.py:79-83 | 计算序列更长就截断 |
| 12 | `add al/eax, base` 参数化桩 + `& 0xFF` | stub_scan.py:66-75 | 特技号 8 位、基数加法形态 |
| 13 | `mov al, imm` 仅在 `op_str.startswith('al, 0x')` 时识别 | stub_scan.py:156 | **capstone 对小立即数渲染成十进制**（见 stub_scan.py:68 注释）⇒ `mov al, 5` 这类**会漏** |
| 14 | `push dword ptr [ebp +`（只认正偏移） | stub_scan.py:103 | 漏 `[ebp-XX]` 局部/参数镜像、`[esp+X]` 完全漏 |
| 15 | `arg_pushes >= 3` | stub_scan.py:111 | 包装桩阈值 |
| 16 | `imm_n >= 3`、`[ebp + 8]` 精确串匹配 | arg_stub.py:35,46 | 只认第一个参数在 `ebp+8` |
| 17 | `push` 首字节 `0x68`、`& 0xFFFF`、`0<=v<=0xFF` | arg_stub.py:98-100 | 起始号 ≤255 且必须是 imm32 |
| 18 | `1 <= max_n <= 0x100` | arg_stub.py:110 | 循环次数上限 |
| 19 | `call - pro > 0x400` | arg_stub.py:86 | 调用者函数长度阈值 |
| 20 | `get_skill_name(entry_size=16, encoding='gbk')`、`skill_id<=0xFF` | stub_scan.py:292-297 | 名表步长/编码/编号范围 |
| 21 | 反汇编窗口 `back=40`、`call_va+5`、序言字节 `55 8B EC`/`55 89 E5` | stub_scan.py:239,243,223-225 | 无帧指针函数（`/Oy`、`sub esp` 开头）定位不到 |
| 22 | 参数语义位序 `eff, stack, equip, per` | stub_scan.py:169-190,200-211 | 位置假设，非结构证明 |

### 明显局限 / bug 风险

1. **两份 E8 扫描器规则不一致**：`_scan_e8` 假 E8 后 `i += 1`（stub_scan.py:33），而 `_callers_of` 任何 `E8` 都 `i += 5`（arg_stub.py:62-67）⇒ 后者会把"恰好是 `0xE8` 的立即数/操作数字节"当成指令吞掉 5 字节，**可能漏掉紧随其后的真 call**。
2. `va2off`/`read_va` **跨节即失败**：`_find_prologue_va` 读 `[call_va-0x800, call_va)` 要求整段在同一节内，节首附近的桩**一定**定位不到序言（read_va 返回 `None`），退化到 `back=40` 线性回溯，容易错位反汇编。
3. **反汇编未做指令边界同步**：仅靠 `55 8B EC` 猜序言；数据区中假序言 → 后续解析全错（无任何校验和/控制流验证）。
4. `_moval_nums` 返回的是**该函数内 `push eax` 之前的全部 `mov al`**（`sorted(set(...))`，stub_scan.py:152-161）⇒ 一个函数里有多处桩时，候选号会互相污染，且丢失"哪个号对应哪个调用点"的映射。
5. `_parse` 纯按立即数**个数**分类；`≥5` 时把 `imms[0]/[1]/[2]/[-1]` 强行当成 eff/stack/equip/per（stub_scan.py:186-189），无交叉验证。
6. `arg_stub_range` 里 `max_n` 会被后续 `cmp` **反复覆盖**（取最后一个），`start` 取第一个 `push imm32`（可能不是循环起点）⇒ 区间可能偏。
7. `scan_stubs()` 内部再 `load_pe(engine_path)`（stub_scan.py:257），而 CLI 已 `load_pe` 过一次（scan_engine.py:51）⇒ 整个文件被读两遍、解析两次；大文件纯浪费。
8. 无 `IMAGE_SCN_MEM_EXECUTE`/`CNT_CODE` 过滤 ⇒ 资源外数据区、填充区都会产生候选；`.rsrc` 之外的节名无法排除。
9. `notes` 自述：**源码定义桩、仅代码洞签名桩、间接调用、跨函数参数准备一律不覆盖**；识别规则只覆盖"能由配置目标命中且符合所列指令模式"的子集。
10. 无去重键（同一 `call_va` 命中多个 tgt 时理论上可重复）、无置信度、无 `--min-score` 之类过滤；结果全量靠人看。

## 证据来源

- 源码：`核心 4 文件 + scan_engine.py + README.md + requirements.txt`（路径见文首），行号已在正文标注。
- `Ekd5.exe` 节表/ImageBase/SHA：`mcp__kb__exe_info`（2026-10-15 现读）。
- 补丁态：`_样本时间线.py`（SHA `25DB2211…`，339 备份 / 46 补丁）。
- 字节证据：`mcp__kb__exe_bytes 0x43F1E8` / `0x43F27F`（静态复读，未实机验证）。
- 类型：**工具源码 + 静态复读**；本页**不含**实机命中结论。

## 待验证项

- P1：按当前 SHA 确认 Ekd5 的"内联核心"真实 VA（`0x43F1E8` 处 call 的 `0x43C31D` 是否即该核心）与 `dispatch_ranges` 候选区间，再决定是否真跑本扫描器。
- P2：`0x43F27F` 的 `E9 → 0x458D7B` 属于哪一篇补丁（46 篇内查），确认"链尾插槽已被占用"。
- P2：capstone 5.0.9 对 `mov al, imm8` 的实际 `op_str` 渲染规则，量化第 13 条的漏检比例。
- P2：`Ekd5.exe` 是否存在 `push imm8×4 + call` 形态的标准桩（决定本参考实现是否值得移植）。
