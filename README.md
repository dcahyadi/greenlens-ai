# 🌿 GreenLens AI

A Retrieval-Augmented Generation (RAG) powered Q&A application for querying Indonesia's green economy policies and sustainability regulations, including NDC climate commitments, JETP energy transition plans, AMDAL environmental guidelines, carbon credit policies, and KLHK regulations.

## 🔗 Links

- **Live App**: see [docs/deployed.md](docs/deployed.md)
- **Task Board**: https://trello.com/your-board
- **Demo Recording**: https://your-demo-link

## 📚 Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Backend | FastAPI + Python 3.13 |
| RAG | LangChain + ChromaDB (embedded) |
| Embeddings | BAAI/bge-m3 (multilingual EN+ID) |
| LLM | OpenRouter (Llama 3.1 8B) |
| Deployment | Render (Docker backend + Static Site frontend) |
| CI/CD | GitHub Actions |

## 🚀 Local Development (Python 3.13)

### Prerequisites
- Python 3.13.x
- Node.js 20+

### 1. Clone & place your documents

```bash
git clone https://github.com/your-org/greenlens-ai.git
cd greenlens-ai
```

Place your PDFs into `data/documents/` by category:
```
data/documents/
├── carbon/    perpres-98-2021-en.pdf, perpres-98-2021-id.pdf,
│              perpres-110-2025-id.pdf, pojk-14-2023-id-carbon-trading.pdf
├── esdm/      permen-esdm-2-2024.pdf, perpres-112-2022.pdf
├── jetp/      jetp-cipp-2023.pdf, jetp-progress-report-2025-en.pdf,
│              jetp-progress-report-2025-id.pdf
├── klhk/      permen-LHK-4-2021.pdf, permen-LHK-21-2022.pdf, pp-22-2021.pdf
├── ndc/       enhanced-ndc-2022-en.pdf, updated-ndc-2021-en.pdf
└── ojk/       tkbi-ver3-2026-en.pdf, tkbi-ver3-2026-id.pdf,
               tkbi-fact-sheets.pdf, tkbi-faq.pdf
```

### 2. Backend setup

```bash
cd backend
cp .env.example .env
# Open .env and set your OPENROUTER_API_KEY

# Python 3.13: install PyTorch CPU first, then the rest
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# Run ingestion — builds chroma_db/ folder
python ingestion/indexer.py

# Start API
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend setup

```bash
cd frontend
npm install
cp .env.example .env.local   # VITE_API_URL=http://localhost:8000
npm run dev
# → Open http://localhost:5173
```

> **No Docker needed locally.** ChromaDB runs embedded inside FastAPI (just a local folder).
> Docker is only used by Render for cloud deployment.

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```

## 📄 Docs

- [Design & Evaluation](docs/design-and-evaluation.md) — architecture decisions, RAG evaluation
- [AI Tooling](docs/ai-tooling.md) — AI tools used during development
- [Deployed](docs/deployed.md) — live deployment link

## 🚀 Deployment (Render)

1. Push to GitHub
2. Connect repo on render.com → "Use Blueprint" (reads `render.yaml` automatically)
3. Set `OPENROUTER_API_KEY` in Render dashboard under Environment
4. Run ingestion locally, then upload to Render disk:
   ```bash
   export RENDER_SSH=ssh-xxxx@ssh.singapore.render.com
   ./backend/ingestion/upload_to_render.sh
   ```
