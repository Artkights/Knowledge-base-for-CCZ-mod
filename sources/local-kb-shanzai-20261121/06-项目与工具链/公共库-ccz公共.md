# 公共库 `_ccz公共.py`：进程/内存/窗口/点击/判据的唯一实现

> 建立 2026-10-15｜动因：`_自检.py` 的 E 项实测**工具类公共函数被反复重写 258 处**
> （`find_pid`×59、`pid_of`×35、`kids`×16、`dialogs`×15、`focus`×14 …）
> **这是本工作区最大的资源浪费来源**；本页 + 该库是根治手段。

## 结论速览

1. **新脚本一律 `import _ccz公共 as C`**，不要再抄 `pid_of` / `read_mem` / `focus` /
   `click_*` / `find_dialog` 这些函数。
2. 把**五条铁律写进实现**，用库就自动遵守：
   ① 自绘窗口不认鼠标消息 ⇒ 一律 `mouse_event` 物理点击；
   ② **只在已最小化时 `SW_RESTORE`**（否则改窗口尺寸 ⇒ 预先算好的坐标点到界面外）；
   ③ **点击前校验目标在实时客户区内**（DPI 两视角差 1.25 倍）；
   ④ **业务生效必须物理点「是」矩形中心**（`WM_COMMAND(IDOK)` 只关框）；
   ⑤ **`Ekd5.exe` 一律不写**（写 EXE 只走 `_dsh写锁.py`）。
3. 常用一行：
   `C.pid_of()` / `C.Mem(pid)` / `C.game_hwnd()` / `C.focus(h)` /
   `C.safe_rclick(h,x,y)` / `C.find_yesno_dialog(pid)` / `C.click_yes_phys(dlg)` /
   `C.probe(m)` / `C.judge_line(before,after)`。
4. **既有工具不强制改**（它们已实测可用）；**只有新脚本必须用本库** ⇒ E 项计数不再增长。

## 适用版本

复刻版 6.6山贼；样本 SHA `813F4D7190EC52CE2A153519491E17158778633176AA3B42CC35722CCDA5C902`。
地址常量：`ADDR_WAR=0x4A7B20`、`LEN_WAR=0x30`、`FIELD_W=0x4B422C`、`PHASE=0x4B3D18`、`QI_SW=0x505EC8`。

## 已确认事实（2026-10-15 实测）

```
_ccz公共.py 自检
  Ekd5 pid         = 10528
  战场宽=20 phase=0 4018=1 敌存活=54
  主窗口 hwnd      = 0xd08d0
  rect / client    = (282, 20, 1248, 797) / (960, 728) origin=(285, 66)
  响应             = True
```

* **★ 客户区尺寸会变**：本机已实测到 **640×440 / 800×550 / 780 / 960×728** 共四种。
  ⇒ 一切坐标必须**按客户区比例**换算；`960×728` 正是**旧工具当年记录的基准**。
* `find_yesno_dialog()` 用**按钮文本**（有「是」且有「否」）判定"结束回合框"，
  不用标题 —— 因为标题是运行时塞进去的（`0x48E120`）。

## 实现·使用方法

```python
import sys, os
sys.path.insert(0, r"大鲸鱼产生专用")
import _ccz公共 as C

pid = C.pid_of()
h = C.game_hwnd()
m = C.Mem(pid)

before = C.probe(m)                      # 真判据（动前）

# 右键空地（自动校验在客户区内；目标超界会被拒绝而不是乱点）
(ox, oy) = C.origin(h)
C.safe_rclick(h, ox + 40, oy + 120)

dlg = C.find_yesno_dialog(pid, timeout=3)  # 找「是/否」框
if dlg:
    C.click_yes_phys(dlg)                  # 物理点「是」（唯一能让业务生效的方式）

import time; time.sleep(8)
after = C.probe(m)
print(C.judge_line(before, after))        # 直接产出「判据：前 … → 后 …」
```

## 风险与边界

* `Mem.wr()` 只做 `WriteProcessMemory`，**不含任何安全检查**；
  写 `unit+0x0E` / `unit+0x10` 这类"托管/保命"操作请照既有工具（带快照回滚）来做。
* `click_yes_phys()` **不校验客户区**（对话框可超出主窗口，按钮中心常在客户区外），
  这是有意的；但它**只认文本为「是」/「Yes」的按钮**，绝不会误点「否」。
* `safe_click`/`safe_rclick` 在目标越界时**返回 False 且不点击** ——
  调用方必须处理返回值，不要假设一定点到了。
* 本库**不替代**场景工具（`_42结束回合.py`、`_找空地并结束回合.py`、
  `_自动读档进战场.py` 等仍是权威用法）；它是**新脚本的底座**。

## 证据来源

* 自检 E 项实测计数：`find_pid`×59 / `pid_of`×35 / `kids`×16 / `dialogs`×15 /
  `focus`×14 / `game_pid`×10 / `rect_of`×10 / `enum_windows`×8 ⇒ 合计约 **258 处**。
* 收敛来源（不改其现有实现，只把口径抄进本库）：
  `_42结束回合.py:262 click_yes`、`_安全点击2.py:click_screen_physical/ack_dialog`、
  `_找空地并结束回合.py:safe_click/safe_rclick/live_rects`。
* 实测运行：`python -B 大鲸鱼产生专用\_ccz公共.py`（上方输出）。

## 待验证项

* **P1**：把"新脚本用公共库"这件事纳入 `_自检.py`——
  可加一项：新脚本若**自定义** `pid_of`/`open_proc`/`focus`/`click_*` 则报 ⚠。
