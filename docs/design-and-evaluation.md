# Design & Evaluation Document

## 1. System Overview

GreenLens AI is a full-stack RAG (Retrieval-Augmented Generation) application that allows users to ask natural language questions about Indonesia's green economy, environmental regulations, and energy transition policies. It answers using a curated corpus of 19 official government documents, always citing the source regulation and year.

### 1.1 Full System Architecture

```
┌──────────────┐     ┌─────────────────────────────────────────────────┐
│     User     │────▶│                React Frontend                   │
│  Web browser │     │  Chat UI · citations · topic filter · EN/ID     │
└──────────────┘     └─────────────────────┬───────────────────────────┘
                                           │ HTTP /api/query
                                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Python 3.13)                     │
│                                                                      │
│  ┌───────────────────┐     ┌──────────────────────────────────────┐  │
│  │    API routers    │────▶│            RAG chain                 │  │
│  │  /query /ingest   │     │  ConversationalRetrievalChain        │  │
│  │  /health          │     │  MMR retrieval · k=5                 │  │
│  └───────────────────┘     │  context + chat history in prompt    │  │
│                            │  retry w/ backoff (tenacity)         │  │
│                            │  metadata category filter            │  │
│                            └──────────────────────────────────────┘  │
└───────────────┬──────────────────────┬───────────────────┬───────────┘
                │                      │                   │
                ▼                      ▼                   ▼
┌──────────────────────┐  ┌───────────────────────┐  ┌───────────────┐
│       ChromaDB       │  │      Embeddings        │  │      LLM      │
│  Embedded vector     │  │  BAAI/bge-m3           │  │  OpenRouter   │
│  store (local /      │  │  multilingual EN+ID    │  │  Llama 3.1 8B │
│  Render disk)        │  └───────────────────────┘  └───────────────┘
└──────────┬───────────┘
           │ (one-time offline ingestion)
           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                Document Ingestion Pipeline (offline)                 │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐ │
│  │    PDF loader    │  │  Text splitter   │  │   Embed + index    │ │
│  │ PyPDF/PyMuPDF    │─▶│ chunk + overlap  │─▶│  write to ChromaDB │ │
│  └──────────────────┘  └──────────────────┘  └────────────────────┘ │
│                                                                      │
│  metadata.py registry · FAQ = 512 tok · regulations = 1000 tok      │
│  18 files · 6 categories · bilingual EN + ID                        │
└──────────────────────────────────────────────────────────────────────┘

Supporting:
  CI/CD  │ GitHub Actions → lint + test + build → auto-deploy to Render
  Eval   │ evaluation/eval_suite.py → keyword score + source accuracy
```

### 1.2 Document Corpus

| Category | Regulation | Year | Lang |
|---|---|---|---|
| Climate commitment | Enhanced NDC 2022 | 2022 | EN |
| Climate commitment | Updated NDC 2021 | 2021 | EN |
| Energy transition | JETP CIPP 2023 | 2023 | EN |
| Energy transition | JETP Progress Report 2025 | 2025 | EN |
| Energy transition | JETP Progress Report 2025 | 2025 | ID |
| Carbon market | Perpres 98/2021 | 2021 | EN |
| Carbon market | Perpres 98/2021 | 2021 | ID |
| Carbon market | Perpres 110/2025 | 2025 | ID |
| Carbon market | POJK 14/2023 (IDX Carbon) | 2023 | ID |
| Environmental law | PermenLHK 4/2021 (AMDAL) | 2021 | ID |
| Environmental law | PermenLHK 21/2022 (NEK) | 2022 | ID |
| Environmental law | PP 22/2021 (AMDAL framework) | 2021 | ID |
| Renewable energy | Perpres 112/2022 (EBT acceleration) | 2022 | ID |
| Renewable energy | Permen ESDM 2/2024 (PLTS Atap) | 2024 | ID |
| Green finance | TKBI Version 3 2026 | 2026 | EN |
| Green finance | TKBI Version 3 2026 | 2026 | ID |
| Green finance | TKBI Fact Sheets | 2026 | EN |
| Green finance | TKBI FAQ | 2026 | EN |

**Total: 18 files across 6 categories** (Updated NDC 2021 is in corpus with status `superseded` — retained for historical context).

---

## 2. Architecture Decisions

### 2.1 RAG over Fine-tuning

**Decision:** Use retrieval-augmented generation rather than fine-tuning a model on the document corpus.

**Reason:** The documents are authoritative government regulations requiring exact, citable answers. RAG preserves the original text and lets us attribute every answer to a specific regulation name and page. Fine-tuning would bake knowledge into model weights with no traceability, and would require expensive retraining every time a regulation is updated (e.g., when Perpres 110/2025 superseded parts of Perpres 98/2021).

