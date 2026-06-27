from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.routers import query, ingest, health
from app.config import settings

logger.remove()
logger.add(sys.stdout, level=settings.LOG_LEVEL, colorize=True,
           format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🌿 GreenLens AI starting up")
    logger.info(f"   env       : {settings.ENVIRONMENT}")
    logger.info(f"   chroma    : {settings.CHROMA_PATH}")
    logger.info(f"   docs      : {settings.DOCS_PATH}")
    logger.info(f"   llm       : {settings.LLM_MODEL}")
    logger.info(f"   embedding : {settings.EMBEDDING_MODEL}")
    yield
    logger.info("GreenLens AI shutting down")


app = FastAPI(
    title="GreenLens AI API",
    description="RAG-powered green policy Q&A for Indonesia's green economy",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(query.router, prefix="/api")
app.include_router(ingest.router, prefix="/api")
