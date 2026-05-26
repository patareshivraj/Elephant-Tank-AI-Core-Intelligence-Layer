import logging
import os
import time
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Reporting.InstitutionalMemoEngine")

class InstitutionalMemoEngine:
    """
    Institutional VC Memo Engine.
    Constructs high-level investment memos resembling institutional venture due diligence
    reports rather than generic AI summaries.
    """
    
    @classmethod
    def generate_institutional_memo(
        cls, 
        synthesis_data: Dict[str, Any], 
        overall_score: int,
        moat_data: Dict[str, Any],
        timing_data: Dict[str, Any],
        trajectory_data: Dict[str, Any],
        scalability_data: Dict[str, Any],
        fit_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes raw metrics, strategic indexes, and narratives into an investor-grade VC memo.
        """
        logger.info("Compiling Institutional-Grade Venture Memo...")
        start_time = time.time()
        
        # Determine strict Institutional Recommendation
        if overall_score >= 80:
            recommendation = "OVERWEIGHT / CONVICTION BUY"
            rationale = "Exceptional moat durability paired with strong execution velocity indicators."
        elif overall_score >= 60:
            recommendation = "ALLOCATE WITH MILESTONES / ACCUMULATE"
            rationale = "Compelling core tech but execution metrics require strict capitalization gates."
        else:
            recommendation = "UNDERWEIGHT / AVOID ROUND"
            rationale = "Substantial structural friction, low moat durability, or market saturation threats."
            
        narrative_thesis = (
            f"We recommend an {recommendation} position. Our due diligence isolates a resolved revenue "
            f"baseline of {synthesis_data.get('resolved_revenue_baseline', '$150k')}. The venture operates in a "
            f"segment characterized as '{timing_data.get('market_maturity_verdict', 'IDEAL')}' timing-wise. "
            f"Moat profile is rated '{moat_data.get('moat_profile', 'STANDARD')}', showing a quantitative Moat Strength Index of "
            f"{moat_data.get('moat_index', 5.0)}/10.0."
        )
        
        market_narrative = (
            f"The segment demonstrates a category maturity of {timing_data.get('category_maturity')}. "
            f"Regulatory headwinds are {timing_data.get('regulatory_timing_status')}. Macro economic tailwinds "
            f"strongly support this entry, though customer switching frictions present intermediate friction."
        )
        
        scalability_narrative = (
            f"Venture scalability forecast yields a score of {scalability_data.get('scalability_index', 5.0)}/10.0. "
            f"Gross margin potential is modeled at {scalability_data.get('gross_margin_profile')}, with hiring complexity "
            f"noted as {scalability_data.get('hiring_leverage_complexity')}."
        )
        
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            try:
                from app.llm.client import GroqReasoningClient
                client = GroqReasoningClient()
                prompt = (
                    "You are a Senior General Partner at an elite institutional venture capital fund (e.g. Sequoia, Benchmark). "
                    "Draft a rigorous, professional 4-sentence Executive Investment Thesis for our General Partner Memo "
                    "using the following strategic vectors. Your tone must be analytical, objective, and deeply commercial:\n"
                    f"Overall Score: {overall_score}/100\n"
                    f"Recommendation: {recommendation} - {rationale}\n"
                    f"Resolved Revenue: {synthesis_data.get('resolved_revenue_baseline')}\n"
                    f"Moat Strength: {moat_data.get('moat_index')}/10.0 ({moat_data.get('moat_profile')})\n"
                    f"Scalability Index: {scalability_data.get('scalability_index')}/10.0\n"
                    f"Startup Narrative: {synthesis_data.get('synthesized_diligence_narrative')}\n"
                    "Return a JSON object containing a single key: 'institutional_thesis'."
                )
                messages = [{"role": "user", "content": prompt}]
                res = client.execute_prompt(messages, mode="EXEC_SUMMARY")
                if res and "institutional_thesis" in res:
                    narrative_thesis = res["institutional_thesis"]
            except Exception as e:
                logger.warning(f"Failed to enrich institutional memo narrative via Groq: {e}. Using deterministic layout.")
                
        elapsed_time = time.time() - start_time
        logger.info(f"Institutional memo generation completed in {elapsed_time:.3f}s.")
        
        return {
            "institutional_recommendation": recommendation,
            "recommendation_rationale": rationale,
            "executive_investment_thesis": narrative_thesis,
            "market_opportunity_outlook": market_narrative,
            "moat_durability_assessment": moat_data.get("moat_diligence_narrative", ""),
            "scalability_forecasting_model": scalability_narrative,
            "founder_investor_fit_analysis": fit_data.get("fit_narrative", ""),
            "trajectory_survivability_verdict": trajectory_data.get("survivability_narrative", ""),
            "execution_log": {
                "stage": "LONG_CONTEXT_REASONING",
                "status": "SUCCESS",
                "message": f"Compiled master institutional VC investment memo for score {overall_score}.",
                "timestamp": int(time.time())
            }
        }
