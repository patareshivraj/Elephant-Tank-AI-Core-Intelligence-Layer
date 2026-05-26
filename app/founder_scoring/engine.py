import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.FounderScoring")

class FounderScoringEngine:
    """
    Calculates deterministic founder scores. 
    Bans psychological inference; relies entirely on explicit data presence.
    """
    
    def calculate_scores(self, raw_founder_data: Dict[str, Any]) -> Dict[str, int]:
        logger.info("Calculating Founder Capability Scores...")
        
        # Base scoring structure
        scores = {
            "leadership_score": 50,
            "technical_capability_score": 50,
            "execution_readiness_score": 50,
            "startup_experience_score": 0,
            "domain_expertise_score": 50
        }
        
        # Calculate Startup Experience
        exits = raw_founder_data.get("prior_exits", 0)
        startups_founded = raw_founder_data.get("prior_startups", 0)
        
        if exits > 0:
            scores["startup_experience_score"] = min(100, 80 + (exits * 10))
        elif startups_founded > 0:
            scores["startup_experience_score"] = min(80, 50 + (startups_founded * 10))
            
        # Calculate Technical Capability
        is_technical = raw_founder_data.get("is_technical", False)
        years_tech = raw_founder_data.get("years_technical_experience", 0)
        
        if is_technical:
            scores["technical_capability_score"] = min(100, 60 + (years_tech * 5))
        else:
            scores["technical_capability_score"] = 0
            
        return scores
