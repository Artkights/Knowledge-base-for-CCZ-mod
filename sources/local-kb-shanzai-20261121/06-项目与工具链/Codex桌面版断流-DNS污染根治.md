# Codex 桌面版断流根治：DNS 污染 → 假 IP → `InvalidContentType`

> 结论页（2026-10-23）。现场：Codex 桌面版（MSIX `OpenAI.Codex`）+「火种」HZVPN（TUN 模式）。

## 结论速览

1. `stream disconnected before completion: IO error: received corrupt message of type InvalidContentType` **不是容量问题，也不是代理/节点问题**，是 **DNS 污染**：系统把 `chatgpt.com` / `api.openai.com` 解析成假 IP（实测 `75.126.115.192`、`108.160.162.104`），连上去后 TLS 里读到非 TLS 数据 ⇒ rustls 报 `InvalidContentType`。
2. **根治 = 把域名钉到真 Cloudflare IP**（hosts）；换节点（同家不同机房）、换模式（系统代理→TUN）都只能压制症状。
3. **判据**：修复后 3~5 分钟内 `InvalidContentType` / `stream disconnected` **= 0**；Codex 的 external 连接应 100% 落在 `104.18.x` / `172.64.x`。
4. 残余 `108.160.x` 连接来自 `ab.chatgpt.com`（埋点域名，同样被污染），**只影响上报，不影响对话**。

## 已确认事实（2026-10-23 实测）

| 项 | 值 |
|---|---|
| 假解析 | `chatgpt.com → 75.126.115.192`、`api.openai.com → 108.160.162.104`、`ab.chatgpt.com → 199.16.156.40` |
| 真 IP | `104.18.32.47`、`172.64.155.209`（Cloudflare anycast）|
| 真 IP 实测 | `api.openai.com` → **401 / 0.58s**；`chatgpt.com` → **403 / 0.5s**（403 = Cloudflare 拦非浏览器 UA，属正常）|
| 直连（无代理） | 24 秒超时 ⇒ 必须走隧道（TUN 或代理），但**隧道不能替它解析域名** |
| 修复前错误率 | `InvalidContentType` 6~8 次 / 10 分钟，`stream disconnected` 10~17 次 / 30 分钟 |
| 修复后 | **0 次 / 5 分钟**；最后一条错误停在重启前 `02:00:37` |
| 传输形态 | TUN 网卡 `hzTunnel / 10.0.0.1`；本地代理端口 `1088/1089/1090` 已全部关闭 |

## 实现·使用方法

### 1. 钉 IP（需管理员 PowerShell；DSH 进程是 Medium 完整性，直接写 hosts 会 PermissionError）

```powershell
$h = "$env:SystemRoot\System32\drivers\etc\hosts"
Add-Content -LiteralPath $h -Encoding ASCII -Value @(
  "104.18.32.47 chatgpt.com",
  "172.64.155.209 chatgpt.com",
  "104.18.32.47 api.openai.com",
  "172.64.155.209 api.openai.com",
  "104.18.32.47 auth.openai.com",
  "104.18.32.47 cdn.oaistatic.com",
  "104.18.32.47 ab.chatgpt.com"
)
ipconfig /flushdns
```

提权方式（实测可用）：`Start-Process powershell -ArgumentList '<args>' -Verb RunAs -PassThru` → 用户点「是」。

### 2. 必须重启应用

改 hosts 后**当前进程仍持旧连接池**：实测重启前 external 12 条里 9 条假 IP、3 条真 IP，错误仍在；重启（`Stop-Process codex` 后 `explorer.exe shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App`）后立刻归零。

### 3. 排查三连（复用命令）

```powershell
ipconfig /all | Select-String 'hzTunnel'                    # TUN 是否在
(Get-NetTCPConnection -State Listen -LocalPort 1088 | Measure-Object).Count   # 本地代理是否还在
Resolve-DnsName chatgpt.com -Type A | Select IPAddress      # 是否假 IP
```
错误计数来源：`%USERPROFILE%\.codex\logs_2.sqlite` 的 `logs` 表，`feedback_log_body like '%InvalidContentType%'`，按 `ts` 分 10 分钟桶。

## 风险与边界

- **Cloudflare anycast IP 可能变**：ip 失效时症状复现，重查真 IP 即可（`http[本地盘]//1.1.1.1/dns-query` 在本机被 MITM，证书校验失败，不可用；改用别的 DoH/外部查询）。
- hosts 对**所有应用**生效；若将来某应用需要该域名的另一 IP，需临时删行。
- 改 hosts / 改 DNS 都需要管理员：`Set-DnsClientServerAddress` 在非提权下报「无法从客户端中访问 CIM 资源」。

## 证据来源

