import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.compliance.compliance_validator import ComplianceValidator

def test_compliance_validations():
    print("Executing compliance tests...")
    
    # 1. Fully compliant payload
    payload_ok = {
        "startup_name": "Alpha Biotech",
        "overall_score": 85.0,
        "founder_score": 9.0
    }
    res_ok = ComplianceValidator.validate_compliance(payload_ok)
    assert res_ok["is_compliant"] is True
    assert res_ok["compliance_rating"] == "FULLY_COMPLIANT"
    
    # 2. Non-compliant payload (missing overall_score)
    payload_bad = {
        "startup_name": "Alpha Biotech",
        "founder_score": 9.0
    }
    res_bad = ComplianceValidator.validate_compliance(payload_bad)
    assert res_bad["is_compliant"] is False
    assert "overall_score" in res_bad["missing_fields"]
    assert res_bad["compliance_rating"] == "NON_COMPLIANT_FIELD_DEFICIT"
    
    print("[SUCCESS] Compliance tests passed!")

if __name__ == "__main__":
    test_compliance_validations()
