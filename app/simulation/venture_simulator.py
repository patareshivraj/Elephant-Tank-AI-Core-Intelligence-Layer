import time
import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Simulation.VentureSimulator")

class VentureSimulator:
    """
    Venture Scenario Simulation Engine.
    Simulates startup trajectory paths under dynamic bull, base, and bear scenarios.
    """
    
    @classmethod
    def run_scenario_simulation(cls, startup_metrics: Dict[str, Any], scenario: str = "BASE_CASE") -> Dict[str, Any]:
        """
        Executes a deterministic simulation run on a startup's operational metrics.
        """
        logger.info(f"Simulating scenario '{scenario}' for startup: {startup_metrics.get('startup_name')}")
        
        score = float(startup_metrics.get("overall_score", 50))
        founder = float(startup_metrics.get("founder_score", 5))
        now = int(time.time())
        
        scenario = scenario.upper().strip()
        
        if scenario == "BULL_CASE":
            score_multiplier = 1.15
            founder_velocity = +1.0
            gtm_index = 90
            narrative = "Exceptional GTM acceleration, strong execution, and rapid valuation expansion."
        elif scenario == "BEAR_CASE":
            score_multiplier = 0.75
            founder_velocity = -1.5
            gtm_index = 40
            narrative = "Regulatory blocks, market headwinds, and execution slowdown drag on capitalization."
        else:  # BASE_CASE
            score_multiplier = 1.00
            founder_velocity = 0.0
            gtm_index = 70
            narrative = "Steady milestone attainment aligned with default growth forecasts."
            
        simulated_score = min(100.0, max(0.0, score * score_multiplier))
        simulated_founder = min(10.0, max(1.0, founder + founder_velocity))
        
        # Scaling Probability index based on GTM index and final simulated score
        scaling_prob = round((simulated_score * 0.7) + (gtm_index * 0.3), 2)
        
        return {
            "startup_name": startup_metrics.get("startup_name", "Unknown"),
            "target_scenario": scenario,
            "simulated_overall_score": round(simulated_score, 2),
            "simulated_founder_score": round(simulated_founder, 2),
            "scaling_probability": scaling_prob,
            "gtm_readiness_index": gtm_index,
            "simulation_narrative": narrative,
            "timestamp": now,
            "log": {
                "stage": "ECOSYSTEM_SIMULATION",
                "status": "SUCCESS",
                "message": f"Successfully simulated scenario '{scenario}' for {startup_metrics.get('startup_name')}",
                "timestamp": now
            }
        }
