import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.portfolio.cross_portfolio_analysis import CrossPortfolioAnalysis
from app.portfolio.exposure_analysis import PortfolioExposureAnalysis

def test_cross_portfolio_and_exposure():
    print("Executing cross-portfolio and exposure tests...")
    
    startups = [
        {"startup_name": "Aether Space", "overall_score": 85, "sectors": ["SpaceTech", "AI"], "tech_stack": "AI", "founder_score": 9},
        {"startup_name": "Nebula Cloud", "overall_score": 72, "sectors": ["SpaceTech", "AI"], "tech_stack": "AI", "founder_score": 5},
        {"startup_name": "Horizon Tech", "overall_score": 64, "sectors": ["SaaS"], "tech_stack": "AI", "founder_score": 4}
    ]
    
    # 1. Cannibalization checks (Aether Space & Nebula Cloud share 2 sectors: SpaceTech, AI)
    cross_res = CrossPortfolioAnalysis.evaluate_cross_portfolio(startups)
    assert cross_res["cannibalization_warnings_count"] == 1
    assert cross_res["cannibalization_warnings"][0]["warning_type"] == "HIGH_CANNIBALIZATION_RISK"
    
    # 2. Exposure analysis checks (AI represent 100% of tech_stack -> >60% -> warning)
    exposure_res = PortfolioExposureAnalysis.evaluate_portfolio_exposure(startups)
    assert exposure_res["systemic_exposure_rating"] == "HIGH"
    assert len(exposure_res["exposure_warnings"]) == 2
    
    print("[SUCCESS] Cross-portfolio and exposure tests passed!")

if __name__ == "__main__":
    test_cross_portfolio_and_exposure()
