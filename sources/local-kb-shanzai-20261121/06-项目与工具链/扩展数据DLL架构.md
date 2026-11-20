# 扩展数据 DLL 架构（ExtendData）

## 结论速览

- `ExtendData.dll` 是**注入型扩展插件**：注入 `Ekd5.exe` 后用
  `SetWindowLong(GWL_WNDPROC)` 挂钩窗口过程，并把**自己的函数指针表**注册到
  游戏内存固定地址 **`0x4F0000`**，供**游戏脚本**用 `call [0x4F00xx]` 回调。
- 它管理的扩展数据（特技 / 策略 / 锻造 / 变量）是 **DLL 内部的全局数组**；
  游戏通过 `[0x4F0004]`（= `person_effect` 地址）直接访问。
- 扩展存档写成 **`.EXS`** 文件（与游戏自带 `.E5S` 并列）。

## 适用版本

- 源码 <http[本地盘]//github.com/Puluomiyuhun/CCZ-ExtendData>（v2.0，2026-06）
- 本地副本：`大鲸鱼产生专用\_外部源码\CCZ-ExtendData\`

## 已确认事实

### 1. 函数表注册（`dllmain.cpp`）

```c
hpro = OpenProcess(PROCESS_CREATE_THREAD | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, FALSE, dwCurrentProcessId);
    DWORD addr = (DWORD)person_mes;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x00), &addr, 4, 0);
    addr = (DWORD)person_effect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x04), &addr, 4, 0);
    addr = (DWORD)GetPersonEffect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x08), &addr, 4, 0);
    addr = (DWORD)AddPersonEffect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x0C), &addr, 4, 0);
    addr = (DWORD)LoadVar;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x10), &addr, 4, 0);
    addr = (DWORD)SaveVar;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x14), &addr, 4, 0);
    addr = (DWORD)ChangePersonEffect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x18), &addr, 4, 0);
    addr = (DWORD)GetRoundChange;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x28), &addr, 4, 0);
    addr = (DWORD)GetAttack;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x2C), &addr, 4, 0);
    addr = (DWORD)GetBook;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x30), &addr, 4, 0);
    addr = (DWORD)person_meff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x34), &addr, 4, 0);
    addr = (DWORD)GetPersonMeff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x38), &addr, 4, 0);
    addr = (DWORD)AddPersonMeff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x3C), &addr, 4, 0);
    addr = (DWORD)ChangePersonMeff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x40), &addr, 4, 0);
    addr = (DWORD)ChangeDir;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x44), &addr, 4, 0);
    addr = (DWORD)forge;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x48), &addr, 4, 0);
    addr = (DWORD)ForgeDialog;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x50), &addr, 4, 0);
    addr = (DWORD)CanForge;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x54), &addr, 4, 0);
    addr = (DWORD)InitTaFang;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x58), &addr, 4, 0);
    addr = (DWORD)random_path;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x5C), &addr, 4, 0);
    addr = (DWORD)ReloadForge;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x60), &addr, 4, 0);
    addr = (DWORD)OperateDialog;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x100), &addr, 4, 0);

    /*载入调色板*/
    for (int i = 0; i < 256; i++) {
        for (int j = 0; j < 3; j++) {
            ReadProcessMemory(hpro, (LPCVOID)(0x511400 + i * 4 + j), &tsb[i][j], 1, 0);
        }
    }
}

#ifdef WIN32
BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        h_dll_ins = hModule;
        h_exe_ins = GetModuleHandle(NULL);
        InitData();
        CreateThread(NULL, 0, MainThread, hModule, 0, NULL);
        CreateThread(NULL, 0, InitThread, hModule, 0, NULL);
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
#else
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    PSTR szCmdLine, int iCmdShow)
{
    h_dll_ins = hInstance;
    h_exe_ins = GetModuleHandle(NULL);
    CreateThread(NULL, 0, MainThread, hInstance, 0, NULL);
    //CreateThread(NULL, 0, InitThread, hInstance, 0, NULL);
    strcpy(path, "[本地盘]/曹操传/楚汉韩信传6.4/");
    loadTSB();
    Maibing();
    return 0;
}
#endif

