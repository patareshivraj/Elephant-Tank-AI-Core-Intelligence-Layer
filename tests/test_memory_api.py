import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8002"

def run_memory_api_tests():
    print("========================================")
    print(" ELEPHANT TANK AI - MEMORY & GRAPH API TESTER")
    print("========================================")

    # 1. Update Persistent Startup & Founder Memory
    print("[1] POST /memory/update -> Performing transactional commit...")
    payload = {
        "startup_name": "Phoenix Health",
        "overall_score": 79,
        "innovation_score": 8,
        "market_score": 8,
        "scalability_score": 7,
        "founder_score": 9,
        "funding_readiness_score": 8,
        "risks": ["FDA regulation delays"],
        "recommendations": ["Initiate clinical trials early"],
        "confidence_score": 9,
        "target_stage": "Seed",
        "sectors": ["MedTech", "AI"],
        "timing_verdict": "WELL_TIMED",
        "founder_name": "Dr. Clara Winters",
        "founder_technical_rating": 9,
        "founder_leadership_rating": 8
    }
    
    resp = requests.post(f"{BASE_URL}/memory/update", json=payload)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Memory update failed! {resp.text}"
    data = resp.json()
    print(f"    Message: {data.get('message')}")
    print(f"    Logs count: {len(data.get('execution_logs', []))}\n")

    # 2. Get Startup timeline & profile
    print("[2] GET /memory/startup/Phoenix Health -> Fetching history milestones...")
    resp = requests.get(f"{BASE_URL}/memory/startup/Phoenix Health")
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Get startup history failed! {resp.text}"
    data = resp.json()
    print(f"    Founder registered: {data.get('startup_name')}")
    print(f"    Evaluation history count: {len(data.get('evaluation_history', []))}\n")

    # 3. Get Founder timeline & profile
    print("[3] GET /memory/founder/Dr. Clara Winters -> Fetching career records...")
    resp = requests.get(f"{BASE_URL}/memory/founder/Dr. Clara Winters")
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Get founder history failed! {resp.text}"
    data = resp.json()
    print(f"    Founder name: {data.get('founder_name')}")
    print(f"    Technical rating: {data.get('current_technical_rating')}\n")

    # 4. Traverse Knowledge Graph
    print("[4] GET /knowledge-graph/traverse/Dr. Clara Winters -> Traversing graph links...")
    resp = requests.get(f"{BASE_URL}/knowledge-graph/traverse/Dr. Clara Winters")
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"KG traverse failed! {resp.text}"
    data = resp.json()
    print(f"    Found relations:")
    for rel in data:
        print(f"      - [{rel['direction']}] Linked to '{rel['neighbor']}' via '{rel['relation']}'")
    print()

    # 5. Discover Sector Network
    print("[5] GET /knowledge-graph/sector/MedTech -> Discovering network subgraphs...")
    resp = requests.get(f"{BASE_URL}/knowledge-graph/sector/MedTech")
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"KG sector discovery failed! {resp.text}"
    data = resp.json()
    print(f"    Discovered subgraph nodes count: {len(data.get('nodes', {}))}")
    print(f"    Discovered subgraph edges count: {len(data.get('edges', []))}\n")

    # 6. Compare Startups
    print("[6] POST /intelligence/compare -> Side-by-side matrices...")
    payload_comp = {
        "startup_a": {"startup_name": "Phoenix Health", "overall_score": 79, "innovation_score": 8, "scalability_score": 7},
        "startup_b": {"startup_name": "Omega Bio", "overall_score": 68, "innovation_score": 6, "scalability_score": 5}
    }
    resp = requests.post(f"{BASE_URL}/intelligence/compare", json=payload_comp)
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Startup comparison failed! {resp.text}"
    data = resp.json()
    print(f"    Verdict: {data.get('relative_performance_verdict')}\n")

    # 7. Get Chronological timeline
    print("[7] GET /timeline/Phoenix Health -> Compiling milestone events...")
    resp = requests.get(f"{BASE_URL}/timeline/Phoenix Health")
    print(f"    Status: {resp.status_code}")
    assert resp.status_code == 200, f"Milestones timeline failed! {resp.text}"
    data = resp.json()
    print(f"    Timeline Narrative: {data.get('timeline_narrative')}")
    print(f"    Events logged: {len(data.get('milestone_events', []))}\n")

    print("========================================")
    print(" [SUCCESS] ALL SPRINT 7 MEMORY & GRAPH API ENDPOINTS VERIFIED!")
    print("========================================")

if __name__ == "__main__":
    try:
        run_memory_api_tests()
    except Exception as e:
        print(f"\n[FAIL] API integration failed: {e}")
        sys.exit(1)
