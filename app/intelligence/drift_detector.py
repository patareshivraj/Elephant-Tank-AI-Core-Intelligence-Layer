import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Intelligence.DriftDetector")

class IntelligenceDriftDetector:
    """
    Intelligence Drift Detection Engine.
    Detects critical shifts, strategic volatility, founder competence changes,
    and confidence variance between consecutive due diligence runs.
    """
    
    @classmethod
    def calculate_drift(cls, run_v1: Dict[str, Any], run_v2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates metric variations between two timeline snapshots to detect trajectory instability.
        """
        logger.info("Computing venture intelligence drift indicators...")
        
        s1 = run_v1.get("overall_score", 50)
        s2 = run_v2.get("overall_score", 50)
        score_diff = s2 - s1
        
        # 1. Trajectory Verdict
        if score_diff <= -10:
            verdict = "CRITICAL_DOWNWARD_DRIFT"
            severity = "HIGH"
            narrative = "Alarming downward drift detected. Core execution velocity has degraded significantly, indicating operational blockages or competitive displacement."
        elif score_diff >= 10:
            verdict = "CRITICAL_UPWARD_DRIFT"
            severity = "LOW"
            narrative = "Exceptional acceleration. The venture has cleared major milestones, indicating strategic acceleration."
        else:
            verdict = "STABLE"
            severity = "NEGLIGIBLE"
            narrative = "The venture remains within stable operational parameters, experiencing minor normal variances."
            
        # 2. Check for individual metric shifts
        m1 = run_v1.get("metrics", {})
        m2 = run_v2.get("metrics", {})
        
        metric_variations = {}
        for k, v in m2.items():
            if k in m1:
                metric_variations[k] = v - m1[k]
                
        return {
            "drift_status": verdict,
            "drift_severity": severity,
            "absolute_score_drift": score_diff,
            "metric_variations": metric_variations,
            "drift_explainable_narrative": narrative
        }
