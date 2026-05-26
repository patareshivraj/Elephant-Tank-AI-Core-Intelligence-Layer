import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Monitoring.ReadinessMonitor")

class InvestmentReadinessMonitor:
    """
    Investment Readiness Monitor.
    Tracks venture maturities and assesses the likelihood of successful
    fundraising cycles based on traction levels.
    """
    
    @classmethod
    def evaluate_readiness(cls, startup_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates maturity score and outputs investment readiness classification.
        """
        logger.info(f"Analyzing fundraising readiness metrics for: {startup_metrics.get('startup_name')}")
        
        score = startup_metrics.get("overall_score", 50)
        trajectory = startup_metrics.get("trajectory_score", 50)
        
        # 1. Investability Classifications
        if score >= 80 and trajectory >= 70:
            classification = "HIGH_READINESS"
            description = "Exceptional target readiness. Venture is ready to proceed to rapid Series A/B syndication."
        elif score >= 60 and trajectory >= 50:
            classification = "GROWING_POTENTIAL"
            description = "Solid traction base. Targeted operational improvements will unlock investment viability."
        else:
            classification = "STAGNANT_RISK"
            description = "Significant operational drag or stagnating trajectory limits investability."
            
        return {
            "startup_name": startup_metrics.get("startup_name", "Unknown"),
            "readiness_status": classification,
            "readiness_score": int((score * 0.6) + (trajectory * 0.4)),
            "strategic_implication": description
        }
