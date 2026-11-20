# Git 版本管理与 GitHub 共享方案（知识库仓库）

## 结论速览

- **本机早就装了 Git**：`[本地盘]\Program Files\Git\cmd\git.exe`（**2.56.0.windows.2**），但**不在 PATH 里** —— `Get-Command git` 会报"未安装"（重装系统后 PATH 没带上）。用全路径，或用封装 `大鲸鱼产生专用\_git.cmd`。
- **工作区已经是本地 git 仓库**（分支 `main`，4 次提交，**1975 个跟踪文件 / 44.5 MB**，`.git` 22.2 MiB）。白名单式：**只收知识与脚本，游戏本体一律不进**。
- **两个坑（都很贵）**：
  1. `fatal: detected dubious ownership` —— 工作区属主是 `NT AUTHORITY\SYSTEM`，当前用户是 Administrator ⇒ 必须先 `git config --global --add safe.directory '<工作区>'`，否则**所有** git 命令都失败。
  2. **`.cmd` 里不能出现中文**（路径、注释都不行）：本机控制台代码页可能是 65001、普通 cmd 是 936，GBK 写的 .cmd 在这边被读成乱码 ⇒ `fatal: pathspec 'aiʹ�ÿ�/…' did not match any files`。**中文路径只写进 `_git_commit.py`**，.cmd 只当纯 ASCII 外壳。
- **日常入口**：`大鲸鱼产生专用\_git.cmd <git 子命令>`（任意查询）；`大鲸鱼产生专用\_git_commit.cmd "说明"`（白名单提交，绝不 `git add -A`）。
- **GitHub 私有库已经建好并推送完成**（2026-10-15）：<http[本地盘]//github.com/JIATUZISYQJWZHX/ccz66-shanzei-kb>（**私有**）。
  远端 `origin` 已绑定，凭据存在 Windows 凭据管理器 ⇒ 以后 `_git.cmd push` 不用再输任何东西。
- **gh 的设备码路线在本机走不通（两次实测）**，改用 **PAT（令牌）** 才成功 —— 详见「已确认事实」第 9~11 条；PAT 建库+推送一步到位，且不需要"轮询换 token"这一步。

## 适用版本

- Git for Windows **2.56.0.windows.2**（本机 `[本地盘]\Program Files\Git\cmd\git.exe`；`ucrt64` 版也在，用 `cmd` 那个）。
- 仓库根 = 工作区根（`复刻版6.6山贼`）；提交身份 `DSH <dsh@local>`，**只写仓库 local config**，不改全局身份。
- 只适用于本工作区；别的 CCZ 目录要另建仓库（版本护栏见 `AGENTS.md` 第 3 条）。

## 已确认事实

1. **Git 在但不在 PATH**：`Get-Command git` → 未安装；`& '[本地盘]\Program Files\Git\cmd\git.exe' --version` → `git version 2.56.0.windows.2`。
2. **safe.directory 必须加**：工作区属主 `NT AUTHORITY\SYSTEM (S-1-5-18)`，当前用户 `DESKTOP-GTKB4T3\Administrator` ⇒ 已执行
   `git config --global --add safe.directory '[本地盘]/ccz/曹操传6.6-V7.30 解压密码：66/复刻版6.6山贼'`（**全局配置**，因为所有权检查发生在读 local config 之前）。
3. **白名单 .gitignore 实测有效**：抽查 `Ekd5.exe` / `Pmapobj.e5` / `Open.avi` / `大鲸鱼产生专用/_填写审计.log` / `_vendor_yaml/package.json` / `ai使用库/英杰传 6.6x` 全部 IGNORED；
   `AGENTS.md` / `ai使用库/小暗的本地知识库/**` / `ai使用库/AI协作/**` / `大鲸鱼产生专用/*.py` / `大鲸鱼产生专用/大鲸鱼专用工具库/**` 均会入库。
   （注意：`git check-ignore -v` 对**取反规则**命中时退出码是 0，别用它判"是否被忽略"；以 `git status --short` 为准。）
