import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.strategy.moat_intelligence import MoatIntelligenceEngine

def test_moat_diligence_engine():
    print("========================================")
    print(" ELEPHANT TANK - MOAT INTELLIGENCE TESTER")
    print("========================================")
    
    # 1. Test Shallow GPT Wrapper
    wrapper_desc = "We build a simple chat widget that acts as an API proxy wrapper for ChatGPT."
    wrapper_moat = MoatIntelligenceEngine.analyze_moat(wrapper_desc, innovation_score=8)
    
    print("[1] Evaluating GPT Wrapper Moat...")
    print(f"  Moat Score: {wrapper_moat['moat_index']}/10.0")
    print(f"  Profile: {wrapper_moat['moat_profile']}")
    print(f"  Narrative: {wrapper_moat['moat_diligence_narrative']}")
    
    assert wrapper_moat["moat_profile"] == "NO_MOAT_WRAPPER", "GPT Wrapper must yield NO_MOAT_WRAPPER."
    assert wrapper_moat["moat_index"] < 5.0, "GPT Wrapper moat index must be low."
    print("  [OK] Successfully penalized shallow GPT wrapper.")
    print("----------------------------------------")
    
    # 2. Test Deep Tech Infrastructure
    deep_desc = "A quantum-inspired proprietary algorithm running on a distributed database mainframe with custom silicon microservices."
    deep_moat = MoatIntelligenceEngine.analyze_moat(deep_desc, innovation_score=8)
    
    print("[2] Evaluating Deep Tech Infrastructure Moat...")
    print(f"  Moat Score: {deep_moat['moat_index']}/10.0")
    print(f"  Profile: {deep_moat['moat_profile']}")
    print(f"  Narrative: {deep_moat['moat_diligence_narrative']}")
    
    assert deep_moat["moat_profile"] == "WIDE_MOAT", "Deep Tech must yield WIDE_MOAT."
    assert deep_moat["moat_index"] >= 7.5, "Deep Tech moat index must be high."
    print("  [OK] Successfully identified wide-moat deep infrastructure.")
    print("========================================")
    print("[SUCCESS] MOAT ANALYSIS TEST PASSED!")

if __name__ == "__main__":
    try:
        test_moat_diligence_engine()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
