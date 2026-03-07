from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Any

import tiktoken
from pypdf import PdfReader

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Newer LangChain versions use langchain_chroma; older use langchain.vectorstores import Chroma
try:
    from langchain_chroma import Chroma
except Exception:  # fallback
    from langchain.vectorstores import Chroma


REPO_ROOT = Path(__file__).resolve().parent
CORPUS_DIR = REPO_ROOT / "corpus"
PERSIST_DIR = REPO_ROOT / "vectorstore" / "aws_security"
COLLECTION_NAME = "aws-security"


@dataclass
class LoadedDoc:
    text: str
    metadata: Dict[str, Any]


def tiktoken_len(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Safely truncate a string to at most max_tokens using tiktoken."""
    enc = tiktoken.get_encoding("cl100k_base")
    ids = enc.encode(text)
    if len(ids) <= max_tokens:
        return text
    return enc.decode(ids[:max_tokens])


def infer_metadata(path: Path) -> Dict[str, Any]:
    # ساده و قابل توسعه: از مسیر فایل topic/domain رو حدس می‌زنیم
    parts = [p.lower() for p in path.parts]
    topic = "unknown"
    if "aws-sra" in parts:
        topic = "aws-sra"
    elif "aws-well-architected" in parts:
        topic = "aws-well-architected"
    elif "aws-sra-examples" in parts:
        topic = "aws-sra-examples"

    return {
        "source_path": str(path),
        "source_name": path.name,
        "topic": topic,
        "domain": "aws-security",
        "doc_type": path.suffix.lower().lstrip("."),
    }


def load_pdf(path: Path) -> LoadedDoc:
    reader = PdfReader(str(path))
    pages_text = []
    for i, page in enumerate(reader.pages):
        txt = page.extract_text() or ""
        if txt.strip():
            pages_text.append(txt)
    full_text = "\n\n".join(pages_text).strip()
    return LoadedDoc(text=full_text, metadata=infer_metadata(path))


def load_text_like(path: Path) -> LoadedDoc:
    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    return LoadedDoc(text=text, metadata=infer_metadata(path))


def iter_corpus_files(corpus_dir: Path) -> Iterable[Path]:
    exts = {".pdf", ".md", ".txt", ".json", ".yaml", ".yml"}
    for p in corpus_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            yield p


def load_corpus(corpus_dir: Path) -> List[LoadedDoc]:
    docs: List[LoadedDoc] = []
    for path in iter_corpus_files(corpus_dir):
        if path.suffix.lower() == ".pdf":
            doc = load_pdf(path)
        else:
            doc = load_text_like(path)

        # فایل‌های خیلی خالی رو رد کنیم
        if len(doc.text.strip()) < 50:
            continue

        docs.append(doc)
    return docs


def chunk_docs(docs: List[LoadedDoc], chunk_tokens: int, overlap_tokens: int):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_tokens,
        chunk_overlap=overlap_tokens,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""],
    )

    texts = []
    metadatas = []

    for d in docs:
        chunks = splitter.split_text(d.text)
        for idx, ch in enumerate(chunks):
            # Safety: some PDFs produce weirdly long chunks; keep embeds under a hard cap
            ch = truncate_to_tokens(ch, max_tokens=min(2000, max(256, chunk_tokens)))

            md = dict(d.metadata)
            md["chunk_index"] = idx
            md["chunk_tokens_approx"] = tiktoken_len(ch)
            texts.append(ch)
            metadatas.append(md)

    return texts, metadatas


def ingest_to_chroma(texts, metadatas, embedding_model: str, rebuild: bool, batch_size: int, max_embed_tokens: int):
    PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    embeddings = OllamaEmbeddings(model=embedding_model)

    # اگر rebuild=True، کل collection رو از نو می‌سازیم
    if rebuild and PERSIST_DIR.exists():
        # Chroma خودش فایل‌ها رو نگه می‌داره؛ این delete ساده‌ترین ریست محلیه
        for p in PERSIST_DIR.glob("*"):
            if p.is_file():
                p.unlink()
            else:
                # folders like index
                import shutil
                shutil.rmtree(p)

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(PERSIST_DIR),
        embedding_function=embeddings,
    )

    # Ollama embed can fail if any single input exceeds the model context.
    # We keep batching for speed, but we also guard each item and retry with stronger truncation.
    total = len(texts)
    done = 0

    def safe_text(i: int, cap: int) -> str:
        t = texts[i]
        # Always enforce a hard cap right before embedding (tokenizers can differ).
        return truncate_to_tokens(t, max_tokens=cap)

    i = 0
    while i < total:
        end = min(i + batch_size, total)
        batch_texts = [safe_text(j, max_embed_tokens) for j in range(i, end)]
        batch_metas = metadatas[i:end]

        try:
            db.add_texts(texts=batch_texts, metadatas=batch_metas)
            done = end
            print(f"  - embedded {done}/{total}")
            i = end
            continue
        except Exception as e:
            msg = str(e).lower()
            # If context-length error happens, fall back to embedding one-by-one with a smaller cap.
            if "exceeds the context length" not in msg and "context length" not in msg:
                raise

        # Fallback: one-by-one with stricter truncation
        for j in range(i, end):
            t = safe_text(j, max(128, max_embed_tokens // 2))
            try:
                db.add_texts(texts=[t], metadatas=[metadatas[j]])
                done = j + 1
                if done % 50 == 0 or done == total:
                    print(f"  - embedded {done}/{total}")
            except Exception as e2:
                # If it still fails, skip and continue (log enough to debug later)
                print(f"  ! skipped chunk due to embed error: {metadatas[j].get('source_name')} chunk={metadatas[j].get('chunk_index')} err={e2}")
                done = j + 1

        i = end

    # Persist (LangChain/Chroma versions differ: some expose db.persist(), some persist automatically)
    if hasattr(db, "persist"):
        db.persist()  # older langchain wrappers
    elif hasattr(db, "_client") and hasattr(db._client, "persist"):
        db._client.persist()  # chromadb client persistence
    else:
        # Newer wrappers persist automatically when using persist_directory
        print("[info] Chroma persistence handled automatically (no persist() method found).")

    return db


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk_tokens", type=int, default=950)
    ap.add_argument("--overlap_tokens", type=int, default=120)
    ap.add_argument("--embedding_model", type=str, default="nomic-embed-text")
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--dry_run", action="store_true", help="Only load+chunk, no vectorstore write")
    ap.add_argument("--batch_size", type=int, default=16, help="How many chunks to embed per request")
    ap.add_argument("--max_embed_tokens", type=int, default=512, help="Hard cap per chunk before embedding (safety vs Ollama context)")
    args = ap.parse_args()

    if not CORPUS_DIR.exists():
        raise SystemExit(f"corpus dir not found: {CORPUS_DIR}")

    print(f"[1/4] Loading corpus from: {CORPUS_DIR}")
    docs = load_corpus(CORPUS_DIR)
    print(f"Loaded docs: {len(docs)}")

    print(f"[2/4] Chunking (target {args.chunk_tokens} tokens, overlap {args.overlap_tokens})")
    texts, metadatas = chunk_docs(docs, args.chunk_tokens, args.overlap_tokens)
    print(f"Total chunks: {len(texts)}")

    # یه نمونه‌ی متادیتا نشون بده
    sample = {"text_preview": texts[0][:200], "metadata": metadatas[0]}
    print("[sample]", json.dumps(sample, indent=2)[:1200])

    if args.dry_run:
        print("[3/4] Dry run enabled, skipping vectorstore ingestion.")
        return

    print(f"[3/4] Ingesting into Chroma: {PERSIST_DIR} (collection={COLLECTION_NAME})")
    ingest_to_chroma(texts, metadatas, args.embedding_model, args.rebuild, args.batch_size, args.max_embed_tokens)

    print("[4/4] Done ✅")


if __name__ == "__main__":
    main()
