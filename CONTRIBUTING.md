# 贡献规则

新增事实必须先写入版本 `data/` JSON，包含唯一 ID、版本、profile、证据和 sourceRefs。地址必须声明种类；Hook 必须补齐旧字节、覆盖长度、ABI、桩和回跳。随后运行 `build_reference.py`、`build_index.py` 和 `validate_kb.py`，不直接编辑 `reference/` 或 `index.json`。
