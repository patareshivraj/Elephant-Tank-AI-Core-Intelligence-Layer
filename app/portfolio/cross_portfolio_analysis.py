import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Portfolio.CrossPortfolioAnalysis")

class CrossPortfolioAnalysis:
    """
    Cross-Portfolio Intelligence System.
    Analyzes cross-venture overlaps, identifies internal cannibalization vectors,
    and supports multi-entity portfolio allocation adjustments.
    """
    
    @classmethod
    def evaluate_cross_portfolio(cls, startups: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs comprehensive redundancy checks across the active portfolio allocations.
        """
        logger.info(f"Analyzing cross-portfolio cannibalization risks for {len(startups)} assets...")
        
        warnings = []
        overlaps_mapped = 0
        
        for i in range(len(startups)):
            for j in range(i + 1, len(startups)):
                st_a = startups[i]
                st_b = startups[j]
                
                sec_a = set(st_a.get("sectors", []))
                sec_b = set(st_b.get("sectors", []))
                
                common = sec_a.intersection(sec_b)
                if len(common) >= 2:
                    overlaps_mapped += 1
                    warnings.append({
                        "warning_type": "HIGH_CANNIBALIZATION_RISK",
                        "startup_a": st_a["startup_name"],
                        "startup_b": st_b["startup_name"],
                        "shared_sectors": list(common),
                        "message": f"Cannibalization hazard: '{st_a['startup_name']}' and '{st_b['startup_name']}' share {len(common)} sectors: {list(common)}."
                    })
                    
        return {
            "portfolio_size": len(startups),
            "cannibalization_warnings_count": len(warnings),
            "overlapping_pairs_mapped": overlaps_mapped,
            "cannibalization_warnings": warnings
        }
