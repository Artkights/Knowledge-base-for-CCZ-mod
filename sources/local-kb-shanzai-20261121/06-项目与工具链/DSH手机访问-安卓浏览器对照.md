# DSH 手机访问（安卓浏览器对照使用）

## 结论速览

- **手机直接打开**：**`htt[本地盘]//192.168.0.104:19388/`**（同 WiFi，零配置，会话认证自动注入）。
- **实现**：`大鲸鱼产生专用\_手机访问DSH代理.py` —— 监听 `0.0.0.0:19388` → 转发 `127.0.0.1:19387`
  → **自动注入自签合法 cookie**。
- **DSH 本体只监听回环** `127.0.0.1:19387`；认证是**签名 cookie**（不是 URL 参数）：
  `dsh-auth-<base64url(sha256(authority))>` = `v1.<b64(payload)>.<b64(HMAC-SHA256(secret, body))>`，
  `payload = {version:1, authority, issuedAt, expiresAt}`。
- **签名 `secret` 持久保存**在 `[本地盘]\Users\Administrator\.dsh\.credentials.yaml`
  （records 里 `kind: grant` 的 `payload.secret`，32 字节）⇒ **可离线签 cookie**；
  而 `launchToken`（`?token=`）每次启动随机、只在内存 ⇒ **不可离线取得**。
- **Host 白名单**：源码放行**回环 + 部署推导的 LAN IP**；实测 `Host: 192.168.0.104:19387`
  + 自签 cookie ⇒ **HTTP 200**（不是 401）。
- **防火墙**：已建入站规则 `DSH Mobile Access 19388`（TCP 19388，Allow，Any profile）。
- **注意**：代理进程需保持运行；cookie 默认 30 天，过期重启代理即重签。

## 适用版本

- 本机 DSH 桌面版（`[本地盘]\新建文件夹 (2)\DeepSeek Harness.exe`，asar `app.asar`），
  网关 `webServer` + `@deepseek-ai/dsh-web-app` + `@deepseek-ai/dsh-client-connection`。
- 本机网络：WLAN `192.168.0.104`（手机需同一 WiFi/网段）。

## 已确认事实

### 一、认证实现（asar 提取，`dsh-client-connection/lib/index.js`）

```javascript
const SECRET_BYTES = 32;
const TOKEN_QUERY = "token";
const AUTH_RECORD_KEY = credentialKey("client-connection", "browser-session");
const COOKIE_PREFIX = "dsh-auth-";
const COOKIE_PAYLOAD_VERSION = 1;

cookieName(authority) { return COOKIE_PREFIX + encodeBase64Url(sha256(authority)); }
encodeCookie(payload, secret) {
  const body = encodeBase64Url(JSON.stringify(payload));
  return `v1.${body}.${encodeBase64Url(HMAC_SHA256(secret, body))}`;
}
initializeSecret(credentials) {          // ★ 持久：已存在则复用，不存在才生成
  const secret = storedSecret(await credentials.modifyRecord(AUTH_RECORD_KEY, (current) => {
    if (current !== void 0) { storedSecret(current); return; }
    return { kind: "grant", payload: { version: 1, secret: encodeBase64Url(randomBytes(32)) } };
  }));
}
authenticatedUrl(baseUrl) { url.searchParams.set(TOKEN_QUERY, this.launchToken); }  // 每次启动随机
```

Host 校验（同文件 L208）：

```javascript
const hostUrl = parseAuthority(host);
if (!isLoopbackHostname(hostUrl.hostname) && !isTrustedAuthority(hostUrl, trustedHosts)) return false;
```

### 二、官方配置项（`dsh-web-app/lib/index.js`）

```javascript
const Config = z.object({
  openBrowser: z.boolean().default(true),
  printUrl: z.boolean().default(true),
  surfaceContext: z.boolean().default(true),
  trustedHosts: z.array(String).default([])
});
const DSH_WEB_URL = "DSH_WEB_URL";
const LOOPBACK_HOST = "127.0.0.1";
const ALL_INTERFACES_HOST = "0.0.0.0";
```

⇒ **官方也支持**局域网：在 profile 的 `cordis.patch.yml` 里给 web-app 加
`trustedHosts: [192.168.0.104]` 并让 webServer 绑 `0.0.0.0`，重启后即可。
**但重启会中断当前会话**，故本项目采用**不重启的代理方案**。

### 三、读 asar 的工具

- `大鲸鱼产生专用\_读asar.py`：`--list <关键字>` / `--extract <内部路径>` /
  `--grep "<字符串>" [--ext]`（把内容命中**归属到具体文件**）。
