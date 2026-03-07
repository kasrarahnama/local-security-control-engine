from __future__ import annotations

from typing import Any, Dict, List

from query_corpus import build_vectorstore
from control_query_builder import build_control_query


def retrieve_control_chunks(
    binding: Dict[str, Any],
    architecture_summary: Dict[str, Any],
    embedding_model: str = "nomic-embed-text",
    k: int = 4,
) -> Dict[str, Any]:
    query = build_control_query(binding, architecture_summary)

    db = build_vectorstore(embedding_model)
    results = db.similarity_search(query, k=k)

    chunks: List[Dict[str, Any]] = []

    for doc in results:
        meta = doc.metadata or {}

        chunks.append(
            {
                "source_name": meta.get("source_name"),
                "topic": meta.get("topic"),
                "source_path": meta.get("source_path"),
                "chunk_index": meta.get("chunk_index"),
                "text": doc.page_content.strip(),
            }
        )

    return {
        "control_id": binding.get("control_id"),
        "control_name": binding.get("control_name"),
        "query": query,
        "chunks": chunks,
    }