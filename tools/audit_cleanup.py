from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CLEANUP = ROOT / "sources" / "cleanup-report.json"
RESEARCH = ROOT / "research" / "research-gaps.json"

# Only these old pages have their reusable facts represented by current entity IDs.
COVERAGE = {
    "00-共性知识/资料与模板/04-版本差异矩阵.md": ["profile.ccz61.legacy", "profile.ccz64.legacy"],
    "00-共性知识/资料与模板/05-人物与兵种.md": ["struct.65.runtime-character", "struct.65.detailed-job-record"],
    "00-共性知识/资料与模板/07-人物与套装特效.md": ["struct.65.effect-assignment", "struct.66.effect-assignment"],
    "00-共性知识/资料与模板/6X版本差异与适配.md": ["profile.ccz65.unencrypted.f9a", "profile.ccz66.xiaoan.fixture.25d"],
    "6.5/02-数据结构/6.4-6.5运行时静态数据表地址.md": ["global.65.tactical-unit-array", "global.65.item-table"],
    "6.5/02-数据结构/全局变量.md": ["global.65.bool-variables", "global.65.int-variables", "global.65.pointer-variables"],
    "6.5/02-数据结构/单位结构体.md": ["struct.65.tactical-unit", "struct.65.runtime-character"],
    "6.5/02-数据结构/战场运行时内存-6.4资料与6.5复核.md": ["struct.65.tactical-unit", "global.65.physical-context"],
    "6.5/03-机制与特效/攻击范围与穿透范围.md": ["mechanism.65.physical-attack-targeting", "struct.65.range-segment"],
    "6.5/03-机制与特效/物理攻击.md": ["mechanism.65.physical-attack-targeting"],
    "6.5/04-函数速查/函数速查表.md": ["fn.65.item-id-to-record", "fn.65.attack-dispatch", "fn.65.core-effect-engine"],
    "6.5/04-数据表与资源/图片处理-E5资源.md": ["format.e5.indexed-archive"],
    "6.5/04-数据表与资源/宝物物品设定.md": ["struct.65.item-record", "format.item.split-data-star"],
    "6.5/06-工具与验证/旧扳手源码专项-功勋引擎特效战场.md": ["global.65.merit", "struct.65.effect-assignment", "fn.65.revive-tactical-unit"],
    "6.5/06-工具与验证/旧扳手调试器源码对照.md": ["profile.ccz65.unencrypted.f9a", "legacy.addresses.64"],
    "6.6/06-工具与验证/小暗补丁6.6源码复用指南.md": ["mechanism.66.xiaoan.super-s", "locator.66.xiaoan.native-super"],
    "6.6/06-工具与验证/曹操传6.6扳手适配与自动回归验证.md": ["struct.66.effect-assignment", "struct.66.item-record"],
}


def version_for(path: str) -> list[str]:
    first = path.split("/", 1)[0]
    return [first] if first in {"6.5", "6.5pl", "6.6"} else ["shared"]


def main() -> None:
    cleanup = json.loads(CLEANUP.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for record in cleanup["records"]:
        path = record["oldPath"]
        if path in COVERAGE:
            record["action"] = "merge-into-entity"
            record["mappedEntities"] = COVERAGE[path]
            record["reason"] = "可复核的地址、字段或调用关系已进入列出的结构化实体；旧叙述页删除。"
        elif record["action"] == "merge-into-entity":
            record["action"] = "research-gap"
            record.pop("mappedEntities", None)
            record["reason"] = "包含潜在技术信息，但尚未完整绑定画像、ABI、原字节或字段证据；不得视为已合并。"
        counts[record["action"]] = counts.get(record["action"], 0) + 1
    cleanup["decisionCounts"] = counts
    cleanup["coverageRule"] = "merge-into-entity 必须列出当前存在的 mappedEntities；其余技术候选进入 research queue。"
    CLEANUP.write_text(json.dumps(cleanup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    research = json.loads(RESEARCH.read_text(encoding="utf-8"))
    base = [item for item in research["entries"] if not item["id"].startswith("research.legacy-doc.")]
    for record in cleanup["records"]:
        if record["action"] != "research-gap":
            continue
        digest = hashlib.sha256(record["oldPath"].encode("utf-8")).hexdigest()[:16]
        base.append({
            "id": f"research.legacy-doc.{digest}",
            "title": "复核旧条目：" + record["oldTitle"],
            "versions": version_for(record["oldPath"]),
            "status": "open",
            "evidence": "legacy-document-only",
            "legacyPath": record["oldPath"],
            "known": ["旧条目已从正式知识树删除；路径和处置决定保留在 cleanup report。"],
            "needed": ["从对应一方源码或样本重新提取", "绑定版本画像和样本", "补齐地址种类、结构或 Hook/ABI 后再进入正式索引"],
            "sourceRefs": [],
        })
    research["entries"] = sorted(base, key=lambda item: item["id"])
    RESEARCH.write_text(json.dumps(research, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"cleanup={len(cleanup['records'])} research={len(base)} counts={counts}")


if __name__ == "__main__":
    main()
