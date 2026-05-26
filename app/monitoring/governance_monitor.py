import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Monitoring.GovernanceMonitor")

class GovernanceMonitor:
    """
    Governance Monitoring System.
    Monitors metrics drift, rating instabilities, and operational policy triggers.
    """
    
    @classmethod
    def evaluate_governance_drift(cls, name: str, history: List[float]) -> Dict[str, Any]:
        """
        Scans history logs to compute score volatility metrics.
        """
        logger.info(f"Auditing scoring drift parameters for startup: {name}")
        
        if len(history) < 2:
            return {
                "startup_name": name,
                "volatility_index": 0.0,
                "drift_alert": "NO_ALERT_INSUFFICIENT_HISTORY",
                "message": "Historical evaluation depth insufficient to calculate variance drift."
            }
            
        # Volatility = Absolute range of history scores
        volatility = max(history) - min(history)
        
        if volatility >= 15.0:
            alert = "HIGH_VOLATILITY_RATING_ALERT"
            msg = f"Alert: Score volatility is very high ({volatility} points). Investigate parameter instability."
        else:
            alert = "STABLE_SCORING_METRICS"
            msg = f"Evaluation scoring remains stable (volatility: {volatility} points)."
            
        return {
            "startup_name": name,
            "volatility_index": round(volatility, 2),
            "drift_alert": alert,
            "message": msg
        }
