import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Strategy.ScalabilityForecast")

class ScalabilityForecastEngine:
    """
    Venture Scalability Forecasting Engine.
    Models operating leverage, software automation potential, infrastructure burden,
    and hiring complexity to separate high-leverage SaaS from operationally constrained agencies.
    """
    
    @classmethod
    def forecast_scalability(cls, startup_description: str) -> Dict[str, Any]:
        """
        Calculates the operating leverage index and maps the scalability narrative.
        """
        logger.info("Forecasting venture operational scalability index...")
        lower_desc = startup_description.lower()
        
        # Base indicators
        leverage = 6.0
        automation = 5.5
        infra_burden = 4.0  # Lower is better (representing low cost)
        hiring_complexity = 5.0 # Lower is better
        
        # 1. Detect Operationally Constrained Business Models
        is_constrained = False
        if any(w in lower_desc for w in ["consulting", "agency", "physical asset", "drivers", "delivery drivers", "brick and mortar", "manual labor", "custom training", "hardware"]):
            is_constrained = True
            leverage = max(1.5, leverage - 3.5)
            automation = max(2.0, automation - 3.0)
            infra_burden = min(10.0, infra_burden + 3.0)
            hiring_complexity = min(10.0, hiring_complexity + 3.5)
            
        # 2. Detect High-Leverage Software SaaS Models
        is_software_leverage = False
        if any(w in lower_desc for w in ["saas", "automated pipeline", "api network", "digital platform", "cloud microservices", "quantum-inspired ml"]):
            is_software_leverage = True
            leverage = min(10.0, leverage + 3.0)
            automation = min(10.0, automation + 3.0)
            infra_burden = max(1.0, infra_burden - 1.5)
            hiring_complexity = max(1.0, hiring_complexity - 2.0)
            
        # Compute quantitative Scalability Index
        # Scalability = Average of (leverage, automation, (10 - infra_burden), (10 - hiring_complexity))
        scalability_score = round((leverage + automation + (10.0 - infra_burden) + (10.0 - hiring_complexity)) / 4.0, 2)
        
        if is_constrained or scalability_score < 4.5:
            profile = "OPERATIONALLY_CONSTRAINED"
            narrative = "The business model relies heavily on linear human scale or physical logistics. Every unit of revenue growth requires proportional headcount expansion, limiting gross margins."
        elif is_software_leverage or scalability_score >= 7.5:
            profile = "HIGH_EXPANSION_LEVERAGE"
            narrative = "Superb software operating leverage. Revenue expansion is decoupled from hiring growth due to self-serve distribution and cloud auto-scaling, enabling 80%+ gross margins."
        else:
            profile = "MODERATE_GROWTH"
            narrative = "Standard hybrid operating leverage. High software component, but scaling requires moderate services support or specialized regional engineering hiring."
            
        return {
            "scalability_index": scalability_score,
            "gross_margin_profile": profile,
            "operating_leverage_ratio": leverage,
            "automation_efficiency": automation,
            "infrastructure_burden_score": infra_burden,
            "hiring_leverage_complexity": "COMPLEX_TALENT_DRIVEN" if hiring_complexity >= 7.0 else ("MODERATE" if hiring_complexity >= 4.0 else "SELF_SUFFICIENT"),
            "scalability_narrative": narrative
        }
