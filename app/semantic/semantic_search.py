import logging
from typing import List, Dict, Any, Optional
from app.semantic.vector_store import VectorStore
from app.semantic.index_manager import IndexManager

logger = logging.getLogger("ElephantTank.Semantic.SemanticSearch")

class SemanticSearchEngine:
    @classmethod
    def search_similar_startups(cls, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves other startups from VectorDB that are semantically similar.
        """
        logger.info(f"Performing startup similarity search for: '{query_text[:60]}...'")
        return VectorStore.search_similarity("startups", query_text, limit=limit)

    @classmethod
    def search_matching_investors(
        cls, 
        query_text: str, 
        limit: int = 5, 
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves matching investors.
        """
        logger.info(f"Performing investor matching vector search...")
        IndexManager.seed_ecosystem_if_empty()
        return VectorStore.search_similarity("investors", query_text, limit=limit, where_metadata=filter_metadata)

    @classmethod
    def search_matching_mentors(
        cls, 
        query_text: str, 
        limit: int = 5, 
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves matching mentors.
        """
        logger.info(f"Performing mentor matching vector search...")
        IndexManager.seed_ecosystem_if_empty()
        return VectorStore.search_similarity("mentors", query_text, limit=limit, where_metadata=filter_metadata)
