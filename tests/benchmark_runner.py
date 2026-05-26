import os
import json
import time
import requests

# Assuming the server is running locally on 8000
API_URL = "http://localhost:8000/evaluate-startup"
BENCHMARK_FILE = os.path.join(os.path.dirname(__file__), "benchmarks", "benchmark_startups.json")

def run_benchmarks():
    print("========================================")
    print(" ELEPHANT TANK AI - BENCHMARK RUNNER")
    print("========================================")
    
    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        startups = json.load(f)
        
    results = []
    
    for startup in startups:
        print(f"\n[TESTING] {startup['category']} -> {startup['startup_name']}")
        
        payload = {
            "startup_name": startup["startup_name"],
            "startup_description": startup["startup_description"],
            "founder_data": startup.get("founder_data", ""),
            "target_stage": startup["target_stage"]
        }
        
        start_time = time.time()
        try:
            response = requests.post(API_URL, json=payload, timeout=30)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                eval_res = data["evaluation_results"]
                overall = eval_res["overall_score"]
                confidence = data["confidence_summary"]["overall_confidence"]
                
                print(f"  [SUCCESS] ({elapsed:.2f}s)")
                print(f"  Overall Score: {overall}/100")
                print(f"  Confidence: {confidence}/10")
                
                results.append({
                    "startup_name": startup["startup_name"],
                    "category": startup["category"],
                    "status": "SUCCESS",
                    "overall_score": overall,
                    "confidence": confidence,
                    "json_valid": True
                })
            else:
                print(f"  [FAILED] ({response.status_code}) - {response.text}")
                results.append({
                    "startup_name": startup["startup_name"],
                    "category": startup["category"],
                    "status": "FAILED",
                    "error": response.text,
                    "json_valid": False
                })
                
        except Exception as e:
            print(f"  [FATAL ERROR]: {str(e)}")
            
    print("\n========================================")
    print(" BENCHMARK REPORT SUMMARY")
    print("========================================")
    for res in results:
        status = res['status']
        name = res['startup_name']
        cat = res['category']
        if status == 'SUCCESS':
            print(f"[{cat}] {name}: Score={res['overall_score']}, Confidence={res['confidence']}")
        else:
            print(f"[{cat}] {name}: FAILED")

if __name__ == "__main__":
    run_benchmarks()
