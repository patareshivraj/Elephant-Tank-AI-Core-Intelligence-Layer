import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.DecisionSupport.InvestmentDecisionEngine")

class InvestmentDecisionEngine:
    """
    Institutional Decision Support System.
    Generates explainable investment signals, flags core operational cautions,
    and structures rigorous due-diligence review pipelines.
    """
    
    @classmethod
    def evaluate_investment_decision(cls, startup_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs deterministic logic to classify investability and suggest actionable review directives.
        """
        logger.info(f"Generating institutional decision support model for venture: {startup_profile.get('startup_name')}")
        
        score = startup_profile.get("overall_score", 50)
        confidence = startup_profile.get("confidence_score", 5)
        risks = startup_profile.get("risks", [])
        
        # 1. Investability Status Classification
        if score >= 80 and confidence >= 8:
            verdict = "HIGH_CONVICTION_INVEST"
            signal = "STRATEGIC_DIRECT_ALLOCATE"
            rationalization = "The startup demonstrates exceptional operational leverage, defensive technology, and high due-diligence confidence."
        elif score >= 65 and confidence >= 6:
            verdict = "WATCHLIST_OPPORTUNITY"
            signal = "MONITOR_AND_PROBE_MILESTONES"
            rationalization = "Strong potential. Key strategic caution areas must be monitored over the next milestone horizon before allocation."
        else:
            verdict = "REJECT_OR_MONITOR"
            signal = "PASS_OR_RECLASSIFY"
            rationalization = "Operational structures or execution metrics do not meet institutional venture investment thresholds."
            
        # 2. Strategic Caution Flags
        caution_flags = []
        if len(risks) >= 3:
            caution_flags.append({
                "flag_type": "HIGH_RISK_DENSITY",
                "severity": "MEDIUM",
                "message": f"Venture has accumulated {len(risks)} distinct risk factors. Core exposure must be mitigated."
            })
            
        if confidence < 6:
            caution_flags.append({
                "flag_type": "LOW_CONFIDENCE_WARNING",
                "severity": "HIGH",
                "message": "Due-diligence confidence rating is extremely shallow. Additional verified evidence is mandatory."
            })
            
        # 3. Due Diligence Escalation Trigger
        trigger_escalation = False
        if score >= 75 and any("founder" in r.lower() or "regulatory" in r.lower() for r in risks):
            trigger_escalation = True
            
        return {
            "startup_name": startup_profile.get("startup_name", "Unknown"),
            "investability_verdict": verdict,
            "operational_signal": signal,
            "strategic_caution_flags": caution_flags,
            "due_diligence_escalation_triggered": trigger_escalation,
            "decision_narrative": rationalization
        }
