import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.reporting.investment_memo import InvestmentMemoEngine

def test_investment_memo_generation():
    print("========================================")
    print(" ELEPHANT TANK - INVESTMENT MEMO TESTER")
    print("========================================")
    
    # 1. Setup Mock High-Score Evaluation
    high_eval = {
        "startup_profile": {
            "startup_name": "Apex Quantum",
            "target_stage": "Seed"
        },
        "evaluation_results": {
            "overall_score": 85,
            "innovation_score": 9,
            "market_score": 8
        }
    }
    
    # 2. Setup Mock Low-Score Evaluation
    low_eval = {
        "startup_profile": {
            "startup_name": "QuickDelivery Chatbot",
            "target_stage": "Pre-seed"
        },
        "evaluation_results": {
            "overall_score": 45,
            "innovation_score": 3,
            "market_score": 4
        }
    }
    
    print("[1] Compiling High-Conviction Memo...")
    high_memo = InvestmentMemoEngine.generate_investment_memo(
        high_eval, 
        raw_description="Quantum-encrypted distributed cybersecurity network for modern aerospace mainframes.",
        raw_founder_data="Dr. Helen Carter, ex-CTO at Lockheed Space Systems, PhD in Aerospace Engineering."
    )
    
    print(f"  Verdict: {high_memo['analyst_verdict']}")
    print(f"  Thesis: {high_memo['investment_thesis']}")
    print(f"  Market Opportunity Summary: {high_memo['market_opportunity_analysis']}")
    print(f"  Founder Summary: {high_memo['founder_capability_assessment']}")
    print(f"  Defensibility summary: {high_memo['defensibility_and_competition_summary']}")
    print("----------------------------------------")
    
    assert "CONVICTION_BUY" in high_memo["analyst_verdict"], "High overall score must yield Conviction Buy."
    
    print("[2] Compiling Pass-Verdict Memo...")
    low_memo = InvestmentMemoEngine.generate_investment_memo(
        low_eval,
        raw_description="Simple food delivery chatbot that replies using a basic ChatGPT wrapper pipeline.",
        raw_founder_data="Jane Doe, first-time hobbyist builder."
    )
    
    print(f"  Verdict: {low_memo['analyst_verdict']}")
    print(f"  Thesis: {low_memo['investment_thesis']}")
    print("----------------------------------------")
    
    assert "PASS_WITH_MONITOR" in low_memo["analyst_verdict"], "Low overall score must yield Pass verdict."
    
    print("[SUCCESS] INVESTMENT MEMO TEST PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_investment_memo_generation()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
