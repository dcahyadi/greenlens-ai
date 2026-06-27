from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache
from loguru import logger
from app.config import settings


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """Load embedding model once and cache. BAAI/bge-m3 supports EN + ID."""
    logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
