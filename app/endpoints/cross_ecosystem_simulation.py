import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

from app.simulation.venture_simulator import VentureSimulator
from app.simulation.competition_model import StartupCompetitionModel
from app.portfolio.cross_portfolio_analysis import CrossPortfolioAnalysis
from app.simulation.ecosystem_shock import EcosystemShockAnalysis
from app.forecasting.venture_forecast import VentureForecast
from app.forecasting.market_simulation import MarketSimulationEngine
from app.reasoning.multi_startup_reasoning import MultiStartupReasoning
from app.portfolio.exposure_analysis import PortfolioExposureAnalysis
from app.intelligence.cascade_detection import EcosystemCascadeDetection

logger = logging.getLogger("ElephantTank.Endpoints.CrossEcosystemSimulation")

router = APIRouter()

@router.post("/simulation/scenario", response_model=Dict[str, Any], tags=["Sprint 9 - Strategic Simulation"])
def run_scenario_simulation(payload: Dict[str, Any]):
    """
    Simulates startup success/failure trajectories under dynamic bull/bear/base scenarios.
    """
    metrics = payload.get("metrics")
    scenario = payload.get("scenario", "BASE_CASE")
    if not metrics:
        raise HTTPException(status_code=400, detail="Missing parameter 'metrics'")
    return VentureSimulator.run_scenario_simulation(metrics, scenario)

@router.post("/simulation/competition", response_model=Dict[str, Any], tags=["Sprint 9 - Strategic Simulation"])
def model_startup_competition(payload: Dict[str, Any]):
    """
    Analyzes direct overlaps, defensibility collisions, and crowding indices.
    """
    startup_a = payload.get("startup_a")
    startup_b = payload.get("startup_b")
    if not startup_a or not startup_b:
        raise HTTPException(status_code=400, detail="Missing parameters 'startup_a' or 'startup_b'")
    return StartupCompetitionModel.evaluate_competition(startup_a, startup_b)

@router.post("/portfolio/cross-analysis", response_model=Dict[str, Any], tags=["Sprint 9 - Portfolio Intelligence"])
def evaluate_cross_portfolio(payload: List[Dict[str, Any]]):
    """
    Maps interactions, cannibalization risks, and redundant coverage.
    """
    return CrossPortfolioAnalysis.evaluate_cross_portfolio(payload)

@router.post("/simulation/shock", response_model=Dict[str, Any], tags=["Sprint 9 - Strategic Simulation"])
def simulate_ecosystem_shock(payload: Dict[str, Any]):
    """
    Simulates systemic macro contractions, regulatory shocks, and AI substitute disruption impacts.
    """
    metrics = payload.get("metrics")
    shock_type = payload.get("shock_type")
    if not metrics or not shock_type:
        raise HTTPException(status_code=400, detail="Missing parameters 'metrics' or 'shock_type'")
    return EcosystemShockAnalysis.simulate_shock(metrics, shock_type)

@router.post("/forecasting/venture-12month", response_model=Dict[str, Any], tags=["Sprint 9 - Strategic Forecasting"])
def compile_venture_forecast(payload: Dict[str, Any]):
    """
    Projects 12-month scaling probabilities and investment readiness curves.
    """
    metrics = payload.get("metrics")
    if not metrics:
        raise HTTPException(status_code=400, detail="Missing parameter 'metrics'")
    return VentureForecast.compile_12_month_forecast(metrics)

@router.post("/forecasting/market-sector", response_model=Dict[str, Any], tags=["Sprint 9 - Strategic Forecasting"])
def run_market_simulation(payload: Dict[str, Any]):
    """
    Simulates sector growth under expansive or contractive capital regimes.
    """
    sector = payload.get("sector")
    regime = payload.get("macro_regime", "NEUTRAL")
    if not sector:
        raise HTTPException(status_code=400, detail="Missing parameter 'sector'")
    return MarketSimulationEngine.run_market_simulation(sector, regime)

@router.post("/reasoning/compare-batch", response_model=Dict[str, Any], tags=["Sprint 9 - Comparative Reasoning"])
def compare_startups_batch(payload: List[Dict[str, Any]]):
    """
    Produces side-by-side matrices contrasting attractiveness indices.
    """
    return MultiStartupReasoning.compare_multiple_startups(payload)

@router.post("/portfolio/exposure-analysis", response_model=Dict[str, Any], tags=["Sprint 9 - Portfolio Intelligence"])
def evaluate_portfolio_exposure(payload: List[Dict[str, Any]]):
    """
    Audits technology concentration and systemic founder risks.
    """
    return PortfolioExposureAnalysis.evaluate_portfolio_exposure(payload)

@router.get("/intelligence/cascade-detection", response_model=Dict[str, Any], tags=["Sprint 9 - Ecosystem Intelligence"])
def detect_ecosystem_cascades():
    """
    Traces and maps dependency cascade hazards in the knowledge graph.
    """
    return EcosystemCascadeDetection.evaluate_dependency_cascades()
