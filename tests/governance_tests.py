import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.governance.governance_engine import AIGovernanceEngine

def test_governance_rules():
    print("Executing governance tests...")
    
    # 1. Compliant check
    payload_ok = {
        "startup_name": "Alpha Biotech",
        "overall_score": 85.0,
        "confidence_score": 9
    }
    res_ok = AIGovernanceEngine.audit_and_governance(payload_ok)
    assert res_ok["governance_status"] == "APPROVED_COMPLIANT"
    
    # 2. Hallucination check (score > 100)
    payload_bad_score = {
        "startup_name": "Alpha Biotech",
        "overall_score": 115.0,
        "confidence_score": 9
    }
    res_bad_score = AIGovernanceEngine.audit_and_governance(payload_bad_score)
    assert res_bad_score["governance_status"] == "REJECTED_VIOLATION"
    assert any(v["policy"] == "HALLUCINATION_GUARD" for v in res_bad_score["violations_list"])
    
    # 3. Insufficient evidence check (score 85, confidence 2)
    payload_bad_evidence = {
        "startup_name": "Alpha Biotech",
        "overall_score": 85.0,
        "confidence_score": 2
    }
    res_bad_evidence = AIGovernanceEngine.audit_and_governance(payload_bad_evidence)
    assert res_bad_evidence["governance_status"] == "REJECTED_VIOLATION"
    assert any(v["policy"] == "INSUFFICIENT_EVIDENCE_POLICY" for v in res_bad_evidence["violations_list"])
    
    print("[SUCCESS] Governance tests passed!")

if __name__ == "__main__":
    test_governance_rules()
