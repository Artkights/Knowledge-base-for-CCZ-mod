# 贡献规范

目标不是收集更多文档，而是增加可检索、可复核、可用于实现的知识实体。提交前先搜索 `index.json`；同一事实应更新既有实体，不得换标题重复收录。

## 1. 选择状态

- `canonical`：结论已绑定精确画像，字段完整，并有源码、样本、静态复核或运行时证据支撑。
- `candidate`：内容具有明确技术价值并已结构化，但证据尚不足以授权自动写回。
- `legacy-reference`：只允许放在 `legacy/data/`，用于保存旧版本参照地址。
- 未知含义、未绑定画像或只有论坛线索的内容进入 `research/research-gaps.json`。

状态不是可信度装饰。候选升级为正式事实时，应补齐缺失字段、更新证据和来源，而不是只改 `status`。

## 2. 公共字段

每个版本数据文件采用集合封装：

```json
{
  "schemaVersion": 1,
  "entityType": "function",
  "entries": [
    {
      "id": "fn.65.example",
      "title": "功能名称",
      "aliases": ["地址或常用别名"],
      "versions": ["6.5"],
      "profile": "profile.ccz65.example",
      "status": "candidate",
      "evidence": "source-reviewed",
      "sourceRefs": ["src.example"]
    }
  ]
}
```

要求：

- `id` 全库唯一且长期稳定，格式为 `类型.版本.短名`；不能把标题或数组序号当稳定 ID。
- `title` 应描述技术语义；地址、opcode 和旧名称放入 `aliases`，保证可检索。
- `versions` 只列实际适用版本；6.5、6.5pl、6.6 不共享固定地址。
- 固定地址必须绑定 `profile`；画像至少说明架构、ImageBase、样本身份或明确的候选边界。
- `evidence` 描述证据本身，例如 `runtime-verified`、`static-verified`、`source-reviewed`、`legacy-structured`、`legacy-patch-bytes`。
- `sourceRefs` 必须引用 `sources/source-manifest.json` 中存在的记录；来源记录包含相对路径和 SHA256。

地址对象统一写法：

```json
{
  "kind": "va",
  "value": "0x004210D0",
  "profile": "profile.ccz65.example",
  "evidence": "static-verified"
}
```

## 3. 类型字段

### 函数与全局量

函数需提供地址、`callingConvention`、寄存器/栈输入、返回值、语义；已知调用点应写出调用点地址、指令和含义。全局量需提供地址、宽度、类型、含义和生命周期。未知字段写明未知，不能凭函数名补全 ABI。

### 数据结构与文件格式

数据结构需提供 `stride`、`indexFormula` 和字段数组；每个字段包含名称、十六进制偏移、宽度、类型和含义。重叠字段必须显式声明同一 overlay 组。文件格式还应描述头部/目录项、字节序、编码、计数规则、空值和校验方式。

### 特效桩

需提供地址、`stubStyle`、寄存器契约、压栈顺序、效果值模式、是否叠加、装备/个人特效 ID、调度器、核心函数和写回策略。历史桩地址不得描述为天然空闲代码洞。

### 补丁与 Hook

每个站点需提供地址、`expectedBytes`、`replacementBytes`、`overwriteLength`、`instructionBoundary` 和 `writeMode`。Hook 还需提供 ABI、桩入口、回跳、重定位、被搬运指令和寄存器/栈守恒。多个配方使用重叠地址时必须登记冲突。

历史记录允许以 `candidate` 暂缺 `expectedBytes` 或指令边界，但必须保留准确替换字节，并在 `writePolicy` 明确禁止自动写入。这种候选不能作为补丁器默认配置。

### 剧本指令

需提供两位十六进制 `opcode`；二级指令增加整数 `subcommand`。参数按 `P1`、`P2` 顺序记录名称、类型、含义、风险和证据。未知参数保留槽位并标注候选，不得用通用模板冒充已确认语义。

### 自动化工作流

需提供目标、输入、从 1 连续编号的步骤、门禁、产物和回滚。只描述“打开某工具并点击按钮”的教程不是工作流；必须包含可判断成功或失败的产物与门禁。

### 自动化测试契约

需提供使用占位符的可复现命令、测试目标、是否/在哪里产生修改、具体断言、必需产物和失败含义。不得写本机绝对路径，也不得用“测试通过”代替断言。

### 制作案例

需提供目标、输入、实际过程、结果和可复用结论。案例必须留下能迁移到其他项目的技术判断；单纯进度记录、宣传文本或截图不收录。

## 4. 来源和去重

提交来源时登记相对路径、SHA256、来源类型和发布状态。原始 EXE、DLL、压缩包、构建产物和受版权限制的大文件不进入仓库，只保存可核查的哈希和结构化结论。

同一事实只存在一个实体。版本差异用独立画像或独立实体表达；别名进入 `aliases`，旧路径进入清理/迁移记录。不要复制 Markdown 形成“另一个版本”。

## 5. 本地验收

依次运行：

```text
python tools/build_reference.py
python tools/build_index.py
python tools/validate_kb.py
git diff --check
```

并至少用 `tools/query_kb.py` 按标题、地址/opcode 和实体类型各查询一次。提交中应包含 JSON、重新生成的参考页、`index.json` 和必要的来源/清理记录；生成器再次运行必须无差异。
