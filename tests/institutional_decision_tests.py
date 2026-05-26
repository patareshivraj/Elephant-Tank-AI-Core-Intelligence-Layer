import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.decision_support.investment_decision_engine import InvestmentDecisionEngine
from app.workflow.startup_prioritizer import StartupPrioritizer

def test_decision_and_priority_logic():
    print("Executing decision and priority engine tests...")
    
    # 1. Prioritization Engine Checks
    startups = [
        {"startup_name": "Phoenix Health", "overall_score": 85, "trajectory_score": 80, "founder_score": 9, "timing_verdict": "WELL_TIMED"},
        {"startup_name": "Omega AI", "overall_score": 72, "trajectory_score": 60, "founder_score": 7, "timing_verdict": "WELL_TIMED"},
        {"startup_name": "Alpha SaaS", "overall_score": 61, "trajectory_score": 50, "founder_score": 5, "timing_verdict": "TOO_EARLY"}
    ]
    
    prioritized = StartupPrioritizer.prioritize_pipeline(startups)
    assert prioritized[0]["startup_name"] == "Phoenix Health"
    assert prioritized[0]["priority_score"] >= 80.0
    
    # 2. Decision Engine Checks
    decision_details = InvestmentDecisionEngine.evaluate_investment_decision({
        "startup_name": "Phoenix Health",
        "overall_score": 85,
        "confidence_score": 9,
        "risks": ["FDA regulation delays"]
    })
    
    assert decision_details["investability_verdict"] == "HIGH_CONVICTION_INVEST"
    assert decision_details["operational_signal"] == "STRATEGIC_DIRECT_ALLOCATE"
    
    print("[SUCCESS] Decision and priority engine tests passed!")

if __name__ == "__main__":
    test_decision_and_priority_logic()
