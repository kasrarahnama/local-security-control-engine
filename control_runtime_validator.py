from __future__ import annotations

from typing import Any, Dict, List

from evidence_categories import EVIDENCE_CATEGORIES


VALID_ARTIFACT_TYPES = set(EVIDENCE_CATEGORIES.keys())


def validate_runtime_output(control_output: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    if not control_output.get("implementation_guidance"):
        errors.append("implementation_guidance must not be empty")

    if not control_output.get("evidence_sources"):
        errors.append("evidence_sources must not be empty")

    verification_steps = control_output.get("verification_steps", [])
    if not verification_steps:
        errors.append("verification_steps must not be empty")

    for i, step in enumerate(verification_steps):
        artifact_type = step.get("artifact_type")
        if artifact_type not in VALID_ARTIFACT_TYPES:
            errors.append(
                f"verification_steps[{i}].artifact_type '{artifact_type}' is not a valid evidence category"
            )

        if not step.get("step"):
            errors.append(f"verification_steps[{i}].step must not be empty")

        if not step.get("expected_result"):
            errors.append(f"verification_steps[{i}].expected_result must not be empty")

    return errors


def validate_all_outputs(outputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    for output in outputs:
        errors = validate_runtime_output(output)
        results.append(
            {
                "control_id": output.get("control_id"),
                "control_name": output.get("control_name"),
                "valid": len(errors) == 0,
                "errors": errors,
            }
        )

    return results