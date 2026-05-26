import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.strategy.trajectory_analysis import TrajectoryAnalysisEngine

def test_trajectory_engine():
    print("========================================")
    print(" ELEPHANT TANK - STARTUP TRAJECTORY TESTER")
    print("========================================")
    
    # 1. Test High Operational Trajectory (Series A Ready)
    print("[1] Evaluating High-Score Trajectory...")
    high_traj = TrajectoryAnalysisEngine.analyze_trajectory(
        overall_score=85,
        founder_readiness="INVESTOR_READY",
        moat_index=8.2
    )
    
    print(f"  Survivability Score: {high_traj['survivability_index']}/10.0")
    print(f"  Funding Target: {high_traj['funding_progression_readiness']}")
    print(f"  Uncertainty bounds: [{high_traj['confidence_bounds']['lower_bound']} - {high_traj['confidence_bounds']['upper_bound']}]")
    
    assert high_traj["funding_progression_readiness"] == "SERIES_A_ACCELERATED"
    assert high_traj["survivability_index"] > 7.0
    print("  [OK] Successfully projected high Series A operational velocity.")
    print("----------------------------------------")
    
    # 2. Test Low Operational Trajectory (Strengthening Required)
    print("[2] Evaluating Low-Score Trajectory...")
    low_traj = TrajectoryAnalysisEngine.analyze_trajectory(
        overall_score=45,
        founder_readiness="VULNERABLE",
        moat_index=3.1
    )
    
    print(f"  Survivability Score: {low_traj['survivability_index']}/10.0")
    print(f"  Funding Target: {low_traj['funding_progression_readiness']}")
    
    assert low_traj["funding_progression_readiness"] == "PRE_SEED_STRENGTHENING"
    assert low_traj["survivability_index"] < 5.0
    print("  [OK] Successfully projected vulnerable pre-seed operational status.")
    
    print("========================================")
    print("[SUCCESS] TRAJECTORY TEST PASSED!")

if __name__ == "__main__":
    try:
        test_trajectory_engine()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
