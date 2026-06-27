"""GreenLens AI — RAG Evaluation Suite"""
import json, asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import get_rag_response
from loguru import logger


async def run_evaluation(test_file: str = "evaluation/test_queries.json") -> dict:
    cases = json.loads(Path(test_file).read_text())
    results = []
    logger.info(f"Running {len(cases)} evaluation queries...")

    for i, case in enumerate(cases, 1):
        q = case["question"]
        exp_src = case.get("expected_source", "")
        exp_kw = case.get("expected_answer_contains", [])
        logger.info(f"[{i}/{len(cases)}] {q[:60]}...")
        try:
            resp = await get_rag_response(question=q)
            answer = resp["answer"].lower()
            sources = [s["source_file"] for s in resp["sources"]]
            kw_found = [kw for kw in exp_kw if kw.lower() in answer]
            results.append({
                "question": q,
                "keyword_score": round(len(kw_found) / len(exp_kw), 2) if exp_kw else 1.0,
                "source_hit": any(exp_src in s for s in sources) if exp_src else True,
                "keywords_found": kw_found,
                "keywords_missing": [kw for kw in exp_kw if kw.lower() not in answer],
                "sources": sources,
                "answer_preview": resp["answer"][:200],
            })
        except Exception as e:
            results.append({"question": q, "error": str(e)})

    ok = [r for r in results if "error" not in r]
    avg_kw = sum(r["keyword_score"] for r in ok) / len(ok) if ok else 0
    src_acc = sum(1 for r in ok if r["source_hit"]) / len(ok) if ok else 0

    print(f"\n=== EVALUATION RESULTS ===")
    print(f"Total   : {len(cases)}")
    print(f"OK      : {len(ok)}")
    print(f"Keywords: {avg_kw:.1%}")
    print(f"Sources : {src_acc:.1%}")
    return {"total": len(cases), "successful": len(ok),
            "avg_keyword_score": round(avg_kw, 3), "source_accuracy": round(src_acc, 3), "results": results}


if __name__ == "__main__":
    asyncio.run(run_evaluation())
