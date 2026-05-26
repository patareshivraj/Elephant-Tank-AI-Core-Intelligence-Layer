import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Workflow.StartupPrioritizer")

class StartupPrioritizer:
    """
    Startup Priority Engine.
    Deterministically ranks startups based on core metrics, growth velocities,
    founder capability ratings, and category timing alignments.
    """
    
    @classmethod
    def calculate_priority_score(cls, startup_metrics: Dict[str, Any]) -> float:
        """
        Calculates a composite priority index score (0-100).
        """
        score = float(startup_metrics.get("overall_score", 50))
        trajectory = float(startup_metrics.get("trajectory_score", 50))
        founder = float(startup_metrics.get("founder_score", 5)) * 10.0  # Scale 1-10 to 10-100
        
        # Timing weight
        timing_str = startup_metrics.get("timing_verdict", "WELL_TIMED").upper()
        if timing_str == "WELL_TIMED":
            timing = 95.0
        elif timing_str == "TOO_EARLY":
            timing = 60.0
        else:  # TOO_LATE_SATURATED
            timing = 30.0
            
        # Weighted sum: 40% Score, 20% Trajectory, 20% Founder, 20% Timing
        priority = (score * 0.40) + (trajectory * 0.20) + (founder * 0.20) + (timing * 0.20)
        return round(priority, 2)

    @classmethod
    def prioritize_pipeline(cls, startups_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranks a batch list of startups in descending order of prioritized index.
        """
        logger.info(f"Prioritizing batch list containing {len(startups_list)} startups...")
        
        ranked_startups = []
        for st in startups_list:
            priority_index = cls.calculate_priority_score(st)
            
            # Map explanation
            explanation = (
                f"Composite Priority Index of {priority_index}/100 computed as: "
                f"40% Overall Score ({st.get('overall_score', 50)}), "
                f"20% Trajectory ({st.get('trajectory_score', 50)}), "
                f"20% Founder Rating ({st.get('founder_score', 5)}/10), "
                f"20% Segment Timing ({st.get('timing_verdict', 'WELL_TIMED')})."
            )
            
            ranked_startups.append({
                "startup_name": st.get("startup_name", "Unknown"),
                "priority_score": priority_index,
                "overall_score": st.get("overall_score", 50),
                "explanation": explanation
            })
            
        # Sort deterministically
        ranked_startups.sort(key=lambda x: (-x["priority_score"], x["startup_name"].lower()))
        return ranked_startups
