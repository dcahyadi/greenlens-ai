# AI Tooling

This document describes the AI-assisted tools used during the development of GreenLens AI, what worked well, and what didn't.

## Tools Used

### Claude (Anthropic) — Primary Development Assistant

**How it was used:**
- Generating initial project scaffolding (FastAPI routers, LangChain RAG pipeline, React components)
- Debugging dependency conflicts — specifically the Python 3.13 + ChromaDB 1.x compatibility issue
- Writing the ingestion pipeline (`indexer.py`, `metadata.py`) and the metadata registry for all 19 documents
- Drafting test cases (`test_api.py`, `test_ingestion.py`) and the RAG evaluation suite
- Explaining ChromaDB 1.x API breaking changes from 0.5.x (e.g., `persist()` removal, new `PersistentClient` import path)
- Writing and iterating on the `render.yaml` blueprint and Render deployment workflow

**What worked well:**
- Very fast at generating boilerplate — the full project structure (60+ files) was scaffolded in a single session
- Strong at explaining *why* certain design decisions were made (e.g., MMR retrieval vs basic similarity, BAAI/bge-m3 for multilingual support)
- Caught the Docker-for-ChromaDB mistake before it caused issues locally — correctly identified that ChromaDB embedded mode needs no container
- Good at producing consistent code style across the full stack (Python backend + TypeScript frontend)

**What didn't work well:**
- Initial `requirements.txt` pinned old versions (`chromadb==0.5.23`, `torch==2.5.1+cpu`) that are not compatible with Python 3.13 — required a follow-up correction pass
- Occasionally over-engineered solutions (e.g., added `docker-compose.yml` unnecessarily for local dev, which was removed after review)
- Needed explicit prompting to use ChromaDB 1.x API conventions rather than the 0.5.x API it was trained on

### GitHub Copilot — In-editor Autocomplete

**How it was used:**
- Inline autocompletion while writing LangChain chain configurations
- Autocompleting Pydantic model fields and FastAPI route signatures
- Suggesting import statements

**What worked well:**
- Useful for repetitive patterns (e.g., completing similar metadata entries across 19 documents)
- Fast, low-friction — stayed in the editor flow without context-switching

**What didn't work well:**
- Suggested outdated LangChain v0.1 patterns (`from langchain.chat_models import ChatOpenAI` instead of `langchain-openai`)
- Occasionally hallucinated non-existent method names on ChromaDB and LangChain objects

### OpenRouter (Llama 3.1 8B) — Runtime LLM

**How it was used:**
- The production LLM powering GreenLens AI's Q&A responses
- Tested during development by querying the running RAG pipeline

**What worked well:**
- Free tier is sufficient for development and capstone demo purposes
- OpenAI-compatible API made integration trivial via `langchain-openai`
- Response quality on policy Q&A is adequate — correctly cites regulation names when context is retrieved

**What didn't work well:**
- Free tier has rate limits that cause occasional `429` errors during rapid evaluation runs
- Answers degrade noticeably when retrieved context chunks are too long or contain dense regulatory language — required tuning `CHUNK_SIZE` down from 1500 to 1000 tokens

## Summary

| Tool | Role | Verdict |
|---|---|---|
| Claude | Scaffolding, debugging, architecture | ✅ High value, needs version-awareness review |
| GitHub Copilot | In-editor autocomplete | ✅ Useful for repetitive code |
| OpenRouter / Llama 3.1 8B | Runtime LLM | ✅ Good for demo, watch rate limits |
