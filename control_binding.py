from __future__ import annotations

from typing import Any, Dict, List

from oscal_parser import (
    load_oscal_json,
    extract_components,
    extract_data_flows,
    extract_iam_constructs,
    generate_architecture_summary,
)


def bind_controls(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    bindings: List[Dict[str, Any]] = []

    components = summary.get("components", [])
    flows = summary.get("flows", [])
    iam = summary.get("iam", {})

    roles = iam.get("roles", [])
    users = iam.get("users", [])
    policies = iam.get("policies", [])

    # Rule 1: IAM-related controls
    if roles or users or policies:
        bindings.append(
            {
                "control_id": "AC-2/AC-3",
                "control_name": "Account Management / Access Enforcement",
                "reason": "IAM constructs detected in architecture",
                "applies_to": {
                    "roles": [r.get("id") for r in roles],
                    "users": [u.get("id") for u in users],
                    "policies": [p.get("id") for p in policies],
                },
            }
        )

        bindings.append(
            {
                "control_id": "LeastPrivilege",
                "control_name": "Least Privilege Access",
                "reason": "Roles and policies should be limited to required permissions only",
                "applies_to": {
                    "roles": [r.get("id") for r in roles],
                    "policies": [p.get("id") for p in policies],
                },
            }
        )

    # Rule 2: Data-flow-related controls
    if flows:
        bindings.append(
            {
                "control_id": "AC-4",
                "control_name": "Information Flow Enforcement",
                "reason": "Architecture contains explicit data flows between components",
                "applies_to": {
                    "flows": [f.get("id") for f in flows],
                },
            }
        )

    # Rule 3: Database-related controls
    database_components = [
        c for c in components if str(c.get("type", "")).lower() == "database"
    ]
    if database_components:
        bindings.append(
            {
                "control_id": "SC-28",
                "control_name": "Protection of Information at Rest",
                "reason": "Database components exist in architecture",
                "applies_to": {
                    "components": [c.get("id") for c in database_components],
                },
            }
        )

    # Rule 4: Application-related controls
    application_components = [
        c for c in components if str(c.get("type", "")).lower() == "application"
    ]
    if application_components:
        bindings.append(
            {
                "control_id": "SI-10",
                "control_name": "Information Input Validation",
                "reason": "Application components accept and process input",
                "applies_to": {
                    "components": [c.get("id") for c in application_components],
                },
            }
        )

    return bindings


def build_summary_from_oscal(path: str) -> Dict[str, Any]:
    data = load_oscal_json(path)
    components = extract_components(data)
    flows = extract_data_flows(data)
    iam = extract_iam_constructs(data)
    return generate_architecture_summary(components, flows, iam)


def main() -> None:
    summary = build_summary_from_oscal("sample_oscal.json")
    bindings = bind_controls(summary)

    print("Control bindings detected:\n")
    for binding in bindings:
        print(binding)


if __name__ == "__main__":
    main()