import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.semantic.index_manager import IndexManager
from app.semantic.ecosystem_intelligence import EcosystemIntelligenceEngine

def test_semantic_clustering():
    print("========================================")
    print(" ELEPHANT TANK AI - SEMANTIC TEST RUNNER")
    print("========================================")
    
    # 1. Reset and Seed Default Databases
    print("[1] Resetting and seeding default ecosystem vectors...")
    IndexManager.reset_all_indices()
    
    # 2. Index a Healthtech and Fintech startup
    print("[2] Indexing test startups...")
    health_startup = {
        "startup_name": "MediBot Diagnostics",
        "startup_description": "AI diagnostics, medical image recognition, and clinical trials tracking.",
        "target_stage": "Series A",
        "founder_data": "Dr. Sarah Jenkins, veteran biomedical researcher."
    }
    fintech_startup = {
        "startup_name": "LedgerFlow Payments",
        "startup_description": "Fintech payment orchestration APIs and subscription transaction billing engine.",
        "target_stage": "Seed",
        "founder_data": "Alex Mercer, former Stripe engineer."
    }
    
    IndexManager.index_startup("st_health_test", health_startup)
    IndexManager.index_startup("st_fintech_test", fintech_startup)
    
    # 3. Trigger Ecosystem Cluster Analysis
    print("[3] Running Dynamic Ecosystem Clustering...")
    analysis = EcosystemIntelligenceEngine.analyze_ecosystem()
    
    clusters = analysis.get("active_market_clusters", [])
    print(f"  [SUCCESS] Discovered {len(clusters)} active market clusters!")
    
    for cluster in clusters:
        print(f"  - Cluster: {cluster['cluster_name']} (Density: {cluster['market_density']})")
        for st in cluster["associated_startups"]:
            print(f"    * Startup: {st['startup_name']} (Stage: {st['target_stage']})")
            
    # Verify expectations
    assert len(clusters) >= 2, "Should have mapped at least 2 distinct clusters."
    print("\n[SUCCESS] ALL SEMANTIC TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_semantic_clustering()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