* **P1**：逐步把**高频复用**的既有脚本（`find_pid`×59 那批）改为 import 本库，
  每改一个必须**跑一次判据自检**（`--probe` 前→后）证明没坏。
  ⇒ **第 1 批已做（2026-10-25，6 文件 / 11 处，`_自检.py` E 项清零）**，做法与差分证据见文末
  「2026-10-25 收尾：E 项清零」节；其余历史脚本仍按**触碰即迁移**处理。
* **P2**：`Mem` 目前无 64 位句柄保护（`restype` 默认 `c_int`）；
  若将来用 64 位 Python 必须显式设 `restype = c_void_p`（见知识库"D. 自动化脚本的铁律"）。
* **P2**：`responding()` 走 PowerShell，慢（约 1 秒）；可换 `SendMessageTimeout` 直查。

## 2026-10-25 收尾：E 项清零（「触碰即迁移」第 1 批 6 文件）

**触发**：`_自检.py` E 项报「公共库建立后仍有 11 处重复实现」（`find_pid`×5 / `rect_of` / `origin` / `children`×2 / `enum_windows` / `focus`）。
**做法**：先分类 —— 等价者直接 import；不等价者**只改名 + 留注释**说明为何不能复用（不改行为）。

| 文件 | 原重复项 | 处理 |
|---|---|---|
| `_42托管我军.py` / `_42托管效果采样.py` / `_加特技v2.py` | `find_pid` | `from _ccz公共 import pid_of_game as find_pid`（多开/僵尸安全） |
| `大鲸鱼启动诊断.py` | `find_pid` | `from _ccz公共 import pid_of as find_pid`（保持"取第一条"语义，另获 timeout/异常兜底） |
| `_安全点击2.py` | `rect_of` / `origin` | 与库逐字相同 ⇒ `from _ccz公共 import origin, rect_of`；对外 `S.origin` / `S.rect_of` 仍可用（`_x32_动态核验3链.py:162`、`_x32_打一场看命中.py:104` 在调） |
| `_安全点击2.py` | `children`（**只走一层**、返回裸句柄） | 与库 `children()`（`EnumChildWindows`、含孙窗口、四元组）**不是同一件事** ⇒ 改名 `direct_children`，同步 1 处调用 |
| `大鲸鱼自动战斗.py` | `find_pid` | import 别名（同 `大鲸鱼启动诊断.py`） |
| `大鲸鱼自动战斗.py` | `children`（dict 形） | 与库 `children_info()` 键位/矩形口径逐字相同 ⇒ `children = _C.children_info` |
| `大鲸鱼自动战斗.py` | `enum_windows`（尺寸形 rect + client + origin） | 库 `enum_windows_info()` 的 rect 是**角点形**且无 client/origin ⇒ 改名 `enum_windows_geo()`：枚举一律走库，本地只做整形 |
| `大鲸鱼自动战斗.py` | `focus`（重试 5 次 + 无条件 `SW_RESTORE`） | 改名 `focus_retry()`：单次动作走库 `focus()`，本地只留重试策略 |

**行为保持证据（差分实测，2026-10-25 21:2x）**

- `enum_windows`：旧实现 vs `enum_windows_geo` 各 **18 条**，逐字段（hwnd/title/cls/pid/rect/client/origin）**全等**；
- `children`：桌面窗口旧 **506** 条 vs 新 **506** 条，逐字段**全等**；
- `_安全点击2.py` 冒烟：`origin.__module__ == _ccz公共`、`find_button(桌面)` 返回 `None`（正常）；
- 三个文件 `py_compile` 通过；`大鲸鱼启动诊断.py` 的 `find_pid()` 返回 `None`（游戏未运行，正常）。

**★ 唯一一处行为变化（按本页「风险与边界」口径取库版本）**
`大鲸鱼自动战斗.py` 抢前台不再**无条件** `ShowWindow(SW_RESTORE)`：库只在**已最小化**时恢复。
理由 = 无条件恢复会改窗口尺寸 ⇒ 已量好的坐标失效（本页原有口径）；重试策略仍在本地（`focus_retry`）。

**★ 分发件约束（本次同步改了，别踩回去）**
`大鲸鱼自动战斗.py` 与 `大鲸鱼启动诊断.py` 是**整目录拷给别人**的分发件。它们一旦 import 本库，
**分发目录必须带 `_ccz公共.py`**，否则对方机器启动即 `ModuleNotFoundError`。已落地：
① `do_pack()` 现在会把 `大鲸鱼启动诊断.py` + `_ccz公共.py` 一起复制进 `大鲸鱼自动战斗-分发版\` 与 zip（缺文件会打印 ⚠ 而不是静默成功）；
② `大鲸鱼自动战斗-使用说明.md` 首段改为「零第三方依赖（纯标准库）+ 三份同目录」；
③ `03-机制详解\自动战斗-识别与驱动.md` 的「自包含分发件」两处同步。

**自检结果**：`38 项 / 5 项待办 / 0 项错误`，**E 项 ⚠ 已清零**。
剩余 5 项 = A（样本 SHA 与 `_基线` 不符）+ P×4（4 个 L1 页写的是别的样本 SHA），
属「哪个样本算现行」的裁定问题，**未擅自回填**。

**库内先例（形态照抄）**：`_42结束回合.py:44-45` 已有
`from _ccz公共 import children_info as children, enum_windows_info as enum_windows, focus, pid_of_game as find_pid`。