4. **首次提交**：`5ccefaf`「初始提交：知识库 + AI协作区 + 自制工具脚本」= 1966 文件 / **44.5 MB**；`git count-objects -vH` → size 22.19 MiB；最大单文件 4.09 MB（`90-来源归档/蒸馏归档-20261014/论坛原帖存档/star175.rar`）。
5. **提交时间线**：`5ccefaf` → `742d925`（git 工具）→ `db083c4`（清残留 + 并发会话改动）→ `bf9a2d8`（工具库归档）；跟踪文件 1975。
6. **`.cmd` 中文坑的失败原文**：`fatal: pathspec 'aiʹ�ÿ�/С���ı���֪ʶ��' did not match any files`（同一份 GBK .cmd 在 936 控制台能用、在 65001 下必炸）。**规避 = 中文只写进 .py**。
7. **并发写已经被 git 抓到一次**：`db083c4` 里含 `ai使用库/小暗的本地知识库/02-数据结构/ADDR_V66-LuaSkill移植地址核验.md` 的改动，而本轮会话**没碰过**该页 ⇒ 存在并发会话在写知识库。这正是 git 相对"追加式台账"的价值：**覆盖不再静默**。
8. **被取代的版本按规则留档**：失败/被取代的 GBK 版 `_git提交.cmd` 保留在 `大鲸鱼产生专用/大鲸鱼专用工具库/09-其它/`（`AGENTS.md` 第 5 条"历史工具不删除"），现行版是 ASCII 名的 `_git_commit.cmd` / `_git_commit.py`。
9. **gh 设备码流程在本机失败两次**（实测原文）：
   ① `failed to authenticate via web browser: Post "http[本地盘]//github.com/login/oauth/access_token": read tcp … wsarecv: … 未能正确答复`（换 token 那一步超时，即便加了 `HTTPS_PROXY=127.0.0.1:1088`）；
   ② 第二次授权页最终跳到 `github.com/login/device/authorize` → **Page not found**。
   ⇒ 结论：**本机不要走 gh 的 device flow**，直接上 PAT。
10. **PAT 路线一次成功**：`_github_push_with_token.py`（从**剪贴板**读令牌，不落盘、不打印全文）
    → `GET /user` 校验 → `POST /user/repos`（private）→ `git push` 带令牌一次 → `git credential approve` 交给凭据管理器 → 远端 URL 改回不含令牌。
    实测输出：`已建私有库: http[本地盘]//github.com/JIATUZISYQJWZHX/ccz66-shanzei-kb` / `* [new branch] main -> main` / `远端现在是: http[本地盘]//github.com/…/ccz66-shanzei-kb.git（不含令牌）`。
11. **取令牌的可靠手法（本机实测）**：GitHub 令牌**只在生成当页显示一次**；页面上那串字可以用
    **鼠标三击选中 → Ctrl+C**（比找那个小复制图标可靠），剪贴板里再正则提取 `ghp_[A-Za-z0-9]{36}`。
    ⚠️ 反面教训：让人"点复制图标"两次都点成了**聊天窗口消息旁边的复制按钮**（剪贴板里出现的是聊天文字）。

## 实现·使用方法

### 1) 只读查询（随时可用）

```cmd
大鲸鱼产生专用\_git.cmd status --short
大鲸鱼产生专用\_git.cmd log --oneline -10
大鲸鱼产生专用\_git.cmd diff -- ai使用库/小暗的本地知识库/README.md
大鲸鱼产生专用\_git.cmd log --oneline -- "ai使用库/小暗的本地知识库/03-机制详解"
```

`_git.cmd` 内部是 `git -C "%~dp0.."`，所以在任何目录调用都作用于工作区根。

### 2) 提交（白名单式）

```cmd
大鲸鱼产生专用\_git_commit.cmd "更新记录：xxx 结论落盘"
```

它会 `git add` 这些**明确路径**（与 `.gitignore` 白名单一一对应）：

| 路径 | 内容 |
|---|---|
| `.gitignore`、`AGENTS.md` | 仓库规则与工作区指令 |
| `ai使用库/小暗的本地知识库` | 全部知识库页面 |
| `ai使用库/AI协作` | 共享台账 / 交接（`_mcp写备份` 被排除） |
| `大鲸鱼产生专用/大鲸鱼专用工具库` | 工具留档 + 索引 |
| `大鲸鱼产生专用/*.py` `*.cmd` `*.ps1` `*.cjs` | 现行运行副本 |

