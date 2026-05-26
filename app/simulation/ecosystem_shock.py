import time
import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Simulation.EcosystemShock")

class EcosystemShockAnalysis:
    """
    Ecosystem Shock Analysis Engine.
    Simulates systemic market contractions, regulatory constraints, and AI infrastructure shifts.
    """
    
    @classmethod
    def simulate_shock(cls, startup_metrics: Dict[str, Any], shock_type: str) -> Dict[str, Any]:
        """
        Calculates survivability metrics and structural sensitivity scores under systemic shocks.
        """
        logger.info(f"Simulating market shock '{shock_type}' on venture: {startup_metrics.get('startup_name')}")
        
        score = float(startup_metrics.get("overall_score", 50))
        sectors = startup_metrics.get("sectors", [])
        now = int(time.time())
        
        shock_type = shock_type.upper().strip()
        
        if shock_type == "REGULATORY_SHIFT":
            score_delta = -15.0
            survivability = 70.0
            vulnerability = "MEDIUM"
            msg = "Regulatory changes increase compliance overhead and operational drag."
        elif shock_type == "MACRO_CONTRACTION":
            score_delta = -25.0
            survivability = 45.0
            vulnerability = "HIGH"
            msg = "Severe capital constraint environment limits scaling runway."
        elif shock_type == "AI_DISRUPTION":
            if any(s.upper() in ["SAAS", "AI", "SOFTWARE"] for s in sectors):
                score_delta = +10.0
                survivability = 90.0
                vulnerability = "LOW"
                msg = "Systemic AI acceleration acts as a force multiplier for cloud tech assets."
            else:
                score_delta = -8.0
                survivability = 75.0
                vulnerability = "MEDIUM"
                msg = "Traditional infrastructure systems experience product substitution pressure."
        else:
            score_delta = 0.0
            survivability = 85.0
            vulnerability = "LOW"
            msg = "Standard macro fluctuation within normal parameter expectations."
            
        sim_score = min(100.0, max(0.0, score + score_delta))
        
        return {
            "startup_name": startup_metrics.get("startup_name", "Unknown"),
            "shock_type_simulated": shock_type,
            "original_score": score,
            "simulated_score": round(sim_score, 2),
            "survivability_index": survivability,
            "vulnerability_rating": vulnerability,
            "operational_impact_summary": msg,
            "timestamp": now,
            "log": {
                "stage": "ECOSYSTEM_SIMULATION",
                "status": "SUCCESS",
                "message": f"Successfully simulated shock '{shock_type}' for {startup_metrics.get('startup_name')}",
                "timestamp": now
            }
        }
