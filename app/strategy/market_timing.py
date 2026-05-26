import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Strategy.MarketTiming")

class MarketTimingEngine:
    """
    Market Timing Analysis Engine.
    Evaluates category maturity, adoption curves, regulatory Windows, and macroeconomic readiness,
    mapping startups to TOO_EARLY, TOO_LATE_SATURATED, or WELL_TIMED.
    """
    
    @classmethod
    def analyze_timing(cls, startup_description: str) -> Dict[str, Any]:
        """
        Determines the market timing score, regulatory readiness, and overall timing category.
        """
        logger.info("Analyzing segment market timing alignment...")
        lower_desc = startup_description.lower()
        
        # Base indicators
        maturity = 5.0
        adoption = 6.0
        saturation = 4.0
        regulatory = 5.0
        
        # 1. Too Early Detections
        is_too_early = False
        if any(w in lower_desc for w in ["quantum mainframe", "fusion energy", "asteroid mining", "cold fusion", "neuro-link", "space elevator"]):
            is_too_early = True
            maturity = max(1.0, maturity - 3.5)
            adoption = max(1.5, adoption - 4.0)
            regulatory = max(1.5, regulatory - 2.5)
            
        # 2. Too Late / Saturated Detections
        is_too_late = False
        if any(w in lower_desc for w in ["food delivery app", "ride sharing", "drop shipping", "generic chatbot", "chat widget", "simple CRM"]):
            is_too_late = True
            maturity = min(10.0, maturity + 4.0)
            saturation = min(10.0, saturation + 4.5)
            
        # 3. Well-Timed Indicators
        is_well_timed = False
        if any(w in lower_desc for w in ["supply chain optimization", "fda-compliant", "distributed mainframe", "ehr automation", "B2B compliance"]):
            is_well_timed = True
            maturity = 6.0
            adoption = 7.5
            saturation = 3.0
            
        # Compute overall Timing Score Index
        # Lower saturation and higher maturity/adoption represents a well-timed market
        timing_index = round((maturity + adoption + (10.0 - saturation) + regulatory) / 4.0, 2)
        
        # Determine verdict
        if is_too_early or timing_index < 4.5:
            verdict = "TOO_EARLY"
            narrative = "The technology is highly innovative, but the market lacks necessary commercial adoption rails. Significant capital runway will be spent educating the customer base."
        elif is_too_late or saturation >= 7.5:
            verdict = "TOO_LATE_SATURATED"
            narrative = "High capital-intensity domain. Customer acquisition costs (CAC) are extremely inflated due to mature, capital-rich incumbents, making startup margins highly vulnerable."
        else:
            verdict = "WELL_TIMED"
            narrative = "Ideal entry window. High macro tailwinds and regulatory clarity are paired with commercial adoption readiness, minimizing initial channel friction."
            
        return {
            "timing_score": timing_index,
            "market_maturity_verdict": verdict,
            "category_maturity": "EMERGING" if is_too_early else ("MATURE" if is_too_late else "GROWTH_PHASE"),
            "adoption_readiness": "LOW" if is_too_early else ("HIGH" if is_too_late else "READY"),
            "saturation_risks": "CRITICAL" if is_too_late else ("NEGLIGIBLE" if is_too_early else "MODERATE"),
            "regulatory_timing_status": "HIGH_FRICTION" if is_too_early else "STABLE",
            "timing_diligence_narrative": narrative
        }
