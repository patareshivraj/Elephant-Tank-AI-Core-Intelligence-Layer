import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def run_api_tests():
    print("========================================")
    print(" ELEPHANT TANK AI - SEMANTIC API TESTER")
    print("========================================")
    
    # 1. Reset / Seed database via API
    print("[1] POST /reset-indices -> Seeding ecosystem...")
    resp = requests.post(f"{BASE_URL}/reset-indices")
    print(f"    Status: {resp.status_code}")
    print(f"    Payload: {resp.json()}\n")
    assert resp.status_code == 200, "Reset index failed!"
    
    # 2. Test Similarity API
    print("[2] POST /similarity -> Calculating startup similarity...")
    payload = {
        "startup_description": "AI diagnostics, medical image recognition scans.",
        "limit": 2
    }
    resp = requests.post(f"{BASE_URL}/similarity", json=payload)
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    print("    Similar Startups:")
    for st in data.get("similar_startups", []):
        print(f"      - {st['startup_name']} (Similarity: {st['similarity_score']})")
    print(f"    Inferred Categories: {data.get('related_market_categories')}")
    print(f"    Logs: {data.get('execution_logs')}\n")
    assert resp.status_code == 200, "Similarity check failed!"
    
    # 3. Test Match Investors API
    print("[3] POST /match-investors -> Matching venture capitalists...")
    payload = {
        "target_stage": "Series A",
        "startup_description": "FDA-cleared computer vision medical scan diagnostics.",
        "limit": 2
    }
    resp = requests.post(f"{BASE_URL}/match-investors", json=payload)
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    for item in data.get("matches", []):
        print(f"      - Investor: {item['investor_name']} (Match: {item['match_score']}/100, Level: {item['match_level']})")
        print(f"        Reasoning: {item['reasoning']}")
    print(f"    Logs: {data.get('execution_logs')}\n")
    assert resp.status_code == 200, "Investor matching failed!"
    
    # 4. Test Match Mentors API
    print("[4] POST /match-mentors -> Matching ecosystem mentors...")
    payload = {
        "target_stage": "Seed",
        "startup_description": "Enterprise transaction ledgers and B2B billing payments engine.",
        "limit": 2
    }
    resp = requests.post(f"{BASE_URL}/match-mentors", json=payload)
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    for item in data.get("matches", []):
        print(f"      - Mentor: {item['mentor_name']} (Match: {item['match_score']}/100, Level: {item['match_level']})")
        print(f"        Specialization: {item['specialization']}")
        print(f"        Reasoning: {item['reasoning']}")
    print(f"    Logs: {data.get('execution_logs')}\n")
    assert resp.status_code == 200, "Mentor matching failed!"
    
    # 5. Test Ecosystem Analysis API
    print("[5] GET /ecosystem-analysis -> Running dynamic clustering...")
    resp = requests.get(f"{BASE_URL}/ecosystem-analysis")
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    print("    Active Market Clusters:")
    for cluster in data.get("active_market_clusters", []):
        print(f"      * Cluster: {cluster['cluster_name']} (Density: {cluster['market_density']})")
    print(f"    Ecosystem Insights: {data.get('ecosystem_insights')}")
    print(f"    Logs: {data.get('execution_logs')}\n")
    assert resp.status_code == 200, "Ecosystem analysis failed!"

    print("========================================")
    print(" [SUCCESS] ALL SEMANTIC API ENDPOINTS OPERATE FLAWLESSLY!")
    print("========================================")

if __name__ == "__main__":
    run_api_tests()
