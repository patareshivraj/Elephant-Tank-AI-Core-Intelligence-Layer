import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Strategy.RecommendationEngine")

class RecommendationEngine:
    """
    Strategic Recommendation Engine.
    Generates and prioritizes startup-specific, actionable recommendations using
    deterministic scoring and ranking. Ensures critical founder/market risks are prioritized first.
    """
    
    @classmethod
    def classify_recommendation(cls, rec_text: str, risk_analysis: List[str], founder_weaknesses: List[str]) -> Dict[str, Any]:
        """
        Deterministically classifies a recommendation into a category and calculates its priority.
        """
        rec_lower = rec_text.lower()
        
        # Determine Category & Priority (Lower priority score = Higher urgency)
        if any(w in rec_lower for w in ["founder", "leadership", "co-founder", "management", "hire", "recruiting"]):
            category = "FOUNDER_RISK"
            priority = 1
        elif any(w in rec_lower for w in ["market", "competitor", "threat", "saturated", "defensibility", "pricing"]):
            category = "MARKET_THREAT"
            priority = 2
        elif any(w in rec_lower for w in ["blocker", "frictional", "legal", "compliance", "regulatory", " patent", " intellectual property"]):
            category = "EXECUTION_BLOCKER"
            priority = 3
        elif any(w in rec_lower for w in ["gtm", "marketing", "acquisition", "distribution", "channel", "sales"]):
            category = "GTM_WEAKNESS"
            priority = 4
        else:
            category = "OPTIMIZATION"
            priority = 5
            
        # Refine mitigation plan based on category
        mitigation = f"Engage dedicated domain advisors to resolve the observed {category.replace('_', ' ').lower()} immediately."
        if category == "FOUNDER_RISK":
            mitigation = "Establish clear founder vesting schedules, build an advisory board, and fill key leadership gaps."
        elif category == "MARKET_THREAT":
            mitigation = "Perform active customer discovery and build proprietary tech/IP for competitive defensibility."
        elif category == "EXECUTION_BLOCKER":
            mitigation = "Engage legal counsel to address compliance, secure patent/IP protections, or clear licensing friction."
        elif category == "GTM_WEAKNESS":
            mitigation = "Launch a micro-pilot target customer segment, iterate pricing structures, and optimize acquisition funnel."
            
        return {
            "title": rec_text.split(":")[0] if ":" in rec_text else f"Address {category.replace('_', ' ').title()}",
            "description": rec_text,
            "category": category,
            "priority_score": priority,
            "mitigation_action": mitigation
        }

    @classmethod
    def generate_recommendations(cls, evaluation_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Accepts the parsed evaluation response, extracts raw recommendations,
        and applies deterministic classification, ranking, and prioritization.
        """
        logger.info("Executing Strategic Recommendation Engine...")
        
        raw_recs = evaluation_response.get("recommendations", [])
        risk_list = evaluation_response.get("risk_analysis", {}).get("risks", [])
        founder_weaknesses = evaluation_response.get("founder_intelligence", {}).get("weaknesses", [])
        
        # Ensure we always have at least some default recommendations if none provided
        if not raw_recs:
            raw_recs = [
                "Founder Transition: Strengthen technical leadership team and clear role definitions.",
                "Market Strategy: Address severe competition by establishing deep technology defensibility.",
                "Regulatory Compliance: Mitigate execution risks by obtaining relevant regional compliance approvals.",
                "GTM Optimization: Restructure pilot program pricing to establish validation metrics."
            ]
            
        structured_recs = []
        for rec in raw_recs:
            classified = cls.classify_recommendation(rec, risk_list, founder_weaknesses)
            structured_recs.append(classified)
            
        # Sort deterministically: priority_score ascending (Priority 1 first), then by title alphabetically
        structured_recs.sort(key=lambda x: (x["priority_score"], x["title"]))
        
        logger.info(f"Successfully generated and sorted {len(structured_recs)} strategic recommendations.")
        return structured_recs
