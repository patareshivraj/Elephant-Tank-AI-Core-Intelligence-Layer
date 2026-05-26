import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.simulation.competition_model import StartupCompetitionModel
from app.reasoning.multi_startup_reasoning import MultiStartupReasoning

def test_competition_and_multi_reasoning():
    print("Executing competition and comparative reasoning tests...")
    
    st_a = {"startup_name": "Aether Space", "overall_score": 85.0, "founder_score": 9.0, "sectors": ["SpaceTech", "AI"], "timing_verdict": "WELL_TIMED"}
    st_b = {"startup_name": "Nebula Rocket", "overall_score": 70.0, "founder_score": 7.0, "sectors": ["SpaceTech"], "timing_verdict": "WELL_TIMED"}
    
    # 1. Competition checks
    comp_res = StartupCompetitionModel.evaluate_competition(st_a, st_b)
    assert comp_res["ecosystem_crowding_index"] == 50.0
    assert comp_res["defensibility_erosion_detected"] is True
    assert comp_res["vulnerable_entity"] == "Nebula Rocket"
    
    # 2. Multi-Startup comparative checks
    comp_batch = MultiStartupReasoning.compare_multiple_startups([st_a, st_b])
    assert comp_batch["primary_recommendation"] == "Aether Space"
    assert comp_batch["comparison_matrix"][0]["attractiveness_index"] >= 80.0
    
    print("[SUCCESS] Competition and comparative reasoning tests passed!")

if __name__ == "__main__":
    test_competition_and_multi_reasoning()
