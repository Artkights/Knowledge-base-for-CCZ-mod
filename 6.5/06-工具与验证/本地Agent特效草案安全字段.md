<!-- generated-kb-entry -->
<!-- source: 工具整合包/本地知识库/06-项目与工具链/本地Agent特效草案安全字段.md -->
<!-- version: 6.5 -->
<!-- topic: tools-validation -->
<!-- status: canonical -->
<!-- evidence: local-or-test-evidence -->

# 本地 Agent 特效草案安全字段

本地 agent 负责根据需求、语义目录和地址契约生成 `InlineSpecialSkillPatchDraft` 或 `AssemblyPatchDraft`。CCZModStudio/MCP 负责编译、代码洞分配、原指令搬迁、预览、旧字节锁、冲突检测、备份和写入。工具内不接入 LLM，也不允许草案直接写 EXE。

## 安全字段

```json
{
  "HookContractId": "strategy-damage-adjust-after-move",
  "HookAddressHex": "0x0043C2B0",
  "OverwriteLength": 5,
  "ExpectedOldBytesHex": "90 90 90 90 90",
  "OriginalInstructionPolicy": "PaddingOnly",
  "OriginalInstructionPlacement": "BeforeBody",
  "PreserveFlags": true,
  "ExpectedStackDelta": 0,
  "RequiredSymbols": ["core_effect_engine"]
}
```

- `PaddingOnly`：覆盖范围只能是 `90/CC` 填充。
- `AutoRelocate`：必须绑定 HookContract，由预览器搬迁原指令。
- `HookReplacesOriginal`：只有 HookContract 明确授权替换原逻辑时允许。

内联特技的 `FunctionAssemblySource` 只写判定通过后的业务功能体，不重复写 `004101D9` 调用、保存现场、原指令或回跳。

## 推荐流程

```text
read_effect_generation_context(keyword?, phase?, hook_contract_id?, character_budget=12000)
-> 生成 InlineSpecialSkillPatchDraft 或 AssemblyPatchDraft
-> preview_special_skill_patch / preview_assembly_patch
-> 检查 HookSafety、反汇编和 warnings
-> apply_special_skill_patch / apply_assembly_patch(preview.Package)
-> scan_installed_effects 复读
```

参数修改走 `scan_installed_effects -> read_effect_instance -> preview_effect_parameter_update -> apply_effect_patch(preview.Package)`。

## 版本与证据边界

- 本条目由发布整理流程归档。
- 具体结论必须结合上方版本、状态和证据等级使用。

## 结论速览

- 本条目整理了当前版本可检索的主题结论；具体使用前必须结合证据等级。

## 适用版本

- 以本目录版本入口和条目元数据为准，不能直接套用到其它版本。

## 已确认事实

- 正文中的确定性结论来自原始知识库整理；仍需以来源索引和纠错台账复核。

## 实现/使用方法

- 先阅读本条目的主体内容，再按版本入口、证据等级和来源索引执行。

## 风险与边界

- 未经目标版本样本、复读、烟测或实机验证的内容，不得作为默认写回依据。

## 证据来源

- 原始来源、哈希和处理状态见根目录 `90-来源归档/source-manifest.csv`。

## 待验证项

- 后续验证应补充目标版本样本、结构复读、烟测或实机证据。