### 2.2 ChromaDB in Embedded Mode

**Decision:** Use ChromaDB as an embedded vector store (runs inside the FastAPI process, persists to a local folder) rather than a hosted vector database like Pinecone or Weaviate.

**Reason:**
- Zero infrastructure cost — no separate server or API key needed
- Data stays local during development; on Render it uses a persistent disk
- Simple Python API integrates directly with LangChain
- The corpus (19 documents, ~50k chunks) is small enough that a local store is more than sufficient

**Trade-off:** Not suitable for very large corpora or multi-instance deployments requiring shared state. Acceptable for this capstone scope.

### 2.3 BAAI/bge-m3 Embeddings

**Decision:** Use `BAAI/bge-m3` instead of the more common `all-MiniLM-L6-v2`.

**Reason:** The document corpus is bilingual — NDC and JETP documents are in English while KLHK, ESDM, OJK, and carbon regulations are in Bahasa Indonesia. `bge-m3` is a multilingual model that handles both languages in the same vector space, so a user asking in Indonesian retrieves from Indonesian-language documents correctly, and vice versa.

**Trade-off:** Larger model (~570MB) vs `all-MiniLM-L6-v2` (~90MB), longer first-load time. Mitigated by pre-downloading at Docker build time (see `Dockerfile`).

### 2.4 ConversationalRetrievalChain (not a separate Prompt Builder)

**Decision:** Use LangChain's `ConversationalRetrievalChain` to handle the full RAG pipeline — retrieval, context injection, chat history, and prompt — in a single component.

**Reason:** This chain handles context + history internally without needing a separate "prompt builder" service. It takes the question and chat history, retrieves relevant chunks via the retriever, injects them into the prompt template alongside the conversation history, and calls the LLM. Keeping this as one LangChain component reduces code surface area and makes the chain easy to swap or extend.

**Implementation:** `backend/app/services/rag_service.py` — `ConversationalRetrievalChain.from_llm()` with a custom `QA_PROMPT` template that instructs the LLM to cite regulations and match the user's language.

### 2.5 MMR Retrieval Strategy

**Decision:** Use Maximal Marginal Relevance (MMR) retrieval instead of basic cosine similarity top-k.

**Reason:** Multiple documents overlap on the same topics (e.g., both Perpres 98/2021 and Perpres 110/2025 cover carbon pricing; both PermenLHK 21/2022 and PP 22/2021 cover environmental law). Basic top-k retrieval would return 5 near-identical chunks from the same document. MMR balances relevance with diversity, ensuring retrieved chunks come from different sections or documents, giving the LLM richer context.

### 2.6 Metadata Tagging per Document

**Decision:** Tag every chunk with structured metadata (`category`, `regulation`, `year`, `language`, `source_file`, `page`) during ingestion.

**Reason:** Enables filtered retrieval — when a user selects "Carbon Market" in the topic filter, the retriever only searches chunks tagged `category: carbon_market`. Without this, a question about AMDAL might retrieve carbon pricing chunks that happen to share keywords.

**Implementation:** `backend/ingestion/metadata.py` is a central registry mapping every filename to its full metadata. This keeps ingestion logic clean and makes it easy to update metadata when regulations change.

### 2.7 Chunking Strategy

**Decision:** Use different chunk sizes by document type — 512 tokens for FAQ/factsheets, 1000 tokens for full regulations.

**Reason:** The OJK TKBI FAQ (`tkbi-faq.pdf`) contains short discrete Q&A pairs. Chunking at 1000 tokens would merge multiple Q&As into one chunk, degrading retrieval precision. Full regulations like the JETP CIPP (234 pages) need larger chunks to preserve paragraph-level context around policy provisions.

### 2.8 Technology Stack

| Component | Choice | Reason |
|---|---|---|
| Backend | FastAPI + Python 3.13 | Async, auto OpenAPI docs, Pydantic validation |
| Frontend | React + TypeScript + Vite | Fast build, type safety, component reuse |
| Styling | Tailwind CSS | Utility-first, no separate CSS files to maintain |
| LLM | OpenRouter (Llama 3.1 8B) | Free tier, OpenAI-compatible API, easy model swap |
| Deployment | Render | Free tier, Docker support, auto-deploy from GitHub, Singapore region |
| CI/CD | GitHub Actions | Lint + test + build check on every PR |

### 2.9 Deployment: Render vs Alternatives

**Decision:** Deploy on Render (free tier + $1/month persistent disk).

**Compared alternatives:**
- **Railway:** Similar free tier but less transparent pricing for disk storage
- **Fly.io:** Good but requires more configuration for persistent volumes
- **Vercel:** Frontend only; can't run Python backends with persistent state
- **Heroku:** No free tier since 2022

