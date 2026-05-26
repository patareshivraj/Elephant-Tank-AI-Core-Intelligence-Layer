from typing import Dict, List, Tuple
from elephant_tank.schemas import RawStartupInput, RiskItem
from elephant_tank.config import (
    STAGE_WEIGHTS,
    CONFIDENCE_BASE_SCORE,
    CONFIDENCE_MINIMUM,
    CONFIDENCE_PENALTY_TAM,
    CONFIDENCE_PENALTY_REVENUE,
    CONFIDENCE_PENALTY_TRACTION,
    CONFIDENCE_PENALTY_FOUNDERS,
    CONFIDENCE_PENALTY_COMPETITION,
    CONFIDENCE_PENALTY_FOUNDER_DETAIL,
    RISK_PENALTY_HIGH,
    RISK_PENALTY_MEDIUM,
    RISK_PENALTY_LOW,
)

# --------------------------------------------------
# DETERMINISTIC CONFIDENCE CALCULATION
# --------------------------------------------------
def calculate_confidence_score(input_data: RawStartupInput) -> float:
    """
    Computes an empirical completeness score (1.0 to 10.0) for the startup profile.
    Apply localized penalty logic for missing or unverified fields.
    """
    confidence = CONFIDENCE_BASE_SCORE
    
    # 1. Market sizing check
    if input_data.tam_usd is None or input_data.sam_usd is None or input_data.som_usd is None:
        confidence -= CONFIDENCE_PENALTY_TAM
        
    # 2. Revenue indicators check
    if input_data.mrr_usd is None or input_data.gross_margins_percent is None:
        confidence -= CONFIDENCE_PENALTY_REVENUE
        
    # 3. Growth and active users traction check
    if input_data.yoy_growth_percent is None or input_data.active_users is None:
        confidence -= CONFIDENCE_PENALTY_TRACTION
        
    # 4. Core team check
    if not input_data.founders:
        confidence -= CONFIDENCE_PENALTY_FOUNDERS
    else:
        # Check details for each founder
        for founder in input_data.founders:
            if founder.domain_experience_years is None or founder.prior_exits is None:
                confidence -= CONFIDENCE_PENALTY_FOUNDER_DETAIL
                
    # 5. Competitor list check
    if not input_data.competitors:
        confidence -= CONFIDENCE_PENALTY_COMPETITION

    # Clamp confidence to configured boundaries
    return max(CONFIDENCE_MINIMUM, round(confidence, 1))

# --------------------------------------------------
# STAGE-WEIGHTED SCORING COMPILER
# --------------------------------------------------
def calculate_weighted_overall_score(dimension_scores: Dict[str, float], stage: str) -> Tuple[float, Dict[str, float]]:
    """
    Applies stage-specific weights to the 7 core qualitative scores.
    Returns:
        weighted_total: Sum of stage-weighted scores.
        weighted_dimensions: Dict mapping dimension names to weighted score components.
    """
    weights = STAGE_WEIGHTS.get(stage, STAGE_WEIGHTS["Seed"]) # Fallback to Seed if stage mismatch
    weighted_total = 0.0
    weighted_dimensions: Dict[str, float] = {}
    
    for key, raw_score in dimension_scores.items():
        weight = weights.get(key, 0.0)
        weighted_val = raw_score * weight
        weighted_dimensions[key] = round(weighted_val, 2)
        weighted_total += weighted_val
        
    return round(weighted_total, 2), weighted_dimensions

# --------------------------------------------------
# RISK DEDUCTION COMPILER
# --------------------------------------------------
def calculate_risk_penalties(risk_registry: List[RiskItem]) -> float:
    """
    Compiles an overall score penalty based on the severity of identified risks.
    """
    penalty = 0.0
    for risk in risk_registry:
        if risk.severity == "High":
            penalty += RISK_PENALTY_HIGH
        elif risk.severity == "Medium":
            penalty += RISK_PENALTY_MEDIUM
        elif risk.severity == "Low":
            penalty += RISK_PENALTY_LOW
            
    return round(penalty, 2)

# --------------------------------------------------
# MASTER DETERMINISTIC INTEGRATION
# --------------------------------------------------
def compute_final_scores(
    input_data: RawStartupInput,
    raw_dimension_scores: Dict[str, float],
    risk_registry: List[RiskItem]
) -> Tuple[float, float, Dict[str, float]]:
    """
    Integrates confidence evaluation, stage weighting, and risk penalties.
    Returns:
        final_overall_score: Final clamped startup grade (1.0 to 10.0).
        confidence_score: Final clamped completeness grade (1.0 to 10.0).
        weighted_dimensions: The localized weighted dimension values.
    """
    # 1. Compute Confidence Grade
    confidence_score = calculate_confidence_score(input_data)
    
    # 2. Compute Base Weighted Overall Score
    weighted_base, weighted_dimensions = calculate_weighted_overall_score(
        raw_dimension_scores, 
        input_data.current_stage
    )
    
    # 3. Compute Risk Penalty Deductions
    risk_penalty = calculate_risk_penalties(risk_registry)
    
    # 4. Aggregate Final Grade
    final_overall_score = weighted_base - risk_penalty
    
    # Clamping & rounding safeguards
    final_overall_score = max(1.0, min(10.0, round(final_overall_score, 1)))
    
    return final_overall_score, confidence_score, weighted_dimensions
