import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.governance.traceability import DecisionTraceabilityLayer
from app.governance.reasoning_lineage import ReasoningLineageTracker
from app.governance.recommendation_provenance import RecommendationProvenanceSystem
from app.monitoring.governance_monitor import GovernanceMonitor

def test_assurance_and_monitoring():
    print("Executing assurance & monitoring tests...")
    
    # 1. Traceability anchor check
    trace = DecisionTraceabilityLayer.compile_traceability_record(
        "Alpha Biotech",
        ["pitch_deck.pdf", "financial_model.xlsx"],
        ["Extracted $50M TAM target", "Forecasted 85% gross margins"]
    )
    assert trace["total_anchors_stamped"] == 2
    assert trace["evidence_provenance_links"][0]["source_document"] == "pitch_deck.pdf"
    
    # 2. Lineage chain check
    steps = [
        {"node": "PDF Parse", "logic": "Structured OCR extraction", "verdict": "SUCCESS"},
        {"node": " TAM Score Calculation", "logic": "Deterministic scaling metrics", "verdict": "80/100"}
    ]
    lineage = ReasoningLineageTracker.record_reasoning_flow("Alpha Biotech", steps)
    assert lineage["total_reasoning_steps"] == 2
    assert lineage["reasoning_lineage_chain"][0]["analytical_node"] == "PDF Parse"
    
    # 3. Recommendation provenance check
    prov = RecommendationProvenanceSystem.compile_provenance(
        "Alpha Biotech",
        "HIGH_CONVICTION_ALLOCATE",
        ["TAM > $10B", "Founder score > 8.0"]
    )
    assert prov["allocated_recommendation"] == "HIGH_CONVICTION_ALLOCATE"
    assert len(prov["evidence_triggers"]) == 2
    
    # 4. Governance monitoring drift check
    history = [85.0, 86.5, 84.0, 72.0]  # Volatility = 14.5 -> stable (<15.0)
    mon = GovernanceMonitor.evaluate_governance_drift("Alpha Biotech", history)
    assert mon["volatility_index"] == 14.5
    assert mon["drift_alert"] == "STABLE_SCORING_METRICS"
    
    history_drift = [85.0, 92.0, 68.0]  # Volatility = 24.0 -> alert
    mon_drift = GovernanceMonitor.evaluate_governance_drift("Alpha Biotech", history_drift)
    assert mon_drift["volatility_index"] == 24.0
    assert mon_drift["drift_alert"] == "HIGH_VOLATILITY_RATING_ALERT"
    
    print("[SUCCESS] Assurance & monitoring tests passed!")

if __name__ == "__main__":
    test_assurance_and_monitoring()
