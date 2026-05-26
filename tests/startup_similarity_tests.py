import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.semantic.index_manager import IndexManager
from app.matching.startup_similarity import StartupSimilarityEngine

def test_startup_similarity():
    print("========================================")
    print(" ELEPHANT TANK AI - SIMILARITY TEST")
    print("========================================")
    
    # 1. Reset and Index three startups
    print("[1] Seeding startups index...")
    IndexManager.reset_all_indices()
    
    health_a = {
        "startup_name": "MediVision AI",
        "startup_description": "FDA-cleared medical diagnostics using neural computer vision models.",
        "target_stage": "Series A",
        "founder_data": "Ex-Mayo clinic radiologist."
    }
    health_b = {
        "startup_name": "BioScan Lab",
        "startup_description": "Biomedical MRI diagnostic platform scanning clinical tissues.",
        "target_stage": "Seed",
        "founder_data": "MD PhD from Johns Hopkins."
    }
    devtool_c = {
        "startup_name": "KubeCloud DB",
        "startup_description": "Developer platform running distributed AWS serverless database pipelines.",
        "target_stage": "Series A",
        "founder_data": "Ex-AWS infrastructure architect."
    }
    
    IndexManager.index_startup("st_health_a", health_a)
    IndexManager.index_startup("st_health_b", health_b)
    IndexManager.index_startup("st_devtool_c", devtool_c)
    
    # 2. Run Similarity Evaluation
    print("\n[2] Checking similarity for medical/healthcare query...")
    query = "AI diagnostics, healthcare medical imaging scan."
    
    res = StartupSimilarityEngine.evaluate_similarity(query, limit=3)
    
    for idx, st in enumerate(res["similar_startups"]):
        print(f"  #{idx+1}: {st['startup_name']} (Similarity Score: {st['similarity_score']}, Stage: {st['target_stage']})")
        
    print(f"\nInferred Categories: {res['related_market_categories']}")
    print(f"Overlapping Models: {res['overlapping_business_models']}")
    
    # Assert healthcare startups are matched higher
    first_match = res["similar_startups"][0]["startup_name"]
    assert "MediVision" in first_match or "BioScan" in first_match, f"Expected a healthcare match, got {first_match}"
    print(f"\n  [SUCCESS] Correctly retrieved {first_match} as the primary similar startup!")
    
    print("\n[SUCCESS] ALL SIMILARITY TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_startup_similarity()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
