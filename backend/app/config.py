from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM
    OPENROUTER_API_KEY: str = ""
    LLM_MODEL: str = "meta-llama/llama-3.1-8b-instruct:free"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1024

    # Embeddings
    EMBEDDING_MODEL: str = "BAAI/bge-m3"

    # Storage
    CHROMA_PATH: str = "./chroma_db"
    DOCS_PATH: str = "../data/documents"

    # RAG
    RETRIEVER_K: int = 5
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150

    # API
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
