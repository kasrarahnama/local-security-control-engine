from __future__ import annotations

from typing import Any, Dict, List

from aws_security_baseline import AWS_SECURITY_BASELINE
from oscal_parser import (
    load_oscal_json,
    extract_components,
    extract_data_flows,
    extract_iam_constructs,
    generate_architecture_summary,
)


def build_summary_from_oscal(path: str) -> Dict[str, Any]:
    data = load_oscal_json(path)
    components = extract_components(data)
    flows = extract_data_flows(data)
    iam = extract_iam_constructs(data)
    return generate_architecture_summary(components, flows, iam)


def detect_architecture_alignment(summary: Dict[str, Any]) -> Dict[str, Any]:
    deviations: List[Dict[str, Any]] = []

    component_names = [
        str(c.get("name", "")).lower()
        for c in summary.get("components", [])
    ]

    # 1) Multi-account expectation
    if AWS_SECURITY_BASELINE.get("multi_account_required"):
        expected_accounts = AWS_SECURITY_BASELINE.get("expected_accounts", [])

        missing_accounts = []
        for account_name in expected_accounts:
            if account_name.lower() not in component_names:
                missing_accounts.append(account_name)

        if missing_accounts:
            deviations.append(
                {
                    "category": "multi_account",
                    "status": "deviation",
                    "message": f"Missing expected account components: {missing_accounts}",
                    "enhancement_opportunity": "Adopt a multi-account structure with dedicated security, logging, and workload accounts",
                }
            )

    # 2) Centralized logging expectation
    centralized_logging = AWS_SECURITY_BASELINE.get("centralized_logging", {})
    if centralized_logging.get("cloudtrail"):
        if "logging" not in component_names:
            deviations.append(
                {
                    "category": "centralized_logging",
                    "status": "deviation",
                    "message": "No dedicated logging component/account detected for centralized logging",
                    "enhancement_opportunity": "Introduce a dedicated logging account or component to centralize CloudTrail and Flow Log collection",
                }
            )

    # 3) Guardrails expectation
    if AWS_SECURITY_BASELINE.get("guardrails"):
        iam = summary.get("iam", {})
        policies = iam.get("policies", [])

        if not policies:
            deviations.append(
                {
                    "category": "guardrails",
                    "status": "deviation",
                    "message": "No IAM/SCP-like policy artifacts detected to represent baseline guardrails",
                    "enhancement_opportunity": "Add baseline guardrails such as SCPs, IAM policy restrictions, and AWS Config rules",
                }
            )

    aligned = len(deviations) == 0

    return {
        "aligned": aligned,
        "deviations": deviations,
    }


def main() -> None:
    summary = build_summary_from_oscal("sample_oscal.json")
    result = detect_architecture_alignment(summary)

    print("Architecture alignment result:\n")
    print(result)


if __name__ == "__main__":
    main()