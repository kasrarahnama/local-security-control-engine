from __future__ import annotations

from typing import Any, Dict, List


def build_control_query(
    binding: Dict[str, Any],
    architecture_summary: Dict[str, Any],
) -> str:
    control_id = binding.get("control_id", "")
    control_name = binding.get("control_name", "")
    reason = binding.get("reason", "")
    applies_to = binding.get("applies_to", {})

    query_parts: List[str] = [control_id, control_name, reason]

    # Add referenced component names
    component_ids = applies_to.get("components", [])
    role_ids = applies_to.get("roles", [])
    policy_ids = applies_to.get("policies", [])
    flow_ids = applies_to.get("flows", [])

    trace_maps = architecture_summary.get("traceability", {}).get("maps", {})

    component_map = trace_maps.get("components", {})
    role_map = trace_maps.get("roles", {})
    policy_map = trace_maps.get("policies", {})
    flow_map = trace_maps.get("flows", {})

    for comp_id in component_ids:
        comp = component_map.get(comp_id)
        if comp:
            query_parts.append(comp.get("name", ""))
            query_parts.append(comp.get("type", ""))

    for role_id in role_ids:
        role = role_map.get(role_id)
        if role:
            query_parts.append(role.get("name", ""))

    for policy_id in policy_ids:
        policy = policy_map.get(policy_id)
        if policy:
            query_parts.append(policy.get("name", ""))

    for flow_id in flow_ids:
        flow = flow_map.get(flow_id)
        if flow:
            query_parts.append(flow.get("description", ""))
            query_parts.append(flow.get("source", ""))
            query_parts.append(flow.get("destination", ""))

    # Normalize and remove empty strings
    cleaned = [part.strip() for part in query_parts if str(part).strip()]
    return " ".join(cleaned)