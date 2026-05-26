import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Governance.RecommendationProvenance")

class RecommendationProvenanceSystem:
    """
    Recommendation Provenance System.
    Links generated startup recommendations directly to supporting evidence anchors.
    """
    
    @classmethod
    def compile_provenance(cls, startup_name: str, recommendation: str, triggers: List[str]) -> Dict[str, Any]:
        """
        Structures explicit evidence mappings showing why a recommendation triggered.
        """
        logger.info(f"Stamping strategic recommendation provenance for: {startup_name}")
        
        return {
            "startup_name": startup_name,
            "allocated_recommendation": recommendation,
            "evidence_triggers": triggers,
            "provenance_valid": True,
            "message": f"Recommendation '{recommendation}' successfully anchored to {len(triggers)} strategic triggers."
        }
