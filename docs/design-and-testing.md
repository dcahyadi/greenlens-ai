# GreenLens AI — Design & Testing Document

## 1. Architecture Overview

GreenLens AI is a full-stack RAG (Retrieval Augmented Generation) application allowing users to query Indonesia's green economy and environmental policy documents using natural language.

```
User → React Frontend → FastAPI Backend → LangChain RAG Chain
                                        → ChromaDB (vector store)
                                        → BAAI/bge-m3 (embeddings)
                                        → OpenRouter LLM
```

## 2. Design Decisions

### 2.1 RAG over Fine-tuning
We chose RAG instead of fine-tuning because:
- Documents are authoritative government PDFs requiring exact citation
- RAG allows easy corpus updates without retraining
- Source attribution is critical for policy Q&A credibility

### 2.2 ChromaDB
Chosen over Pinecone/Weaviate because:
- Runs embedded (no separate server process)
- Free and open source — no API cost
- Persistent disk storage works well on Render
- Simple Python API integrates cleanly with LangChain

### 2.3 BAAI/bge-m3 Embeddings
Chosen over all-MiniLM-L6-v2 because:
- Multilingual — supports Bahasa Indonesia natively
- Corpus contains both EN and ID documents
- Higher retrieval quality on non-English text

### 2.4 OpenRouter (Llama 3.1 8B)
Chosen because:
- Free tier available for development/demo
- OpenAI-compatible API — easy to swap models
- Llama 3.1 8B is strong enough for policy Q&A with good context

### 2.5 MMR Retrieval
Using Maximal Marginal Relevance instead of basic similarity search:
- Reduces redundancy in retrieved chunks
- Returns more diverse, complementary context
- Better answers when documents overlap on same topic

### 2.6 Monorepo Structure
Single GitHub repo with `backend/` and `frontend/` for:
- Single render.yaml to deploy both services
- Unified CI pipeline
- Easier cross-service refactoring

## 3. Software Patterns Used

| Pattern | Where Used | Reason |
|---|---|---|
| Repository pattern | `retriever_service.py` | Abstracts ChromaDB from RAG logic |
| Singleton (lru_cache) | embeddings, vectorstore | Heavy models loaded once |
| Strategy pattern | `get_splitter()` | Different chunking per doc type |
| Retry with backoff | `rag_service.py` (tenacity) | LLM API flakiness |
| Background tasks | `ingest.py` | Non-blocking ingestion |
| Metadata tagging | `metadata.py` registry | Filtered retrieval by category |

## 4. Deployment Architecture

### Local Development
```
localhost:5173 (Vite dev server) → proxy → localhost:8000 (FastAPI)
ChromaDB: ./chroma_db/
Documents: ./data/documents/
```

### Production (Render)
```
greenlens.onrender.com (Static Site CDN)
    ↓ API calls
greenlens-api.onrender.com (Docker Web Service, Singapore)
    ↓ reads
/data/chroma_db  (Render Persistent Disk, 10GB)
/data/documents  (Render Persistent Disk, shared mount)
    ↑ uploaded via
rsync / upload_to_render.sh (one-time + on corpus update)
```

**Cost**: Free tier (both services) + $1/month (10GB persistent disk).

## 5. Testing Strategy

### 5.1 Unit Tests (`tests/test_ingestion.py`)
- Metadata registry completeness — all required fields present
- Category validation — only known categories used
- Year range validation — no typos in dates
- Chunking strategy — FAQ uses smaller chunks than regulations

### 5.2 API Tests (`tests/test_api.py`)
- Endpoint availability (root, health, query, ingest)
- Input validation — empty question, too long, invalid language
- Mocked RAG response — tests API contract without LLM calls
- Chat history — multi-turn conversation passed correctly
- Category filter — metadata filter forwarded to retriever

### 5.3 RAG Evaluation (`evaluation/eval_suite.py`)
End-to-end evaluation using ground-truth Q&A pairs:
- **Keyword score**: % of expected answer keywords present
- **Source accuracy**: whether expected source document was retrieved

Run: `python evaluation/eval_suite.py`
Target: keyword_score ≥ 0.7, source_accuracy ≥ 0.8

### 5.4 CI/CD (`/.github/workflows/ci.yml`)
Runs on every PR and push to main:
- Python lint (ruff)
- pytest unit + API tests
- TypeScript type check (tsc --noEmit)
- Frontend production build

## 6. Document Corpus

| Category | Files | Content |
|---|---|---|
| carbon_market | perpres-98-2021 (EN+ID), perpres-110-2025, pojk-14-2023 | Carbon pricing, trading, IDX Carbon |
| renewable_energy | permen-esdm-2-2024, perpres-112-2022 | PLTS Atap, EBT acceleration |
| energy_transition | jetp-cipp-2023, jetp-progress-report-2025 (EN+ID) | JETP investment plan, 2025 status |
| environmental_law | permen-LHK-4-2021, permen-LHK-21-2022, PP-22-2021 | AMDAL, NEK implementation |
| climate_commitment | enhanced-ndc-2022-en, updated-ndc-2021-en | Indonesia NDC targets |
| green_finance | tkbi-ver3-2026 (EN+ID), tkbi-fact-sheets, tkbi-faq | OJK taxonomy |
