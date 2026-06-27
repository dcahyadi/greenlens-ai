from fastapi import APIRouter, HTTPException, BackgroundTasks
from loguru import logger
from app.models.schemas import IngestRequest, IngestResponse

router = APIRouter(tags=["ingest"])
_ingestion_running = False


async def _run_ingestion(category: str | None):
    global _ingestion_running
    _ingestion_running = True
    try:
        from ingestion.indexer import ingest_all
        result = ingest_all(category_filter=category)
        logger.info(f"Ingestion complete: {result}")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
    finally:
        _ingestion_running = False


@router.post("/ingest", response_model=IngestResponse)
async def trigger_ingestion(request: IngestRequest, background_tasks: BackgroundTasks):
    """Trigger document ingestion into ChromaDB (runs in background)."""
    global _ingestion_running
    if _ingestion_running:
        raise HTTPException(status_code=409, detail="Ingestion already running")
    background_tasks.add_task(_run_ingestion, request.category)
    return IngestResponse(
        status="started", files_processed=0, chunks_indexed=0,
        message=f"Ingestion started. Category: {request.category or 'all'}",
    )


@router.get("/ingest/status")
async def ingestion_status():
    return {"running": _ingestion_running}