- `FILE:%USERPROFILE%\.codex\logs_2.sqlite`（`at capacity` / `InvalidContentType` / `Request completed` 计数）
- `FILE:[本地盘]\Windows\System32\drivers\etc\hosts`（现行 7 行）
- 实测：真 IP 直连 401/403、假 IP TLS 读到非 TLS 数据；修复后 3 分钟窗口 0 错误
- 时间线：SHA 无关（本条是网络/环境问题，不涉 `Ekd5.exe`）

## 待验证项

- `ab.chatgpt.com` 已加入 hosts，尚未单独统计其连接是否归零。
- 若换机/重装「火种」，需确认 TUN 网卡名是否仍为 `hzTunnel`、本地端口是否重新开放（届时若开 1088，可二选一走代理或 TUN，但**不要同时把系统代理指向已关闭端口**）。

## 2026-10-26 19:2x 复核：DNS 已修好，同症状再现 ⇒ 这次是「系统代理 1088」这条链路（补注；不改上文结论的适用条件）

- **现象同型、成因不同**：cannot decrypt peer's message（rustls DecryptError）、received corrupt message of type InvalidContentType、received corrupt message of type UnknownProtocolVersion 三种并存 = TLS 记录级损坏，**既可能是假 IP，也可能是中间链路把 TLS 流弄坏**。上文结论 1「不是代理/节点问题」只在 2026-10-23 的现场（TUN hzTunnel 在、1088/1089/1090 全关）成立；本次现场相反。
- **本次现读（2026-10-26 19:20~19:26，只读）**：
  - DNS 正确：chatgpt.com / api.openai.com → 104.18.32.47, 172.64.155.209（hosts 10 行钉住，Select-String 现读存在）⇒ **不是 DNS 污染**。
  - **无 TUN 网卡**（Get-NetAdapter 只有 WLAN）；**系统代理重新打开**：ProxyEnable=1, ProxyServer=127.0.0.1:1088，1088 由 **xray** 监听；~/.codex/config.toml 里 respect_system_proxy = true ⇒ Codex 全部外部连接落在 127.0.0.1:1088（现读 3 条）。
  - 直连（不走代理）chatgpt.com:443 TLS 握手 **3/3 被 RST** ⇒ 必须走代理，没有第二条路。
  - 经代理**短请求**成功：http[本地盘]//chatgpt.com/cdn-cgi/trace **200 × 3**；**长流/大块失败**：speed.cloudflare.com/__down?bytes=8000000 第 1 次 3 秒中途 read operation failed，第 2 次成功但耗时 **110 s（≈72 KB/s）**；同期 .NET 报 The decryption operation failed。
  - Codex 侧计数（~/.codex/logs_2.sqlite 的 logs 表，target=codex_core::responses_retry，近 3 h）：**9 条**重试 —— InvalidContentType 6、cannot decrypt peer's message 2、UnknownProtocolVersion 1；最近一次 19:23:02，其中一轮 **retries=5/5 耗尽**（max_retries=5）后向 UI 抛 error，即用户看到的那句。之后新一轮重试成功、会话继续（19:25:57 仍有 assistant 输出）⇒ **断流是瞬时的，会话未损坏**。
  - 另一类 6 次 Selected model is at capacity / server_overloaded 与网络无关，是服务端过载。
- **判据（修复后怎么算好）**：① logs_2.sqlite 近 10 分钟 %decrypt% + %InvalidContentType% = 0；② 经代理 8 MB ×3 全成功且耗时 < 30 s；③ Codex external 连接不再长期挂 127.0.0.1:1088（改 TUN 时）或该端口稳定无重连。
- **处置（按优先级；均需用户点头，本轮只读、未改任何配置）**：
  1. **换 HZVPN 节点/线路**（当前只有 1088 一条出站，节点决定长流质量）；
  2. 换节点无效 ⇒ **回到 2026-10-23 已验证形态**：开 TUN（hzTunnel）、**关系统代理 1088**（respect_system_proxy=true 时若系统代理指向已关闭端口会直接拒连，见本页待验证项）；
  3. xray 侧尝试**关 mux / 换传输**（长流 TLS 记录损坏的常见源）；
  4. 临时兜底：-c model_provider="gmncode" 走中转（成本口径见 06-项目与工具链\Codex-CLI两条通道与中转成本.md）。
- **工作区无损（本次复核）**：Ekd5.exe SHA256 = 2B279F3F0A917B1BD6E6F812E473DFB4B06A4101F38903EE1092EF3BDB70652A（= 工作基底，未变）；_dsh写锁.py status = 无锁；游戏与 x32dbg 均未运行；RS/SV 未碰。
- **复用命令（照抄）**：

    (Get-ItemProperty 'HKC[本地盘]\Software\Microsoft\Windows\CurrentVersion\Internet Settings').ProxyServer
    Get-NetTCPConnection -LocalPort 1088 -State Listen | Select OwningProcess
    Resolve-DnsName chatgpt.com -Type A | Select IPAddress
    Invoke-WebRequest 'http[本地盘]//speed.cloudflare.com/__down?bytes=8000000' -Proxy 'htt[本地盘]//127.0.0.1:1088' -OutFile "$env:TEMP\t.bin" -TimeoutSec 60