```

- `ADDR_FUNC_TABLE = 0x4F0000`，按 **4 字节一个槽**依次写入各功能入口。
- `+0x00`、**`+0x04 = (DWORD)person_effect`**、`+0x08`、`+0x0C`、`+0x10`、
  `+0x14`、`+0x18`、`+0x28`、`+0x2C`、`+0x30`；
  `+0x34 = (DWORD)person_meff`；`+0x38`、`+0x3C`、`+0x40`、`+0x44`、`+0x48`、
  `+0x50`、`+0x54`、`+0x58`、`+0x5C`、`+0x60`、`+0x100`。
- 进程句柄权限：
  `PROCESS_CREATE_THREAD | PROCESS_VM_OPERATION | PROCESS_VM_WRITE |
   PROCESS_VM_READ | PROCESS_QUERY_INFORMATION`

### 2. 导出接口（游戏回调 DLL）

| 导出 | 触发时机 | 作用 |
|---|---|---|
| `GetRoundChange(kind)` | `kind=0` 每回合 / `kind=1` 关卡结束 | 临时特技回合递减 / 清理 |
| `GetAttack(kind)` | `kind=0` 物理 / `kind=1` 策略 | 取攻击者角色号，供特技判定 |
| 其它 | 见 `dllmain.cpp` | 加特技 / 改策略 / 经验等 |

### 3. 扩展存档（`.EXS`）

```c
memset(person_effect, 0, sizeof(person_effect));

    ifstream file("Effect.e5", ios::binary);
    if (file) {
        file.read(reinterpret_cast<char*>(person_effect), sizeof(person_effect));
        file.close();
    }

    ifstream file4("Effectmsg.e5", ios::binary);
    if (file4) {
        file4.read(reinterpret_cast<char*>(effect_message), sizeof(effect_message));
        file4.close();
    }

    ifstream file5("Forge.e5", ios::binary);
    if (file5) {
        file5.read(reinterpret_cast<char*>(forge), sizeof(forge));
        file5.close();
    }

    ifstream file6("MeffStudy.e5", ios::binary);
    if (file6) {
        file6.read(reinterpret_cast<char*>(person_meff), sizeof(person_meff));
        file6.close();
    }

    GetCurrentDirectoryA(104, path);
    strcat_s(path, "\\");

    DWORD dwCurrentProcessId = GetCurrentProcessId();
    hpro = OpenProcess(PROCESS_CREATE_THREAD | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, FALSE, dwCurrentProcessId);
    DWORD addr = (DWORD)person_mes;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x00), &addr, 4, 0);
    addr = (DWORD)person_effect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x04), &addr, 4, 0);
    addr = (DWORD)GetPersonEffect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x08), &addr, 4, 0);
    addr = (DWORD)AddPersonEffect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x0C), &addr, 4, 0);
    addr = (DWORD)LoadVar;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x10), &addr, 4, 0);
    addr = (DWORD)SaveVar;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x14), &addr, 4, 0);
    addr = (DWORD)ChangePersonEffect;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x18), &addr, 4, 0);
    addr = (DWORD)GetRoundChange;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x28), &addr, 4, 0);
    addr = (DWORD)GetAttack;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x2C), &addr, 4, 0);
    addr = (DWORD)GetBook;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x30), &addr, 4, 0);
    addr = (DWORD)person_meff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x34), &addr, 4, 0);
    addr = (DWORD)GetPersonMeff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x38), &addr, 4, 0);
    addr = (DWORD)AddPersonMeff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x3C), &addr, 4, 0);
    addr = (DWORD)ChangePersonMeff;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x40), &addr, 4, 0);
    addr = (DWORD)ChangeDir;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x44), &addr, 4, 0);
    addr = (DWORD)forge;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x48), &addr, 4, 0);
    addr = (DWORD)ForgeDialog;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x50), &addr, 4, 0);
    addr = (DWORD)CanForge;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x54), &addr, 4, 0);
    addr = (DWORD)InitTaFang;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x58), &addr, 4, 0);
    addr = (DWORD)random_path;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x5C), &addr, 4, 0);
    addr = (DWORD)ReloadForge;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x60), &addr, 4, 0);
    addr = (DWORD)OperateDialog;
    WriteProcessMemory(hpro, (LPVOID)(ADDR_FUNC_TABLE + 0x100), &addr, 4, 0);

    /*载入调色板*/
    for (int i = 0; i < 256; i++) {
        for (int j = 0; j < 3; j++) {
            ReadProcessMemory(hpro, (LPCVOID)(0x511400 + i * 4 + j), &tsb[i][j], 1, 0);
        }
    }
}

