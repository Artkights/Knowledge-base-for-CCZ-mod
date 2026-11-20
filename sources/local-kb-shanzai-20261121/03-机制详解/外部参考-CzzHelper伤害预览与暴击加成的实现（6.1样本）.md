# 外部参考：CzzHelper「友军/敌军伤害预览 + 暴击加成」是怎么做的（6.1 样本）

> **本页回答**：`ai使用库\CzzHelper及源码\` 这份**2017 年的外置辅助 DLL**（CzzHelper v3.09b / 面向 5.9~S6.1）
> 是用什么手法做到「**在伤害预览里显示暴击加成**」的；哪些手法可以搬到本工作区的 6.6 补丁、哪些不能。
> 建立：2026-10-15（用户口径：「这个是早期加速补丁及其源码，那的应该是外置的预览，
> 能实现暴击伤害的预览，不过版本比较老，适配的是6.1的，需要思考调试」）。
> **证据类型：对方源码正文（C/C++，GBK）+ 本样本 `Ekd5.exe` 离线字节复读**；
> **本页所有"结论"分三档标注：`[对方源码]` / `[本样本复读]` / `[待实机]`。**

## 结论速览

1. **★ 对方的核心手法 = 钩住游戏自己的"伤害计算函数"，用它的 `bIsPreview` 形参区分预览与实战**，
   预览时就地加成、把加成后的值**当函数返回值交还给引擎** —— 引擎直接拿去显示 ⇒ **预览数字就带暴击了**。
   ```
   引擎（预览显示 / 实战结算）
        │ call 0x43BC62（6.1 伤害公式）
        ▼
   CheatFunc::UnitAtkFnRpl（外置 DLL 的替换函数；ecx=攻击者）
        ├─ 先算 dwPreHurt = 原函数(bIsReal=FALSE)   ← ★ 预览口径
        ├─ 再算 dwHurt    = 原函数(bIsReal=TRUE)    ← ★ 实战口径
        └─ g_pAdjHurt->Attack(..., dwHurt, dwPreHurt, bIsReal, ...)
             └─ bIsReal==false ⇒ PreHurt() ⇒ 加双击/暴击加成 ⇒ return dwHurt
   ```
2. **★ 暴击加成就在 `CAdjHurt::PreHurt()` 里，而且只有预览分支会走**（实战分支不调 `PreHurt`）：
   ```cpp
   // AdjHurt.cpp:254-286（原文，已转 UTF-8 副本 _tmp_czz\AdjHurt.cpp.txt）
   void CAdjHurt::PreHurt(UnitStatus* pUnitAtk, UnitStatus* pUnitDef, DWORD &dwHurt)
   {
       if(CczFunc::IsControlable(pUnitAtk)) {                 // 我方（玩家可控）
           if(!g_pCfgDlg->IsCbEnable(IDV_ShowAdjLuckHurt)) return;
       } else {                                               // 敌方
           if(!g_pUnitLuck->IsAiPreLuck()) return;
       }
       if(g_pUnitLuck->IsMiss(pUnitAtk, pUnitDef)) { dwHurt=0; return; }   // 会打空 ⇒ 预览 0
       DWORD dwAdd=0;
       if(g_pUnitLuck->CanDbl(pUnitAtk, pUnitDef, true))  dwAdd+=dwHurt*g_pUnitLuck->DblHurtPnt()/100; // 双击
       if(g_pUnitLuck->CanDbl(pUnitAtk, pUnitDef, false)) dwAdd+=dwHurt*g_pUnitLuck->CrtHurtPnt()/100; // ★暴击
       dwHurt+=dwAdd;
       if(dwHurt>pUnitDef->dwHP) dwHurt=pUnitDef->dwHP;        // ★预览封顶 = 目标当前 HP
   }
   ```
3. **★ 暴击判定用的不是"概率"，而是 `附加 + 差值 ≥ 100` 的确定式**：
   `CUnitLuck::CanDbl()`（UnitLuck.cpp:603）＝ `GetCrtVal(攻击者) + CczFunc::GetDiff(攻,防,false) ≥ 100`；
   暴击**加成幅度**是配置项 `CrtHurtPnt`（默认 **50** ⇒ 预览显示 **×1.5**，不是本引擎的 `100+K/2`）。
   ⇒ 所以**它的数值口径不能照搬**，可搬的是**结构与落点**。
4. **★ 这正好印证我们 6.6 的判断**：6.6 的 `0x43BC5A`（伤害公式）同样把预览与实战**分成两条调用路径**
   （预览 `0x440668` / 实战 `0x405E6D`），而**暴击加成只在实战路径上**（`0x405ECD~0x405F0B`）。
   ⇒ 对方选择"在预览那一遍的返回口上加成"，与我们现在的补丁（钩预览 `0x44066D`）**是同一设计**，
   **互为独立来源的印证**（对方 2014 年实现、本工作区 2026-10-15 独立复读得出）。
5. **能搬的三件**：① 预览封顶 `min(值, 目标HP)`；② "预览/实战同一函数、用形参区分"的落点选择；
   ③ **参数与模式值的实机取证方法**（下面 §实现）。**不能搬的两件**：随机暴击模型、固定 50% 加成。
6. **`[待实机]` 未闭环**：6.6 公式 `0x43BC5A` 的**形参顺序**（哪个是目标指针、哪个是"预览标志"、
   预览时该标志到底是 `1` 还是 `0`）**必须实机取证**才能下结论（见 §待验证项，附现成断点命令）。

## 适用版本

* 对方样本：**CzzHelper v3.09b（2017-06-11）**，`VersionHistory.txt` 自述覆盖 **5.9~S6.1** 与多个 mod
  （原版 / 宋江传 / 豪曹 11&14 / 新金庸群侠 / 岳飞 6.0）；伤害预览与暴击加成部分最早见于 **2014-10** 的版本记录。
* 本工作区样本：复刻版 6.6山贼 `Ekd5.exe`，SHA 见 `_样本时间线.md` 现读（本页复读时 = `69A9074A…`）。
* **6.1 与 6.6 的结论不得互相套用**（`AGENTS.md §3`）：对方全部是 **6.1 地址**，
  其地址表见 `Publish\HelperRes\FunctionList.txt`，**不能直用**。

## 已确认事实

### 一、它是"外置 DLL + 覆盖函数头"，不是二进制补丁

* 投放方式：`Koeicda.dll` / `MenuScript.dll` / `StatusIconEx.dll` 等 **DLL 注入**
  （`Publish\Extra\独立Exe\LoaderEx.ini` 指明挂载），**不改 `Ekd5.exe` 字节**
  ⇒ 与本工作区"改 Ekd5.exe"是**两条不同的工程路线**。
* 覆盖机制在 `CodeList.cpp:85-138` 的一张表里：`(地址, 启用, 形参个数, 接近偏移, 是否取ecx, 备用地址)`，例如
  ```cpp
   0x0043BC62, 1, 3, -0x50, true, 0   // UnitAtkFnRplCC   ← 伤害公式（预览+实战）
   0x0043BFAA, 1, 4, -0x10, true, 0x0043C013 // MagHurnFnRplCC ← 策略伤害（bIsPreview 形参）
   0x0047FB32, 1, 1,  0x00, false, 0  // GetRandNumFnRplCC ← 随机数（对方自己接管暴击随机）
  ```
* **跨版本适配**：`RenewAutoRplCC()` 读 `HelperRes\FunctionList.txt`（6.1 地址表），再用
  `CCodeList::GetApprFuncAddr(addr, nOffset)` **向前扫描函数序言**（`55 8B EC …`）修正到当前版本的函数入口；
  个别地方用**字节签名**（`CommFunc::FindAddr(addr, ±n, "8A8411")`、`"558BEC6AFF"` 等）。
  ⇒ **思路可借**：用序言/签名定位，比硬编码地址抗版本漂移（我们库里已有 `_dsh反汇编工作台.py funcstart/func`）。
* `RecallOrgFn(cc, dwEcx, ...)`：临时**关掉**该处覆盖 → 按原调用约定调一次原函数 → **恢复**覆盖 → 返回 `eax`
  （`CheatFunc.cpp:91-153`）。⚠ 变参循环 `*(pParam+nCount-i)` 配 push 顺序的写法**可读性极差**
  （`dwEcx` 实际落在 `[esp+4]`＝目标函数第一个形参），**不要照抄这一段**，容易把形参顺序读反。

### 二、预览与实战的分叉点（`CheatFunc.cpp:265-345`）

```cpp
int CheatFunc::UnitAtkFnRpl(DWORD dwDefUnitDataAddr, bool bIsReal, bool bIsCounter)
{                       // ecx = 攻击者单位指针（表里 "取ecx=true"）
    ...
    DWORD dwPreHurt=0, dwHurt=0;
    if(bIsReal) dwPreHurt = RecallOrgFn(UnitAtkFnRplCC, dwUnitAddr, dwDefUnitDataAddr, FALSE, bIsCounter);
    dwHurt = RecallOrgFn(UnitAtkFnRplCC, dwUnitAddr, dwDefUnitDataAddr, bIsReal, bIsCounter);
    ...
    g_pAdjHurt->Attack(pUnitAtk, pUnitDef, dwHurt, dwPreHurt, bIsReal, bIsCounter);
    return dwHurt;      // ★ 引擎拿这个返回值去显示
}
```

* **`bIsReal` 来自引擎自己的形参** ⇒ 引擎每调用一次，DLL 都按"预览 / 实战"分别处理。
* 预览时（`bIsReal=false`）只调一次原函数、随后进 `PreHurt()`；实战时（`true`）多算一遍"无加成值"，
  留给"逃跑/劝降/保命"等逻辑做比较。
* 策略路径 `MagHurnFnRpl`（同文件 347-406）完全同构，且**引擎的策略伤害函数本身就带 `bIsPreview` 形参**
  ⇒ 对方还能顺手把"AI 计算"（调用者地址落在 `0x43xxxx` 且 AI 正在工作）也当成预览。

### 三、暴击判定的口径（对方，随机模型）

```cpp
// UnitLuck.cpp:603
bool CUnitLuck::CanDbl(UnitStatus* pUnitAtk, UnitStatus* pUnitDef, bool bIsDbl)
{   int nAdd  = bIsDbl ? GetDblVal(pUnitAtk) : GetCrtVal(pUnitAtk);
    int nDiff = CczFunc::GetDiff(pUnitAtk, pUnitDef, bIsDbl);
    return nAdd+nDiff >= 100;  }
