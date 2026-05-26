import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Strategy.WeaknessPrioritizer")

class WeaknessPrioritizer:
    """
    Deterministic Weakness Prioritizer.
    Ranks startup weaknesses by strict business urgency, identifying existential threats,
    GTM blockers, founder execution risks, and scalability bottlenecks.
    """
    
    DOMAIN_WEIGHTS = {
        "FOUNDER_RISK": 95,
        "EXISTENTIAL_THREAT": 85,
        "GTM_BLOCKER": 70,
        "SCALABILITY_BOTTLENECK": 55,
        "STANDARD_OPTIMIZATION": 30
    }
    
    @classmethod
    def classify_weakness(cls, text: str) -> Dict[str, Any]:
        """
        Classifies a raw weakness text into one of the 5 domains based on semantic keywords.
        """
        lower = text.lower()
        
        # Founder risk matches
        if any(w in lower for w in ["founder", "solo", "technical capability", "leadership", "key man"]):
            domain = "FOUNDER_RISK"
            explanation = "Direct risk to execution capacity due to founder talent gaps or dependency."
        # Existential threats matches
        elif any(w in lower for w in ["runway", "burn rate", "capital", "cash", "regulatory", "fda", "legal"]):
            domain = "EXISTENTIAL_THREAT"
            explanation = "Existential threat capable of causing startup death within 6-12 months."
        # GTM Blockers matches
        elif any(w in lower for w in ["gtm", "cac", "marketing", "sales", "channel", "acquisition", "saturation"]):
            domain = "GTM_BLOCKER"
            explanation = "Blocker impeding initial customer acquisition or commercial scalability."
        # Scalability bottleneck matches
        elif any(w in lower for w in ["scaling", "infrastructure", "manual", "database", "ops", "margin"]):
            domain = "SCALABILITY_BOTTLENECK"
            explanation = "Bottleneck capping long-term operating leverage and margin expansion."
        else:
            domain = "STANDARD_OPTIMIZATION"
            explanation = "Standard operational optimization to improve efficiency."
            
        return {
            "weakness_description": text,
            "classified_domain": domain,
            "priority_score": cls.DOMAIN_WEIGHTS[domain],
            "urgency_rating": "CRITICAL" if cls.DOMAIN_WEIGHTS[domain] >= 80 else ("HIGH" if cls.DOMAIN_WEIGHTS[domain] >= 55 else "MEDIUM"),
            "impact_explanation": explanation
        }

    @classmethod
    def prioritize_weaknesses(cls, raw_weaknesses: List[str]) -> List[Dict[str, Any]]:
        """
        Prioritizes a list of weaknesses using our deterministic domain-urgency scoring.
        """
        logger.info(f"Prioritizing {len(raw_weaknesses)} startup weaknesses...")
        classified_list = []
        for rw in raw_weaknesses:
            if rw.strip():
                classified_list.append(cls.classify_weakness(rw.strip()))
                
        # Sort descending by priority_score
        prioritized = sorted(classified_list, key=lambda x: x["priority_score"], reverse=True)
        logger.info("Weakness prioritization complete.")
        return prioritized
