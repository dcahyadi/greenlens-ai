from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from typing import Optional
from app.config import settings
from app.services.retriever_service import get_retriever

SYSTEM_PROMPT = """You are GreenLens AI, an expert assistant on Indonesia's green economy,
environmental regulations, and energy transition policies.

Your knowledge base contains official documents:
- NDC 2022 — Indonesia's climate commitments (31.89% unconditional, 43.20% conditional)
- JETP CIPP 2023 + Progress Report 2025 — energy transition investment plan
- Perpres 98/2021 & 110/2025 — carbon pricing regulations
- KLHK regulations — AMDAL, environmental law (PP 22/2021, PermenLHK 4/2021, 21/2022)
- ESDM regulations — renewable energy (Perpres 112/2022, Permen ESDM 2/2024)
- OJK TKBI v3 2026 — sustainable finance taxonomy
- POJK 14/2023 — carbon exchange regulation

RULES:
1. Answer ONLY based on the provided context documents.
2. Always cite the regulation name and year (e.g. "According to Perpres 98/2021...").
3. If context is insufficient, say: "I couldn't find specific information about this in the available documents."
4. Match the user's language: respond in Bahasa Indonesia if asked in Indonesian, English otherwise.
5. Use bullet points for lists of requirements or steps.

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Answer:"""

QA_PROMPT = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=SYSTEM_PROMPT,
)


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS,
        default_headers={
            "HTTP-Referer": "https://greenlens.onrender.com",
            "X-Title": "GreenLens AI",
        },
    )


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def get_rag_response(
    question: str,
    language: str = "en",
    category_filter: Optional[str] = None,
    chat_history: list[dict] = [],
) -> dict:
    retriever = get_retriever(category_filter)
    llm = get_llm()

    # Convert to LangChain tuple format [(human_msg, ai_msg), ...]
    formatted_history = []
    for i in range(0, len(chat_history) - 1, 2):
        if chat_history[i]["role"] == "user" and i + 1 < len(chat_history):
            formatted_history.append((chat_history[i]["content"], chat_history[i + 1]["content"]))

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
        verbose=settings.ENVIRONMENT == "development",
    )

    result = await chain.ainvoke({"question": question, "chat_history": formatted_history})

    sources = []
    seen = set()
    for doc in result.get("source_documents", []):
        meta = doc.metadata
        key = f"{meta.get('source_file', '')}:{meta.get('page', 0)}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "content": doc.page_content[:500].strip(),
                "source_file": meta.get("source_file", "unknown"),
                "regulation": meta.get("regulation", "unknown"),
                "category": meta.get("category", "unknown"),
                "year": int(meta.get("year", 0)),
                "page": int(meta.get("page", 0)),
            })

    logger.info(f"RAG complete — {len(sources)} sources retrieved")
    return {"answer": result["answer"], "sources": sources[:3], "model_used": settings.LLM_MODEL}