## 2026-10-26 19:40~19:46 续：桌面版摘不下系统代理（两法实测失败，均已还原）

- **A（配置开关）失败**：config.toml 的 respect_system_proxy 改 false + 重启（19:38:04）后，`Get-NetTCPConnection` 仍是 5~6 条 established 连 127.0.0.1:1088、**0 条直连 443**；同一时刻 models 请求 200、响应 568 KB ⇒ 仍走代理。
- **B（系统代理绕过名单）失败**：给 HKCU\...\Internet Settings 的 ProxyOverride 追加 `*.openai.com;*.chatgpt.com;chatgpt.com;auth.openai.com;api.openai.com;ab.chatgpt.com;*.oaistatic.com` 后重启（19:39:52），仍是 5 条 1088、0 条 443 ⇒ WinINET 绕过名单对它的 HTTP 客户端无效。
- **已全部还原**：config.toml 改回 `respect_system_proxy = true`；ProxyOverride 恢复原 1802 字串（原值留在 %TEMP%\_dsh_proxyoverride_old.txt）；桌面版最后一次重启 19:41:32，历史线程未动。
- **结论**：桌面版的 HTTP 客户端在 Windows 上直读系统代理，不认 `respect_system_proxy`、也不认 ProxyOverride ⇒ **要它直连，只能把系统代理整个关掉（ProxyEnable=0）或改用 TUN 并关 1088**；否则修复只能落在代理链路本身。
- **代理现状（19:44 复测）**：`speed.cloudflare.com` 500 KB × 10 走 1088 → **成功 5 / 失败 5**，失败落在 4 KB~77 KB 处被切（curl exit 56）；同目标直连 5/5 全通（2~4 s）。⚠ 这与上文「短请求 200×3」并不矛盾：坏的是**中长寿命连接**，正是模型流式响应的形态。
- **旁证**：19:29:32 xray PID 由 20020 换成 18084（HZVPN 重起）⇒ 每次重起都斩断在传的流，`InvalidContentType` 就是「流被切断后 rustls 读到半截记录」。
- **待用户操作（HZVPN 只能手点，DSH 改不了它的界面）**：① 换节点/线路；或 ② 切 TUN 模式并关掉系统代理 1088（回到 2026-10-23 形态）。做完我复测：10×500 KB 全通 + Codex 10 分钟 0 条 retry。

## 2026-10-26 19:56~20:06 复核（用户已切 TUN + 关系统代理）：TUN 生效，但链路本身仍在丢连接

- **环境现读**：hzTunnel 网卡 Up 且默认路由 metric 0；ProxyEnable=0；netsh winhttp show proxy = Direct；1088 仍由 xray 监听（TUN 模式保留该 inbound）。
- **链路质量（TUN 直连测，curl --noproxy）**：500 KB × 10 → **成功 6 / 失败 4**（失败点 23 KB、32 KB、335 KB，另 1 次 TLS 握手直接失败 curl 35）；1 MB × 3 曾 3/3；海外 1 MB 三次 5.5~8.1 s。国内 mirrors.aliyun.com 1.79 MB × 3 全通（9~19 s）⇒ **本地网络栈正常，丢流只发生在隧道出口**。
- **Codex 侧仍挂 127.0.0.1:1088**：为让它改走 TUN，依次 ① respect_system_proxy 改 false + 重启 ② WinINET 的 ProxyOverride 加绕过名单 ③ ProxyEnable=0（用户已做）④ 清空 ProxyServer ⑤ 清空用户级 HTTPS_PROXY / ALL_PROXY ⑥ 给 NO_PROXY 追加 *.openai.com;chatgpt.com;*.chatgpt.com;*.oaistatic.com —— 每次重启后 Get-NetTCPConnection 仍是 5~8 条连 127.0.0.1:1088、0 条直连 443；state_5.sqlite 等库里也搜不到 1088。⇒ 该代理来源不在上述六处（疑为 HZVPN 侧注入/持久化），**DSH 侧摘不掉**。②④⑤⑥ 均已还原（NO_PROXY 回到 963 字符原值，其余留 %TEMP% 备份）。
- **中转站可用（兜底路径已实测）**：http[本地盘]//ai.gmncode.com/v1/models 带 GMNCODE_API_KEY（用户级环境变量里**存在**，67 字符）直连 → **200 × 2**（5.9 s / 10.6 s），且 ai.gmncode.com 本就在 NO_PROXY 内。⇒ 需要时可用 -c model_provider=gmncode 立即绕开坏线路。
- **结论**：TUN 只是换通道，**同一节点出口仍成串丢连接**；InvalidContentType / cannot decrypt peer's message 的成因仍是「流被切断」。⇒ 修复动作 = **换节点/线路**（首选）或临时走中转。判据：10×500 KB ≥ 9/10 成功、Codex 10 分钟 0 条 retry。

