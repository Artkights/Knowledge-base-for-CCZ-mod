# 文档体系：CONTEXT.md + ADR（DSH ⇄ Codex 协作共识）

## 结论速览

1. 仓库根 `CONTEXT.md` = **现在**的认知：术语（含禁用别名）、不变量、边界、待定项。**DSH 与 Codex 同等有效。**
2. `docs/adr/NNNN-*.md` = **历史决策**：背景 / 选项（含被放弃的）/ 决定 / 代价 / 影响面 / 回滚。**只追加不改写**，取代关系写在新记录的「状态」行。
3. 三类信息分家，不要混写：**现在是什么** → `CONTEXT.md`；**为什么这样定** → ADR；**证据在哪（地址/字节/实机命中）** → 知识库页面。
4. 维护技能：用户级技能 `grill-with-docs`（`~/.agents/skills/grill-with-docs/SKILL.md`，含 `templates/CONTEXT-template.md`、`templates/ADR-template.md`）。口诀：**先读 CONTEXT.md → 盘问时对照词汇表并澄清措辞 → 收尾写回 CONTEXT.md**。
5. 技能放置实测：`~/.agents/skills/<name>/SKILL.md`（目录名 = 技能名 = frontmatter `name`）；写入后**本会话技能表当场出现该条，不需要重启**。

## 适用版本

- 本工作区（复刻版 6.6 山贼）任何会话；与 `Ekd5.exe` 样本 SHA 无关（文档体系本身不依赖样本）。
- 建立日：2026-10-21。

## 已确认事实

- DSH 安装包 `app.asar` 内字节级出现 `.agents/skills`（5 处）、`SKILL.md`（87 处），并自带 `skills/<name>/SKILL.md` 结构（如 `agent-experience`、`cordis-composition-reference`）⇒ `~/.agents/skills/` 是既定约定，不是社区传闻。
- 技能写入后，**本会话技能目录表即时刷新**（实测：写完后系统提示里的 available_skills 新增 `grill-with-docs`），无需重启 DSH。
- 上游 `grill-me` 的四条提问规则（原样抄进本技能）：① 每个问题走选择器工具，不写成正文纯文本；② 一次只问一个；③ 每题给 2~4 个具体选项（避免"是/否"式废话）；④ 用户永远保留"其它"自填。
- 本仓库已落地：`CONTEXT.md`（5488 B）、`docs/adr/0001-引入CONTEXT与ADR文档体系.md`（3517 B）。

## 实现·使用方法

**读（每次开工）**：先读 `CONTEXT.md` 的术语表与不变量 → 再看 `docs/adr/` 最新几条的「状态」行，确认没有「已取代」。

**写（两种触发）**：
- 术语/口径变化 ⇒ 改 `CONTEXT.md` 对应行，**保留出处**（文件:行 或「本轮决策」）；两种叫法必须定案为「规范词 + 禁用别名」。
- 重大决策（不可逆 / 跨模块 / 将来必有人问"当初为什么"）⇒ 复制模板生成 `docs/adr/NNNN-短标题.md`，编号取现有最大 +1；放弃的选项必须留在「选项」表里。

**跨 AI 交接**：DSH 改完在共享台账追加一行；Codex 改完同样。**不要把结论只写在对话里**（§1）。

**校验**：`Get-ChildItem CONTEXT.md, docs/adr/*.md` —— 两个路径存在即体系在位。

## 风险与边界

- ADR 只追加 ⇒ 旧记录会被"取代"，读者需按状态行跳到最新那条；**不要**直接改旧 ADR 的正文。
- `CONTEXT.md` 放在**游戏根目录**与 AGENTS.md §3「工作区根目录只保留游戏本体」相抵，**已登记为待定项**（`CONTEXT.md` §5），未擅自解释规则。
- 术语表不是证据库：行内只放"定义 + 出处指针"，证据（字节复读、实机命中）仍写知识库页面。
- 盘问类交互依赖 `ask_user_question`；若会话未启用该工具，退化为"正文一次一问"，但仍在收尾写回 `CONTEXT.md`。

## 证据来源

- 字节实测：`[IO.File]::ReadAllBytes(app.asar)` + Latin1 直搜 → `.agents/skills`×5、`SKILL.md`×87、`grill`×0（DSH 不自带 grill-me）。
- 上游原文：RobMitt/grill-me-skill 的 `SKILL.md`（四条提问规则）、incubyte/ai-plugins 版（"先理解形状、先深后广"）。
- 运行时：技能写入后 available_skills 立即包含 `grill-with-docs`（本会话 2026-10-21）。
- 文件：`CONTEXT.md`、`docs/adr/0001-引入CONTEXT与ADR文档体系.md`、`~/.agents/skills/grill-with-docs/` 三个文件（SKILL.md 5223 B / CONTEXT 模板 1108 B / ADR 模板 933 B）。

## 待验证项

- `CONTEXT.md` 是否长期留在游戏根目录（用户 2026-10-21 已点头建立，长期归属待定）。
- ADR 与知识库 `00-总览与规范/更新记录.md` 的记账分工是否重复（暂定：ADR 记决策、更新记录记事实）。
- Codex 侧是否读到本页并遵守同一套术语（下次 Codex 会话可在台账里回应）。
