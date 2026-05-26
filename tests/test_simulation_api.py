import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8004"

def run_simulation_api_tests():
    print("========================================")
    print(" ELEPHANT TANK AI - STRATEGIC SIMULATION API TESTER")
    print("========================================")

    # 1. Scenario Simulation
    print("[1] POST /simulation/scenario -> Running BULL_CASE...")
    payload = {
        "metrics": {"startup_name": "Titanium Aerospace", "overall_score": 80, "founder_score": 8},
        "scenario": "BULL_CASE"
    }
    resp = requests.post(f"{BASE_URL}/simulation/scenario", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Scenario simulation failed! {resp.text}"
    data = resp.json()
    print(f"    Simulated Score: {data.get('simulated_overall_score')}")
    print(f"    Scaling Prob: {data.get('scaling_probability')}%")
    print(f"    Narrative: {data.get('simulation_narrative')}\n")

    # 2. Startup Competition
    print("[2] POST /simulation/competition -> Assessing defensibility overlap...")
    payload = {
        "startup_a": {"startup_name": "Titanium Aerospace", "overall_score": 85, "sectors": ["SpaceTech", "AI"]},
        "startup_b": {"startup_name": "Nebula Space", "overall_score": 70, "sectors": ["SpaceTech"]}
    }
    resp = requests.post(f"{BASE_URL}/simulation/competition", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Competition failed! {resp.text}"
    data = resp.json()
    print(f"    Crowding Index: {data.get('ecosystem_crowding_index')}%")
    print(f"    Vulnerable: {data.get('vulnerable_entity')}\n")

    # 3. Cross-Portfolio Cannibalization
    print("[3] POST /portfolio/cross-analysis -> Mapping redundant segments...")
    payload_port = [
        {"startup_name": "Titanium Aerospace", "sectors": ["SpaceTech", "AI"]},
        {"startup_name": "Nebula Space", "sectors": ["SpaceTech", "AI"]}
    ]
    resp = requests.post(f"{BASE_URL}/portfolio/cross-analysis", json=payload_port)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Cross portfolio analysis failed! {resp.text}"
    data = resp.json()
    print(f"    Cannibalization Warnings: {data.get('cannibalization_warnings_count')}\n")

    # 4. Ecosystem Shock
    print("[4] POST /simulation/shock -> Running AI_DISRUPTION shock...")
    payload = {
        "metrics": {"startup_name": "Titanium Aerospace", "overall_score": 80, "sectors": ["SpaceTech", "SaaS"]},
        "shock_type": "AI_DISRUPTION"
    }
    resp = requests.post(f"{BASE_URL}/simulation/shock", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Shock simulation failed! {resp.text}"
    data = resp.json()
    print(f"    Simulated Score: {data.get('simulated_score')}")
    print(f"    Survivability: {data.get('survivability_index')}% (Vulnerability: {data.get('vulnerability_rating')})\n")

    # 5. Venture Forecasting
    print("[5] POST /forecasting/venture-12month -> Running 12-month GTM curves...")
    payload = {
        "metrics": {"startup_name": "Titanium Aerospace", "overall_score": 75, "founder_score": 8}
    }
    resp = requests.post(f"{BASE_URL}/forecasting/venture-12month", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Forecasting failed! {resp.text}"
    data = resp.json()
    print(f"    Month 12 Proj Score: {data['twelve_month_projection'][-1]['projected_readiness_score']}")
    print(f"    Terminal Category: {data.get('terminal_readiness_classification')}\n")

    # 6. Market Simulation
    print("[6] POST /forecasting/market-sector -> Running Contractive Regime...")
    payload = {
        "sector": "FinTech",
        "macro_regime": "CONTRACTIVE"
    }
    resp = requests.post(f"{BASE_URL}/forecasting/market-sector", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Market simulation failed! {resp.text}"
    data = resp.json()
    print(f"    VC Capital Multiplier: {data.get('capital_funding_multiplier')}x")
    print(f"    Scaling Velocity: {data.get('scaling_velocity')}\n")

    # 7. Portfolio Exposure Analysis
    print("[7] POST /portfolio/exposure-analysis -> Auditing concentration risk...")
    payload_exp = [
        {"startup_name": "Titanium Aerospace", "tech_stack": "AI", "founder_score": 8},
        {"startup_name": "Nebula Space", "tech_stack": "AI", "founder_score": 5},
        {"startup_name": "Cosmic Rocket", "tech_stack": "AI", "founder_score": 4}
    ]
    resp = requests.post(f"{BASE_URL}/portfolio/exposure-analysis", json=payload_exp)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Exposure audit failed! {resp.text}"
    data = resp.json()
    print(f"    Exposure Rating: {data.get('systemic_exposure_rating')}")
    print(f"    Warnings list: {[w['message'] for w in data.get('exposure_warnings', [])]}\n")

    # 8. Ecosystem Cascade Detection
    print("[8] GET /intelligence/cascade-detection -> Scans graph subgraphs...")
    resp = requests.get(f"{BASE_URL}/intelligence/cascade-detection")
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Cascade detection failed! {resp.text}"
    data = resp.json()
    print(f"    Cascade Status: {data.get('ecosystem_cascade_status')}")
    print(f"    Warnings: {data.get('cascade_warnings_count')}\n")

    print("========================================")
    print(" [SUCCESS] ALL SPRINT 9 SIMULATION & MULTI-ENTITY ENDPOINTS VERIFIED!")
    print("========================================")

if __name__ == "__main__":
    try:
        run_simulation_api_tests()
    except Exception as e:
        print(f"\n[FAIL] Simulation API integration failed: {e}")
        sys.exit(1)
