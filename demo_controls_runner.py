import json
from typing import Any, Dict, List

from control_implementation_engine import generate_all_control_outputs


TARGET_CONTROLS = {"AC-4", "AU-2", "SC-7"}


def filter_demo_controls(outputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    selected = []
    for output in outputs:
        control_id = output.get("control_id", "")
        if control_id in TARGET_CONTROLS:
            selected.append(output)
    return selected


def main() -> None:
    outputs = generate_all_control_outputs("sample_oscal.json")
    demo_outputs = filter_demo_controls(outputs)

    print("\nDemo control outputs:\n")
    print(json.dumps(demo_outputs, indent=2))

    with open("demo_controls_output.json", "w", encoding="utf-8") as f:
        json.dump(demo_outputs, f, indent=2)

    print("\nSaved demo output to demo_controls_output.json")


if __name__ == "__main__":
    main()