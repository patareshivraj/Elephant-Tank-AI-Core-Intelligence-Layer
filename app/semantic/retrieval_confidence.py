import logging
from typing import List, Dict, Any

logger = logging.getLogger("ElephantTank.Semantic.RetrievalConfidence")

class RetrievalConfidenceEngine:
    @staticmethod
    def calculate_investor_match_confidence(
        startup_stage: str,
        startup_description: str,
        investor_metadata: Dict[str, Any],
        semantic_similarity: float
    ) -> Dict[str, Any]:
        """
        Calculates a deterministic matching confidence score (0 to 10) between 
        a startup and an investor based on semantic alignment and business criteria.
        """
        score = semantic_similarity * 6.0  # Base similarity contributes up to 6 points
        reasons = []
        
        # 1. Stage Compatibility Check
        ideal_stage = investor_metadata.get("ideal_stage", "")
        stages_supported = investor_metadata.get("stages", [])
        if isinstance(stages_supported, str):
            # Parse back stringified list if stringified by ChromaDB
            import ast
            try:
                stages_supported = ast.literal_eval(stages_supported)
            except Exception:
                stages_supported = []
                
        if startup_stage.lower() == ideal_stage.lower():
            score += 2.0
            reasons.append("Perfect investment stage compatibility (Ideal Stage).")
        elif any(startup_stage.lower() == s.lower() for s in stages_supported):
            score += 1.0
            reasons.append("Target stage falls within investor's active investment lifecycle.")
        else:
            score -= 2.0
            reasons.append("Warning: Stage mismatch. Investor typically targets different developmental maturity.")
            
        # 2. Industry Overlap Check
        industries = investor_metadata.get("industries", [])
        if isinstance(industries, str):
            import ast
            try:
                industries = ast.literal_eval(industries)
            except Exception:
                industries = []
                
        overlap_count = 0
        desc_lower = startup_description.lower()
        for ind in industries:
            if ind.lower() in desc_lower:
                overlap_count += 1
                
        if overlap_count > 0:
            bonus = min(2.0, overlap_count * 1.0)
            score += bonus
            reasons.append(f"Strong industry overlap detected in sector tags: {', '.join(industries)}.")
        else:
            score -= 1.0
            reasons.append("Warning: Limited direct semantic alignment with investor's primary sector tags.")
            
        # Bound score between 1 and 10
        final_score = round(max(1.0, min(10.0, score)), 1)
        
        return {
            "confidence_score": final_score,
            "match_level": "HIGH" if final_score >= 7.5 else ("MEDIUM" if final_score >= 5.0 else "LOW"),
            "alignment_traces": reasons
        }

    @staticmethod
    def calculate_mentor_match_confidence(
        startup_stage: str,
        startup_description: str,
        mentor_metadata: Dict[str, Any],
        semantic_similarity: float
    ) -> Dict[str, Any]:
        """
        Calculates a deterministic matching confidence score (0 to 10) between 
        a startup and a mentor based on semantic alignment and business criteria.
        """
        score = semantic_similarity * 6.0  # Base similarity contributes up to 6 points
        reasons = []
        
        # 1. Stage Compatibility
        stages_supported = mentor_metadata.get("compatible_stages", [])
        if isinstance(stages_supported, str):
            import ast
            try:
                stages_supported = ast.literal_eval(stages_supported)
            except Exception:
                stages_supported = []
                
        if any(startup_stage.lower() == s.lower() for s in stages_supported):
            score += 2.0
            reasons.append("Mentor provides dedicated advisory for this developmental stage.")
        else:
            score -= 1.0
            reasons.append("Warning: Potential stage-fit friction for mentor expertise.")
            
        # 2. Industry Overlap
        industries = mentor_metadata.get("industries", [])
        if isinstance(industries, str):
            import ast
            try:
                industries = ast.literal_eval(industries)
            except Exception:
                industries = []
                
        overlap_count = 0
        desc_lower = startup_description.lower()
        for ind in industries:
            if ind.lower() in desc_lower:
                overlap_count += 1
                
        if overlap_count > 0:
            score += 2.0
            reasons.append("Domain expertise perfectly mirrors startup market landscape.")
        else:
            score -= 1.0
            reasons.append("Warning: Limited direct domain alignment with mentor's standard sector tags.")
            
        final_score = round(max(1.0, min(10.0, score)), 1)
        
        return {
            "confidence_score": final_score,
            "match_level": "HIGH" if final_score >= 7.5 else ("MEDIUM" if final_score >= 5.0 else "LOW"),
            "alignment_traces": reasons
        }
