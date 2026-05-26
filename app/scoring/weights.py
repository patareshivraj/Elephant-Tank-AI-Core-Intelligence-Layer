from typing import Dict

# Define the baseline deterministic weights across 10 evaluation dimensions.
# Weights MUST sum to 1.0 (100%) for proper score normalization.

STAGE_AWARE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "Pre-seed": {
        "innovation": 0.20,
        "market_potential": 0.15,
        "scalability": 0.10,
        "revenue_viability": 0.05,
        "founder_capability": 0.25,
        "competition_risk": 0.10,
        "funding_readiness": 0.05,
        "operational_readiness": 0.05,
        "technology_readiness": 0.05,
        "execution_readiness": 0.00
    },
    "Seed": {
        "innovation": 0.15,
        "market_potential": 0.15,
        "scalability": 0.15,
        "revenue_viability": 0.10,
        "founder_capability": 0.10,
        "competition_risk": 0.10,
        "funding_readiness": 0.10,
        "operational_readiness": 0.05,
        "technology_readiness": 0.05,
        "execution_readiness": 0.05
    },
    "Series A": {
        "innovation": 0.10,
        "market_potential": 0.10,
        "scalability": 0.20,
        "revenue_viability": 0.20,
        "founder_capability": 0.10,
        "competition_risk": 0.05,
        "funding_readiness": 0.05,
        "operational_readiness": 0.10,
        "technology_readiness": 0.05,
        "execution_readiness": 0.05
    },
    "Default": {
        "innovation": 0.15,
        "market_potential": 0.15,
        "scalability": 0.15,
        "revenue_viability": 0.10,
        "founder_capability": 0.10,
        "competition_risk": 0.10,
        "funding_readiness": 0.10,
        "operational_readiness": 0.05,
        "technology_readiness": 0.05,
        "execution_readiness": 0.05
    }
}
