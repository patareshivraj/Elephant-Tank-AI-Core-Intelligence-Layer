import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

from app.governance.explainability_engine import ExplainabilityEngine
from app.governance.traceability import DecisionTraceabilityLayer
from app.governance.reasoning_lineage import ReasoningLineageTracker
from app.governance.governance_engine import AIGovernanceEngine
from app.governance.confidence_explainer import ConfidenceExplainabilityEngine
from app.governance.recommendation_provenance import RecommendationProvenanceSystem
from app.audit.audit_engine import InstitutionalAuditEngine
from app.compliance.compliance_validator import ComplianceValidator
from app.monitoring.governance_monitor import GovernanceMonitor

logger = logging.getLogger("ElephantTank.Endpoints.GovernanceIntelligence")

router = APIRouter()

@router.post("/governance/explain-score", response_model=Dict[str, Any], tags=["Sprint 10 - AI Governance"])
def explain_score(payload: Dict[str, Any]):
    """
    Exposes deterministic mathematical score deconstructions and justifications.
    """
    name = payload.get("startup_name")
    score = payload.get("overall_score")
    metrics = payload.get("metrics")
    if not name or score is None or not metrics:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name', 'overall_score', or 'metrics'")
    return ExplainabilityEngine.explain_score(name, float(score), metrics)

@router.post("/governance/traceability", response_model=Dict[str, Any], tags=["Sprint 10 - AI Governance"])
def compile_traceability_record(payload: Dict[str, Any]):
    """
    Compiles audited connections associating raw PDF/PPTX sources to decision assets.
    """
    name = payload.get("startup_name")
    docs = payload.get("source_documents", [])
    snippets = payload.get("evidence_snippets", [])
    if not name:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name'")
    return DecisionTraceabilityLayer.compile_traceability_record(name, docs, snippets)

@router.post("/governance/reasoning-lineage", response_model=Dict[str, Any], tags=["Sprint 10 - AI Governance"])
def record_reasoning_flow(payload: Dict[str, Any]):
    """
    Registers sequential logic nodes to preserve multi-step evidence lineage.
    """
    name = payload.get("startup_name")
    steps = payload.get("steps", [])
    if not name or not steps:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name' or 'steps'")
    return ReasoningLineageTracker.record_reasoning_flow(name, steps)

@router.post("/governance/policy-audit", response_model=Dict[str, Any], tags=["Sprint 10 - AI Governance"])
def audit_and_governance(payload: Dict[str, Any]):
    """
    Enforces operational hallucination guardrails and evidence threshold policies.
    """
    return AIGovernanceEngine.audit_and_governance(payload)

@router.post("/governance/explain-confidence", response_model=Dict[str, Any], tags=["Sprint 10 - AI Governance"])
def explain_confidence(payload: Dict[str, Any]):
    """
    Decomposes confidence scores to map parameter omissions.
    """
    name = payload.get("startup_name")
    score = payload.get("confidence_score")
    gaps = payload.get("data_gaps", 0)
    if not name or score is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name' or 'confidence_score'")
    return ConfidenceExplainabilityEngine.explain_confidence(name, int(score), int(gaps))

@router.post("/governance/recommendation-provenance", response_model=Dict[str, Any], tags=["Sprint 10 - AI Governance"])
def compile_provenance(payload: Dict[str, Any]):
    """
    Anchors VC recommendation verdicts directly to structural indices.
    """
    name = payload.get("startup_name")
    rec = payload.get("recommendation")
    triggers = payload.get("evidence_triggers", [])
    if not name or not rec:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name' or 'recommendation'")
    return RecommendationProvenanceSystem.compile_provenance(name, rec, triggers)

@router.post("/governance/log-audit", response_model=Dict[str, Any], tags=["Sprint 10 - System Audit"])
def record_audit_entry(payload: Dict[str, Any]):
    """
    Appends structured validation audits and verification traces to persistent JSON files.
    """
    name = payload.get("startup_name")
    details = payload.get("payload")
    if not name or not details:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name' or 'payload'")
    return InstitutionalAuditEngine.record_audit_entry(name, details)

@router.post("/governance/compliance-validate", response_model=Dict[str, Any], tags=["Sprint 10 - Compliance Validation"])
def validate_compliance(payload: Dict[str, Any]):
    """
    Audits schema consistency bounds and compliance values.
    """
    return ComplianceValidator.validate_compliance(payload)

@router.post("/governance/monitor-drift", response_model=Dict[str, Any], tags=["Sprint 10 - Governance Monitoring"])
def evaluate_governance_drift(payload: Dict[str, Any]):
    """
    Scans sequential rating histories to alert on metric drift variance.
    """
    name = payload.get("startup_name")
    history = payload.get("history", [])
    if not name or not history:
        raise HTTPException(status_code=400, detail="Missing parameter 'startup_name' or 'history'")
    return GovernanceMonitor.evaluate_governance_drift(name, history)
