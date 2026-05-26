import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Portfolio.PortfolioIntelligence")

class PortfolioIntelligence:
    """
    Venture Portfolio Intelligence Layer.
    Coordinates institutional portfolio allocations, measures sector concentration risk exposure,
    and uncovers cross-venture scaling targets.
    """
    
    @classmethod
    def analyze_portfolio(cls, portfolio_startups: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs comprehensive analysis metrics across a batch portfolio list.
        """
        logger.info(f"Analyzing institutional portfolio containing {len(portfolio_startups)} active allocations...")
        
        if not portfolio_startups:
            return {
                "portfolio_status": "EMPTY",
                "allocation_count": 0,
                "warnings": [],
                "message": "Portfolio database has no registered venture targets."
            }
            
        total_score = 0
        sector_distribution = {}
        high_performers = []
        
        for st in portfolio_startups:
            total_score += st.get("overall_score", 50)
            
            # Count sectors
            for s in st.get("sectors", ["SaaS"]):
                sector_distribution[s] = sector_distribution.get(s, 0) + 1
                
            # Filter top opportunities
            if st.get("overall_score", 50) >= 80:
                high_performers.append(st["startup_name"])
                
        avg_score = round(total_score / len(portfolio_startups), 2)
        
        # 1. Sector Concentration Exposure Check
        warnings = []
        for s, count in sector_distribution.items():
            ratio = count / len(portfolio_startups)
            if ratio >= 0.50:
                warnings.append({
                    "warning_type": "HIGH_SECTOR_CONCENTRATION",
                    "sector": s,
                    "exposure_percentage": round(ratio * 100, 2),
                    "message": f"Portfolio concentration exposure in sector '{s}' is very high ({round(ratio * 100, 2)}%). Diversification advised."
                })
                
        return {
            "portfolio_status": "HEALTHY" if len(warnings) == 0 else "CONCENTRATION_EXPOSURE_WARNING",
            "allocation_count": len(portfolio_startups),
            "average_portfolio_score": avg_score,
            "sector_allocations": sector_distribution,
            "top_scaling_targets": high_performers,
            "concentration_warnings": warnings
        }
