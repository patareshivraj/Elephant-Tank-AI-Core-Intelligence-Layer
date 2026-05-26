import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Strategy.MoatIntelligence")

class MoatIntelligenceEngine:
    """
    Competitive Moat Intelligence Engine.
    Analyzes proprietary defensibility, switching costs, data advantages, network effects,
    and penalizes shallow AI GPT wrappers while prioritizing deep engineering architecture.
    """
    
    @classmethod
    def analyze_moat(cls, startup_description: str, innovation_score: int) -> Dict[str, Any]:
        """
        Computes a comprehensive moat profile and defensibility rating.
        """
        logger.info("Analyzing startup competitive moat profile...")
        lower_desc = startup_description.lower()
        
        # 1. Base Scores derived from historical Innovation Score
        tech_diff = min(10.0, float(innovation_score))
        switching_costs = 5.0
        network_effects = 4.0
        data_advantages = 5.0
        
        # 2. Check for Shallow Wrapper Penalties
        is_wrapper = False
        if any(w in lower_desc for w in ["gpt wrapper", "chatgpt wrapper", "api proxy", "simple ui", "wrapper for"]):
            is_wrapper = True
            tech_diff = max(1.5, tech_diff - 4.5)
            switching_costs = max(1.0, switching_costs - 3.0)
            data_advantages = max(1.5, data_advantages - 2.5)
            
        # 3. Check for Deep Tech / High Defensibility Bonuses
        is_deep_tech = False
        if any(w in lower_desc for w in ["quantum", "proprietary algorithm", "custom silicon", "patented", "fda-compliant", "distributed mainframe", "microservice database"]):
            is_deep_tech = True
            tech_diff = min(10.0, tech_diff + 2.5)
            switching_costs = min(10.0, switching_costs + 3.0)
            data_advantages = min(10.0, data_advantages + 3.0)
            network_effects = min(10.0, network_effects + 1.5)
            
        # 4. Compute overall indices
        moat_index = round((tech_diff + switching_costs + network_effects + data_advantages) / 4.0, 2)
        
        # Profile classification
        if is_wrapper or moat_index < 4.0:
            profile = "NO_MOAT_WRAPPER"
            narrative = "High commoditization risk. The venture lacks structural barriers, relying heavily on third-party APIs with low switching costs, exposing it to direct competitor clones."
        elif is_deep_tech or moat_index >= 7.5:
            profile = "WIDE_MOAT"
            narrative = "Strong proprietary defensibility. Deep architectural differentiation, high customer integration friction, and strong data feedback loops protect margins."
        else:
            profile = "NARROW_MOAT"
            narrative = "Standard competitive defensibility. Moderate switching costs exist, but the long-term barrier relies heavily on execution speed rather than structural patents."
            
        return {
            "moat_index": moat_index,
            "moat_profile": profile,
            "technical_differentiation": tech_diff,
            "switching_costs": switching_costs,
            "network_effects": network_effects,
            "data_advantages": data_advantages,
            "moat_diligence_narrative": narrative,
            "is_commodity_wrapper": is_wrapper,
            "is_deep_infrastructure": is_deep_tech
        }
