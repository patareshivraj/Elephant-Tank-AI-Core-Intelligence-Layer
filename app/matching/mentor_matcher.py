import logging
from typing import List, Dict, Any
from app.semantic.semantic_search import SemanticSearchEngine
from app.semantic.retrieval_confidence import RetrievalConfidenceEngine

logger = logging.getLogger("ElephantTank.Matching.MentorMatcher")

class MentorMatcherEngine:
    @staticmethod
    def match_mentors(startup_stage: str, startup_description: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves matching ecosystem mentors from the VectorDB index, computes deterministic compatibility scores,
        and provides highly explainable mentorship reasoning.
        """
        logger.info(f"Matching mentors for startup in stage '{startup_stage}'...")
        query_text = f"Stage compatibility: {startup_stage}. Specialization/Expertise: {startup_description}"
        
        candidates = SemanticSearchEngine.search_matching_mentors(query_text, limit=limit * 2)
        
        results = []
        for cand in candidates:
            meta = cand["metadata"]
            similarity = cand["similarity"]
            name = meta.get("name", "Unknown Mentor")
            
            confidence = RetrievalConfidenceEngine.calculate_mentor_match_confidence(
                startup_stage=startup_stage,
                startup_description=startup_description,
                mentor_metadata=meta,
                semantic_similarity=similarity
            )
            
            # Map industries from string back to list if serialized by Chroma
            import ast
            industries = meta.get("industries", [])
            if isinstance(industries, str):
                try:
                    industries = ast.literal_eval(industries)
                except Exception:
                    industries = []
                    
            specialization = meta.get("specialization", "")
            
            results.append({
                "mentor_name": name,
                "match_score": int(confidence["confidence_score"] * 10),  # Map to scale 0 - 100
                "match_level": confidence["match_level"],
                "specialization": specialization,
                "target_industries": industries,
                "reasoning": confidence["alignment_traces"]
            })
            
        # Deterministic sorting: Highest match_score first
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        return results[:limit]
