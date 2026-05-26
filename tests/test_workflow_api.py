import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8003"

def run_workflow_api_tests():
    print("========================================")
    print(" ELEPHANT TANK AI - WORKFLOW & DECISION API TESTER")
    print("========================================")

    # 1. Enqueue startup
    print("[1] POST /workflow/enqueue -> Registering venture pipeline queue...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "stage": "IN_REVIEW"
    }
    resp = requests.post(f"{BASE_URL}/workflow/enqueue", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Enqueue failed! {resp.text}"
    data = resp.json()
    print(f"    Message: {data.get('message')}\n")

    # 2. Transition state
    print("[2] POST /workflow/transition -> Moving to Due Diligence stage...")
    payload = {
        "startup_name": "Titanium Aerospace",
        "new_state": "DUE_DILIGENCE",
        "rationale": "High structural score achieved."
    }
    resp = requests.post(f"{BASE_URL}/workflow/transition", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Transition failed! {resp.text}"
    data = resp.json()
    print(f"    Message: {data.get('message')}\n")

    # 3. Prioritize Batch list
    print("[3] POST /workflow/prioritize -> Sorting batch with GTM timing and scores...")
    payload_batch = [
        {"startup_name": "Titanium Aerospace", "overall_score": 85, "trajectory_score": 80, "founder_score": 9, "timing_verdict": "WELL_TIMED"},
        {"startup_name": "Omega Bio", "overall_score": 68, "trajectory_score": 60, "founder_score": 6, "timing_verdict": "TOO_EARLY"}
    ]
    resp = requests.post(f"{BASE_URL}/workflow/prioritize", json=payload_batch)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Prioritization failed! {resp.text}"
    data = resp.json()
    print(f"    Ranked Batch list:")
    for st in data:
        print(f"      - {st['startup_name']} (Priority Index: {st['priority_score']}/100)")
    print()

    # 4. Investment Decision Engine Model
    print("[4] POST /workflow/decision -> Running institutional readiness model...")
    payload_dec = {
        "startup_name": "Titanium Aerospace",
        "overall_score": 85,
        "confidence_score": 9,
        "risks": ["Supply chain constraints"]
    }
    resp = requests.post(f"{BASE_URL}/workflow/decision", json=payload_dec)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Decision model failed! {resp.text}"
    data = resp.json()
    print(f"    Verdict: {data.get('investability_verdict')}")
    print(f"    Direct Signal: {data.get('operational_signal')}\n")

    # 5. Escalation Rule trigger
    print("[5] POST /workflow/escalation-check -> Checking severity thresholds...")
    payload_esc = {
        "startup_name": "Titanium Aerospace",
        "current_metrics": {"overall_score": 65, "confidence_score": 8, "founder_score": 9},
        "previous_metrics": {"overall_score": 85, "confidence_score": 8, "founder_score": 9}
    }
    resp = requests.post(f"{BASE_URL}/workflow/escalation-check", json=payload_esc)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Escalation check failed! {resp.text}"
    data = resp.json()
    print(f"    Escalated: {data.get('escalated')} (Severity: {data.get('escalation_severity')})")
    print(f"    Action Plan: {data.get('recommended_action')}\n")

    # 6. Venture Monitor
    print("[6] GET /workflow/monitor/Titanium Aerospace -> Fetching warnings...")
    resp = requests.get(f"{BASE_URL}/workflow/monitor/Titanium Aerospace")
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Venture monitor failed! {resp.text}"
    data = resp.json()
    print(f"    Monitoring Status: {data.get('status')}")
    print(f"    Warnings: {data.get('warnings')}\n")

    # 7. Portfolio concentration analysis
    print("[7] POST /workflow/portfolio-analysis -> Checking exposure concentration metrics...")
    payload_port = [
        {"startup_name": "Titanium Aerospace", "overall_score": 85, "sectors": ["SpaceTech", "AI"]},
        {"startup_name": "Nebula Space", "overall_score": 72, "sectors": ["SpaceTech"]},
        {"startup_name": "Cosmic Rocket", "overall_score": 68, "sectors": ["SpaceTech"]}
    ]
    resp = requests.post(f"{BASE_URL}/workflow/portfolio-analysis", json=payload_port)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Portfolio analysis failed! {resp.text}"
    data = resp.json()
    print(f"    Portfolio Status: {data.get('portfolio_status')}")
    print(f"    Warnings list: {[w['message'] for w in data.get('concentration_warnings', [])]}\n")

    print("========================================")
    print(" [SUCCESS] ALL SPRINT 8 WORKFLOW & DECISION ENDPOINTS VERIFIED!")
    print("========================================")

if __name__ == "__main__":
    try:
        run_workflow_api_tests()
    except Exception as e:
        print(f"\n[FAIL] Workflow API integration failed: {e}")
        sys.exit(1)
