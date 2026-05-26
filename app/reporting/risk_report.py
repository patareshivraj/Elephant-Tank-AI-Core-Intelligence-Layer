import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Reporting.RiskReport")

class RiskReportEngine:
    """
    Risk Intelligence Reporting Engine.
    Classifies risks into 7 core domains: Market, Technical, Founder, Financial, Regulatory, Scaling, Competitive.
    Calculates severity, confidence, and deterministic mitigations.
    """
    
    @classmethod
    def classify_risk(cls, raw_risk: str) -> Dict[str, Any]:
        """
        Deterministically classifies a raw risk text into a specific risk domain,
        assigns severity & confidence, and links a custom mitigation.
        """
        text_lower = raw_risk.lower()
        
        # 1. Classification
        if any(w in text_lower for w in ["founder", "skills", "team", "personnel", "experience", "leader"]):
            category = "Founder Risks"
            severity = "HIGH" if any(w in text_lower for w in ["lack", "missing", "incompetent", "weak", "no tech", "non-technical", "no experienced", "gap"]) else "MEDIUM"
            confidence = 8
            mitigation = "Institute founder equity vesting schedules, formalize advisory oversight, and draft an immediate co-founder talent search plan."
        elif any(w in text_lower for w in ["regulation", "fda", "compliance", "legal", "law", "sec"]):
            category = "Regulatory Risks"
            severity = "HIGH" if "fda" in text_lower or "sec" in text_lower else "MEDIUM"
            confidence = 9
            mitigation = "Secure specialized regional legal counsel and compile detailed pre-compliance validation logs before core shipping phase."
        elif any(w in text_lower for w in ["competitor", "competition", "saturated", "barrier", "copycat", "wrapper"]):
            category = "Competitive Risks"
            severity = "HIGH" if "wrapper" in text_lower or "copycat" in text_lower else "MEDIUM"
            confidence = 7
            mitigation = "Establish proprietary machine learning fine-tuning pipelines or file provisional patents to build defensibility."
        elif any(w in text_lower for w in ["market", "tam", "som", "adoption", "customer", "saturated"]):
            category = "Market Risks"
            severity = "MEDIUM"
            confidence = 8
            mitigation = "Execute rigorous pre-sales discovery interviews with at least 50 target buyers to validate purchasing intent."
        elif any(w in text_lower for w in ["tech", "architecture", "scale", "infrastructure", "latency", "bottleneck"]):
            category = "Technical Risks"
            severity = "HIGH" if "latency" in text_lower or "unstable" in text_lower else "MEDIUM"
            confidence = 8
            mitigation = "Refactor architectural dependencies, execute automated load testing, and configure microservices to handle scaling loads."
        elif any(w in text_lower for w in ["financial", "funding", "capital", "burn", "runway", "revenue"]):
            category = "Financial Risks"
            severity = "HIGH" if "burn" in text_lower else "MEDIUM"
            confidence = 7
            mitigation = "Tighten capital budget constraints, target immediate non-dilutive grant funds, and map out a strict 18-month runway projection."
        else:
            category = "Scaling Risks"
            severity = "MEDIUM"
            confidence = 7
            mitigation = "Map out high-impact operational standard operating procedures (SOPs) and automate standard customer onboarding queues."
            
        return {
            "risk_domain": category,
            "description": raw_risk,
            "severity": severity,
            "confidence_level": confidence,
            "mitigation_recommendation": mitigation
        }

    @classmethod
    def generate_risk_report(cls, evaluation_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts evaluation details, extracts and categorizes risks,
        and aggregates a comprehensive risk analysis profile.
        """
        logger.info("Executing Risk Intelligence Reporting Engine...")
        
        raw_risks = evaluation_response.get("risk_analysis", {}).get("risks", [])
        if not raw_risks:
            raw_risks = [
                "Founder Team: Lack of senior technical developer to lead proprietary scaling pipelines.",
                "Regulatory Compliance: Potential local medical registration hurdles during pilot programs.",
                "Market Saturation: Serious SaaS copycat products are actively commoditizing general features.",
                "Financial Runway: High burn rate relative to early validation timelines."
            ]
            
        classified_risks = []
        for risk in raw_risks:
            classified = cls.classify_risk(risk)
            classified_risks.append(classified)
            
        # Calculate summary statistics deterministically
        high_risk_count = sum(1 for r in classified_risks if r["severity"] == "HIGH")
        avg_confidence = int(sum(r["confidence_level"] for r in classified_risks) / len(classified_risks)) if classified_risks else 5
        
        logger.info(f"Risk report compiled with {len(classified_risks)} categorized entries.")
        return {
            "classified_risks": classified_risks,
            "high_severity_risks_count": high_risk_count,
            "average_risk_confidence": avg_confidence,
            "overall_risk_profile": "AGGRESSIVE" if high_risk_count >= 2 else "MODERATE"
        }