// UnitTips.cpp:278-301：把 (双击值,双击差值) / (暴击值,暴击差值) 拼成面板文本，达标时整行变红(clr=0xff)
```

* 面板显示（`UnitTips.cpp`）用 `nAdd + nDiff >= 100` 决定**变红=必定触发**；
  伤害预览（`AdjHurt.cpp`）用同一条件的 `CanDbl(...)` ⇒ **面板与预览口径一致**。
  ⚠ **注意：这是 2014 年的"每单位幸运值 + 差值"随机模型**；
  **本工作区 6.6 是集气模式 `4018=1` 的"累计必触发"模型**（`0x4930C8 + slot*4 + 字节`），
  **两者不是一回事**，`CrtHurtPnt=50` 更不能照搬到我们的 `K = 暴击率(+100)` 公式上。
* 对方还要**接管游戏的随机数**（`GetRandNumFnRplCC` 钩 `0x47FB32`）才能把随机变成可控 ⇒ 我们**不需要**这一层。

### 四、[本样本复读] 6.6 侧的对应位置（同一设计的两条路径）

| 语义 | 6.1 对方地址 | 6.6 本样本（现读复读） |
|---|---|---|
| 伤害公式（预览+实战共用） | `0x0043BC62` | **`0x43BC5A`**（函数入口 8 字节序言，`ret 0xC`=3 参数；`ecx`=攻击者 ctx） |
| 预览调用点 | 由引擎传入（未标） | **`0x440668`**，返回值存预览伤害槽 **`0x44066D mov [ebp-0x18],eax`** |
| 实战调用点 | 由引擎传入（未标） | **`0x405E6D`**，返回值在 `0x405E9A` 写伤害槽 `ctx+0x84` |
| 实战的暴击加成段 | 对方在 DLL 内做 | **`0x405ECD`(取暴击率)→`0x405EDD`(集气判定)→`0x405EE6`(+100)→`0x405F0B`(call `0x42E4FD`)** |
| 预览的暴击加成段 | `CAdjHurt::PreHurt()` | **原本不存在** ⇒ 本工作区补丁：钩 `0x44066D` → 槽体 `0x457DB4`（87 字节） |
| 策略伤害 | `0x0043BFAA`（带 `bIsPreview`） | 策略预览 `0x445D3A`；策略伤害公式待重定位（本页不展开） |

> ⇒ **两条独立来源得出同一个设计**：**"在预览那一遍的返回口上加暴击加成"**。
> 本工作区当前补丁（`_算暴击预览字节.py`）与对方 2014 年的做法**结构一致**。

## 实现·使用方法

### 1. 6.6 侧可立即采纳的两点

* **预览封顶**：`if (预览值 > 目标当前HP) 预览值 = 目标当前HP;`
  6.6 落点：槽体 `0x457DB4` 在写回 `[ebp-0x18]` 之前插 5~8 字节即可
  （目标单位指针 = 公式第 1 形参；预览帧里可从 `[ebp-0x28]`(攻击者 ctx) 的 `+1` 取目标 slot，
  再 `slot*0x30 + 0x4A7B20 + 0x10` 读当前 HP）⇒ **但需实机确认目标 HP 字段与时机**，属 P2。
* **区分"给玩家看的预览"和"AI 试算"**：对方把"调用者地址落在 AI 段且 AI 在工作"也算预览。
  6.6 里 `0x43BC5A` 的 **5 个调用者**已复读为
  `0x405E6D`(实战) / `0x419AED` / `0x438A2A` / `0x438CCA` / `0x440668`(面板预览)
  ⇒ 若要"只给玩家预览加成、AI 试算不加成"，就把槽体挂到 `0x44066D`（只覆盖面板那一支）——
  **本工作区补丁正是这么落的**，天然满足。

### 2. 跨版本适配（若将来要看对方别的功能）

* **序言定位**：`CCodeList::GetApprFuncAddr(addr, nOffset)` 的做法 = 从 6.1 地址向前找 `55 8B EC`
  ⇒ 本地等价工具：`_dsh反汇编工作台.py funcstart <VA>` / `func <VA>`（已归档）。
* **签名定位**：`CommFunc::FindAddr` 支持在 `±n` 字节内找任意字节串（如 `"8A8411"`）
  ⇒ 本地等价：`_dsh反汇编工作台.py db` + 全映像字节扫描（本会话已用它定位 `call 0x40C7D8` 的 2 个调用点）。
* **别名表**：`HelperRes\FunctionList.txt`（6.1 地址）与 `CodeList.cpp:85-138` 的表**是同一份数据的两种载体**，
  改地址要两处同步；我们**不要**引入这种双源，仍按 `AGENTS.md §2.5` 用"单一生成源"。

### 3. [待实机] 6.6 公式形参取证的现成命令

```
:: 先按 §7「先放行再叫人」：设断点→循环 debug_run 到 running→确认可操作→再请人动鼠标
:: 悬停观测**不推回合** ⇒ 用保留件（退役件 `_x32断点探针.py` 已移入 `_废弃实验\自动战斗历史件-20261026\`）
python 大鲸鱼产生专用\_先放行再叫人.py 0x44066D      # 设断点 → 循环放行到 running+Responding → 才叫人
python 大鲸鱼产生专用\_等命中读数.py 0x44066D --timeout 180   # 自动等命中并抓寄存器/上下文
python 大鲸鱼产生专用\大鲸鱼自动战斗.py --cleanup-bps  # 收尾：全清断点 + 放行
:: ⚠ 旧命令的 `--stack 6` / `--reg-mem ecx,32` / `--mem <地址表>` 三项**尚未确认被上面两件等价覆盖**
::   （`_等命中读数.py` 抓 register_list + context_get_basic，不读任意地址表）⇒ 首次实机前先核对
:: 要「边推回合边统计命中」才用唯一入口：
::   python 大鲸鱼产生专用\大鲸鱼自动战斗.py --go --breakpoint --rounds 1 --set-bp 0x44066D=预览公式
:: 玩家把鼠标移到敌人身上（触发面板预览，不必真打）
:: 要读到的四件事：
::   ① eax / [ebp-0x18] = 预览伤害（两者应一致）
::   ② [ebp-0x28] = 攻击者 ctx；[ebp-0x28+0xC] = 攻击者单位指针（= 0x4A7B20 + slot*0x30）
::   ③ [ebp+8] / [ebp+0xC] / [ebp+0x10] = 公式三个形参的原值（定"目标指针 / 预览标志"顺序与取值）
::   ④ [0x505EC8] = 4018（集气模式开关，必须=1）；byte[0x4930C8+slot*4+2] = 攻击者暴击集气
```
判据：**同一目标、同一攻击者，把该 slot 的暴击集气从 <100 改成 100**，
预览数字应从 `D` 变为 `D×(100+K/2+0x70特效)/100`；改回 <100 应还原。

