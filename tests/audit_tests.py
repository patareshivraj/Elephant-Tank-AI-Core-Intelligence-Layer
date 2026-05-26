import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.audit.audit_engine import InstitutionalAuditEngine

TEST_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

def setup_module():
    os.makedirs(os.path.join(TEST_UPLOADS, "audit"), exist_ok=True)
    audit_file = os.path.join(TEST_UPLOADS, "audit", "audit_log.json")
    if os.path.exists(audit_file):
        os.remove(audit_file)

def test_audit_logs():
    print("Executing audit tests...")
    
    payload = {
        "overall_score": 85.0,
        "confidence_score": 9,
        "action": "APPROVED"
    }
    
    res = InstitutionalAuditEngine.record_audit_entry("Alpha Biotech", payload)
    assert res["status"] == "AUDITED"
    assert os.path.exists(res["audit_file_path"])
    assert res["logged_entry"]["startup_name"] == "Alpha Biotech"
    assert res["logged_entry"]["signature"] == "ELEPHANT_TANK_SECURE_HASH_0xff"
    
    print("[SUCCESS] Audit tests passed!")

if __name__ == "__main__":
    setup_module()
    test_audit_logs()