- asar 结构：`[8B pickle][4B JSON大小][JSON 目录][内容区]`；本机 `app.asar` 有 **12967** 个文件，
  数据区起点 `0x33C23C`。

## 实现·使用方法

1. **启动代理**（后台常驻）：

   ```
   python 大鲸鱼产生专用\_手机访问DSH代理.py --port 19388
   ```

2. **手机浏览器打开** `htt[本地盘]//192.168.0.104:19388/`。

3. **仅造 cookie（调试用）**：

   ```
   python 大鲸鱼产生专用\_造DSHcookie.py --authority 192.168.0.104:19388 --test
   ```

4. **防火墙**（已建，重建时用管理员 PowerShell）：

   ```
   New-NetFirewallRule -DisplayName "DSH Mobile Access 19388" -Direction Inbound -LocalPort 19388 -Protocol TCP -Action Allow -Profile Any
   ```

## 风险与边界

- 代理是**转发层**，DSH 关闭时它没有内容；代理停止则手机不可访问。
- 代理会**注入 cookie 并改写上游连接**，仅在本机局域网使用；不要暴露到公网。
- 官方 `trustedHosts` 方案更"正统"，但需要重启 DSH；两条路不要同时开。
- cookie 有有效期（默认 30 天），过期重启代理即可；`authority` 必须与请求的 Host 一致。

## 证据来源

- **静态复读**（asar 提取）：`dsh-client-connection/lib/index.js`（`SECRET_BYTES`/`TOKEN_QUERY`/
  `encodeCookie`/`initializeSecret`/Host 白名单）、`dsh-web-app/lib/index.js`（Config 模式）。
- **实机命中**：`_造DSHcookie.py --test` 两次 —— `Host: 127.0.0.1:19387` ⇒ **200**、
  `Host: 192.168.0.104:19387` ⇒ **200**（证明 LAN IP 在白名单内）；
  经代理：`Host: 192.168.0.104:19388` ⇒ **200** 且返回 DSH 的 HTML（`window.__ModuleLoader__`）。
- **用户口径**（2026-10-14）：手机与电脑同一 WiFi；此前未用浏览器打开过 web 界面。

## 待验证项

- 浏览器**长时间使用**（含 SSE/WebSocket 长连接）经代理的稳定性未长测；
  若出现断流，考虑改用官方 `trustedHosts` + `0.0.0.0` 绑定（需重启）。
- 手机端**上传附件**等大请求未测。


## ★★ 2026-10-14 踩坑：代理转发导致手机页面**乱码**（gzip 当明文）

**现象**：手机打开 `htt[本地盘]//192.168.0.104:19388/` 后页面全是乱码
（`Ɇ�� ��m��`、大量 `◊`/`�` 符号）。

**根因**：`_手机访问DSH代理.py` 初版在转发响应时**跳过 `Content-Encoding` 头但没解压响应体**，
而请求里**保留了浏览器的 `Accept-Encoding`** ⇒ 上游返回 gzip/br ⇒ 压缩字节被当明文发给浏览器。

```python
# 旧（错）
if k.lower() in (..., "content-encoding"):
    continue
data = resp.read()        # 压缩字节
self.wfile.write(data)    # ⇒ 浏览器按明文渲染 ⇒ 乱码
```

**修法（双层）**：

```python
# ① 请求上游时去掉 accept-encoding ⇒ 上游给明文
headers = {k: v for k, v in self.headers.items()
           if k.lower() not in ("cookie", "connection", "proxy-connection",
                                "accept-encoding")}
# ② 转发响应时**不要**再丢 content-encoding（万一仍压缩，交给浏览器解）
if k.lower() in ("connection", "keep-alive", "transfer-encoding", "content-length"):
    continue
```

**验证**：`HTTP/1.1 200 OK` + `content-type: text/html; charset=utf-8`（无 content-encoding）
+ `Content-Length: 36559` + 正文为 `<!doctype html>…` ✓

**附带提醒**：

1. 手机浏览器会**缓存**乱码响应 ⇒ 改完要**无痕打开**或加 `?v=N` 绕过缓存；
2. 本代理是「读完整响应再转发」，遇 **SSE/长连接** 会卡 ⇒ 需要时改为**边收边发**的流式转发。

**通用教训**：**任何自写反向代理都必须显式处理 `Accept-Encoding` 与 `Content-Encoding` 的一致性** ——
要么两端都不压缩，要么保留编码头交给客户端解，**绝不能只丢头不解压**。


