import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.reporting.risk_report import RiskReportEngine

def test_risk_classification():
    print("========================================")
    print(" ELEPHANT TANK - RISK REPORT TESTER")
    print("========================================")
    
    # 1. Setup Mock Evaluation Response with diverse raw risks
    mock_eval = {
        "risk_analysis": {
            "risks": [
                "Founder Team: Single non-technical founder with no experienced executive backup.",
                "Regulatory compliance: High friction dealing with FDA registration and medical compliance.",
                "Competitor copycat: Extremely low barrier to entry allowing commodity GPT wrappers to copy.",
                "Technical scaling: Latency problems due to monolithic backend infrastructure database.",
                "Financial capital: Burn rate is high with only 6 months of capital runway left."
            ]
        }
    }
    
    print("[1] Compiling Categorized Risk Report...")
    report = RiskReportEngine.generate_risk_report(mock_eval)
    
    print("\n[RESULT] Compiled Risk Matrix:")
    print(f"  Overall Risk Profile: {report['overall_risk_profile']}")
    print(f"  High Severity Risks Count: {report['high_severity_risks_count']}")
    print(f"  Average Risk Assessment Confidence: {report['average_risk_confidence']}/10")
    print("----------------------------------------")
    
    for idx, r in enumerate(report["classified_risks"]):
        print(f"  Risk #{idx+1}: [{r['risk_domain']}] Severity: {r['severity']} | Conf: {r['confidence_level']}/10")
        print(f"     - Raw Risk: {r['description']}")
        print(f"     - Mitigation Plan: {r['mitigation_recommendation']}")
        print()
        
    # 2. Assertions
    domains = [r["risk_domain"] for r in report["classified_risks"]]
    assert "Founder Risks" in domains, "Founder Risks classification failed."
    assert "Regulatory Risks" in domains, "Regulatory Risks classification failed."
    assert "Competitive Risks" in domains, "Competitive Risks classification failed."
    assert "Technical Risks" in domains, "Technical Risks classification failed."
    assert "Financial Risks" in domains, "Financial Risks classification failed."
    
    # Check severity assignments
    founder_risk = next(r for r in report["classified_risks"] if r["risk_domain"] == "Founder Risks")
    assert founder_risk["severity"] == "HIGH", "Founder risk with keyword 'lack' or 'no tech' should have HIGH severity."
    
    print("[SUCCESS] RISK ANALYSIS TEST PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_risk_classification()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
