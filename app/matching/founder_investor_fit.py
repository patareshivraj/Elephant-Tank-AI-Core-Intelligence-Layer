import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Matching.FounderInvestorFit")

class FounderInvestorFitEngine:
    """
    Founder-Investor Fit Engine.
    Computes professional-grade compatibility profiles evaluating stage, domain,
    and risk-appetite alignment, complete with detailed reasoning traces.
    """
    
    @classmethod
    def evaluate_fit(cls, startup_stage: str, startup_domains: List[str], founder_risk_appetite: str, investor_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates alignment between founder startup parameters and investor preferences.
        """
        logger.info("Computing founder-investor portfolio alignment profile...")
        
        traces = []
        scores = []
        
        # 1. Stage Compatibility check
        pref_stages = [s.lower() for s in investor_profile.get("preferred_stages", ["seed"])]
        if startup_stage.lower() in pref_stages:
            scores.append(100)
            traces.append(f"[SUCCESS] Target stage '{startup_stage}' matches investor focus stages {pref_stages}.")
        else:
            scores.append(40)
            traces.append(f"[MISMATCH] Target stage '{startup_stage}' is outside preferred investor stages {pref_stages}.")
            
        # 2. Domain Alignment check
        pref_domains = [d.lower() for d in investor_profile.get("preferred_domains", ["deep tech", "ai"])]
        matched_domains = [d for d in startup_domains if d.lower() in pref_domains]
        if matched_domains:
            domain_score = 60 + (len(matched_domains) * 20)
            scores.append(min(100, domain_score))
            traces.append(f"[SUCCESS] Found domain focus overlap on: {matched_domains}.")
        else:
            scores.append(30)
            traces.append(f"[MISMATCH] Startup domains {startup_domains} do not intersect with investor domains {pref_domains}.")
            
        # 3. Risk Appetite Alignment check
        inv_risk = investor_profile.get("risk_tolerance", "balanced").lower()
        f_risk = founder_risk_appetite.lower()
        
        if inv_risk == f_risk:
            scores.append(100)
            traces.append(f"[SUCCESS] Risk appetite match: Founder '{f_risk}' meets Investor '{inv_risk}'.")
        elif (inv_risk == "aggressive" and f_risk == "balanced") or (inv_risk == "balanced" and f_risk == "conservative"):
            scores.append(75)
            traces.append(f"[STABLE] Compatible risk boundary: Founder '{f_risk}' and Investor '{inv_risk}'.")
        else:
            scores.append(40)
            traces.append(f"[CAUTION] Divergent risk tolerances: Founder is '{f_risk}' while Investor is '{inv_risk}'.")
            
        # Compute final overall fit index
        fit_score = int(sum(scores) / len(scores))
        
        # Determine overall narrative
        if fit_score >= 80:
            narrative = f"Exceptional strategic alignment. The venture matches primary preferred stages and offers a direct portfolio synergy on '{', '.join(startup_domains)}'."
        elif fit_score >= 55:
            narrative = "Moderate matching. Segment interests align, but some adjustments to funding timelines or stage milestones are required to satisfy risk parameters."
        else:
            narrative = "Poor investor fit. High thesis divergence in either stage mismatch or risk appetite parameters."
            
        return {
            "match_score": fit_score,
            "confidence_rating": 8 if fit_score >= 75 else 6,
            "reasoning_traces": traces,
            "fit_narrative": narrative
        }
