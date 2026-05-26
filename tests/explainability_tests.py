import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.governance.explainability_engine import ExplainabilityEngine
from app.governance.confidence_explainer import ConfidenceExplainabilityEngine

def test_explainability_and_confidence():
    print("Executing explainability tests...")
    
    st_metrics = {
        "tam_score": 80.0,
        "moat_score": 90.0,
        "traction_score": 70.0
    }
    
    # 1. Score explanation check
    res = ExplainabilityEngine.explain_score("Alpha Biotech", 80.0, st_metrics)
    assert res["overall_score"] == 80.0
    assert res["reconstructed_score"] == 80.5  # (80*0.35)+(90*0.35)+(70*0.3) = 28+31.5+21 = 80.5
    assert res["mathematical_reconciliation_variance"] == 0.5
    
    # 2. Confidence explanation check
    conf_res = ConfidenceExplainabilityEngine.explain_confidence("Alpha Biotech", 7, 2)
    assert conf_res["overall_confidence_score"] == 7
    assert conf_res["reconstructed_confidence"] == 7  # 10 - 2 * 1.5 = 7
    assert conf_res["data_gaps_identified"] == 2
    
    print("[SUCCESS] Explainability and confidence tests passed!")

if __name__ == "__main__":
    test_explainability_and_confidence()
