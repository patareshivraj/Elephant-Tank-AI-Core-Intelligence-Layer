import logging
from app.embeddings.generator import EmbeddingGenerator
from app.vector_store.chroma_client import ChromaDBManager
from app.retrieval.hybrid_search import HybridRetriever
from app.ranking.similarity import SimilarityRanker

logger = logging.getLogger("ElephantTank.InvestorMatching")

class InvestorMatcher:
    def __init__(self):
        self.embedding_engine = EmbeddingGenerator()
        self.db = ChromaDBManager()
        self.retriever = HybridRetriever()
        self.ranker = SimilarityRanker()
        self.investor_collection = self.db.get_collection("investors")

    def find_matching_investors(self, startup_summary_text: str, stage: str, sector: str) -> list:
        """
        1. Encodes the startup's narrative into a vector.
        2. Queries the investor database, strictly filtering for stage and sector.
        3. Ranks and returns highly relevant VCs.
        """
        logger.info(f"Generating semantic embedding for Startup Investor Match...")
        query_vector = self.embedding_engine.generate_embedding(startup_summary_text)
        
        # Hard filtering prevents matching a Seed startup with a Series C growth fund
        strict_filters = {
            "preferred_stage": stage,
            "target_sector": sector
        }
        
        logger.info("Executing Hybrid Retrieval against ChromaDB...")
        raw_results = self.retriever.search(
            collection=self.investor_collection,
            query_vector=query_vector,
            metadata_filters=strict_filters,
            top_k=10
        )
        
        # Only return matches > 0.70 similarity
        ranked_matches = self.ranker.rank_and_filter(raw_results, similarity_threshold=0.70)
        
        logger.info(f"Retrieved {len(ranked_matches)} valid deterministic investor matches.")
        return ranked_matches
