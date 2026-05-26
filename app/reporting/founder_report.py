import logging
import os
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Reporting.FounderReport")

class FounderReportEngine:
    """
    Founder Intelligence Reporting Module.
    Analyzes founder execution readiness, technical capacity, leadership risk, and operational viability.
    """
    
    @classmethod
    def generate_founder_report(cls, evaluation_response: Dict[str, Any], raw_founder_data: str = "") -> Dict[str, Any]:
        """
        Builds a balanced, evidence-based, confidence-aware founder intelligence profile.
        """
        logger.info("Executing Founder Intelligence Reporting Engine...")
        
        # 1. Base Score Extraction
        founder_score = evaluation_response.get("evaluation_results", {}).get("founder_score", 5)
        raw_strengths = evaluation_response.get("founder_intelligence", {}).get("strengths", [])
        raw_weaknesses = evaluation_response.get("founder_intelligence", {}).get("weaknesses", [])
        
        founder_lower = (raw_founder_data or "").lower()
        
        # 2. Technical Capability Level (Deterministic)
        if any(w in founder_lower for w in ["cto", "engineer", "developer", "computer science", "phd", "technical"]):
            tech_capability = "HIGH"
        elif any(w in founder_lower for w in ["builder", "hacker", "technical lead", "ex-stripe"]):
            tech_capability = "HIGH"
        elif any(w in founder_lower for w in ["experienced", "pms", "designer"]):
            tech_capability = "MEDIUM"
        else:
            tech_capability = "LOW"
            
        # 3. Leadership Risks
        leadership_risks = []
        for weak in raw_weaknesses:
            leadership_risks.append(f"Leadership Threat: {weak}")
        if not leadership_risks:
            leadership_risks.append("Execution Gap: Single founder setup without mature technical co-pilot.")
            
        # 4. Execution Readiness
        if founder_score >= 8:
            readiness = "INVESTOR_READY"
        elif founder_score >= 5:
            readiness = "OPERATIONAL_STABLE"
        else:
            readiness = "VULNERABLE"
            
        # 5. Startup Operating Potential
        operating_potential = float(founder_score * 1.0)
        if tech_capability == "HIGH":
            operating_potential += 1.0
            
        # 6. Qualitative Operational Assessment Narrative
        narrative = (
            f"The founding team presents {readiness.replace('_', ' ').lower()} execution readiness with a founder due diligence "
            f"score of {founder_score}/10. Technical capability is evaluated as '{tech_capability}', presenting an overall operating potential of {operating_potential}/10."
        )
        
        # Enrichment via Groq if key exists
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            try:
                from app.llm.client import GroqReasoningClient
                client = GroqReasoningClient()
                prompt = (
                    "You are an elite venture diligence partner profiling a startup's founding team capability. "
                    f"Bio/Background: {raw_founder_data}\n"
                    f"Strengths: {', '.join(raw_strengths)}\n"
                    f"Weaknesses: {', '.join(raw_weaknesses)}\n"
                    "Return a JSON object with a single key 'operating_potential_narrative' containing a highly objective, balanced, 3-sentence venture-style analysis of their capability."
                )
                messages = [{"role": "user", "content": prompt}]
                enrichment = client.execute_prompt(messages, mode="ANALYST_REPORT")
                if enrichment and "operating_potential_narrative" in enrichment:
                    narrative = enrichment["operating_potential_narrative"]
            except Exception as e:
                logger.warning(f"Failed to enrich founder operational narrative via Groq: {e}. Bypassing to fallback.")
                
        return {
            "execution_readiness_level": readiness,
            "technical_capability_rating": tech_capability,
            "leadership_risks_identified": leadership_risks,
            "operating_potential_index": min(operating_potential, 10.0),
            "strengths_summary": raw_strengths if raw_strengths else ["Industry domain expertise"],
            "operational_capability_narrative": narrative
        }