## 风险与边界

* **不要把对方的数值口径搬过来**：`CrtHurtPnt=50`、`CanDbl = 值+差 ≥ 100`、
  `GetRandNumFnRplCC` 接管随机 —— 全部属于 **2014 年的随机暴击模型**；
  本工作区是**集气模式 4018=1 的累计必触发**（`已有集气 + 本次理论值 ≥ 100`）。
* **不要把 6.1 地址搬过来**：对方 `FunctionList.txt` 里的地址在本样本**无一可直接使用**
  （例：`0x0043BC62` 本样本是公式内部；`0x0043BFAA` 本样本落在别的函数里）；
  引用前一律按 `AGENTS.md §2.5` 第 3 步现读。
* **`RecallOrgFn` 的变参序不要照抄**（见 §一 末注）。要复刻"调一次原函数"的语义，
  在 6.6 里应该**显式按 `__thiscall` 写**：`ecx=攻击者 ctx`，再 `push` 三个形参。
* 对方是 **DLL 注入**，本工作区是**改 EXE**：两者的回滚方式、审计方式完全不同，
  不能因为"对方没崩"就认为"我们的补丁一定安全"。

## 证据来源

* 对方源码（GBK 原文 + 本会话转出的 UTF-8 复本 `_tmp_czz\*.txt`，**属临时副本，不是交付物**）：
  `AdjHurt.cpp:254-286`（`PreHurt` 暴击加成）、`CheatFunc.cpp:265-345`（`UnitAtkFnRpl` 预览/实战分叉）、
  `CheatFunc.cpp:347-406`（策略同构，`bIsPreview`）、`UnitLuck.cpp:597-609`（`IsMiss`/`CanDbl` 判定口径）、
  `UnitTips.cpp:250-356`（面板显示与变红）、`CodeList.cpp:85-138`（覆盖表）、
  `CodeList.cpp:205-219` + `CommFunc.cpp:1488-1539`（`FunctionList.txt` + `FindAddr` 跨版本适配）、
  `CheatFunc.cpp:91-153`（`RecallOrgFn`）、`Publish\HelperRes\FunctionList.txt`（6.1 地址表）。
