import pytest
from elephant_tank.schemas import RawStartupInput, FounderProfile
from elephant_tank.orchestrator import VentureScreeningOrchestrator
from elephant_tank.deterministic_logic import calculate_confidence_score

# --------------------------------------------------
# MOCK RAW STARTUP INPUTS
# --------------------------------------------------

@pytest.fixture
def pre_seed_unverified_startup():
    """
    A highly typical Pre-seed startup profile.
    Missing all financials, market sizing, and competitor lists.
    Expected: Low confidence score, early-stage weights applied.
    """
    return RawStartupInput(
        name="Lumina Labs",
        sector="DeepTech",
        current_stage="Pre-seed",
        location="Austin, TX",
        problem_statement="High-speed quantum key distribution is unstable over long distances.",
        solution_overview="Proprietary room-temperature quantum repeater networks using custom optics.",
        tech_stack_differentiation="Proprietary custom routing hardware combined with a room-temperature optical lattice.",
        founders=[
            FounderProfile(
                name="Dr. Aris Vance",
                role="CEO / Chief Scientist",
                domain_experience_years=8,
                prior_exits=0,
                technical_expertise="PhD in Quantum Optics"
            )
        ],
        competitors=[], # Missing
        perceived_defensibility="We possess 2 pending patents on optical lattice stabilizer layouts.",
        known_risks=["Hardware supply chain delays", "Quantum coherence sensitivity"]
    )

@pytest.fixture
def series_a_validated_startup():
    """
    A highly mature Series A startup.
    Contains complete financials, market figures, and team backgrounds.
    Expected: High confidence score, late-stage growth weights applied.
    """
    return RawStartupInput(
        name="ApexFin AI",
        sector="Fintech",
        current_stage="Series A",
        location="New York, NY",
        problem_statement="Enterprise reconciliation in banking takes 3 to 5 business days, introducing severe cash drag.",
        solution_overview="Real-time multi-ledger reconciliation utilizing a deterministic transaction funnel.",
        tech_stack_differentiation="Deterministic funnel matching compiled in Go, connected to llama-3.3-70b-versatile for exception analysis.",
        tam_usd=5000000000.0,
        sam_usd=1200000000.0,
        som_usd=250000000.0,
        mrr_usd=185000.0,
        gross_margins_percent=84.0,
        yoy_growth_percent=145.0,
        active_users=42, # 42 financial institution clients
        founders=[
            FounderProfile(
                name="Sarah Jenkins",
                role="CEO / Co-founder",
                domain_experience_years=12,
                prior_exits=1,
                technical_expertise="Ex-Stripe VP, MBA"
            ),
            FounderProfile(
                name="Marcus Vance",
                role="CTO / Co-founder",
                domain_experience_years=10,
                prior_exits=0,
                technical_expertise="Ex-Google Staff Engineer, Distributed Systems Specialist"
            )
        ],
        competitors=["ReconInc", "ClearMatch"],
        perceived_defensibility="Exclusive core multi-ledger data sync patents, high enterprise switching costs.",
        known_risks=["Long enterprise sales cycles", "Strict sovereign banking regulatory compliance"]
    )

# --------------------------------------------------
# VERIFICATION TEST SUITE
# --------------------------------------------------

def test_pre_seed_pipeline(pre_seed_unverified_startup):
    """
    Validates that a Pre-seed startup with missing metrics is successfully analyzed
    and that the confidence deductions are correctly applied.
    """
    orchestrator = VentureScreeningOrchestrator()
    report = orchestrator.run_screening_pipeline(pre_seed_unverified_startup)
    
    # 1. Structural assertions
    assert report.startup_name == "Lumina Labs"
    assert report.stage == "Pre-seed"
    assert isinstance(report.overall_score, float)
    assert 1.0 <= report.overall_score <= 10.0
    
    # 2. Confidence assertions
    # Base confidence = 10.0
    # Omissions:
    # - Missing TAM/SAM/SOM: -1.5
    # - Missing MRR/Gross Margin: -2.0
    # - Missing Growth/Active Users: -1.5
    # - Empty competitors list: -1.5
    # - Founder vance has prior_exits=0 (not None, so no penalty there)
    # Expected Confidence = 10.0 - 1.5 - 2.0 - 1.5 - 1.5 = 3.5
    expected_confidence = calculate_confidence_score(pre_seed_unverified_startup)
    assert report.confidence_score == expected_confidence
    assert report.confidence_score == 3.5
    
    # 3. Stage weight logic assertion
    # Pre-seed weights: innovation_defensibility = 0.25, founder_capability = 0.25
    assert report.dimension_scores["innovation_defensibility"].weighted_score == round(
        report.dimension_scores["innovation_defensibility"].qualitative_score * 0.25, 2
    )
    assert report.dimension_scores["founder_capability"].weighted_score == round(
        report.dimension_scores["founder_capability"].qualitative_score * 0.25, 2
    )
    # Check that due diligence questions and risk items were extracted
    assert len(report.due_diligence_questions) > 0
    assert len(report.risk_registry) > 0

def test_series_a_pipeline(series_a_validated_startup):
    """
    Validates that a Series A startup with complete details receives a high
    confidence grade and is evaluated using Series A scoring weights.
    """
    orchestrator = VentureScreeningOrchestrator()
    report = orchestrator.run_screening_pipeline(series_a_validated_startup)
    
    # 1. Structural assertions
    assert report.startup_name == "ApexFin AI"
    assert report.stage == "Series A"
    assert isinstance(report.overall_score, float)
    
    # 2. Confidence assertions
    # No omissions should yield a perfect 10.0 confidence score
    assert report.confidence_score == 10.0
    
    # 3. Stage weight logic assertion
    # Series A weights: revenue_viability = 0.25, scalability = 0.20
    assert report.dimension_scores["revenue_viability"].weighted_score == round(
        report.dimension_scores["revenue_viability"].qualitative_score * 0.25, 2
    )
    assert report.dimension_scores["scalability"].weighted_score == round(
        report.dimension_scores["scalability"].qualitative_score * 0.20, 2
    )
    
    # Check that structural recommendation fields are populated
    assert len(report.recommendations) > 0
    assert len(report.strengths) > 0
    assert len(report.weaknesses) > 0