**加新目录进仓库**要同时改两处：`.gitignore` 加 `!路径/`，`_git_commit.py` 的 `PATHS` 加一行。

### 3) 撤销 / 回滚

```cmd
大鲸鱼产生专用\_git.cmd status                 :: 先看改了什么
大鲸鱼产生专用\_git.cmd restore -- <文件>       :: 丢弃单个文件的未提交改动
大鲸鱼产生专用\_git.cmd log --oneline           :: 找到目标提交
大鲸鱼产生专用\_git.cmd show <提交>:<文件>       :: 看那时的版本（可比对、可另存）
```

### 4) 接 GitHub（**尚未执行**，需要用户拍板）

1. 在 GitHub 建**私有**空库（例如 `ccz66-shanzei-kb`），**不要**勾选自动生成 README。
2. 本地挂远端并推：
   ```cmd
   大鲸鱼产生专用\_git.cmd remote add origin http[本地盘]//github.com/<账号>/<库名>.git
   大鲸鱼产生专用\_git.cmd push -u origin main
   ```
3. 认证用 **PAT**（fine-grained，仅对该库 Contents: Read/Write）。本机 Git 带凭据管理器时会弹窗；若走 MinGit 之类没有凭据管理器的环境，**别把 PAT 写进 remote URL 后忘了清**。
4. 之后每次同步：`_git_commit.cmd "说明"` → `_git.cmd push`（或 `_git.cmd pull --rebase` 再推）。

### 5) 现状：两个远端（都已验证）

| 远端 | 地址 | 用途 |
|---|---|---|
| `origin` | `http[本地盘]//github.com/JIATUZISYQJWZHX/ccz66-shanzei-kb.git`（**私有**） | 异地备份 / 多机 / 历史 |
| `backup` | `[本地盘]\ccz-kb-backup\ccz66-kb.git`（本地裸库） | 本机第二份，断网也能推 |

日常一条龙：

```cmd
大鲸鱼产生专用\_git_commit.cmd "说明"      :: 白名单提交
大鲸鱼产生专用\_git.cmd push origin main   :: 上 GitHub
大鲸鱼产生专用\_git.cmd push backup main   :: 本地备份（或 git push --all 两个一起）
```

**凭据**：PAT 已存进 Windows 凭据管理器（`git credential approve`），远端 URL 里**不含令牌**。
令牌到期（约 2026-11-14）后重新生成一个，复制到剪贴板，跑 `python _github_push_with_token.py` 即可刷新。

## 风险与边界

- **绝不 `git add -A`**：工作区里躺着 2.9 GB（`大鲸鱼产生专用` 的 dmp/bmp/日志/备份）+ 1.4 GB `ai使用库`（英杰传 6.6x 895 MB、复刻版6.6 300 MB、扳手 108 MB）。白名单 .gitignore 是兜底，**明确路径 add 才是保险**。
- **仓库里 ~36 MB 是归档文档**（docx/rar/htm）。它们每次改动都会留历史 ⇒ 尽量别频繁动；真要频繁改，再考虑 Git LFS 或把 `90-来源归档` 移出仓库。
- **私有库**：路径里带"解压密码"字样、库里有论坛原帖存档与作者文稿，公开等于泄露。
- **6.6 / 6.5 护栏**：远端一旦多人协作，必须在库 README 顶部写明"6.6 与 6.5 结论不得互相套用"。
- **远端不是实时通道**：两个 AI 平时读写的仍是本地磁盘；git 只在提交/推送时同步。DSH 与 Codex 的**会话上下文依旧不互通**。
- 并发会话同时提交会产生冲突 —— 这是**特性**（能看见），处理方式：`git pull --rebase` 或人工合；不要用 `-X ours/theirs` 糊过去。
- 大仓库状态扫描有成本：仓库根目录含上万文件，`git status` 比纯知识库仓库慢（白名单让 git 跳过被忽略目录）。

## 证据来源

