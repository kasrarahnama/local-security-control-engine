from __future__ import annotations

from typing import Any, Dict, List

from oscal_parser import (
    load_oscal_json,
    extract_components,
    extract_data_flows,
    extract_iam_constructs,
    generate_architecture_summary,
)

from control_binding import bind_controls
from control_retriever import retrieve_control_chunks


def build_summary_from_oscal(path: str) -> Dict[str, Any]:
    data = load_oscal_json(path)
    components = extract_components(data)
    flows = extract_data_flows(data)
    iam = extract_iam_constructs(data)
    return generate_architecture_summary(components, flows, iam)


def build_control_contexts(path: str) -> List[Dict[str, Any]]:
    summary = build_summary_from_oscal(path)
    bindings = bind_controls(summary)

    contexts: List[Dict[str, Any]] = []

    for binding in bindings:
        retrieved = retrieve_control_chunks(binding, summary, k=3)

        context = {
            "control_id": binding.get("control_id"),
            "control_name": binding.get("control_name"),
            "reason": binding.get("reason"),
            "applies_to": binding.get("applies_to"),
            "architecture_context": {
                "architecture_id": summary.get("architecture_id"),
                "component_count": summary.get("component_count"),
                "data_flow_count": summary.get("data_flow_count"),
                "role_count": summary.get("role_count"),
                "user_count": summary.get("user_count"),
                "policy_count": summary.get("policy_count"),
                "traceability": summary.get("traceability", {}),
            },
            "retrieval_query": retrieved.get("query"),
            "retrieved_guidance": retrieved.get("chunks", []),
        }

        contexts.append(context)

    return contexts


def main() -> None:
    contexts = build_control_contexts("sample_oscal.json")

    print("LLM-ready control contexts:\n")

    for item in contexts:
        print("=" * 80)
        print(f"CONTROL: {item['control_id']} - {item['control_name']}")
        print(f"REASON : {item['reason']}")
        print(f"APPLIES: {item['applies_to']}")
        print(f"QUERY  : {item['retrieval_query']}")
        print("\nARCHITECTURE CONTEXT:")
        print(item["architecture_context"])

        print("\nRETRIEVED GUIDANCE:")
        for i, g in enumerate(item["retrieved_guidance"], start=1):
            print(f"\n  [{i}] {g['source_name']} | topic={g['topic']} | chunk={g['chunk_index']}")
            print(f"      {g['text'][:250]}...")
        print("=" * 80)


if __name__ == "__main__":
    main()