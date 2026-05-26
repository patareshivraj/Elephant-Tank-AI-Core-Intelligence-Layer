import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Intelligence.ComparativeAnalysis")

class ComparativeStartupIntelligence:
    """
    Comparative Startup Intelligence Engine.
    Coordinates deterministic, side-by-side matrices contrasting startup scores,
    scalability parameters, competitive moats, and founder strengths.
    """
    
    @classmethod
    def compare_startups(cls, startup_a_data: Dict[str, Any], startup_b_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs detailed side-by-side evaluation parameters.
        """
        logger.info(f"Contrasting '{startup_a_data.get('startup_name')}' vs '{startup_b_data.get('startup_name')}'...")
        
        name_a = startup_a_data.get("startup_name", "Venture A")
        name_b = startup_b_data.get("startup_name", "Venture B")
        
        score_a = startup_a_data.get("overall_score", 50)
        score_b = startup_b_data.get("overall_score", 50)
        
        score_delta = score_b - score_a
        winner = name_b if score_delta > 0 else (name_a if score_delta < 0 else "Draw")
        
        # Contrast core categories
        comparison_matrix = {
            "overall_scores": {name_a: score_a, name_b: score_b, "delta": abs(score_delta)},
            "innovation_indexes": {
                name_a: startup_a_data.get("innovation_score", 5),
                name_b: startup_b_data.get("innovation_score", 5)
            },
            "market_potentials": {
                name_a: startup_a_data.get("market_score", 5),
                name_b: startup_b_data.get("market_score", 5)
            },
            "scalability_parameters": {
                name_a: startup_a_data.get("scalability_score", 5),
                name_b: startup_b_data.get("scalability_score", 5)
            }
        }
        
        return {
            "comparison_parties": [name_a, name_b],
            "comparison_matrix": comparison_matrix,
            "relative_performance_verdict": f"The comparison yields {winner} as the stronger venture based on deterministic Python scoring metrics."
        }
