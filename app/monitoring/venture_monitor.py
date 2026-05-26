import time
import logging
from typing import Dict, Any, List
from app.memory.startup_memory import StartupMemoryEngine

logger = logging.getLogger("ElephantTank.Monitoring.VentureMonitor")

class VentureMonitor:
    """
    Automated Venture Monitoring Layer.
    Continuously tracks longitudinal changes, scans startup histories,
    and returns comprehensive warnings when performance drops are logged.
    """
    
    @classmethod
    def monitor_startup(cls, startup_name: str) -> Dict[str, Any]:
        """
        Scans a startup's entire evaluation trajectory to construct a monitoring report.
        """
        logger.info(f"Scanning milestones history for startup: {startup_name}")
        
        history = StartupMemoryEngine.get_startup_history(startup_name)
        if not history or not history.get("evaluation_history"):
            return {
                "startup_name": startup_name,
                "status": "NO_HISTORY",
                "warnings": [],
                "message": "Venture has no registered milestone records."
            }
            
        snapshots = history["evaluation_history"]
        warnings = []
        
        # 1. Check for score decline
        if len(snapshots) >= 2:
            s_prev = snapshots[-2]["overall_score"]
            s_curr = snapshots[-1]["overall_score"]
            if s_curr < s_prev:
                warnings.append(f"Score drop detected: Slipped from {s_prev} to {s_curr} ARR valuation levels.")
                
        # 2. Check for risk item additions
        r_curr = snapshots[-1].get("risks", [])
        if len(snapshots) >= 2:
            r_prev = snapshots[-2].get("risks", [])
            if len(r_curr) > len(r_prev):
                warnings.append(f"New risk parameters detected: Active risks increased from {len(r_prev)} to {len(r_curr)}.")
                
        status = "ALERT_ACTIVE" if len(warnings) > 0 else "STABLE"
        
        return {
            "startup_name": startup_name,
            "status": status,
            "warnings": warnings,
            "latest_score": snapshots[-1]["overall_score"],
            "latest_confidence": snapshots[-1].get("confidence_score", 7),
            "timestamp": int(time.time())
        }
