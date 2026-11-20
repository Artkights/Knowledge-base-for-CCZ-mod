# 可复用 Skills（本工作区适配版）

> 本目录是**技能权威副本**（随知识库进 Git 版本管理、DSH/Codex 都能读）。
> 运行时副本在项目根 `.dsh\skills\<name>\SKILL.md` —— DSH 的 `@deepseek-ai/dsh-skill-filesystem`
> 按 rank 100 扫描该目录（`AGENTS.md` 同级的项目根），**带 watcher：新增/改名/删除技能无需重启**。

## 现有技能

| 技能 | 用途 | 直接加载 |
|---|---|---|
| `engine-feature-development` | 引擎功能开发与移植：七步工作流 / 行为契约六项 / 五级证据 / 单一生成源与回滚 | `skill name=engine-feature-development` |
| `x32dbg-debugging` | 动态调试取证：附加、断点规划、命中取证、条件断点陷阱、运行时写入、崩溃现场、收尾顺序 | `skill name=x32dbg-debugging` |

**来源与许可（必读）**：两者均**改编自**《曹操传 Mod 公共知识库》
（<http[本地盘]//github.com/lanceyuki/caocao-mod-public-knowledge-base>，基于 6.5pl 样本）。
许可：**曹操传 Mod 公共知识库非商业使用许可 1.0** —— 非商业可复制/改编，
**须署名 + 附来源与许可链接 + 说明修改**，**任何商业用途均禁止**。
修改：已按本工作区（复刻版6.6山贼 / `Ekd5.exe`）的工具、规则与实测教训改写。
外部原文只读留档：`大鲸鱼产生专用\_外部源码\caocao-mod-public-knowledge-base\`。

**优先级**：与本工作区 `AGENTS.md` 冲突时，**一律以 `AGENTS.md` 为准**。

## 同步方法（改了权威副本后必须做）

```powershell
$root = '[本地盘]\ccz\曹操传6.6-V7.30 解压密码：66\复刻版6.6山贼'
$kb   = "$root\ai使用库\小暗的本地知识库\06-项目与工具链\可复用Skills"
foreach ($n in 'engine-feature-development','x32dbg-debugging') {
  New-Item -ItemType Directory -Force "$root\.dsh\skills\$n" | Out-Null
  Copy-Item "$kb\$n\SKILL.md" "$root\.dsh\skills\$n\SKILL.md" -Force
}
```

- ⚠ **改动正文后无需重启 DSH**：watcher 会在下一个模型步骤刷新目录；但**已加载过的正文不会自动重读**，
  下一次 `skill` 调用才拿到新内容。
- ⚠ **`.dsh\` 不进 Git**（`.gitignore` 是白名单式、根目录默认忽略）⇒ **权威副本永远以本目录为准**，
  别只改 `.dsh\skills` 而不回写知识库。（若希望技能随仓库分发，可在 `.gitignore` 加 `!.dsh/` + `!.dsh/skills/`。）

## 维护坑（实测）

- **`mcp__kb__kb_write_page` 的 `path` 是按页名模糊匹配的**：两个页面都叫 `SKILL.md` 时，
  后一次写入会**覆盖前一次**（本次实测：先写的 `engine-feature-development/SKILL.md` 被
  `x32dbg-debugging/SKILL.md` 覆盖）。⇒ **写同名文件（`SKILL.md`/`README.md` 等）必须用文件系统写工具
  （`write` / `edit`）走精确路径**，不要用 MCP 页面工具。
- 技能格式要求（来自 `dsh-skill-filesystem` 文档）：frontmatter **必填 `name`（kebab-case，须与目录名一致）与 `description`**；
  可选 `whenToUse` / `metadata` / `disable-model-invocation` / `user-invocable`；
  只识别 `<root>/<name>/SKILL.md` 与 `<root>/<name>.md` **两层**，**不支持嵌套 `**/SKILL.md`**。
- 本目录文件用 **UTF-8 带 BOM**（本知识库规范），已实测 DSH 可正常解析。

## 关联页面

- 方法层总纲：`00-总览与规范/逆向方法层-行为契约与五级证据.md`
- 外部来源对账（哪些结论能用、哪些已分叉）：`90-来源归档/外部公共知识库-曹操传Mod公共知识库-吸收与对账.md`
- 工具层 checklist：`06-项目与工具链/外部参考-特技桩扫描器stub-scanner-拆解与移植清单.md`