- 命令输出（本机实跑）：`git --version`、`git config --local --list`、`git check-ignore -v` 抽查、`git diff --cached --name-only`（1966）、`git count-objects -vH`、`git log --oneline`、`git ls-files`（1975）。
- 失败原文：`fatal: detected dubious ownership in repository at '…'`、`fatal: pathspec 'aiʹ�ÿ�/…' did not match any files`。
- 工具源码：`大鲸鱼产生专用\_git.cmd`、`_git_commit.cmd`、`_git_commit.py`、`.gitignore`。
- 与双 AI 的关系见 [Codex与DSH协同-共享知识库与MCP.md](Codex与DSH协同-共享知识库与MCP.md)。

## ★ 事故与恢复：`refs/heads/main` 被写坏（2026-10-15 10:24 实际发生并已修复）

- **症状**：`git log` → `fatal: your current branch appears to be broken`；
  `rev-parse HEAD` → `unknown revision`；`git status` 把 1999 个文件显示成 **`A`（新增）**。
- **根因（实测）**：`.git/refs/heads/main` 变成了 **41 个 0x00 字节** ——
  典型的"写 ref 过程中被打断"（多会话并发提交 + 期间 DSH 重启/进程被杀）。
  `.git/logs/HEAD`（reflog 原文）**完好**，`.git/COMMIT_EDITMSG` 时间戳指向被打断的那次提交。
- **恢复步骤（本次实测有效，务必照抄顺序）**：
  1. 读 `.git/logs/HEAD` 最后一行，取第 2 个 SHA = **真链末端**（本例 `d3135da`）
  2. **确认对象还在**：`git cat-file -t <sha>` → `commit`
  3. **删掉坏 ref**：`Remove-Item .git\refs\heads\main`
     （⚠️ 不删的话 `git update-ref` 会报 `unable to resolve reference: reference broken`）
  4. `git update-ref refs/heads/main <真链末端 SHA>`
  5. `git reset --mixed HEAD`（只刷新索引，**不动工作区文件**）
  6. `git status` 复核 → 正常提交 + 推送
- **⚠️ 两个"根提交"陷阱**：ref 坏掉期间产生的提交会变成**没有父提交的根提交**（本例
  `3ec237e`/`e459f48`），**不能**直接拿来当 main —— 那样会丢掉全部历史。它们的**文件内容仍在工作区**，
  所以正确做法是"回真链 + 重新提交一次"，内容不会丢。
- **预防**：`_git_commit.py` 已加**提交后自检**（HEAD 解析不了就自动按上面步骤从 reflog 修复）。

## 待验证项

- ~~**P1**：GitHub 私有库首次推送~~ → **2026-10-15 已完成**（见「结论速览」；远端 `ls-remote origin` 实测有 `refs/heads/main`）。
- **P1**：PAT **30 天有效期**（到期约 2026-11-14）⇒ 到期前要重新生成令牌并重跑 `_github_push_with_token.py`；或改用手工把凭据更新进凭据管理器。
- **P1**：仓库根含 1.4 GB `ai使用库` 旁的目录时，`git status` 的实际耗时（未计时；体感正常）。
- **P2**：是否让两个 AI 在**收工时自动提交**（现在靠人/手动跑 `_git_commit.cmd`；自动化前要先定"提交粒度"与提交信息规范）。
- **P2**：`90-来源归档` 的大文件是否上 Git LFS。

## ⚠️ 推送依赖（2026-10-15 13:40 实测）

- **GitHub 推送走的是 `~/.gitconfig` 里的代理 `http.proxy=htt[本地盘]//127.0.0.1:1088`**（HZVPN）。
  代理没开时报：`Failed to connect to github.com:443 over proxy 127.0.0.1 after 0 ms`。
- **直连不一定行**：同一次实测中 `git -c http.proxy= push` 也超时（`curl 28 ... after 21093 ms`）——
  说明"代理挂了"时 GitHub 这条线整体不可用，**不是仓库问题**。
- **兜底不受影响**：本地仓库 + `[本地盘]\ccz-kb-backup\ccz66-kb.git` 一直可用，提交照常。
- **补推命令**（代理恢复后执行即可，幂等）：
  ```
  大鲸鱼产生专用\_git.cmd push origin main
  ```
- 未推送时会体现在：`git log --oneline origin/main..main` 有内容。