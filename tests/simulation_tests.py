import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.simulation.venture_simulator import VentureSimulator

def test_venture_simulation_cases():
    print("Executing venture simulation tests...")
    
    st_metrics = {
        "startup_name": "Aether Space",
        "overall_score": 80.0,
        "founder_score": 8.0
    }
    
    # 1. Bull Case check
    bull_res = VentureSimulator.run_scenario_simulation(st_metrics, "BULL_CASE")
    assert bull_res["simulated_overall_score"] == 92.0
    assert bull_res["simulated_founder_score"] == 9.0
    assert bull_res["scaling_probability"] > 80.0
    
    # 2. Bear Case check
    bear_res = VentureSimulator.run_scenario_simulation(st_metrics, "BEAR_CASE")
    assert bear_res["simulated_overall_score"] == 60.0
    assert bear_res["simulated_founder_score"] == 6.5
    assert bear_res["scaling_probability"] < 65.0
    
    print("[SUCCESS] Venture simulation tests passed!")

if __name__ == "__main__":
    test_venture_simulation_cases()
