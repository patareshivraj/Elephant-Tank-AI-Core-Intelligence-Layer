import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.strategy.recommendation_engine import RecommendationEngine

def test_recommendation_prioritization():
    print("========================================")
    print(" ELEPHANT TANK - RECOMMENDATION TESTER")
    print("========================================")
    
    # 1. Setup Mock Unsorted Evaluation Response
    mock_eval = {
        "recommendations": [
            "Optimizing AWS billing systems and cloud server structures.",  # OPTIMIZATION (Priority 5)
            "Address severe GTM weaknesses by redesigning customer acquisition pipeline.",  # GTM_WEAKNESS (Priority 4)
            "Resolve founder equity split friction and technical leadership gap.",  # FOUNDER_RISK (Priority 1)
            "Mitigate market competitor pressure by establishing proprietary IP barriers."  # MARKET_THREAT (Priority 2)
        ]
    }
    
    print("[1] Running Recommendation Prioritization Engine...")
    sorted_recs = RecommendationEngine.generate_recommendations(mock_eval)
    
    print("\n[RESULT] Prioritized Recommendation Pipeline:")
    for idx, rec in enumerate(sorted_recs):
        print(f"  #{idx+1}: [{rec['category']}] (Score: {rec['priority_score']}) - {rec['title']}")
        print(f"     - Detail: {rec['description']}")
        print(f"     - Action Plan: {rec['mitigation_action']}")
        
    # 2. Strict Priority Assertions (Founder Risks first, Market Threats second, etc.)
    assert sorted_recs[0]["category"] == "FOUNDER_RISK", "Founder risk must be prioritized first."
    assert sorted_recs[1]["category"] == "MARKET_THREAT", "Market threat must be prioritized second."
    assert sorted_recs[2]["category"] == "GTM_WEAKNESS", "GTM weaknesses must precede optimizations."
    assert sorted_recs[3]["category"] == "OPTIMIZATION", "Optimization suggestions must be ranked last."
    
    print("\n[SUCCESS] RECOMMENDATION PRIORITIZATION TEST PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_recommendation_prioritization()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
