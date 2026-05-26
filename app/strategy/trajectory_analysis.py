import logging
import time
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Strategy.TrajectoryAnalysis")

class TrajectoryAnalysisEngine:
    """
    Startup Trajectory Analyzer.
    Projects operational velocity, scaling readiness, capital progression benchmarks,
    and returns a confidence-aware survivability index.
    """
    
    @classmethod
    def analyze_trajectory(cls, overall_score: int, founder_readiness: str, moat_index: float) -> Dict[str, Any]:
        """
        Estimates the startup trajectory indicators.
        """
        logger.info("Computing startup operational execution trajectory...")
        
        # 1. Compute Survivability Index
        # A combination of overall evaluation score and competitive defensibility
        base_survival = (float(overall_score) * 0.7) + (moat_index * 3.0)
        survivability_score = round(min(10.0, max(1.0, base_survival / 10.0)), 2)
        
        # 2. Funding Progression Readiness
        if overall_score >= 80:
            progression = "SERIES_A_ACCELERATED"
            scaling_complexity = "HIGH_GROWTH"
            narrative = "High operational trajectory. The venture shows robust readiness for large-scale institutional series rounds, needing only standard GTM capitalization."
        elif overall_score >= 60:
            progression = "SEED_STAGE_READY"
            scaling_complexity = "MANAGEABLE_RISK"
            narrative = "Stable execution runway. Core technology has reached initial readiness, but securing seed capital requires locking in more defensive IP assets."
        else:
            progression = "PRE_SEED_STRENGTHENING"
            scaling_complexity = "HIGH_FRICTION"
            narrative = "Vulnerable trajectory. High threat of early failure. Immediate operational focus should shift to founder restructuring and product validation before seeking VC backing."
            
        return {
            "survivability_index": survivability_score,
            "funding_progression_readiness": progression,
            "scaling_complexity": scaling_complexity,
            "operational_maturity_level": "ADVANCED" if survivability_score >= 7.5 else ("STABLE" if survivability_score >= 5.0 else "INITIAL"),
            "survivability_narrative": narrative,
            "confidence_bounds": {
                "upper_bound": min(10.0, survivability_score + 1.2),
                "lower_bound": max(1.0, survivability_score - 1.5)
            }
        }
