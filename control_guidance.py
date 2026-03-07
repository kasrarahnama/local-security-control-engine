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
from query_corpus import build_vectorstore


CONTROL_QUERY_MAP = {
    "AC-2/AC-3": "account management access enforcement IAM",
    "LeastPrivilege": "least privilege IAM permissions",
    "AC-4": "information flow enforcement network segmentation",
    "SC-28": "protection of information at rest database encryption",
    "SI-10": "input validation application security",
}


def build_summary_from_oscal(path: str) -> Dict[str, Any]:
    data = load_oscal_json(path)
    components = extract_components(data)
    flows = extract_data_flows(data)
    iam = extract_iam_constructs(data)
    return generate_architecture_summary(components, flows, iam)


def retrieve_guidance_for_control(
    control_id: str,
    db,
    k: int = 3,
) -> List[Dict[str, Any]]:
    query = CONTROL_QUERY_MAP.get(control_id, control_id)

    results = db.similarity_search(query, k=k)

    extracted = []
    for doc in results:
        meta = doc.metadata or {}
        extracted.append(
            {
                "source_name": meta.get("source_name"),
                "topic": meta.get("topic"),
                "source_path": meta.get("source_path"),
                "chunk_index": meta.get("chunk_index"),
                "text": doc.page_content[:500],
            }
        )

    return extracted


def build_control_guidance(path: str) -> List[Dict[str, Any]]:
    summary = build_summary_from_oscal(path)
    bindings = bind_controls(summary)

    db = build_vectorstore("nomic-embed-text")

    enriched = []

    for binding in bindings:
        control_id = binding["control_id"]

        guidance = retrieve_guidance_for_control(control_id, db, k=3)

        enriched.append(
            {
                "control_id": binding["control_id"],
                "control_name": binding["control_name"],
                "reason": binding["reason"],
                "applies_to": binding["applies_to"],
                "guidance": guidance,
            }
        )

    return enriched

import json
from pathlib import Path
def save_control_guidance_json(results: List[Dict[str, Any]], output_path: str) -> None:
    path = Path(output_path)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")

def main() -> None:
    results = build_control_guidance("sample_oscal.json")

    print("Control guidance results:\n")

    for item in results:
        print("=" * 80)
        print(f"CONTROL: {item['control_id']} - {item['control_name']}")
        print(f"REASON : {item['reason']}")
        print(f"APPLIES: {item['applies_to']}")
        print("\nRetrieved guidance:")
        for i, g in enumerate(item["guidance"], start=1):
            print(f"\n  [{i}] {g['source_name']} | topic={g['topic']} | chunk={g['chunk_index']}")
            print(f"      {g['text'][:250]}...")
        print("=" * 80)

    save_control_guidance_json(results, "control_guidance_output.json")
    print("\nSaved structured output to control_guidance_output.json")

if __name__ == "__main__":
    main()