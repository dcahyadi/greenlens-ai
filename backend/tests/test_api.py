"""GreenLens AI — API endpoint tests"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

MOCK_RESPONSE = {
    "answer": "Indonesia's unconditional target is 31.89% under Enhanced NDC 2022.",
    "sources": [{
        "content": "Sample NDC content.",
        "source_file": "ndc/enhanced-ndc-2022-en.pdf",
        "regulation": "Enhanced NDC 2022",
        "category": "climate_commitment",
        "year": 2022,
        "page": 5,
    }],
    "model_used": "meta-llama/llama-3.1-8b-instruct:free",
}


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "GreenLens" in r.json()["name"]


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()


def test_query_empty_rejected():
    r = client.post("/api/query", json={"question": ""})
    assert r.status_code == 422


def test_query_too_long_rejected():
    r = client.post("/api/query", json={"question": "x" * 2001})
    assert r.status_code == 422


def test_query_invalid_language():
    r = client.post("/api/query", json={"question": "test", "language": "fr"})
    assert r.status_code == 422


@patch("app.routers.query.get_rag_response", new_callable=AsyncMock)
def test_query_success(mock_rag):
    mock_rag.return_value = MOCK_RESPONSE
    r = client.post("/api/query", json={"question": "What is Indonesia's emission target?"})
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert "sources" in data
    assert "31.89" in data["answer"]


@patch("app.routers.query.get_rag_response", new_callable=AsyncMock)
def test_query_with_category(mock_rag):
    mock_rag.return_value = MOCK_RESPONSE
    r = client.post("/api/query", json={
        "question": "Apa itu AMDAL?", "language": "id", "category": "environmental_law"
    })
    assert r.status_code == 200
    call_kwargs = mock_rag.call_args.kwargs
    assert call_kwargs["category_filter"] == "environmental_law"
    assert call_kwargs["language"] == "id"


@patch("app.routers.query.get_rag_response", new_callable=AsyncMock)
def test_query_with_chat_history(mock_rag):
    mock_rag.return_value = MOCK_RESPONSE
    r = client.post("/api/query", json={
        "question": "Tell me more",
        "chat_history": [
            {"role": "user", "content": "What is NDC?"},
            {"role": "assistant", "content": "NDC is..."},
        ]
    })
    assert r.status_code == 200


def test_ingest_status():
    r = client.get("/api/ingest/status")
    assert r.status_code == 200
    assert "running" in r.json()
