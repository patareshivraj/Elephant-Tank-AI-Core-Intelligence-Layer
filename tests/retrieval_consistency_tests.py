import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.semantic.index_manager import IndexManager
from app.matching.investor_matcher import InvestorMatcherEngine
from app.semantic.vector_store import VectorStore

def test_retrieval_consistency():
    print("========================================")
    print(" ELEPHANT TANK AI - CONSISTENCY TEST")
    print("========================================")
    
    # 1. Seed vector index
    print("[1] Initializing vector database indices...")
    IndexManager.reset_all_indices()
    
    query_desc = "AI deep learning diagnostics and medical scans."
    query_stage = "Series A"
    
    # 2. Test Idempotency (Consistency over consecutive runs)
    print("\n[2] Testing Search Idempotency...")
    run_1 = InvestorMatcherEngine.match_investors(query_stage, query_desc, limit=3)
    run_2 = InvestorMatcherEngine.match_investors(query_stage, query_desc, limit=3)
    
    assert len(run_1) == len(run_2), "Failed: Different match candidate counts retrieved."
    
    for idx in range(len(run_1)):
        name_1 = run_1[idx]["investor_name"]
        name_2 = run_2[idx]["investor_name"]
        score_1 = run_1[idx]["match_score"]
        score_2 = run_2[idx]["match_score"]
        
        assert name_1 == name_2, f"Failed Idempotency: Run 1 matched {name_1}, Run 2 matched {name_2} at position #{idx+1}"
        assert score_1 == score_2, f"Failed Score Consistency: Score mismatch for {name_1}"
        print(f"  Position #{idx+1}: {name_1} ({score_1}/100) -> Consistently matched!")
        
    print("  [SUCCESS] Search retrieval is fully idempotent and ordered!")
    
    # 3. Test Metadata Filtering Integrity
    print("\n[3] Testing Metadata Filtering Consistency...")
    # Insert startups with different stage metadatas
    startup_seed = {
        "startup_name": "Early Health",
        "startup_description": "Healthcare diagnosis scans.",
        "target_stage": "Seed",
        "founder_data": "Dr. Vance"
    }
    startup_series_a = {
        "startup_name": "Late Health",
        "startup_description": "Biomedical scanning system.",
        "target_stage": "Series A",
        "founder_data": "Dr. Jenkins"
    }
    
    IndexManager.index_startup("st_early", startup_seed)
    IndexManager.index_startup("st_late", startup_series_a)
    
    # Filter search by target_stage = "Seed"
    seed_hits = VectorStore.search_similarity(
        "startups", 
        "healthcare medical scans", 
        limit=5, 
        where_metadata={"target_stage": "Seed"}
    )
    
    for hit in seed_hits:
        print(f"  Hit: {hit['metadata']['startup_name']} (Stage: {hit['metadata']['target_stage']})")
        assert hit["metadata"]["target_stage"] == "Seed", "Metadata filtering failed to isolate Seed stage."
        
    print("  [SUCCESS] Metadata isolating filter operates cleanly and securely!")

    # 4. Test Confidence Score Bounds
    print("\n[4] Testing Retrieval Confidence Bounds...")
    for item in run_1:
        score = item["match_score"]
        assert 0 <= score <= 100, f"Confidence score {score} out of bounds!"
        
    print(f"  [SUCCESS] All match scores cleanly bounded inside [0, 100] range.")
    print("\n[SUCCESS] RETRIEVAL CONSISTENCY SUITE COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_retrieval_consistency()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
