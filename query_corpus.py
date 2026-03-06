from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from langchain_ollama import OllamaEmbeddings

# Newer LangChain versions use langchain_chroma; older use langchain.vectorstores import Chroma
try:
    from langchain_chroma import Chroma
except Exception:
    from langchain.vectorstores import Chroma


REPO_ROOT = Path(__file__).resolve().parent
PERSIST_DIR = REPO_ROOT / "vectorstore" / "aws_security"
COLLECTION_NAME = "aws-security"


def build_vectorstore(embedding_model: str) -> Chroma:
    if not PERSIST_DIR.exists():
        raise SystemExit(f"Vectorstore not found: {PERSIST_DIR}")

    embeddings = OllamaEmbeddings(model=embedding_model)

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(PERSIST_DIR),
        embedding_function=embeddings,
    )
    return db


def serialize_results(results, show_full_text: bool = False):
    items = []
    for i, doc in enumerate(results, start=1):
        meta = doc.metadata or {}
        text = doc.page_content.strip()

        if not show_full_text and len(text) > 700:
            text = text[:700] + " ..."

        items.append(
            {
                "rank": i,
                "source_name": meta.get("source_name", "N/A"),
                "topic": meta.get("topic", "N/A"),
                "chunk_index": meta.get("chunk_index", "N/A"),
                "source_path": meta.get("source_path", "N/A"),
                "text": text,
            }
        )
    return items


def print_results(results, show_full_text: bool = False) -> None:
    items = serialize_results(results, show_full_text=show_full_text)
    if not items:
        print("No results found.")
        return

    print(f"\nFound {len(items)} result(s)\n")
    print("=" * 80)

    for item in items:
        print(f"[{item['rank']}]")
        print(f"source_name : {item['source_name']}")
        print(f"topic       : {item['topic']}")
        print(f"chunk_index : {item['chunk_index']}")
        print(f"source_path : {item['source_path']}")
        print("-" * 80)
        print(item["text"])
        print("=" * 80)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", type=str, help="Search query")
    ap.add_argument("--k", type=int, default=5, help="Number of top results")
    ap.add_argument(
        "--min_results",
        type=int,
        default=0,
        help="Fail with exit code 1 if fewer than this many results are returned",
    )
    ap.add_argument(
        "--embedding_model",
        type=str,
        default="nomic-embed-text",
        help="Embedding model used for retrieval",
    )
    ap.add_argument(
        "--show_full_text",
        action="store_true",
        help="Show full chunk text instead of truncating output",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Print results as JSON instead of formatted text",
    )
    args = ap.parse_args()

    print(f"[1/3] Loading vectorstore from: {PERSIST_DIR}")
    db = build_vectorstore(args.embedding_model)

    print(f"[2/3] Running similarity search for query: {args.query!r}")
    results = db.similarity_search(args.query, k=args.k)

    if len(results) < args.min_results:
        message = (
            f"Expected at least {args.min_results} result(s), "
            f"but got {len(results)} for query: {args.query!r}"
        )
        if args.json:
            print(json.dumps({"ok": False, "error": message, "results": []}, indent=2))
        else:
            print(message)
        sys.exit(1)

    print("[3/3] Results")
    if args.json:
        payload = {
            "ok": True,
            "query": args.query,
            "k": args.k,
            "result_count": len(results),
            "results": serialize_results(results, show_full_text=args.show_full_text),
        }
        print(json.dumps(payload, indent=2))
    else:
        print_results(results, show_full_text=args.show_full_text)


if __name__ == "__main__":
    main()