**Render advantages:** Single `render.yaml` deploys both services, persistent disk for ChromaDB, Singapore region (low latency from Indonesia), auto-deploy on `git push main`.

---

## 3. Software Patterns Used

| Pattern | Where | Reason |
|---|---|---|
| Repository abstraction | `retriever_service.py` | Decouples ChromaDB from RAG logic; easy to swap vector store |
| Singleton via `lru_cache` | `embed_service.py`, `retriever_service.py` | Heavy models (570MB embedding) loaded once per process |
| Strategy pattern | `get_splitter()` in `indexer.py` | Different chunking strategy per document type without if/else throughout |
| Retry with exponential backoff | `rag_service.py` via `tenacity` | LLM API (OpenRouter) can return 429s; retry transparently |
| Background tasks | `ingest.py` router | Ingestion takes minutes — runs without blocking the API |
| Metadata registry | `ingestion/metadata.py` | Central truth for all document metadata; ingestion stays clean |

---

## 4. RAG Evaluation

### 4.1 Approach

Evaluation uses a ground-truth Q&A set (`evaluation/test_queries.json`) with 10 questions covering all document categories. Two metrics are measured:

**Keyword Score** — percentage of expected answer keywords present in the model's response. Tests whether the answer contains the right factual content.

**Source Accuracy** — whether the expected source document appears in the top-3 retrieved chunks. Tests whether retrieval is working correctly.

Run: `cd backend && python evaluation/eval_suite.py`

### 4.2 Test Cases

| # | Question | Expected Source | Key Terms |
|---|---|---|---|
| 1 | Indonesia's unconditional NDC target? | enhanced-ndc-2022-en.pdf | 31.89%, unconditional |
| 2 | JETP financing commitment? | jetp-cipp-2023.pdf | 20 billion, USD |
| 3 | PLTS Atap under Permen ESDM 2/2024? | permen-esdm-2-2024.pdf | PLTS, net metering |
| 4 | Carbon instruments in Perpres 98/2021? | perpres-98-2021-en.pdf | carbon trading, carbon levy |
| 5 | JETP status 2025? | jetp-progress-report-2025-en.pdf | financing, approved |
| 6 | Apa itu AMDAL? (Indonesian) | permen-LHK-4-2021.pdf | AMDAL, lingkungan |
| 7 | TKBI v3 renewable classification? | tkbi-ver3-2026-en.pdf | green, classification |
| 8 | IDX Carbon regulation? | pojk-14-2023-id-carbon-trading.pdf | bursa karbon, carbon |
| 9 | Renewable targets Perpres 112/2022? | perpres-112-2022.pdf | renewable, energy |
| 10 | Perpres 110/2025 vs 98/2021? | perpres-110-2025-id.pdf | karbon, emisi |

### 4.3 Target Metrics

| Metric | Target | Notes |
|---|---|---|
| Keyword Score | ≥ 0.70 | 70%+ of expected terms present in answer |
| Source Accuracy | ≥ 0.80 | Correct document retrieved in top-3 for 8/10 questions |

### 4.4 Results

> **Fill in after running:** `cd backend && python evaluation/eval_suite.py`

```
=== EVALUATION RESULTS ===
Total   : 10
OK      : 10
Keywords: ___%
Sources : ___%
```

### 4.5 Known Limitations

- Indonesian-language questions (Q6, Q10) depend on `bge-m3` correctly embedding Bahasa Indonesia — retrieval quality is slightly lower than English due to smaller Indonesian training data in the base model
- Perpres 110/2025 is in Indonesian only; cross-language comparison questions (Q10) require the LLM to synthesize from an English question against an Indonesian document
- Free-tier LLM (Llama 3.1 8B) occasionally truncates long regulatory text in the answer — mitigated by `max_tokens=1024`

---

## 5. Testing Strategy

### 5.1 Unit Tests (`tests/test_ingestion.py`)
Tests the metadata registry and chunking logic without touching ChromaDB or the LLM:
- All 19 documents have required metadata fields
- All categories are from the valid set
- All year values are in reasonable range (2000–2030)
- FAQ/factsheet documents use smaller chunk size than full regulations

### 5.2 API Tests (`tests/test_api.py`)
Tests the FastAPI layer using `TestClient` with mocked RAG responses:
- Endpoint availability (root, health, query, ingest status)
- Input validation — empty question, too-long question, invalid language code
- Correct forwarding of category filter and language to the RAG service
- Multi-turn chat history passing

### 5.3 CI/CD Pipeline (`.github/workflows/ci.yml`)
Runs on every pull request and push to `main`:
- Python lint (ruff)
- pytest unit + API tests
- TypeScript type check (`tsc --noEmit`)
- Frontend production build