## ★★ 2026-10-14 关键修正：拦路石是 **Host 白名单**；且**验认证必须用 API**

### 一、对照矩阵（实测，带/不带自签 cookie）

| Host 头 | 无 cookie | 有 cookie | 判定 |
|---|---|---|---|
| `127.0.0.1:19387` | 401 | **200**（`POST /api/credentials/describe`） | ✅ **cookie 有效** |
| `localhost:19387` | 401 | 404（`/api/remote.mux`，端点自身） | ✅ 接受 |
| `192.168.0.104:19387` | 403 | **403** | ✗ **Host 不准入** |
| `192.168.0.104:19388` | 403 | **403** | ✗ 同上 |

- **`401` = 缺认证（Host 已通过）；`403` = Host 不准入（不看 cookie）** —— 语义不同，勿混。
- ⇒ **本机服务端只放行回环 authority**；源码注释提到的 "deployment-derived LAN IP literals"
  在此**未覆盖该 LAN IP**（先前我据一次首页 200 误判为"LAN IP 在白名单"，**已纠正**）。

### 二、修法：代理把 Host 改写成回环

```python
authority = "127.0.0.1:19387"                 # 唯一被放行的 authority
headers["Host"]    = authority                # ★ 关键一步
headers["Cookie"]  = "<按该 authority 自签>"   # cookie 的 authority 必须与 Host 一致
headers["Origin"]  = "htt[本地盘]//" + authority     # 一并改写，避免来源校验
headers["Referer"] = ref.replace(client_host, authority)
```

**修复后经代理**：`POST /api/credentials/describe`、`POST /api/session/modelCatalog`、
`POST /api/agentPresets/list` ⇒ **全部 200**（修复前 403）⇒ 客户端可拉到会话列表。

### 三、★ 方法论：验认证**必须打 API**，首页 200 是**假阳性**

- `GET /`（引导页）**无需认证也返回 200** ⇒ 拿它验证会误判"认证已通"（第一版即栽此坑）。
- 正确探针：`POST /api/credentials/describe`（**401 → 200** 才算过）；
  `/api/remote.mux` 属子端点，**正常也 404**，只有 401/403 才有诊断价值。
- 工具：`大鲸鱼产生专用\_验DSH认证.py`（多 Host × 有无 cookie 对照矩阵）。

### 四、已修 / 已知

| 项 | 状态 |
|---|---|
| 页面乱码 | 已修：请求上游去掉 `Accept-Encoding`（否则 gzip 被当明文） |
| API 403 | 已修：代理改写 Host/Origin/Referer + 按回环 authority 签 cookie |
| `/api/remote.mux` | 带 cookie 也是 404（直连/经代理一致）⇒ 属端点自身；如客户端长连接仍依赖它，再上流式转发 |

---


## 结论速览

- **手机访问地址**：**`htt[本地盘]//192.168.0.104:19388/`**（同 WiFi，零配置，cookie 自动注入）。
- **DSH 本体已绑全网卡**：`0.0.0.0:19387` —— 由用户 patch 层
  `%USERPROFILE%\.dsh\profiles\desktop\cordis.patch.yml` 里的
  `- id: webserver / config: {host: 0.0.0.0, port: 19387}` 实现（改后需重启 DSH）。
- **为什么必须绑 0.0.0.0**：`dsh-web-app` 的 `resolveLanTrust(bindHost, extra)` 只在
  `bindHost === "0.0.0.0"` 时才把网卡 IP 收进 `trustedHosts`；绑回环时 LAN Host 一律 **403**。
- **认证是签名 cookie**：`dsh-auth-<b64(sha256(authority))>` = `v1.<b64(payload)>.<b64(HMAC-SHA256(secret,body))>`；
  `secret`（32B）持久存于 `~/.dsh/.credentials.yaml` ⇒ 可离线自签；`launchToken` 每次启动随机、不可离线取。
- **三项界面模式可选值**：`transcriptView ∈ {compact, standard, detailed}`、
  `performanceUsage ∈ {compact, detailed}`。
  **简洁模式 = `transcriptView: compact`**；本机已设 `transcriptView/performanceUsage/process = compact`。
- **改配置后需重启 DSH**（重启会中断当前会话数秒，对话记录不丢）。

## 一、手机访问链路（现状）

