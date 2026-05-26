import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.semantic.index_manager import IndexManager
from app.matching.investor_matcher import InvestorMatcherEngine

def test_investor_matching():
    print("========================================")
    print(" ELEPHANT TANK AI - INVESTOR MATCH TEST")
    print("========================================")
    
    # 1. Seed index
    print("[1] Seeding vector database indexes...")
    IndexManager.reset_all_indices()
    
    # 2. Test Healthcare Matching
    print("\n[2] Testing matching for Healthcare Startup...")
    health_desc = "FDA-cleared medical diagnostics using AI computer vision computer diagnostics imaging."
    health_stage = "Series A"
    
    health_matches = InvestorMatcherEngine.match_investors(health_stage, health_desc, limit=3)
    
    for idx, match in enumerate(health_matches):
        print(f"  #{idx+1}: {match['investor_name']} (Match Score: {match['match_score']}/100, Level: {match['match_level']})")
        for trace in match["reasoning"]:
            print(f"     - Trace: {trace}")
            
    best_health_match = health_matches[0]["investor_name"]
    assert "Aegis Healthcare" in best_health_match, f"Expected Aegis Healthcare to be the top match, got {best_health_match}"
    print(f"  [SUCCESS] Correctly matched {best_health_match} to Healthcare startup!")
    
    # 3. Test Fintech Matching
    print("\n[3] Testing matching for Fintech Startup...")
    fin_desc = "High-performance digital payment gateways, B2B billing ledgers, and transactions."
    fin_stage = "Seed"
    
    fin_matches = InvestorMatcherEngine.match_investors(fin_stage, fin_desc, limit=3)
    
    for idx, match in enumerate(fin_matches):
        print(f"  #{idx+1}: {match['investor_name']} (Match Score: {match['match_score']}/100, Level: {match['match_level']})")
        for trace in match["reasoning"]:
            print(f"     - Trace: {trace}")
            
    best_fin_match = fin_matches[0]["investor_name"]
    assert "Fintech Partners" in best_fin_match or "Stripe" in best_fin_match, f"Expected Fintech Partners to be the top match, got {best_fin_match}"
    print(f"  [SUCCESS] Correctly matched {best_fin_match} to Fintech startup!")

    print("\n[SUCCESS] ALL INVESTOR MATCHING TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_investor_matching()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
