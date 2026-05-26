import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.strategy.market_timing import MarketTimingEngine

def test_market_timing_engine():
    print("========================================")
    print(" ELEPHANT TANK - MARKET TIMING TESTER")
    print("========================================")
    
    # 1. Test "Too Early"
    early_desc = "We plan to build a commercial space elevator utilizing cold fusion space engines and asteroid mining mainframe grids."
    early_timing = MarketTimingEngine.analyze_timing(early_desc)
    
    print("[1] Evaluating Emerging Space Tech (Too Early)...")
    print(f"  Timing Verdict: {early_timing['market_maturity_verdict']}")
    print(f"  Narrative: {early_timing['timing_diligence_narrative']}")
    
    assert early_timing["market_maturity_verdict"] == "TOO_EARLY", "Space Elevator must yield TOO_EARLY."
    print("  [OK] Successfully caught immature segment timing.")
    print("----------------------------------------")
    
    # 2. Test "Too Late"
    late_desc = "A standard generic chatbot food delivery app widget that works on simple drop shipping Shopify platforms."
    late_timing = MarketTimingEngine.analyze_timing(late_desc)
    
    print("[2] Evaluating Saturated Chatbot App (Too Late)...")
    print(f"  Timing Verdict: {late_timing['market_maturity_verdict']}")
    print(f"  Narrative: {late_timing['timing_diligence_narrative']}")
    
    assert late_timing["market_maturity_verdict"] == "TOO_LATE_SATURATED", "Delivery App must yield TOO_LATE_SATURATED."
    print("  [OK] Successfully caught saturated mature timing.")
    print("----------------------------------------")
    
    # 3. Test "Well Timed"
    well_desc = "FDA-compliant B2B compliance registry logs for medical and pharmaceutical hardware pipelines."
    well_timing = MarketTimingEngine.analyze_timing(well_desc)
    
    print("[3] Evaluating Regulatory EHR platform (Well Timed)...")
    print(f"  Timing Verdict: {well_timing['market_maturity_verdict']}")
    print(f"  Narrative: {well_timing['timing_diligence_narrative']}")
    
    assert well_timing["market_maturity_verdict"] == "WELL_TIMED", "B2B compliance must yield WELL_TIMED."
    print("  [OK] Successfully validated well-timed entry window.")
    
    print("========================================")
    print("[SUCCESS] MARKET TIMING TEST PASSED!")

if __name__ == "__main__":
    try:
        test_market_timing_engine()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
