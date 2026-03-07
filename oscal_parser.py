from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


# ------------------------------------------------------------
# Load OSCAL JSON
# ------------------------------------------------------------
def load_oscal_json(path: str | Path) -> Dict[str, Any]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"OSCAL JSON file not found: {path}")

    if path.suffix.lower() != ".json":
        raise ValueError(f"Expected a .json file, got: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in {path}: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("Expected top-level OSCAL JSON object to be a dictionary")

    return data


# ------------------------------------------------------------
# Extract Components
# ------------------------------------------------------------
def extract_components(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    system_impl = data.get("system-implementation")

    if not system_impl:
        return []

    components = system_impl.get("components", [])

    extracted = []

    for comp in components:
        extracted.append(
            {
                "id": comp.get("uuid"),
                "name": comp.get("title"),
                "type": comp.get("type"),
            }
        )

    return extracted


# ------------------------------------------------------------
# Extract Data Flows
# ------------------------------------------------------------
def extract_data_flows(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    system_impl = data.get("system-implementation", {})

    data_flows = system_impl.get("data-flows", [])

    extracted = []

    for flow in data_flows:
        extracted.append(
            {
                "id": flow.get("uuid"),
                "source": flow.get("source"),
                "destination": flow.get("destination"),
                "description": flow.get("description"),
            }
        )

    return extracted


# ------------------------------------------------------------
# Extract IAM Constructs
# ------------------------------------------------------------
def extract_iam_constructs(data: Dict[str, Any]) -> Dict[str, Any]:
    system_impl = data.get("system-implementation", {})
    iam = system_impl.get("iam", {})

    roles = iam.get("roles", [])
    users = iam.get("users", [])
    policies = iam.get("policies", [])

    extracted_roles = []
    for role in roles:
        extracted_roles.append(
            {
                "id": role.get("uuid"),
                "name": role.get("name"),
                "description": role.get("description"),
            }
        )

    extracted_users = []
    for user in users:
        extracted_users.append(
            {
                "id": user.get("uuid"),
                "name": user.get("name"),
                "type": user.get("type"),
            }
        )

    extracted_policies = []
    for policy in policies:
        extracted_policies.append(
            {
                "id": policy.get("uuid"),
                "name": policy.get("name"),
                "rules": policy.get("rules", []),
            }
        )

    return {
        "roles": extracted_roles,
        "users": extracted_users,
        "policies": extracted_policies,
    }


# ------------------------------------------------------------
# Generate Architecture Summary
# ------------------------------------------------------------
def build_traceability_map(
    components: List[Dict[str, Any]],
    flows: List[Dict[str, Any]],
    iam: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "components": {c["id"]: c for c in components if c.get("id")},
        "flows": {f["id"]: f for f in flows if f.get("id")},
        "roles": {r["id"]: r for r in iam.get("roles", []) if r.get("id")},
        "users": {u["id"]: u for u in iam.get("users", []) if u.get("id")},
        "policies": {p["id"]: p for p in iam.get("policies", []) if p.get("id")},
    }
def generate_architecture_summary(
    components: List[Dict[str, Any]],
    flows: List[Dict[str, Any]],
    iam: Dict[str, Any],
) -> Dict[str, Any]:
    traceability_map = build_traceability_map(components, flows, iam)

    summary = {
        "architecture_id": "arch-summary-001",
        "component_count": len(components),
        "data_flow_count": len(flows),
        "role_count": len(iam.get("roles", [])),
        "user_count": len(iam.get("users", [])),
        "policy_count": len(iam.get("policies", [])),
        "components": components,
        "flows": flows,
        "iam": iam,
        "trust_zones": [],
        "boundaries": [],
        "traceability": {
            "component_ids": list(traceability_map["components"].keys()),
            "flow_ids": list(traceability_map["flows"].keys()),
            "role_ids": list(traceability_map["roles"].keys()),
            "user_ids": list(traceability_map["users"].keys()),
            "policy_ids": list(traceability_map["policies"].keys()),
            "maps": traceability_map,
        },
    }

    return summary
# ------------------------------------------------------------
# Main Runner
# ------------------------------------------------------------
def main() -> None:
    sample_path = "sample_oscal.json"

    data = load_oscal_json(sample_path)

    print("OSCAL file loaded successfully.")
    print(f"Top-level keys: {list(data.keys())}")

    # Extract architecture pieces
    components = extract_components(data)
    flows = extract_data_flows(data)
    iam_constructs = extract_iam_constructs(data)

    # Print components
    print("\nComponents detected:\n")
    for comp in components:
        print(comp)

    # Print data flows
    print("\nData flows detected:\n")
    for flow in flows:
        print(flow)

    # Print IAM
    print("\nIAM constructs detected:\n")

    print("\nRoles:")
    for role in iam_constructs["roles"]:
        print(role)

    print("\nUsers:")
    for user in iam_constructs["users"]:
        print(user)

    print("\nPolicies:")
    for policy in iam_constructs["policies"]:
        print(policy)

    # Generate architecture summary
    summary = generate_architecture_summary(
        components,
        flows,
        iam_constructs,
    )

    print("\nArchitecture summary:\n")
    print(summary)


if __name__ == "__main__":
    main()