```
手机浏览器 ──► 192.168.0.104:19388 （_手机访问DSH代理.py）
                │  ① 注入自签 cookie  ② 改写 Host/Origin/Referer 为 127.0.0.1:19387
                │  ③ WebSocket 双向透传（阻塞 socket + select）
                ▼
             127.0.0.1:19387 （DSH 本体，实际已绑 0.0.0.0）
```

备用纯看画面：`htt[本地盘]//192.168.0.104:19389/`（`_窗口镜像.py`，MJPEG，只截 DSH 窗口）。

## 二、代理踩过的四个坑（都已修）

| # | 症状 | 根因 | 修法 |
|---|---|---|---|
| 1 | 页面**乱码** | 请求保留了 `Accept-Encoding`，上游回 gzip 而代理不解压 | 请求上游时去掉 `Accept-Encoding`；转发时不丢 `Content-Encoding` |
| 2 | API 全 **403** | 服务端 Host 白名单只放行回环 | 代理把 `Host/Origin/Referer` 改写为 `127.0.0.1:19387`；或按 Plan B 让 DSH 绑 `0.0.0.0` |
| 3 | 一直**重新连接中** | 不支持 WebSocket Upgrade | 加 TCP 级双向透传；**必须补 `Connection: Upgrade`**、且**不能重复** `Sec-WebSocket-*` |
| 4 | WS 握手成功**立刻断** | ① 读客户端用了 `connection.recv()`，而 `http.server` 的 `rfile` 已缓冲 ⇒ 拿到空误判 EOF；② socket 设为**非阻塞** ⇒ `sendall` 抛 **10035(WSAEWOULDBLOCK)** 被当断开 | ① 读客户端改用 `self.rfile.read1()`；② 透传用**阻塞 socket + select** |

## 三、配置速查（用户 patch 层）

文件：`[本地盘]\Users\Administrator\.dsh\profiles\desktop\cordis.patch.yml`

```yaml
- id: webserver                     # 局域网访问（Plan B）
  config:
    host: 0.0.0.0
    port: 19387
- id: ui-settings-account
  config:
    process: compact
    usage: compact                  # 用量展示：简洁
- id: ui-chat
  config:
    transcriptView: compact         # ★ 对话视图：简洁（每个对话默认）
    performanceUsage: compact       # 性能与用量：简洁
```

改配置的两个脚本：
- `大鲸鱼产生专用\_配置-DSH局域网访问.py --apply|--revert|--check`
- `大鲸鱼产生专用\_配置-DSH简洁模式.py --apply|--revert|--check`

两个脚本都会**自动备份 + YAML 自检**。

## 四、证据来源

- **静态复读**（asar 提取）：`dsh-host-webserver/lib/index.js`（`Config.host` 仅接受 `127.0.0.1|0.0.0.0`）、
  `dsh-web-app/lib/index.js`（`resolveLanTrust`）、`dsh-client-connection/lib/index.js`（cookie 签名）、
  `dsh-client-ui-chat/lib/client.js`（`TRANSCRIPT_VIEW_MODES` / `PERFORMANCE_USAGE_MODES`）。
- **实机验证**：绑定前 `Host: 192.168.0.104:19387` ⇒ **403**；绑 `0.0.0.0` 后 ⇒ **401/200**（放行）；
  经代理 `POST /api/credentials/describe`、`/api/session/list` ⇒ **200**；
  WebSocket `/api/remote.mux` ⇒ **101 Switching Protocols**；手机端已能显示对话并输入。

## 五、待验证 / 边界

- 代理长时间稳定性（含浏览器前台/后台切换、锁屏重连）未长测。
- 手机上传附件等大请求未测。
- `0.0.0.0` 绑定会把 GUI 暴露给同网段（有 cookie 认证，但**无 TLS**）⇒ 仅在可信局域网使用。

---


## 结论速览

- **手机访问地址**：**`htt[本地盘]//192.168.0.104:19388/`**（同 WiFi，零配置，cookie 自动注入）。
- **DSH 本体已绑全网卡**：`0.0.0.0:19387` —— 由用户 patch 层
  `%USERPROFILE%\.dsh\profiles\desktop\cordis.patch.yml` 里的
  `- id: webserver / config: {host: 0.0.0.0, port: 19387}` 实现（改后需重启 DSH）。
- **为什么必须绑 0.0.0.0**：`dsh-web-app` 的 `resolveLanTrust(bindHost, extra)` 只在
  `bindHost === "0.0.0.0"` 时才把网卡 IP 收进 `trustedHosts`；绑回环时 LAN Host 一律 **403**。