## 2026-10-26 21:10~21:20 静态住宅代理首测（ipdeep 静态 IP）

- **资产（用户提供）**：70.39.158.251:7085，SOCKS5/HTTP/HTTPS 三协议 + user:pass 认证；归属 New York / PacketExchange / ASN 2914 NTT America / 住宅 / 原生 / IP 滥用=否；面板 http[本地盘]//user.ipdeep.cn/static-residential-proxies。**凭据不写进库**（放 %TEMP% 与本机环境）。
- **直连该端口的实测（此时 HZVPN 无隧道）**：TCP 7085 需 **约 21 s** 才连上（25 s 窗口内成功）；随后经它访问 api.github.com/zen、www.python.org、api.ipify.org、chatgpt.com/cdn-cgi/trace **全部在 21.0 s 超时（curl exit 28）**。⇒ 典型「握手能过、数据被丢」，**从本机直连 7085 不可用**。
- **同时基线**：网关 ping 通、baidu.com 200/0.26 s、api.github.com/zen 直连 200/4.9 s、www.python.org 直连 200/1.1 s、chatgpt.com 直连 exit 35 ⇒ 本地网络与 DNS 正常，问题只在「到 7085 这个方向」和「chatgpt 直连」。
- **HZVPN 状态（21:15 现读）**：进程 20:53:37 重启过（PID 28140/30016），**xray 不在**、**无 hzTunnel 网卡**、**1088 无监听**、经 1088 请求 exit 7 ⇒ 隧道整体不通，**链式测试无法进行**。
- **下一步（等用户动作）**：① 先把 HZVPN 连上（TUN 模式）；② 到 ipdeep 面板确认是否启用 **IP 白名单**——若启用，要加的是**隧道出口 IP**（链式后代理看到的是隧道出口，不是家宽 IP），否则会一直卡在认证/超时。之后按「TUN → 静态代理 → chatgpt」测，并用 大鲸鱼产生专用/_链路体检.py --proxy 出判据（500KB ≥9/10、2MB 3/3、重传率 ≤2%）。

## ★ 2026-10-26 22:2x 登录链条打通：桥的 TLS 丢字节 + Chrome 旧实例

**症状**：Chrome 经本地桥打开 `http[本地盘]//auth.openai.com/` 报 `ERR_SSL_PROTOCOL_ERROR`（"发送的响应无效"）；Codex 登录页报 `token_exchange_failed`。

**根因 1（桥的真 bug，已修）**：`_代理桥-SOCKS5转HTTP.py` 在 `CONNECT` 回 200 之前把已读到的字节全丢掉了。
Chrome 会在 CONNECT 之后**立刻**把 TLS ClientHello 一起发来，桥把它当垃圾丢掉 ⇒ 上游收到半截握手 ⇒ 浏览器侧 TLS 协议错误。
curl 不受影响（它等 200 才握手），所以**"curl 通、浏览器不通"就是这个 bug 的指纹**。
修法：`rest = head.split(b"\r\n\r\n",1)[1]`，`CONNECT` 回 200 后先 `remote.sendall(rest)` 再 pump。

**根因 2（Chrome 侧）**：Chrome **已有实例**会沿用旧进程的启动参数与缓存，双击快捷方式只是开新窗口，
新加的 `--disable-quic` / 改过的 bypass 名单**不会生效**。⇒ 必须 `Stop-Process -Name chrome -Force` 全退再启。

**判据（可复现的对照）**：无头真实 Chrome 走同一座桥连测 5 次加载 `auth.openai.com` = **5/5 成功**（返回 Cloudflare "请稍候…" 页，DOM 约 29KB），
证明桥与住宅线路本身没问题；把 Chrome 全退重开后，用户登录成功。

**附带事实**：
- 住宅代理偶发 RST：桥日志 `[WinError 10054] 远程主机强迫关闭了一个现有的连接`（22:08 / 21:55 各数条），刷新/重试即过；
- 并发 8 路经桥请求 `auth.openai.com/oauth/token` = **8/8 成功**（405），排除"并发被限"；
- 桥已做**开机自启**：`启动\_住宅代理桥.vbs`（pythonw 静默）；
- Codex 侧：用户级环境变量 `HTTPS_PROXY/HTTP_PROXY/ALL_PROXY = htt[本地盘]//127.0.0.1:7891`，重启后 Codex 连接稳定落在 7891（不再出现"顽固连 7085"）。
