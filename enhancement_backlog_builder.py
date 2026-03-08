from __future__ import annotations

from typing import Any, Dict, List

from architecture_deviation_detector import (
    build_summary_from_oscal,
    detect_architecture_alignment,
)


def build_backlog_items_from_deviations(deviations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    backlog_items: List[Dict[str, Any]] = []

    for deviation in deviations:
        category = deviation.get("category", "unknown")
        message = deviation.get("message", "")
        enhancement = deviation.get("enhancement_opportunity", "")

        backlog_items.append(
            {
                "work_item_type": "Task",
                "title": f"Address architectural deviation: {category}",
                "description": message,
                "proposed_action": enhancement,
                "priority": 2,
                "tags": ["security", "architecture", "deviation"],
                "status": "New",
            }
        )

    return backlog_items


def main() -> None:
    summary = build_summary_from_oscal("sample_oscal.json")
    result = detect_architecture_alignment(summary)

    deviations = result.get("deviations", [])
    backlog_items = build_backlog_items_from_deviations(deviations)

    print("Generated backlog items:\n")
    for item in backlog_items:
        print(item)


if __name__ == "__main__":
    main()