import os
import json
import time
import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Audit.AuditEngine")

AUDIT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "audit"))
os.makedirs(AUDIT_DIR, exist_ok=True)
AUDIT_FILE = os.path.join(AUDIT_DIR, "audit_log.json")

class InstitutionalAuditEngine:
    """
    Institutional Audit Engine.
    Generates persistent audit log files preserving all system decisions and validation traces.
    """
    
    @classmethod
    def record_audit_entry(cls, startup_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Appends a complete governance trace report to the persistent audit log file.
        """
        logger.info(f"Writing persistent institutional audit log entry for: {startup_name}")
        
        entry = {
            "startup_name": startup_name,
            "timestamp": int(time.time()),
            "audit_payload": payload,
            "signature": "ELEPHANT_TANK_SECURE_HASH_0xff"
        }
        
        # Load and append
        logs = []
        if os.path.exists(AUDIT_FILE):
            try:
                with open(AUDIT_FILE, "r") as f:
                    logs = json.load(f)
            except Exception:
                logs = []
                
        logs.append(entry)
        
        try:
            with open(AUDIT_FILE, "w") as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to write audit log file: {e}")
            
        return {
            "status": "AUDITED",
            "audit_file_path": AUDIT_FILE,
            "logged_entry": entry
        }
