import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.strategy.weakness_prioritizer import WeaknessPrioritizer
from app.strategy.scalability_forecast import ScalabilityForecastEngine
from app.matching.founder_investor_fit import FounderInvestorFitEngine

def test_strategic_consistency_and_leveraging():
    print("========================================")
    print(" ELEPHANT TANK - STRATEGIC CONSISTENCY TESTER")
    print("========================================")
    
    # 1. Test Weakness Prioritizer Urgency Sorting
    print("[1] Evaluating Strategic Weakness Prioritizer...")
    weaknesses = [
        "Infrastructure scaling bottleneck cap on core cloud databases.",
        "Founder Team lacks technical capability and B2B medical experience.",
        "GTM CAC is extremely high due to competitive marketing channels."
    ]
    
    prioritized = WeaknessPrioritizer.prioritize_weaknesses(weaknesses)
    
    # Assert founder risk is first, followed by GTM CAC blocker, then infra database scaling
    assert prioritized[0]["classified_domain"] == "FOUNDER_RISK", "Founder risk must be prioritized first."
    assert prioritized[1]["classified_domain"] == "GTM_BLOCKER", "GTM blocker must be prioritized second."
    assert prioritized[2]["classified_domain"] == "SCALABILITY_BOTTLENECK", "Scalability bottleneck must be prioritized third."
    
    print(f"  Rank 1: [{prioritized[0]['classified_domain']}] Urgency: {prioritized[0]['urgency_rating']} - {prioritized[0]['weakness_description']}")
    print(f"  Rank 2: [{prioritized[1]['classified_domain']}] Urgency: {prioritized[1]['urgency_rating']} - {prioritized[1]['weakness_description']}")
    print(f"  Rank 3: [{prioritized[2]['classified_domain']}] Urgency: {prioritized[2]['urgency_rating']} - {prioritized[2]['weakness_description']}")
    print("  [OK] Deterministic weakness urgency priority sorting validated.")
    print("----------------------------------------")
    
    # 2. Test Scalability Forecasting Software vs Agency Leverage
    print("[2] Evaluating Venture Scalability Forecast Engine...")
    saas_desc = "We plan to build a highly scalable auto-scaling B2B software SaaS platform using API networks."
    agency_desc = "A specialized marketing consulting agency providing brick and mortar manual labor designs."
    
    saas_fc = ScalabilityForecastEngine.forecast_scalability(saas_desc)
    agency_fc = ScalabilityForecastEngine.forecast_scalability(agency_desc)
    
    print(f"  SaaS Scalability Index: {saas_fc['scalability_index']}/10.0 ({saas_fc['gross_margin_profile']})")
    print(f"  Agency Scalability Index: {agency_fc['scalability_index']}/10.0 ({agency_fc['gross_margin_profile']})")
    
    assert saas_fc["gross_margin_profile"] == "HIGH_EXPANSION_LEVERAGE"
    assert agency_fc["gross_margin_profile"] == "OPERATIONALLY_CONSTRAINED"
    print("  [OK] SaaS high expansion operating leverage vs Agency manual constraints validated.")
    print("----------------------------------------")
    
    # 3. Test Founder-Investor Fit Alignment
    print("[3] Evaluating Founder-Investor Portfolio Fit...")
    investor = {
        "preferred_stages": ["seed", "series a"],
        "preferred_domains": ["deep tech", "ai saas", "logistics"],
        "risk_tolerance": "balanced"
    }
    
    fit = FounderInvestorFitEngine.evaluate_fit(
        startup_stage="Seed",
        startup_domains=["AI SaaS", "Logistics"],
        founder_risk_appetite="Balanced",
        investor_profile=investor
    )
    
    print(f"  Portfolio Alignment Match Score: {fit['match_score']}/100")
    print(f"  Fit Narrative: {fit['fit_narrative']}")
    for trace in fit["reasoning_traces"]:
        print(f"    Trace: {trace}")
        
    assert fit["match_score"] >= 80, "Perfect alignment parameters must yield outstanding fit score."
    print("  [OK] Strategic founder-investor fit parameters validated.")
    print("========================================")
    print("[SUCCESS] STRATEGIC CONSISTENCY TEST PASSED!")

if __name__ == "__main__":
    try:
        test_strategic_consistency_and_leveraging()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
