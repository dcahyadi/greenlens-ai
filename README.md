# GreenLens-AI RAG based Assistant

A Retrieval-Augmented Generation (RAG) web application where users query real Indonesia Government Documents about 
green economy, energy policy, and environmental regulations (KLHK regulations, NDC Indonesia, JETP framework, carbon credit policies, AMDAL guidelines) 
and get AI-powered answers with source citations.
---

## Features

- 🔍 **Semantic search** over 10 company policy documents
- 📚 **Citation-grounded answers** — every answer links to source documents
- 🛡️ **Guardrails** — refuses out-of-scope questions, limits output length
- 💬 **Chat UI** — clean web interface with suggestion chips
- ⚡ **REST API** — `/chat` endpoint for programmatic access
- 🧪 **Evaluation** — groundedness, citation accuracy, and latency metrics
- 🔄 **CI/CD** — GitHub Actions pipeline

---

## Quick Start

### 1. Prerequisites

- Python 3.13+
- A free [OpenRouter](https://openrouter.ai) API key

### 2. Clone and set up environment

```bash
git clone https://github.com/yourname/greenlens-ai.git
cd greenlens-ai

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

### 4. Run ingestion (build the vector index)

```bash
python scripts/ingest.py
```

This parses all policy documents in `data/policies/`, chunks them, embeds with a local HuggingFace model, and stores in ChromaDB. Runs once; re-run only if policies change.

### 5. Start the application

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## API Reference

### `GET /health`
Returns system status.
```json
{ "status": "ok", "vectorstore_ready": true, "version": "1.0.0" }
```

### `POST /chat`
Ask a policy question.

**Request:**
```json
{ "question": "How many PTO days do I get?" }
```

**Response:**
```json
{
  "answer": "Full-time employees in their first two years receive 15 days of PTO per year [1].",
  "citations": [
    {
      "index": 1,
      "doc_id": "pto_policy",
      "source": "pto_policy.md",
      "snippet": "Years 0–2: 15 days per year (1.25 days/month)",
      "score": 0.8921
    }
  ],
  "latency_ms": 1243.5
}
```

### `GET /`
Chat web interface.

---

## Running Evaluation

```bash
python src/evaluation/evaluator.py
```

Results are saved to `src/evaluation/eval_report.json`.

---

## Project Structure

```
greenlens-ai/
├── data/policies/          # 10 synthetic company policy documents
├── src/
│   ├── ingestion/          # Parser, chunker, embedder
│   ├── retrieval/          # ChromaDB vectorstore, retriever
│   ├── generation/         # LLM client, prompt templates, guardrails
│   ├── evaluation/         # Eval set and evaluator
│   └── app/                # Flask routes and chat UI
├── scripts/ingest.py       # Run ingestion pipeline
├── tests/                  # Pytest smoke tests
├── app.py                  # Application entry point
├── requirements.txt
└── .env.example
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | *(required)* | OpenRouter API key |
| `LLM_MODEL` | `z-ai/glm-4.5-air:free` | Model to use |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Local embedding model |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB storage path |
| `RETRIEVAL_TOP_K` | `5` | Number of chunks to retrieve |
| `FLASK_PORT` | `5000` | Port for the Flask server |
| `RANDOM_SEED` | `42` | Seed for reproducibility |

---

## Policy Documents

| Document | Topics Covered |
|----------|---------------|
| `pto_policy.md` | Accrual, carryover, blackout periods |
| `sick_leave_policy.md` | Sick days, medical documentation |
| `holiday_policy.md` | 11 holidays, floating holidays, holiday pay |
| `remote_work_policy.md` | Hybrid rules, core hours, equipment |
| `expense_policy.md` | Meals, travel, home office, receipts |
| `security_policy.md` | Passwords, MFA, data classification |
| `code_of_conduct.md` | Ethics, anti-harassment, gifts |
| `onboarding_policy.md` | Day 1, 30/60/90-day goals, benefits |
| `performance_review_policy.md` | Ratings, merit increases, PIP |
| `data_privacy_policy.md` | GDPR, CCPA, data subject rights |