* 本样本复读（只读，`capstone` 逐条反汇编）：`0x43BC5A` 入口与 `ret 0xC`、`0x43BF00 cmp [ebp+0xC],0`、
  `0x440660~0x440699`（预览调用与伤害槽）、`0x405E60~0x405F10`（实战调用与暴击段）、
  `call 0x43BC5A` 全映像 5 个调用点、`call 0x40C7D8` 全映像 2 个调用点。
* 版本：`ai使用库\CzzHelper及源码\VersionHistory.txt`（v3.09b 2017-06-11；2014-10 条目含加速/存档等功能）。

## 待验证项

* **P0**：6.6 `0x43BC5A` 的形参顺序与"预览标志"取值（`[ebp+8]`/`[ebp+0xC]` 谁是目标指针；
  预览时 `[ebp+0xC]` 是 `1` 还是别的）——命令见 §实现 3，需实机。
* **P0**：本工作区补丁（钩 `0x44066D`）在实机下的预览数字是否真的变（五级证据第 4~5 级未做）。
* **P1**：预览封顶 `min(预览值, 目标当前HP)` 是否要加（对方加了；我们未加，需看观感）。
* **P1**：策略路径的对应关系（对方 `MagHurnFnRplCC` ←→ 本样本策略伤害函数与 `0x445D3A` 策略预览）。
* **P2**：对方"AI 试算也当预览"的处理，在本样本是否需要（`0x419AED`/`0x438A2A`/`0x438CCA` 三个非预览调用者）。
* **P2**：对方 `FunctionList.txt` 其余条目能否用"序言扫描"在 6.6 一一对上（可作对照工具集的素材）。
