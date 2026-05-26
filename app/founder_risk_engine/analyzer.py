import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.FounderRiskEngine")

class FounderRiskAnalyzer:
    """
    Identifies deterministic operational and team-composition risks.
    """
    def analyze_risks(self, startup_context: Dict[str, Any], founder_scores: Dict[str, int]) -> List[str]:
        logger.info("Analyzing Founder Execution Risks...")
        risk_flags = []
        
        # 1. Solo Founder Risk
        if startup_context.get("founder_count", 1) == 1:
            risk_flags.append("Single-founder dependency risk. Operational bandwidth is severely limited.")
            
        # 2. Technical Missing Link
        is_tech_product = startup_context.get("is_software_or_hardware", True)
        if is_tech_product and founder_scores.get("technical_capability_score", 0) < 40:
            risk_flags.append("Critical Skill Gap: High-tech product being built without in-house technical leadership.")
            
        # 3. Domain Mismatch
        if founder_scores.get("domain_expertise_score", 0) < 30:
            risk_flags.append("Domain Misalignment: Founders lack direct operational history in the target sector.")
            
        return risk_flags
