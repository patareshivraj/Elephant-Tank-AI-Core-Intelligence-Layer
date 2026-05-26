import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8005"

def run_governance_api_tests():
    print("========================================")
    print(" ELEPHANT TANK AI - GOVERNANCE & EXPLAINABILITY API TESTER")
    print("========================================")

    # 1. Score Explanation
    print("[1] POST /governance/explain-score...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "overall_score": 85.0,
        "metrics": {"tam_score": 80, "moat_score": 90, "traction_score": 85}
    }
    resp = requests.post(f"{BASE_URL}/governance/explain-score", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Score explanation failed! {resp.text}"
    data = resp.json()
    print(f"    Reconstructed: {data.get('reconstructed_score')}")
    print(f"    Variance: {data.get('mathematical_reconciliation_variance')}")
    print(f"    Interpretation: {data.get('interpretation_narrative')}\n")

    # 2. Traceability Record
    print("[2] POST /governance/traceability...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "source_documents": ["pitch.pdf", "cap_table.xlsx"],
        "evidence_snippets": ["TAM of $5B", "Founder shares 60%"]
    }
    resp = requests.post(f"{BASE_URL}/governance/traceability", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Traceability failed! {resp.text}"
    data = resp.json()
    print(f"    Total Stamped Anchors: {data.get('total_anchors_stamped')}")
    print(f"    First Anchor Doc: {data['evidence_provenance_links'][0]['source_document']}\n")

    # 3. Reasoning Lineage
    print("[3] POST /governance/reasoning-lineage...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "steps": [
            {"node": "PDF Parse", "logic": "Structured OCR extraction", "verdict": "SUCCESS"},
            {"node": "TAM Scoring", "logic": "Weighted growth metrics", "verdict": "80/100"}
        ]
    }
    resp = requests.post(f"{BASE_URL}/governance/reasoning-lineage", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Lineage failed! {resp.text}"
    data = resp.json()
    print(f"    Steps Tracked: {data.get('total_reasoning_steps')}")
    print(f"    Lineage Chain Stamped: {data.get('lineage_integrity_verified')}\n")

    # 4. Policy Audit (Compliant)
    print("[4] POST /governance/policy-audit -> APPROVED...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "overall_score": 85.0,
        "confidence_score": 9
    }
    resp = requests.post(f"{BASE_URL}/governance/policy-audit", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Policy audit failed! {resp.text}"
    data = resp.json()
    print(f"    Governance Status: {data.get('governance_status')}\n")

    # 5. Policy Audit (Violation - Hallucination)
    print("[5] POST /governance/policy-audit -> REJECTED (Out of bounds score)...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "overall_score": 120.0,
        "confidence_score": 9
    }
    resp = requests.post(f"{BASE_URL}/governance/policy-audit", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Policy audit error check failed! {resp.text}"
    data = resp.json()
    print(f"    Governance Status: {data.get('governance_status')}")
    print(f"    Violations list: {[v['reason'] for v in data.get('violations_list', [])]}\n")

    # 6. Confidence Explanation
    print("[6] POST /governance/explain-confidence...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "confidence_score": 7,
        "data_gaps": 2
    }
    resp = requests.post(f"{BASE_URL}/governance/explain-confidence", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Confidence explainer failed! {resp.text}"
    data = resp.json()
    print(f"    Reconstructed Conf: {data.get('reconstructed_confidence')}/10")
    print(f"    Explanation: {data.get('confidence_explanation')}\n")

    # 7. Recommendation Provenance
    print("[7] POST /governance/recommendation-provenance...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "recommendation": "HIGH_CONVICTION_ALLOCATE",
        "evidence_triggers": ["TAM > $1B", "Founder rating 9/10"]
    }
    resp = requests.post(f"{BASE_URL}/governance/recommendation-provenance", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Provenance failed! {resp.text}"
    data = resp.json()
    print(f"    Provenance Valid: {data.get('provenance_valid')}")
    print(f"    Msg: {data.get('message')}\n")

    # 8. Log Audit to persistent file
    print("[8] POST /governance/log-audit...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "payload": {"overall_score": 85.0, "compliance_rating": "FULLY_COMPLIANT"}
    }
    resp = requests.post(f"{BASE_URL}/governance/log-audit", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Log audit failed! {resp.text}"
    data = resp.json()
    print(f"    Log Status: {data.get('status')}")
    print(f"    Path: {data.get('audit_file_path')}\n")

    # 9. Compliance Schema Validation
    print("[9] POST /governance/compliance-validate...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "overall_score": 85.0,
        "founder_score": 9.0
    }
    resp = requests.post(f"{BASE_URL}/governance/compliance-validate", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Compliance check failed! {resp.text}"
    data = resp.json()
    print(f"    Compliant: {data.get('is_compliant')} ({data.get('compliance_rating')})\n")

    # 10. Metric Drift Monitoring
    print("[10] POST /governance/monitor-drift...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "history": [85.0, 92.0, 68.0]
    }
    resp = requests.post(f"{BASE_URL}/governance/monitor-drift", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Drift monitoring failed! {resp.text}"
    data = resp.json()
    print(f"    Volatility Index: {data.get('volatility_index')}")
    print(f"    Alert Level: {data.get('drift_alert')}")
    print(f"    Msg: {data.get('message')}\n")

    print("========================================")
    print(" [SUCCESS] ALL SPRINT 10 GOVERNANCE & EXPLAINABILITY ENDPOINTS VERIFIED!")
    print("========================================")

if __name__ == "__main__":
    try:
        run_governance_api_tests()
    except Exception as e:
        print(f"\n[FAIL] Governance API integration failed: {e}")
        sys.exit(1)
