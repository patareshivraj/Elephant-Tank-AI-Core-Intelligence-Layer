import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

from app.memory.startup_memory import StartupMemoryEngine
from app.memory.founder_memory import FounderMemoryEngine
from app.knowledge_graph.venture_graph import VentureKnowledgeGraph
from app.memory.evaluation_history import EvaluationHistoryTracker
from app.intelligence.evolution_analysis import StartupEvolutionAnalyzer
from app.knowledge_graph.ecosystem_mapper import EcosystemRelationshipMapper
from app.intelligence.drift_detector import IntelligenceDriftDetector
from app.intelligence.comparative_analysis import ComparativeStartupIntelligence
from app.intelligence.continuous_updates import ContinuousIntelligenceUpdateEngine
from app.timeline.venture_timeline import VentureTimelineIntelligence

logger = logging.getLogger("ElephantTank.API.ContinuousIntelligence")
router = APIRouter()

# Schema declarations
class UpdateMemoryRequest(BaseModel):
    startup_name: str = Field(description="Name of the startup")
    overall_score: int = Field(default=75, ge=0, le=100)
    innovation_score: int = Field(default=8, ge=1, le=10)
    market_score: int = Field(default=7, ge=1, le=10)
    scalability_score: int = Field(default=7, ge=1, le=10)
    founder_score: int = Field(default=8, ge=1, le=10)
    funding_readiness_score: int = Field(default=7, ge=1, le=10)
    risks: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    confidence_score: int = Field(default=8, ge=1, le=10)
    target_stage: str = Field(default="Seed")
    sectors: List[str] = Field(default_factory=lambda: ["SaaS"])
    timing_verdict: str = Field(default="WELL_TIMED")
    founder_name: Optional[str] = Field(default=None)
    founder_technical_rating: int = Field(default=8, ge=1, le=10)
    founder_leadership_rating: int = Field(default=7, ge=1, le=10)

class CompareStartupsRequest(BaseModel):
    startup_a: Dict[str, Any] = Field(description="Profile parameters for Startup A")
    startup_b: Dict[str, Any] = Field(description="Profile parameters for Startup B")

class DriftCheckRequest(BaseModel):
    startup_name: str
    run_v1: int
    run_v2: int

@router.post("/memory/update", tags=["Memory & Continuous Intelligence"])
async def transactional_memory_update(request: UpdateMemoryRequest):
    """
    Triggers a transaction-safe continuous intelligence update.
    Updates persistent startup memory, founder timeline details, and graph connections.
    """
    logger.info(f"API request to update persistent states for: {request.startup_name}")
    try:
        eval_dict = request.model_dump()
        founder_metrics = {
            "technical_competence": request.founder_technical_rating,
            "leadership_index": request.founder_leadership_rating,
            "execution_velocity": request.founder_leadership_rating
        }
        
        result = ContinuousIntelligenceUpdateEngine.update_venture_intelligence(
            startup_name=request.startup_name,
            evaluation_results=eval_dict,
            founder_name=request.founder_name or "",
            founder_metrics=founder_metrics
        )
        return result
    except Exception as e:
        logger.error(f"Failed to commit continuous intelligence milestone: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/startup/{name}", tags=["Memory & Continuous Intelligence"])
async def get_startup_timeline_profile(name: str):
    """
    Fetches the persistent startup profile and chronological evaluation milestones.
    """
    history = StartupMemoryEngine.get_startup_history(name)
    if not history:
        raise HTTPException(status_code=404, detail=f"Venture profile '{name}' not found in persistent memory.")
    return history

@router.get("/memory/founder/{name}", tags=["Memory & Continuous Intelligence"])
async def get_founder_profile_timeline(name: str):
    """
    Fetches the persistent founder career timeline and leadership competence metrics.
    """
    history = FounderMemoryEngine.get_founder_history(name)
    if not history:
        raise HTTPException(status_code=404, detail=f"Founder profile '{name}' not found in persistent memory.")
    return history

@router.get("/knowledge-graph/traverse/{node}", tags=["Memory & Continuous Intelligence"])
async def traverse_knowledge_graph(node: str):
    """
    Traverses the Venture Knowledge Graph to find direct connections for an entity.
    """
    return VentureKnowledgeGraph.traverse_relations(node)

@router.get("/knowledge-graph/sector/{sector}", tags=["Memory & Continuous Intelligence"])
async def discover_sector_network(sector: str):
    """
    Discovers all clustered startup and technology connections operating within a sector.
    """
    return VentureKnowledgeGraph.discover_sector_subgraph(sector)

@router.post("/intelligence/compare", tags=["Memory & Continuous Intelligence"])
async def compare_startups_matrix(request: CompareStartupsRequest):
    """
    Produces side-by-side matrices contrasting startup scores, moats, and metrics.
    """
    return ComparativeStartupIntelligence.compare_startups(request.startup_a, request.startup_b)

@router.post("/intelligence/drift", tags=["Memory & Continuous Intelligence"])
async def check_trajectory_drift(request: DriftCheckRequest):
    """
    Measures trajectory score, founder execution, and confidence drift between two runs of a startup.
    """
    comp = EvaluationHistoryTracker.compare_runs(request.startup_name, request.run_v1, request.run_v2)
    if "error" in comp:
        raise HTTPException(status_code=400, detail=comp["error"])
        
    drift = IntelligenceDriftDetector.calculate_drift(
        {"overall_score": comp["score_shift"]["v1_score"], "metrics": comp["metric_shifts"]},
        {"overall_score": comp["score_shift"]["v2_score"], "metrics": comp["metric_shifts"]}
    )
    
    return {
        "comparison_metadata": comp["comparison_window"],
        "score_comparison": comp["score_shift"],
        "drift_metrics": drift
    }

@router.get("/timeline/{name}", tags=["Memory & Continuous Intelligence"])
async def get_milestone_timeline(name: str):
    """
    Retrieves chronological milestone trajectory details.
    """
    return VentureTimelineIntelligence.get_timeline(name)
