from __future__ import annotations
from pydantic import ValidationError
from control_output_schema import validate_control_output

import json
from typing import Any, Dict, List

from langchain_ollama import ChatOllama

from control_context_builder import build_control_contexts
from shared_responsibility import SHARED_RESPONSIBILITY


def build_prompt(context: Dict[str, Any]) -> str:
    return f"""
You are a security control implementation assistant.

Your task is to generate a structured JSON output for a single security control.

Requirements:
- Return ONLY valid JSON
- Do not include markdown
- Do not include explanations outside JSON
- Keep references to architecture element IDs
- Use the retrieved guidance as evidence
- Produce concise implementation guidance
- Use only architecture element IDs that are explicitly present in the provided applies_to section
- Do not invent new component, role, user, policy, or flow IDs
- If a binding category does not apply, return an empty list for that category

The required JSON structure is:

{{
  "control_id": "...",
  "control_name": "...",
  "reason": "...",
  "architecture_binding": {{
    "components": [],
    "roles": [],
    "users": [],
    "policies": [],
    "flows": []
  }},
  "implementation_guidance": [
    "..."
  ],
  "evidence_sources": [
    {{
      "source_name": "...",
      "chunk_index": 0,
      "topic": "..."
    }}
  ],
  "verification_steps": [
    {{
      "step": "...",
      "artifact_type": "...",
      "expected_result": "..."
    }}
  ],
  "shared_responsibility": {{
    "provider": "...",
    "customer": "..."
  }}
}}

Architecture-aware control context:
{json.dumps(context, indent=2)}
""".strip()

def enforce_binding_ids(
    generated_output: Dict[str, Any],
    context: Dict[str, Any],
) -> Dict[str, Any]:
    allowed = context.get("applies_to", {})

    allowed_components = set(allowed.get("components", []))
    allowed_roles = set(allowed.get("roles", []))
    allowed_users = set(allowed.get("users", []))
    allowed_policies = set(allowed.get("policies", []))
    allowed_flows = set(allowed.get("flows", []))

    binding = generated_output.get("architecture_binding", {})

    cleaned_binding = {
        "components": [x for x in binding.get("components", []) if x in allowed_components],
        "roles": [x for x in binding.get("roles", []) if x in allowed_roles],
        "users": [x for x in binding.get("users", []) if x in allowed_users],
        "policies": [x for x in binding.get("policies", []) if x in allowed_policies],
        "flows": [x for x in binding.get("flows", []) if x in allowed_flows],
    }

    generated_output["architecture_binding"] = cleaned_binding
    return generated_output

def build_verification_steps(control_id: str) -> list[dict]:
    if control_id == "LeastPrivilege":
        return [
            {
                "step": "Review IAM policies attached to the referenced roles and confirm permissions are limited to required actions only",
                "artifact_type": "IAM_POLICY",
                "expected_result": "No excessive permissions are present",
            },
            {
                "step": "Review SCPs to confirm organization-wide privilege guardrails are enforced",
                "artifact_type": "SCP",
                "expected_result": "Privilege escalation paths are restricted",
            },
        ]

    if control_id == "AC-2/AC-3":
        return [
            {
                "step": "Review IAM roles, users, and policies for account management and access enforcement",
                "artifact_type": "IAM_POLICY",
                "expected_result": "Access is limited to approved identities and actions",
            },
            {
                "step": "Review CloudTrail logs for account and policy change events",
                "artifact_type": "CLOUDTRAIL",
                "expected_result": "All account and permission changes are logged",
            },
        ]

    if control_id == "AC-4":
        return [
            {
                "step": "Review VPC Flow Logs for the referenced flows and confirm only approved communication paths are present",
                "artifact_type": "FLOW_LOGS",
                "expected_result": "Only authorized traffic flows are observed",
            },
            {
                "step": "Review AWS Config rules for network boundary enforcement settings",
                "artifact_type": "AWS_CONFIG",
                "expected_result": "Boundary-related configuration is compliant",
            },
        ]

    if control_id == "SC-28":
        return [
            {
                "step": "Review AWS Config and storage settings to confirm encryption at rest is enabled",
                "artifact_type": "AWS_CONFIG",
                "expected_result": "Referenced storage resources are encrypted at rest",
            }
        ]

    if control_id == "SI-10":
        return [
            {
                "step": "Review application logging and CloudTrail-related traces for input validation enforcement",
                "artifact_type": "CLOUDTRAIL",
                "expected_result": "Input validation controls are active and auditable",
            }
        ]

    return []


def generate_control_output(
    context: Dict[str, Any],
    model_name: str = "llama3.1",
) -> Dict[str, Any]:
    llm = ChatOllama(model=model_name, temperature=0)

    prompt = build_prompt(context)
    response = llm.invoke(prompt)

    raw_text = response.content.strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "control_id": context.get("control_id"),
            "control_name": context.get("control_name"),
            "error": "Model did not return valid JSON",
            "raw_output": raw_text,
        }

    try:
        validated = validate_control_output(parsed)
        cleaned = enforce_binding_ids(validated.model_dump(), context)
        cleaned["verification_steps"] = build_verification_steps(cleaned["control_id"])
        cleaned["shared_responsibility"] = SHARED_RESPONSIBILITY.get(
            cleaned["control_id"],
            {"provider": "unknown", "customer": "unknown"},
        )
        return cleaned
    except ValidationError as e:
        return {
            "control_id": context.get("control_id"),
            "control_name": context.get("control_name"),
            "error": "Schema validation failed",
            "validation_details": e.errors(),
            "raw_output": parsed,
        }

def generate_all_control_outputs(
    oscal_path: str,
    model_name: str = "llama3.1",
) -> List[Dict[str, Any]]:
    contexts = build_control_contexts(oscal_path)
    results: List[Dict[str, Any]] = []

    for context in contexts:
        output = generate_control_output(context, model_name=model_name)
        results.append(output)

    return results


def save_outputs(outputs: List[Dict[str, Any]], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=2)


def main() -> None:
    outputs = generate_all_control_outputs("sample_oscal.json", model_name="llama3.1")

    print("Structured control implementation outputs:\n")
    for item in outputs:
        print("=" * 80)
        print(json.dumps(item, indent=2))
        print("=" * 80)

    save_outputs(outputs, "control_implementation_output.json")
    print("\nSaved output to control_implementation_output.json")


if __name__ == "__main__":
    main()