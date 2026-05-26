import logging
import os
from typing import Dict, Any, List
from app.semantic.vector_store import VectorStore

logger = logging.getLogger("ElephantTank.Strategy.EcosystemOpportunity")

class EcosystemOpportunityEngine:
    """
    Ecosystem Opportunity Engine.
    Identifies strategic ecosystem opportunities, underserved markets, and
    adjacent business expansion vectors.
    """
    
    @classmethod
    def analyze_opportunities(cls, evaluation_response: Dict[str, Any], raw_description: str = "") -> Dict[str, Any]:
        """
        Calculates adjacent market opportunities and maps out expansion paths
        leveraging vector database similarity when available.
        """
        logger.info("Executing Ecosystem Opportunity Analysis...")
        
        # 1. Semantic Proximity Analysis (retrieved from Vector DB startups)
        adjacent_peers = []
        try:
            hits = VectorStore.search_similarity("startups", raw_description or "technology venture", limit=3)
            for hit in hits:
                meta = hit.get("metadata", {})
                if meta and meta.get("startup_name"):
                    adjacent_peers.append(meta["startup_name"])
        except Exception as e:
            logger.warning(f"Vector search bypassed or failed during opportunity analysis: {e}")
            
        desc_lower = raw_description.lower()
        
        # 2. Underserved Market Identification
        underserved = "Niche workflow automation for underserved mid-market enterprise teams."
        if "health" in desc_lower:
            underserved = "Unlocking FDA clinical data pipelines and legacy EHR vendor integrations."
        elif "finance" in desc_lower or "pay" in desc_lower:
            underserved = "Cross-border compliance orchestration and low-fee transaction routing."
        elif "ai" in desc_lower or "model" in desc_lower:
            underserved = "Private on-premise model execution with zero-retention data privacy guarantees."
            
        # 3. Adjacent Market Possibilities
        adjacent_markets = ["Direct API licensing", "White-label integration modules"]
        if "health" in desc_lower:
            adjacent_markets = ["Clinical trial participant tracking", "Pharma research metadata monetization"]
        elif "finance" in desc_lower:
            adjacent_markets = ["Fraud detection intelligence", "Automated bookkeeping reconciliations"]
        elif "ai" in desc_lower:
            adjacent_markets = ["Explainable AI auditing layers", "Synthetic training dataset production"]
            
        # 4. Expansion Paths
        expansion_paths = [
            "Vertical integration: Deepen integration with active industry platforms.",
            "Developer API: Release self-serve API endpoints to capture platform ecosystem billing."
        ]
        
        # 5. Strategic Recommendation
        api_key = os.environ.get("GROQ_API_KEY")
        strategic_narrative = (
            f"The venture is uniquely positioned to target the underserved area of '{underserved}'. "
            "Leveraging adjacent markets like B2B integration APIs will provide significant leverage."
        )
        
        if api_key:
            try:
                from app.llm.client import GroqReasoningClient
                client = GroqReasoningClient()
                prompt = (
                    "You are an elite venture strategist. "
                    "Based on this startup's pitch: \n"
                    f"{raw_description}\n"
                    "Provide a highly specific, 2-sentence VC-grade strategic ecosystem opportunity recommendation "
                    "focusing on underserved markets and long-term expansion paths. Return JSON with 'strategic_narrative'."
                )
                messages = [{"role": "user", "content": prompt}]
                enrichment = client.execute_prompt(messages, mode="ANALYST_REPORT")
                if enrichment and "strategic_narrative" in enrichment:
                    strategic_narrative = enrichment["strategic_narrative"]
            except Exception as e:
                logger.warning(f"Failed to enrich ecosystem opportunities via Groq: {e}")
                
        return {
            "underserved_market_opportunity": underserved,
            "adjacent_market_possibilities": adjacent_markets,
            "strategic_expansion_paths": expansion_paths,
            "adjacent_peers_detected": adjacent_peers,
            "strategic_opportunity_summary": strategic_narrative
        }
