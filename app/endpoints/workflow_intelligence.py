import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

from app.workflow.venture_orchestrator import VentureOrchestrator
from app.workflow.startup_prioritizer import StartupPrioritizer
from app.decision_support.investment_decision_engine import InvestmentDecisionEngine
from app.decision_support.escalation_engine import StrategicEscalationEngine
from app.monitoring.venture_monitor import VentureMonitor
from app.monitoring.readiness_monitor import InvestmentReadinessMonitor
from app.monitoring.founder_risk_monitor import FounderRiskMonitor
from app.alerts.ecosystem_alerts import EcosystemOpportunityAlerts
from app.portfolio.portfolio_intelligence import PortfolioIntelligence

logger = logging.getLogger("ElephantTank.Endpoints.WorkflowIntelligence")

router = APIRouter()

@router.post("/workflow/enqueue", response_model=Dict[str, Any], tags=["Sprint 8 - Workflow Orchestration"])
def enqueue_startup(payload: Dict[str, Any]):
    """
    Enrolls a startup into the review pipeline and review queue.
    """
    name = payload.get("startup_name")
    if not name:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name'")
    stage = payload.get("stage", "IN_REVIEW")
    return VentureOrchestrator.initialize_pipeline(name, stage)

@router.post("/workflow/transition", response_model=Dict[str, Any], tags=["Sprint 8 - Workflow Orchestration"])
def transition_startup_state(payload: Dict[str, Any]):
    """
    Transitions review stage queues with tracked rationales.
    """
    name = payload.get("startup_name")
    new_state = payload.get("new_state")
    rationale = payload.get("rationale", "Manual administrative queue shift.")
    if not name or not new_state:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name' or 'new_state'")
    return VentureOrchestrator.transition_state(name, new_state, rationale)

@router.post("/workflow/prioritize", response_model=List[Dict[str, Any]], tags=["Sprint 8 - Workflow Orchestration"])
def prioritize_startup_batch(payload: List[Dict[str, Any]]):
    """
    Ranks startups using weighted scoring, founder ratings, and GTM timing.
    """
    return StartupPrioritizer.prioritize_pipeline(payload)

@router.post("/workflow/decision", response_model=Dict[str, Any], tags=["Sprint 8 - Decision Support"])
def evaluate_investment_decision(payload: Dict[str, Any]):
    """
    Generates explainable investment signal verdicts and strategic caution flags.
    """
    return InvestmentDecisionEngine.evaluate_investment_decision(payload)

@router.post("/workflow/escalation-check", response_model=Dict[str, Any], tags=["Sprint 8 - Decision Support"])
def trigger_escalation_rules(payload: Dict[str, Any]):
    """
    Evaluates metric drops to trigger severity-aware escalations.
    """
    name = payload.get("startup_name")
    curr = payload.get("current_metrics")
    prev = payload.get("previous_metrics")
    if not name or not curr or not prev:
        raise HTTPException(status_code=400, detail="Missing 'startup_name', 'current_metrics', or 'previous_metrics'")
    return StrategicEscalationEngine.evaluate_escalation_rules(name, curr, prev)

@router.get("/workflow/monitor/{name}", response_model=Dict[str, Any], tags=["Sprint 8 - Automated Monitoring"])
def monitor_startup_changes(name: str):
    """
    Scans entire milestone history to compile status warning notifications.
    """
    return VentureMonitor.monitor_startup(name)

@router.post("/workflow/readiness", response_model=Dict[str, Any], tags=["Sprint 8 - Automated Monitoring"])
def evaluate_fundraising_readiness(payload: Dict[str, Any]):
    """
    Assesses high GTM preparedness and investability ratios.
    """
    return InvestmentReadinessMonitor.evaluate_readiness(payload)

@router.get("/workflow/founder-risk/{name}", response_model=Dict[str, Any], tags=["Sprint 8 - Automated Monitoring"])
def monitor_founder_risk_levels(name: str):
    """
    Scans dependency indices and execution drift parameters.
    """
    return FounderRiskMonitor.evaluate_founder_risks(name)

@router.get("/workflow/ecosystem-alerts", response_model=List[Dict[str, Any]], tags=["Sprint 8 - Opportunity Alerts"])
def scan_ecosystem_whitespace():
    """
    Surfaces emerging opportunity clusters and underserved sectors inside the graph.
    """
    return EcosystemOpportunityAlerts.scan_for_opportunities()

@router.post("/workflow/portfolio-analysis", response_model=Dict[str, Any], tags=["Sprint 8 - Portfolio Intelligence"])
def evaluate_portfolio_metrics(payload: List[Dict[str, Any]]):
    """
    Analyzes average allocation valuations and sector risk concentrations.
    """
    return PortfolioIntelligence.analyze_portfolio(payload)
