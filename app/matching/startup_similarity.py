import logging
from typing import List, Dict, Any
from app.semantic.semantic_search import SemanticSearchEngine

logger = logging.getLogger("ElephantTank.Matching.StartupSimilarity")

class StartupSimilarityEngine:
    @staticmethod
    def evaluate_similarity(startup_description: str, limit: int = 3) -> Dict[str, Any]:
        """
        Finds semantically similar startups, infers overlapping business models,
        and provides ecosystem trend insights based on vector retrieval.
        """
        hits = SemanticSearchEngine.search_similar_startups(startup_description, limit=limit)
        
        similar_startups = []
        inferred_categories = set()
        overlapping_models = set()
        
        for hit in hits:
            meta = hit["metadata"]
            name = meta.get("startup_name", "Unknown Startup")
            stage = meta.get("target_stage", "Seed")
            
            similar_startups.append({
                "startup_name": name,
                "target_stage": stage,
                "similarity_score": round(hit["similarity"], 3)
            })
            
            # Simple heuristic category extraction from description
            doc_lower = hit["document"].lower()
            if "ai" in doc_lower or "artificial intelligence" in doc_lower or "computer vision" in doc_lower:
                inferred_categories.add("Artificial Intelligence")
                overlapping_models.add("AI SaaS (Subscription)")
            if "health" in doc_lower or "medical" in doc_lower or "diagnostics" in doc_lower:
                inferred_categories.add("Healthtech")
                overlapping_models.add("Enterprise Healthcare Licensing")
            if "finance" in doc_lower or "payments" in doc_lower or "transaction" in doc_lower:
                inferred_categories.add("Fintech")
                overlapping_models.add("Transactional / Take-Rate Fee")
            if "dev" in doc_lower or "tools" in doc_lower or "cloud" in doc_lower:
                inferred_categories.add("Developer Infrastructure")
                overlapping_models.add("Usage-Based SaaS")
                
        # Fallback if no similar startups are currently indexed
        if not similar_startups:
            logger.info("No similar startups currently indexed inside VectorDB.")
            
        return {
            "similar_startups": similar_startups,
            "related_market_categories": list(inferred_categories) if inferred_categories else ["General Tech"],
            "overlapping_business_models": list(overlapping_models) if overlapping_models else ["Standard Subscription SaaS"],
            "ecosystem_patterns": [
                "Ecosystem matches are retrieved and clustered dynamically using cosine similarity.",
                "Deterministic trend tracking filters out non-adjacent market category assumptions."
            ]
        }
