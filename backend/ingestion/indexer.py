"""
GreenLens AI — Document Ingestion Pipeline
PDFs → chunks → embeddings → ChromaDB
"""
import argparse
import sys
from pathlib import Path

# Allow running as: python ingestion/indexer.py from backend/
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger

from ingestion.metadata import DOCUMENT_METADATA
from app.config import settings


def get_splitter(doc_key: str) -> RecursiveCharacterTextSplitter:
    """Smaller chunks for FAQ/factsheets, larger for full regulations."""
    if any(k in doc_key for k in ["faq", "fact-sheet", "fact_sheet"]):
        return RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
    )


def ingest_all(category_filter: str | None = None) -> dict:
    docs_path = Path(settings.DOCS_PATH)
    if not docs_path.exists():
        logger.error(f"Documents path not found: {docs_path}")
        return {"files_processed": 0, "chunks_indexed": 0}

    logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = Chroma(
        persist_directory=settings.CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="greenlens_docs",
    )

    files_processed = 0
    chunks_indexed = 0
    categories = [docs_path / category_filter] if category_filter else list(docs_path.iterdir())

    for cat_path in categories:
        if not cat_path.is_dir():
            continue
        for pdf_file in sorted(cat_path.glob("*.pdf")):
            doc_key = f"{cat_path.name}/{pdf_file.name}"
            meta = DOCUMENT_METADATA.get(doc_key, {
                "category": cat_path.name, "regulation": pdf_file.stem,
                "year": 0, "language": "unknown", "issuer": "unknown", "status": "unknown",
            })
            logger.info(f"Ingesting: {doc_key}")
            try:
                pages = PyPDFLoader(str(pdf_file)).load()
                for page in pages:
                    page.metadata.update(meta)
                    page.metadata["source_file"] = doc_key
                chunks = get_splitter(doc_key).split_documents(pages)
                vectorstore.add_documents(chunks)
                chunks_indexed += len(chunks)
                files_processed += 1
                logger.info(f"  ✓ {len(chunks)} chunks — {pdf_file.name}")
            except Exception as e:
                logger.error(f"  ✗ Failed {pdf_file.name}: {e}")

    logger.info(f"Done: {files_processed} files, {chunks_indexed} chunks")
    return {"files_processed": files_processed, "chunks_indexed": chunks_indexed}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GreenLens AI Ingestion")
    parser.add_argument("--category", type=str, default=None,
                        help="Only ingest this category folder (e.g. ndc, jetp)")
    args = parser.parse_args()
    result = ingest_all(category_filter=args.category)
    print(f"\n✅ {result['files_processed']} files, {result['chunks_indexed']} chunks indexed")
