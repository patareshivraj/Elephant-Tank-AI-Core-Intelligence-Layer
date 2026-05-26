import logging
import os
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Strategy.MarketPositioning")

class MarketPositioningEngine:
    """
    Market Positioning Analysis Module.
    Evaluates market saturation, defensibility, timing, and differentiation.
    Uses a hybrid approach: local deterministic logic with optional LLM narrative enrichment.
    """
    
    @classmethod
    def analyze_positioning(cls, evaluation_response: Dict[str, Any], raw_description: str = "") -> Dict[str, Any]:
        """
        Runs the market positioning analysis using evaluation results and description context.
        """
        logger.info("Executing Market Positioning Analysis...")
        
        # 1. Deterministic Scores Extraction
        eval_results = evaluation_response.get("evaluation_results", {})
        mkt_score = eval_results.get("market_score", 5)
        inv_score = eval_results.get("innovation_score", 5)
        scl_score = eval_results.get("scalability_score", 5)
        
        desc_lower = raw_description.lower()
        
        # 2. Market Saturation Assessment
        if "wrapper" in desc_lower or "copycat" in desc_lower or "saturated" in desc_lower:
            saturation = "HIGH"
        elif mkt_score < 5:
            saturation = "HIGH"
        elif mkt_score < 8:
            saturation = "MEDIUM"
        else:
            saturation = "LOW"
            
        # 3. Defensibility Rating
        if inv_score > 7 and scl_score > 7:
            defensibility = "ROBUST"
        elif inv_score >= 5:
            defensibility = "MODERATE"
        else:
            defensibility = "VULNERABLE"
            
        # 4. Differentiation Index
        diff_index = float((inv_score * 0.6) + (scl_score * 0.4))
        
        # 5. Category Overlap Detection
        overlap_flags = []
        if "ai" in desc_lower or "llm" in desc_lower:
            overlap_flags.append("AI-SaaS Congestion: High overlap with commodity GPT wrappers.")
        if "delivery" in desc_lower or "e-commerce" in desc_lower:
            overlap_flags.append("Market Saturation: Extremely high customer acquisition costs.")
        if "crypto" in desc_lower or "web3" in desc_lower:
            overlap_flags.append("Regulatory Volatility: Potential regulatory headwinds.")
            
        if not overlap_flags:
            overlap_flags.append("Emergent Market Segment: Limited immediate category overlap observed.")
            
        # 6. Market Timing Fit
        if "trend" in desc_lower or "emerging" in desc_lower or inv_score > 8:
            timing = "IDEAL"
        elif inv_score > 5:
            timing = "FAVORABLE"
        else:
            timing = "MISMATCHED"
            
        # 7. Qualitative Narrative (LLM-enriched if possible, else deterministic fallback)
        narrative = f"The startup presents a {defensibility.lower()} market positioning in a segment marked by {saturation.lower()} market saturation. With a differentiation index of {diff_index}/10, defending margins will require continuous technological barrier building."
        
        # Try to enrich via Groq if API key is active
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            try:
                from app.llm.client import GroqReasoningClient
                client = GroqReasoningClient()
                prompt = (
                    "You are an elite venture partner analyzing a startup's market positioning. "
                    "Analyze competitive positioning, defensibility, and timing based on this description:\n"
                    f"Startup Pitch: {raw_description}\n"
                    f"Market Score: {mkt_score}, Innovation Score: {inv_score}\n"
                    "Return a JSON object with a single key 'competitive_narrative' containing a concise, 3-sentence institutional-grade market positioning summary."
                )
                messages = [{"role": "user", "content": prompt}]
                enrichment = client.execute_prompt(messages, mode="ANALYST_REPORT")
                if enrichment and "competitive_narrative" in enrichment:
                    narrative = enrichment["competitive_narrative"]
            except Exception as e:
                logger.warning(f"Failed to enrich positioning narrative via Groq: {e}. Falling back to deterministic narrative.")
                
        return {
            "market_saturation": saturation,
            "defensibility_rating": defensibility,
            "differentiation_index": diff_index,
            "competitive_positioning_narrative": narrative,
            "category_overlap_warning": overlap_flags,
            "market_timing_fit": timing
        }
