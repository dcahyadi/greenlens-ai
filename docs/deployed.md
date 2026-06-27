# Deployed Application

## Live Links

| Service | URL |
|---|---|
| **Frontend (Web App)** | https://greenlens.onrender.com |
| **Backend API** | https://greenlens-api.onrender.com |
| **API Docs (Swagger)** | https://greenlens-api.onrender.com/docs *(dev only)* |
| **Health Check** | https://greenlens-api.onrender.com/health |

> **Note:** The Render free tier spins down after 15 minutes of inactivity.
> The first request after inactivity may take 20–30 seconds to respond while the service wakes up.
> The frontend will show a loading state during this time.

## GitHub Repository

**Repository:** https://github.com/your-org/greenlens-ai

The repository contains:
- All source code (backend + frontend)
- This deployment documentation
- [Design & Evaluation document](design-and-evaluation.md)
- [AI Tooling document](ai-tooling.md)
- CI/CD pipeline (`.github/workflows/ci.yml`)
- Render Blueprint (`render.yaml`)

> **To access the repository as grader:** Share access with `quantic-grader` on GitHub.

## Deployment Architecture

```
GitHub (main branch)
    │
    ├── push → GitHub Actions CI
    │           └── lint + test + build check
    │
    └── merge → Render auto-deploy (via render.yaml)
                ├── greenlens-api  (Docker Web Service, Singapore)
                │   └── FastAPI + ChromaDB on /data disk (10GB)
                └── greenlens      (Static Site, global CDN)
                    └── React app built from frontend/dist/
```

## Deployment Steps (for reference)

1. Connected GitHub repo to Render → selected "Use Blueprint" → Render reads `render.yaml`
2. Set `OPENROUTER_API_KEY` in Render dashboard → greenlens-api → Environment
3. Ran ingestion locally: `cd backend && python ingestion/indexer.py`
4. Uploaded ChromaDB + documents to Render persistent disk:
   ```bash
   export RENDER_SSH=ssh-xxxx@ssh.singapore.render.com
   ./backend/ingestion/upload_to_render.sh
   ```
5. Triggered manual deploy → verified `/health` endpoint returns `chroma_accessible: true`

## Demo Recording

**Recording link:** https://your-demo-recording-link

The recording covers:
- Overview of the GreenLens AI system and document corpus
- Live demonstration of querying in English and Bahasa Indonesia
- Topic filter demonstration (e.g., filtering to JETP or carbon market docs)
- Source citation display
- Brief walkthrough of the codebase and CI/CD pipeline
