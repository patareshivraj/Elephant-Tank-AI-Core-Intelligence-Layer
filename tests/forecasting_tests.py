import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.forecasting.venture_forecast import VentureForecast
from app.forecasting.market_simulation import MarketSimulationEngine

def test_forecasting_and_market_sim():
    print("Executing forecasting and market simulation tests...")
    
    st_metrics = {
        "startup_name": "Aether Space",
        "overall_score": 75.0,
        "founder_score": 8.0
    }
    
    # 1. 12-Month Forecast check
    fc_res = VentureForecast.compile_12_month_forecast(st_metrics)
    assert fc_res["starting_readiness_score"] == 75.0
    assert len(fc_res["twelve_month_projection"]) == 12
    assert fc_res["twelve_month_projection"][0]["month"] == 1
    assert fc_res["terminal_readiness_classification"] == "HIGH_CONVICTION"
    
    # 2. Market Simulation check
    market_res = MarketSimulationEngine.run_market_simulation("MedTech", "EXPANSIVE")
    assert market_res["capital_funding_multiplier"] == 1.35
    assert market_res["scaling_velocity"] == "RAPID"
    
    print("[SUCCESS] Forecasting and market simulation tests passed!")

if __name__ == "__main__":
    test_forecasting_and_market_sim()
