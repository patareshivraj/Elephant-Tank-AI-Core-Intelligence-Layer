from typing import Dict, Tuple
from app.scoring.weights import STAGE_AWARE_WEIGHTS

class ScoringEngine:
    def compute_weighted_aggregate(self, raw_scores: Dict[str, float], stage: str) -> Tuple[float, Dict[str, float]]:
        """
        Receives raw qualitative scores (1-10) and applies deterministic stage-aware weights.
        Outputs a normalized score out of 100.
        """
        weights = STAGE_AWARE_WEIGHTS.get(stage, STAGE_AWARE_WEIGHTS["Default"])
        
        weighted_total = 0.0
        weighted_breakdown = {}
        
        for dimension, raw_value in raw_scores.items():
            # Standardize raw_value to prevent out-of-bounds math
            safe_val = max(1.0, min(10.0, float(raw_value)))
            weight = weights.get(dimension, 0.0)
            
            # Since raw is 1-10, raw * weight * 10 aligns to a 0-100 scale
            computed = safe_val * weight * 10
            weighted_breakdown[dimension] = round(computed, 2)
            weighted_total += computed
            
        return round(weighted_total, 2), weighted_breakdown
        
    def interpret_score(self, final_score: float) -> str:
        """
        Translates the final numerical venture score into strict categorical definitions.
        """
        if final_score < 31.0:
            return "High Risk / Weak Viability"
        elif final_score < 51.0:
            return "Early Potential / Significant Gaps"
        elif final_score < 71.0:
            return "Moderate Investment Potential"
        elif final_score < 86.0:
            return "Strong Startup Candidate"
        else:
            return "High-Potential Venture Opportunity"
