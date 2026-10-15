# 6.5 文件格式

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/file-formats/binary-formats.json`

## E5 索引资源封包

ID: `format.e5.indexed-archive`；状态: `canonical`；证据: `source-reviewed`

字节序: `big for directory fields`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `stored_length` | `0x0` | 4 | `uint32be` | 封包中实际字节数 |
| `decoded_length` | `0x4` | 4 | `uint32be` | 解码后字节数 |
| `payload_offset` | `0x8` | 4 | `uint32be` | 相对文件开头的负载偏移 |

- stored_length != decoded_length 表示 LS12 压缩
- 首项 payload_offset 决定目录项数量
- 完全相同的负载范围允许共享；其它相交范围为异常
- 未压缩负载可按 BMP/JPG/PNG/RAW 魔数或尺寸识别

## EEX 文件识别魔数

ID: `format.eex.probed-header`；状态: `canonical`；证据: `source-reviewed`

字节序: `not applicable to the verified magic`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `magic` | `0x0` | 4 | `bytes` | 固定字节 45 45 58 00，即 ASCII EEX\0 |

- offset 0x00 的四字节魔数用于识别 EEX 文件

## Hexzmap 地形目录

ID: `format.hexzmap.terrain-directory`；状态: `canonical`；证据: `source-reviewed`

字节序: `big for directory fields`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `segment_length` | `0x0` | 4 | `uint32be` | 存储段长度 |
| `decoded_length` | `0x4` | 4 | `uint32be` | 解码长度/长度副本 |
| `file_offset` | `0x8` | 4 | `uint32be` | 段起始文件偏移 |


## 6.5/6.6 分段物品表存储

ID: `format.item.split-data-star`；状态: `canonical`；证据: `source-reviewed`

字节序: `little`

- 合计 255 条
- 6.5 名称区 0x11 字节
- 6.6 名称区 0x0F 字节，后续字段位置相应不同
