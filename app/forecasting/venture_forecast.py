import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Forecasting.VentureForecast")

class VentureForecast:
    """
    Strategic Venture Forecasting Layer.
    Forecasts milestone trajectory velocities, maturity indices, and investability
    preparedness curves over a 12-month horizon.
    """
    
    @classmethod
    def compile_12_month_forecast(cls, startup_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs deterministic growth modeling to project monthly investability curves.
        """
        logger.info(f"Generating 12-month scaling forecast for: {startup_metrics.get('startup_name')}")
        
        score = float(startup_metrics.get("overall_score", 50))
        founder = float(startup_metrics.get("founder_score", 5))
        
        # Monthly growth velocity: higher founder score accelerates GTM maturity
        growth_velocity = (founder / 10.0) * 1.5
        
        projections = []
        current_score = score
        
        for month in range(1, 13):
            current_score = min(100.0, current_score + growth_velocity)
            projections.append({
                "month": month,
                "projected_readiness_score": round(current_score, 2),
                "scaling_probability": round(min(99.0, current_score * 0.95), 2)
            })
            
        final_readiness = "HIGH_CONVICTION" if current_score >= 80 else ("VIABLE" if current_score >= 60 else "STAGNANT")
        
        return {
            "startup_name": startup_metrics.get("startup_name", "Unknown"),
            "starting_readiness_score": score,
            "monthly_velocity_applied": round(growth_velocity, 2),
            "twelve_month_projection": projections,
            "terminal_readiness_classification": final_readiness
        }
