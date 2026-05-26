import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.reasoning.long_context_orchestrator import LongContextOrchestrator
from app.reasoning.intelligence_synthesizer import IntelligenceSynthesizer
from app.reporting.institutional_memo import InstitutionalMemoEngine

def test_institutional_reasoning_pipeline():
    print("========================================")
    print(" ELEPHANT TANK - INSTITUTIONAL REASONER TEST")
    print("========================================")
    
    # 1. Mock Disparate Documents with Conflicts
    docs = [
        {
            "source_type": "pitch_deck",
            "content": "Page 1. Confidential. Zenith AI is a next-gen quantum-inspired SaaS. We reached a sales revenue of $1.5M ARR."
        },
        {
            "source_type": "market_notes",
            "content": "Competitor landscape is highly saturated, but Zenith's proprietary algorithms offer wide defensibility."
        },
        {
            "source_type": "founder_bio",
            "content": "Dr. Sarah Jenkins, former DeepMind scientist. PhD in Computer Science."
        },
        {
            "source_type": "financial_summary",
            "content": "Zenith has historical ARR at $1.2M according to verified accounting statements."
        }
    ]
    
    # 2. Test Long-Context Orchestrator
    print("[1] Executing Context Orchestrator...")
    orchestrated = LongContextOrchestrator.orchestrate_context(docs)
    
    assert orchestrated["execution_log"]["status"] == "SUCCESS"
    assert len(orchestrated["consolidated_context"]) > 0
    print("  [OK] Cleaned consolidated context generated successfully.")
    
    # 3. Test Intelligence Synthesizer and Metric Conflict Resolution
    print("[2] Executing Intelligence Synthesizer...")
    synthesis = IntelligenceSynthesizer.synthesize_intelligence(orchestrated)
    
    # Check metric reconciliation: must choose $1.2M (min of $1.5M and $1.2M)
    assert synthesis["resolved_revenue_baseline"] == "$1.20M", "Conflict resolution must choose conservative minimum ARR."
    print("  [OK] Successfully reconciled conflicting revenue baseline to $1.20M ARR.")
    
    # 4. Test Institutional GP Memo Compilation
    print("[3] Compiling GP Institutional Memo...")
    moat = {"moat_profile": "WIDE_MOAT", "moat_index": 8.5}
    timing = {"market_maturity_verdict": "WELL_TIMED", "category_maturity": "GROWTH_PHASE"}
    trajectory = {"survivability_narrative": "Robust upward velocity."}
    scalability = {"scalability_index": 9.2, "gross_margin_profile": "HIGH_EXPANSION_LEVERAGE"}
    fit = {"fit_narrative": "Excellent founder-investor alignment."}
    
    memo = InstitutionalMemoEngine.generate_institutional_memo(
        synthesis_data=synthesis,
        overall_score=85,
        moat_data=moat,
        timing_data=timing,
        trajectory_data=trajectory,
        scalability_data=scalability,
        fit_data=fit
    )
    
    assert "CONVICTION BUY" in memo["institutional_recommendation"]
    assert len(memo["executive_investment_thesis"]) > 0
    print("  [OK] Institutional GP Recommendation: OVERWEIGHT / CONVICTION BUY")
    print("  [OK] Executive Thesis Statement Compiled successfully.")
    
    print("\n[SUCCESS] INSTITUTIONAL REASONING TEST PASSED!")

if __name__ == "__main__":
    try:
        test_institutional_reasoning_pipeline()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
