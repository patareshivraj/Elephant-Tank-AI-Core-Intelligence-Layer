import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Intelligence.EvolutionAnalysis")

class StartupEvolutionAnalyzer:
    """
    Startup Evolution Analyzer.
    Analyzes multi-eval longitudinal patterns, scoring velocities,
    and identifies pivots or defensibility trajectory shifts.
    """
    
    @classmethod
    def analyze_evolution(cls, historical_runs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates score changes across historical runs to categorize evolution speed.
        """
        logger.info("Analyzing startup progression and strategic evolution index...")
        
        if not historical_runs or len(historical_runs) < 2:
            return {
                "evolution_status": "INSUFFICIENT_DATA",
                "score_delta": 0,
                "evolution_narrative": "Venture has only one registered evaluation snapshot. Continuous intelligence tracking requires at least two milestones."
            }
            
        # Chronological sort
        sorted_runs = sorted(historical_runs, key=lambda x: x["timestamp"])
        r_first = sorted_runs[0]
        r_last = sorted_runs[-1]
        
        score_delta = r_last["overall_score"] - r_first["overall_score"]
        
        # Categorization logic
        if score_delta >= 10:
            status = "RAPIDLY_SCALING"
            narrative = "Exceptional trajectory. The venture shows swift capability improvement, closing core execution gaps and strengthening its proprietary barrier."
        elif score_delta > 0:
            status = "STEADY_IMPROVEMENT"
            narrative = "Positive execution trajectory. Constant operational adjustments are converting risk areas into stable value milestones."
        elif score_delta >= -5:
            status = "STAGNATING"
            narrative = "Flatline velocity. Execution speed has stalled. Strategic pivots or capitalization boosts are required to unlock scaling opportunities."
        else:
            status = "DECLINING"
            narrative = "Severe operational decay. Core defensibility is eroding, or structural risk accumulation is outpacing technical progression."
            
        return {
            "evolution_status": status,
            "milestones_count": len(historical_runs),
            "score_trajectory": {
                "initial_score": r_first["overall_score"],
                "latest_score": r_last["overall_score"],
                "absolute_shift": score_delta
            },
            "evolution_narrative": narrative
        }
