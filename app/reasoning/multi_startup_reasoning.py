import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Reasoning.MultiStartupReasoning")

class MultiStartupReasoning:
    """
    Multi-Startup Comparative Reasoning Engine.
    Structures deterministic score matrices contrasting startups across defensibility,
    founder competence, timing, and scalability.
    """
    
    @classmethod
    def compare_multiple_startups(cls, startups_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates side-by-side matrices and outputs the clear top allocation targets.
        """
        logger.info(f"Comparing a batch of {len(startups_list)} startups side-by-side...")
        
        if not startups_list:
            return {
                "comparison_matrix": [],
                "primary_recommendation": None,
                "message": "No startups provided for comparative modeling."
            }
            
        matrix = []
        for st in startups_list:
            score = st.get("overall_score", 50)
            founder = st.get("founder_score", 5)
            timing = st.get("timing_verdict", "WELL_TIMED")
            
            # Attractiveness composite rating (0-100)
            attractiveness = round((score * 0.5) + (founder * 5.0) + (100.0 if timing == "WELL_TIMED" else 50.0) * 0.25, 2)
            
            matrix.append({
                "startup_name": st.get("startup_name", "Unknown"),
                "overall_score": score,
                "founder_score": founder,
                "timing": timing,
                "attractiveness_index": attractiveness
            })
            
        # Sort by attractiveness
        matrix.sort(key=lambda x: -x["attractiveness_index"])
        
        return {
            "comparison_matrix": matrix,
            "primary_recommendation": matrix[0]["startup_name"] if matrix else None,
            "rationale": f"Venture '{matrix[0]['startup_name']}' is prioritized due to its dominant attractiveness index of {matrix[0]['attractiveness_index']}." if matrix else ""
        }