#ifdef WIN32
BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        h_dll_ins = hModule;
        h_exe_ins = GetModuleHandle(NULL);
        InitData();
        CreateThread(NULL, 0, MainThread, hModule, 0, NULL);
        CreateThread(NULL, 0, InitThread, hModule, 0, NULL);
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
#else
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    PSTR szCmdLine, int iCmdShow)
{
    h_dll_ins = hInstance;
    h_exe_ins = GetModuleHandle(NULL);
    CreateThread(NULL, 0, MainThread, hInstance, 0, NULL);
    //CreateThread(NULL, 0, InitThread, hInstance, 0, NULL);
    strcpy(path, "[本地盘]/曹操传/楚汉韩信传6.4/");
    loadTSB();
    Maibing();
    return 0;
}
#endif

```

- 自写文件头 + `person_effect` / `person_meff` 整块读写。
- ⇒ **读档会覆盖内存里的特技表**（与我们"写了没效果"的实测吻合）。

### 4. 菜单与资源

- 在游戏菜单追加**「扩展系统」**子菜单（`IDM_MENUITEM1..4`、`IDM_DUEL`、
  `IDM_BLACKJACK`、`IDM_RELATION`、`IDM_CITYMAP`、`IDM_RENDER_HOOK`）。
- 资源在 `ExtendData.rc` / `resource.h`。

### 5. 运行时依赖的数据文件

| 文件 | 内容 | 生成方 |
|---|---|---|
| `Effect.e5` | 特技数据 | `CCZ-ExtendModifier` |
| `MeffStudy.e5` | 策略数据 | 同上 |
| `Forge.e5` | 锻造配方 | 同上 |
| `Effectmsg.e5` | 特技消息配置 | 同上 |
| `ExtendData/worldmap.png` | 大地图背景 1228×819 | 手工准备 |

## 实现·使用方法

- 注入：用 DLL 注入器（如 Winject）注入 `Ekd5.exe`，或在启动器里配置自动注入。
- 编译：VS2019+，`Release | x86`，产物 `Release/ExtendData.dll`。

## 风险与边界

- 这是**第三方 DLL**，与我们的 `Ekd5.exe` 补丁**共享同一进程地址空间**；
  改 `Ekd5.exe` 时要注意不与它抢 `0x4F00xx` 区。
- `0x4F0000` 是**游戏脚本与 DLL 的约定接口**；脚本里 `call [0x4F00xx]` 依赖它。

## 证据来源

- `CCZ-ExtendData/ExtendData/dllmain.cpp`、`README.md`（本地副本）。

## 待验证项

- **P1**：`0x4F00xx` 每个槽**具体对应哪个功能**（源码里 `addr=` 前一行可辨）。
- **P1**：`.EXS` 的文件头格式（是否能被外部工具解析）。
- **P2**：与工作区现有 `ExtendData.dll`（2026-10-11 版）的版本差异。
