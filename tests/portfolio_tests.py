import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.portfolio.portfolio_intelligence import PortfolioIntelligence

def test_portfolio_concentration_and_scores():
    print("Executing portfolio layer tests...")
    
    startups = [
        {"startup_name": "Phoenix Health", "overall_score": 85, "sectors": ["MedTech", "AI"]},
        {"startup_name": "Aura Health", "overall_score": 72, "sectors": ["MedTech"]},
        {"startup_name": "Zephyr Med", "overall_score": 64, "sectors": ["MedTech"]}
    ]
    
    # Analyze portfolio (3 allocations, all containing MedTech -> >50% concentration risk)
    analysis = PortfolioIntelligence.analyze_portfolio(startups)
    
    assert analysis["portfolio_status"] == "CONCENTRATION_EXPOSURE_WARNING"
    assert analysis["allocation_count"] == 3
    assert len(analysis["concentration_warnings"]) == 1
    assert "Phoenix Health" in analysis["top_scaling_targets"]
    
    print("[SUCCESS] Portfolio layer tests passed!")

if __name__ == "__main__":
    test_portfolio_concentration_and_scores()
