import os
import requests

API_URL = "http://127.0.0.1:8000/upload-startup-documents"

def test_upload_flow():
    print("========================================")
    print(" ELEPHANT TANK AI - INGESTION TESTER")
    print("========================================")
    
    # 1. Test Ingesting Resume
    resume_path = os.path.join(os.path.dirname(__file__), "temp_resume.txt")
    print(f"\n[TESTING RESUME INGESTION] -> {resume_path}")
    with open(resume_path, "rb") as f:
        response = requests.post(API_URL, files={"file": ("resume_john_doe.txt", f, "text/plain")})
        
    if response.status_code == 200:
        data = response.json()
        print("  [SUCCESS] RESUME INGESTED SUCCESSFULLY!")
        print(f"  Startup Name: {data['startup_profile']['startup_name']}")
        print(f"  Overall Score: {data['evaluation_results']['overall_score']}/100")
        print(f"  Founder Confidence: {data['confidence_summary']['overall_confidence']}/10")
        print(f"  Execution Stage: {data['execution_logs'][0]['stage']}")
    else:
        print(f"  [FAILED] RESUME INGESTION FAILED ({response.status_code}): {response.text}")
        
    # 2. Test Ingesting Pitch Deck
    deck_path = os.path.join(os.path.dirname(__file__), "temp_pitch_deck.txt")
    print(f"\n[TESTING PITCH DECK INGESTION] -> {deck_path}")
    with open(deck_path, "rb") as f:
        response = requests.post(API_URL, files={"file": ("medi_tech_pitch_deck.txt", f, "text/plain")})
        
    if response.status_code == 200:
        data = response.json()
        print("  [SUCCESS] PITCH DECK INGESTED SUCCESSFULLY!")
        print(f"  Startup Name: {data['startup_profile']['startup_name']}")
        print(f"  Overall Score: {data['evaluation_results']['overall_score']}/100")
        print(f"  Market Confidence: {data['confidence_summary']['overall_confidence']}/10")
    else:
        print(f"  [FAILED] PITCH DECK INGESTION FAILED ({response.status_code}): {response.text}")

if __name__ == "__main__":
    test_upload_flow()
