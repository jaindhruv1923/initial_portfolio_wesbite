import os
import sys
import json
import time
from pathlib import Path

try:
    from app.rag.ingest import ingest_repository, Chunk
    from app.rag.embed_store import index_chunks, search
except ImportError as e:
    sys.exit(1)

def run_evaluation():
    repo_path = str(Path(__file__).resolve().parent.parent / "demo_repo")
    
    chunks = ingest_repository(repo_path)
    index_chunks(chunks)

    queries = [
        {"query": "How does KAVACH detect Aadhaar-like identifiers?", "ground_truth": ["app/security/detector.py"]},
        {"query": "What is the role of the orchestrator?", "ground_truth": ["app/agent/orchestrator.py"]},
        {"query": "Explain the RAG ingestion process.", "ground_truth": ["app/rag/ingest.py"]},
        {"query": "How are embeddings generated?", "ground_truth": ["app/rag/embed_store.py"]},
        {"query": "What does the impact analyzer do?", "ground_truth": ["app/impact/analyzer.py"]}
    ]
    
    results = []
    latencies = []
    
    for _ in range(3):
        search("Kavach security", top_k=5)
        
    for q in queries:
        start_time = time.perf_counter()
        retrieved = search(q["query"], top_k=5)
        end_time = time.perf_counter()
        
        latency_ms = (end_time - start_time) * 1000
        latencies.append(latency_ms)
        
        retrieved_paths = [r["file_path"].replace("\\", "/") for r in retrieved]
        ground_truth_normalized = [gt.replace("\\", "/") for gt in q["ground_truth"]]

        hit = 1 if any(gt in retrieved_paths for gt in ground_truth_normalized) else 0
        found_gt_count = sum(1 for gt in ground_truth_normalized if gt in retrieved_paths)
        recall = found_gt_count / len(ground_truth_normalized)
        
        results.append({
            "query": q["query"],
            "ground_truth": q["ground_truth"],
            "retrieved_top_5": retrieved_paths,
            "hit": hit,
            "recall": recall,
            "latency_ms": latency_ms
        })
        
    total_hits = sum(r["hit"] for r in results)
    avg_recall = sum(r["recall"] for r in results) / len(results)
    
    avg_latency = sum(latencies) / len(latencies)
    sorted_latencies = sorted(latencies)
    median_latency = sorted_latencies[len(sorted_latencies)//2]
    p95_latency = sorted_latencies[int(len(sorted_latencies)*0.95)] if len(sorted_latencies) > 1 else sorted_latencies[0]
    
    with open(Path(__file__).resolve().parent / "eval_results.json", "w") as f:
        json.dump({
            "evaluation_queries": len(results),
            "hit_at_5": total_hits / len(results),
            "mean_recall_at_5": avg_recall,
            "avg_latency_ms": avg_latency,
            "median_latency_ms": median_latency,
            "p95_latency_ms": p95_latency,
            "results": results
        }, f, indent=2)

if __name__ == "__main__":
    run_evaluation()

