from pydantic import BaseModel, Field
from typing import Optional


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(default="en", pattern="^(en|id)$")
    category: Optional[str] = Field(default=None)
    chat_history: list[ChatMessage] = Field(default=[])


class SourceDocument(BaseModel):
    content: str
    source_file: str
    regulation: str
    category: str
    year: int
    page: int


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
    model_used: str


class IngestRequest(BaseModel):
    category: Optional[str] = None


class IngestResponse(BaseModel):
    status: str
    files_processed: int
    chunks_indexed: int
    message: str
