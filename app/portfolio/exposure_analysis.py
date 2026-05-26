import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Portfolio.ExposureAnalysis")

class PortfolioExposureAnalysis:
    """
    Portfolio Exposure Intelligence.
    Analyzes systemic exposure gaps across technology categories,
    geographic nodes, and founder dependency factors.
    """
    
    @classmethod
    def evaluate_portfolio_exposure(cls, portfolio_startups: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs rigorous checks on portfolio concentration parameters.
        """
        logger.info(f"Analyzing multi-entity exposure parameters across {len(portfolio_startups)} assets...")
        
        if not portfolio_startups:
            return {
                "systemic_exposure_rating": "LOW",
                "exposure_warnings": [],
                "message": "Portfolio database has no registered venture targets."
            }
            
        tech_allocations = {}
        founder_dependency_count = 0
        
        for st in portfolio_startups:
            # Tech types
            tech_type = st.get("tech_stack", "Software")
            tech_allocations[tech_type] = tech_allocations.get(tech_type, 0) + 1
            
            # Founder dependency: high if founder score < 6
            if st.get("founder_score", 5) < 6:
                founder_dependency_count += 1
                
        warnings = []
        
        # 1. Tech Concentration Warn
        for tech, count in tech_allocations.items():
            ratio = count / len(portfolio_startups)
            if ratio >= 0.60:
                warnings.append({
                    "exposure_type": "HIGH_TECHNOLOGY_CONCENTRATION",
                    "value": tech,
                    "exposure_ratio": round(ratio, 2),
                    "message": f"Exposure threat: '{tech}' represents {round(ratio*100, 2)}% of technology stack allocation. Diversification needed."
                })
                
        # 2. Systemic Founder Dependency Warn
        founder_ratio = founder_dependency_count / len(portfolio_startups)
        if founder_ratio >= 0.40:
            warnings.append({
                "exposure_type": "SYSTEMIC_FOUNDER_DEPENDENCY_RISK",
                "value": "CRITICAL_FOUNDER_DEPENDENCY",
                "exposure_ratio": round(founder_ratio, 2),
                "message": f"Exposure threat: {round(founder_ratio*100, 2)}% of portfolio operates with low founder execution ratings."
            })
            
        rating = "HIGH" if len(warnings) >= 2 else ("MEDIUM" if len(warnings) == 1 else "LOW")
        
        return {
            "systemic_exposure_rating": rating,
            "portfolio_size": len(portfolio_startups),
            "tech_distribution": tech_allocations,
            "founder_dependency_ratio": round(founder_ratio, 2),
            "exposure_warnings": warnings
        }
