import logging
import os
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Reporting.InvestmentMemo")

class InvestmentMemoEngine:
    """
    Investment Memo Generation Engine.
    Exclusively emulates elite venture analyst reasoning to produce institutional-style investment memos.
    """
    
    @classmethod
    def generate_investment_memo(
        cls, 
        evaluation_response: Dict[str, Any], 
        raw_description: str = "",
        raw_founder_data: str = ""
    ) -> Dict[str, Any]:
        """
        Creates a structured, venture-partner grade investment memo.
        """
        logger.info("Executing Investment Memo Engine...")
        
        # 1. Primary Variables
        profile = evaluation_response.get("startup_profile", {})
        startup_name = profile.get("startup_name", "Unknown Venture")
        target_stage = profile.get("target_stage", "Pre-seed")
        
        eval_results = evaluation_response.get("evaluation_results", {})
        overall_score = eval_results.get("overall_score", 50)
        innovation_score = eval_results.get("innovation_score", 5)
        market_score = eval_results.get("market_score", 5)
        
        # 2. Deterministic Thesis Formulation (Analyst-style)
        if overall_score >= 80:
            recommendation_verdict = "CONVICTION_BUY: Highly compelling opportunity matching premium technical defensibility markers."
            thesis = f"We recommend a high-conviction investment in {startup_name} at the {target_stage} stage. The team possesses structural advantages in innovation, demonstrating high technical defensibility that shields it from commodity wrappers."
        elif overall_score >= 60:
            recommendation_verdict = "CONDITIONAL_INVEST: Favorable market indicators paired with addressable team execution gaps."
            thesis = f"We propose a strategic investment in {startup_name} at {target_stage}, contingent upon resolving current product differentiation blockers and strengthening key engineering lead hire queues."
        else:
            recommendation_verdict = "PASS_WITH_MONITOR: High market saturation or low technical barriers present immediate execution blockers."
            thesis = f"We recommend passing on {startup_name} for the current round. The venture operates in a highly saturated competitive landscape with immediate GTM friction, presenting substantial capital-efficiency risk."
            
        # 3. Standard Analyst Narratives (Offline Fallback)
        opportunity_summary = f"The venture operates within a target market scored at {market_score}/10. While macroeconomic tailwinds favor immediate entry, high client acquisition friction requires highly disciplined vertical product focus."
        founder_narrative = f"The founding team demonstrates a baseline of operational domain capability. Addressing long-term scaling milestones requires adding structural co-founder depth."
        competition_summary = f"With an innovation rating of {innovation_score}/10, defending market margins requires shifting immediately towards proprietary algorithms or workflow integrations that build customer switching costs."
        
        # 4. Venture Analyst Narrative Enrichment (via Groq Llama 3)
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            try:
                from app.llm.client import GroqReasoningClient
                client = GroqReasoningClient()
                prompt = (
                    "You are an elite principal VC venture analyst compiling a comprehensive institutional due diligence investment memo. "
                    "Draft highly technical, premium VC analyst paragraphs (2-3 sentences each) for the following sections based on the inputs below:\n"
                    f"Startup: {startup_name}\n"
                    f"Description: {raw_description}\n"
                    f"Founder: {raw_founder_data}\n"
                    f"Scoring: Overall={overall_score}/100, Innovation={innovation_score}/10, Market={market_score}/10\n"
                    "Provide a JSON object containing precisely three keys:\n"
                    "1. 'market_opportunity': an elite summary of market timing, segment tailwinds, and TAM capture.\n"
                    "2. 'founder_narrative': an insightful, balanced operational capability assessment.\n"
                    "3. 'competition_summary': a rigorous strategic competitive positioning and defensibility posture analysis."
                )
                messages = [{"role": "user", "content": prompt}]
                enrichment = client.execute_prompt(messages, mode="ANALYST_REPORT")
                if enrichment:
                    opportunity_summary = enrichment.get("market_opportunity", opportunity_summary)
                    founder_narrative = enrichment.get("founder_narrative", founder_narrative)
                    competition_summary = enrichment.get("competition_summary", competition_summary)
            except Exception as e:
                logger.warning(f"Failed to enrich investment memo via Groq: {e}. Falling back to default analyst narratives.")
                
        return {
            "investment_thesis": thesis,
            "analyst_verdict": recommendation_verdict,
            "market_opportunity_analysis": opportunity_summary,
            "founder_capability_assessment": founder_narrative,
            "defensibility_and_competition_summary": competition_summary,
            "strategic_diligence_score": overall_score
        }
