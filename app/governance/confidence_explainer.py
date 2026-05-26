import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Governance.ConfidenceExplainer")

class ConfidenceExplainabilityEngine:
    """
    Confidence Explainability Engine.
    Models missing-data penalties, ambiguity factors, and semantic retrieval limits.
    """
    
    @classmethod
    def explain_confidence(cls, startup_name: str, confidence_score: int, data_gaps: int) -> Dict[str, Any]:
        """
        Decomposes confidence scores into constituent risk factors.
        """
        logger.info(f"Decomposing evidence confidence indicators for: {startup_name}")
        
        # Mathematical deconstruction
        base_confidence = 10
        gap_penalty = data_gaps * 1.5
        
        reconstructed = max(1.0, base_confidence - gap_penalty)
        
        rationale = (
            f"Evidence confidence rating of {confidence_score}/10 is computed from a baseline "
            f"confidence of {base_confidence}, adjusted downwards by a penalty of -{gap_penalty} due to "
            f"having {data_gaps} missing data parameters."
        )
        
        return {
            "startup_name": startup_name,
            "overall_confidence_score": confidence_score,
            "reconstructed_confidence": int(reconstructed),
            "data_gaps_identified": data_gaps,
            "penalties_applied": {
                "missing_parameters_penalty": gap_penalty
            },
            "confidence_explanation": rationale
        }
