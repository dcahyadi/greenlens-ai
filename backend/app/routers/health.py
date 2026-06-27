from fastapi import APIRouter
from app.config import settings
import os

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    return {"name": "GreenLens AI API", "version": "1.0.0", "docs": "/docs", "health": "/health"}


@router.get("/health")
async def health_check():
    """Health check for Render — verifies ChromaDB is accessible."""
    result = {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "chroma_accessible": False,
        "collection_count": 0,
        "docs_path_exists": os.path.exists(settings.DOCS_PATH),
    }
    try:
        # chromadb 1.x API — PersistentClient is accessed via chromadb module
        import chromadb
        client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
        cols = client.list_collections()
        result["chroma_accessible"] = True
        result["collection_count"] = len(cols)
        result["collections"] = [c.name for c in cols]
    except Exception as e:
        result["status"] = "degraded"
        result["chroma_error"] = str(e)
    return result