- **认证是签名 cookie**：`dsh-auth-<b64(sha256(authority))>` = `v1.<b64(payload)>.<b64(HMAC-SHA256(secret,body))>`；
  `secret`（32B）持久存于 `~/.dsh/.credentials.yaml` ⇒ 可离线自签；`launchToken` 每次启动随机、不可离线取。
- **三项界面模式可选值**：`transcriptView ∈ {compact, standard, detailed}`、
  `performanceUsage ∈ {compact, detailed}`。
  **简洁模式 = `transcriptView: compact`**；本机已设 `transcriptView/performanceUsage/process = compact`。
- **改配置后需重启 DSH**（重启会中断当前会话数秒，对话记录不丢）。

## 一、手机访问链路（现状）

```
手机浏览器 ──► 192.168.0.104:19388 （_手机访问DSH代理.py）
                │  ① 注入自签 cookie  ② 改写 Host/Origin/Referer 为 127.0.0.1:19387
                │  ③ WebSocket 双向透传（阻塞 socket + select）
                ▼
             127.0.0.1:19387 （DSH 本体，实际已绑 0.0.0.0）
```

备用纯看画面：`htt[本地盘]//192.168.0.104:19389/`（`_窗口镜像.py`，MJPEG，只截 DSH 窗口）。

## 二、代理踩过的四个坑（都已修）

| # | 症状 | 根因 | 修法 |
|---|---|---|---|
| 1 | 页面**乱码** | 请求保留了 `Accept-Encoding`，上游回 gzip 而代理不解压 | 请求上游时去掉 `Accept-Encoding`；转发时不丢 `Content-Encoding` |
| 2 | API 全 **403** | 服务端 Host 白名单只放行回环 | 代理把 `Host/Origin/Referer` 改写为 `127.0.0.1:19387`；或按 Plan B 让 DSH 绑 `0.0.0.0` |
| 3 | 一直**重新连接中** | 不支持 WebSocket Upgrade | 加 TCP 级双向透传；**必须补 `Connection: Upgrade`**、且**不能重复** `Sec-WebSocket-*` |
| 4 | WS 握手成功**立刻断** | ① 读客户端用了 `connection.recv()`，而 `http.server` 的 `rfile` 已缓冲 ⇒ 拿到空误判 EOF；② socket 设为**非阻塞** ⇒ `sendall` 抛 **10035(WSAEWOULDBLOCK)** 被当断开 | ① 读客户端改用 `self.rfile.read1()`；② 透传用**阻塞 socket + select** |

## 三、配置速查（用户 patch 层）

文件：`[本地盘]\Users\Administrator\.dsh\profiles\desktop\cordis.patch.yml`

```yaml
- id: webserver                     # 局域网访问（Plan B）
  config:
    host: 0.0.0.0
    port: 19387
- id: ui-settings-account
  config:
    process: compact
    usage: compact                  # 用量展示：简洁
- id: ui-chat
  config:
    transcriptView: compact         # ★ 对话视图：简洁（每个对话默认）
    performanceUsage: compact       # 性能与用量：简洁
```

改配置的两个脚本：
- `大鲸鱼产生专用\_配置-DSH局域网访问.py --apply|--revert|--check`
- `大鲸鱼产生专用\_配置-DSH简洁模式.py --apply|--revert|--check`

两个脚本都会**自动备份 + YAML 自检**。

## 四、证据来源

- **静态复读**（asar 提取）：`dsh-host-webserver/lib/index.js`（`Config.host` 仅接受 `127.0.0.1|0.0.0.0`）、
  `dsh-web-app/lib/index.js`（`resolveLanTrust`）、`dsh-client-connection/lib/index.js`（cookie 签名）、
  `dsh-client-ui-chat/lib/client.js`（`TRANSCRIPT_VIEW_MODES` / `PERFORMANCE_USAGE_MODES`）。
- **实机验证**：绑定前 `Host: 192.168.0.104:19387` ⇒ **403**；绑 `0.0.0.0` 后 ⇒ **401/200**（放行）；
  经代理 `POST /api/credentials/describe`、`/api/session/list` ⇒ **200**；
  WebSocket `/api/remote.mux` ⇒ **101 Switching Protocols**；手机端已能显示对话并输入。

## 五、待验证 / 边界

- 代理长时间稳定性（含浏览器前台/后台切换、锁屏重连）未长测。
- 手机上传附件等大请求未测。
- `0.0.0.0` 绑定会把 GUI 暴露给同网段（有 cookie 认证，但**无 TLS**）⇒ 仅在可信局域网使用。
