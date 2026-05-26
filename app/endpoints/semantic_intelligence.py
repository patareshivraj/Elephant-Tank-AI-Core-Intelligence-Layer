import logging
import time
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.matching.startup_similarity import StartupSimilarityEngine
from app.matching.investor_matcher import InvestorMatcherEngine
from app.matching.mentor_matcher import MentorMatcherEngine
from app.semantic.ecosystem_intelligence import EcosystemIntelligenceEngine
from app.semantic.index_manager import IndexManager

logger = logging.getLogger("ElephantTank.API.SemanticIntelligence")
router = APIRouter()

# --- Request / Response Schemas ---

class SimilarityRequest(BaseModel):
    startup_description: str = Field(..., description="Unstructured pitch description of the startup.")
    limit: Optional[int] = Field(3, description="Maximum similar startups to retrieve.")

class SimilarityResponse(BaseModel):
    similar_startups: List[Dict[str, Any]]
    related_market_categories: List[str]
    overlapping_business_models: List[str]
    ecosystem_patterns: List[str]
    execution_logs: List[Dict[str, Any]]

class MatchRequest(BaseModel):
    target_stage: str = Field(..., description="Startup developmental stage (e.g. Pre-seed, Seed, Series A).")
    startup_description: str = Field(..., description="Unstructured startup description to compute semantic fit.")
    limit: Optional[int] = Field(3, description="Maximum candidates to return.")

class InvestorMatchResponse(BaseModel):
    matches: List[Dict[str, Any]]
    execution_logs: List[Dict[str, Any]]

class MentorMatchResponse(BaseModel):
    matches: List[Dict[str, Any]]
    execution_logs: List[Dict[str, Any]]

class EcosystemResponse(BaseModel):
    active_market_clusters: List[Dict[str, Any]]
    ecosystem_insights: List[str]
    execution_logs: List[Dict[str, Any]]

# --- API Routes ---

@router.post("/similarity", response_model=SimilarityResponse, tags=["Semantic Ecosystem Intelligence"])
async def get_startup_similarity(req: SimilarityRequest):
    """
    Retrieves semantically similar startups, infers overlapping business models,
    and maps adjacent tech clusters using cosine vector matching.
    """
    logger.info("Received request for startup similarity check...")
    try:
        start_time = time.time()
        res = StartupSimilarityEngine.evaluate_similarity(req.startup_description, limit=req.limit)
        
        logs = [
            {
                "stage": "SEMANTIC_SIMILARITY",
                "status": "SUCCESS",
                "message": f"Successfully calculated cosine similarity across startups index in {time.time() - start_time:.3f}s.",
                "timestamp": int(time.time())
            }
        ]
        return SimilarityResponse(
            similar_startups=res["similar_startups"],
            related_market_categories=res["related_market_categories"],
            overlapping_business_models=res["overlapping_business_models"],
            ecosystem_patterns=res["ecosystem_patterns"],
            execution_logs=logs
        )
    except Exception as e:
        logger.error(f"Similarity mapping failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match-investors", response_model=InvestorMatchResponse, tags=["Ecosystem Matching"])
async def match_investors(req: MatchRequest):
    """
    Aligns a startup's stage and description with indexed venture capital profiles 
    to retrieve deterministic match ratings and explainable reasoning.
    """
    logger.info("Received request for investor matchmaking...")
    try:
        start_time = time.time()
        matches = InvestorMatcherEngine.match_investors(req.target_stage, req.startup_description, limit=req.limit)
        
        logs = [
            {
                "stage": "INVESTOR_MATCHING",
                "status": "SUCCESS",
                "message": f"Retrieved top {len(matches)} investor matches from active vector database index.",
                "timestamp": int(time.time())
            }
        ]
        return InvestorMatchResponse(matches=matches, execution_logs=logs)
    except Exception as e:
        logger.error(f"Investor matchmaking failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match-mentors", response_model=MentorMatchResponse, tags=["Ecosystem Matching"])
async def match_mentors(req: MatchRequest):
    """
    Maps early-stage startups to aligned industry advisors, serial founders, and experts.
    """
    logger.info("Received request for mentor matchmaking...")
    try:
        start_time = time.time()
        matches = MentorMatcherEngine.match_mentors(req.target_stage, req.startup_description, limit=req.limit)
        
        logs = [
            {
                "stage": "MENTOR_MATCHING",
                "status": "SUCCESS",
                "message": f"Retrieved top {len(matches)} mentor matches from active vector database index.",
                "timestamp": int(time.time())
            }
        ]
        return MentorMatchResponse(matches=matches, execution_logs=logs)
    except Exception as e:
        logger.error(f"Mentor matchmaking failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ecosystem-analysis", response_model=EcosystemResponse, tags=["Semantic Ecosystem Intelligence"])
async def get_ecosystem_analysis():
    """
    Performs real-time pairwise cosine distance mapping to discover ecosystem relations 
    and output active market clusters.
    """
    logger.info("Received request for dynamic ecosystem clustering...")
    try:
        start_time = time.time()
        res = EcosystemIntelligenceEngine.analyze_ecosystem()
        
        logs = [
            {
                "stage": "ECOSYSTEM_ANALYSIS",
                "status": "SUCCESS",
                "message": f"Successfully mapped and cataloged ecosystem vectors in {time.time() - start_time:.3f}s.",
                "timestamp": int(time.time())
            }
        ]
        return EcosystemResponse(
            active_market_clusters=res["active_market_clusters"],
            ecosystem_insights=res["ecosystem_insights"],
            execution_logs=logs
        )
    except Exception as e:
        logger.error(f"Ecosystem clustering failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-indices", tags=["Vector Index Management"])
async def reset_indices():
    """
    Resets all vector collections (dropping active indices) and seeds default high-fidelity ecosystem resources.
    """
    logger.info("Received index rebuild/reset request...")
    try:
        IndexManager.reset_all_indices()
        return {"status": "SUCCESS", "message": "Successfully wiped all indexes and re-seeded default ecosystem entities."}
    except Exception as e:
        logger.error(f"Index rebuild failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
