import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Governance.ExplainabilityEngine")

class ExplainabilityEngine:
    """
    Explainability Engine for Venture Intelligence.
    Justifies scores, maps confidence triggers, and translates decision parameters
    into deterministic, transparent institutional rationales.
    """
    
    @classmethod
    def explain_score(cls, startup_name: str, overall_score: float, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decomposes how a score was calculated from underlying parameters.
        """
        logger.info(f"Generating deterministic score explanation for startup: {startup_name}")
        
        # Deconstruct score mathematically
        tam_weight = 0.35
        moat_weight = 0.35
        traction_weight = 0.30
        
        tam_score = float(metrics.get("tam_score", 50))
        moat_score = float(metrics.get("moat_score", 50))
        traction_score = float(metrics.get("traction_score", 50))
        
        reconstructed = (tam_score * tam_weight) + (moat_score * moat_weight) + (traction_score * traction_weight)
        
        justification = (
            f"The overall score of {overall_score} for '{startup_name}' is driven by a market potential rating of "
            f"{tam_score} (35% weight), a competitive moat score of {moat_score} (35% weight), and execution traction "
            f"index of {traction_score} (30% weight)."
        )
        
        return {
            "startup_name": startup_name,
            "overall_score": overall_score,
            "reconstructed_score": round(reconstructed, 2),
            "mathematical_reconciliation_variance": round(abs(overall_score - reconstructed), 2),
            "weighted_contributions": {
                "market_potential_contribution": round(tam_score * tam_weight, 2),
                "competitive_moat_contribution": round(moat_score * moat_weight, 2),
                "execution_traction_contribution": round(traction_score * traction_weight, 2)
            },
            "interpretation_narrative": justification
        }
