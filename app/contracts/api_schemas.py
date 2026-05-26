from pydantic import BaseModel, Field
from typing import Dict, Any, List

class ErrorResponse(BaseModel):
    error_type: str = Field(description="Categorical error code (e.g., VALIDATION_ERROR, GROQ_TIMEOUT)")
    message: str
    module: str = Field(description="The internal system module where the error occurred")
    validation_errors: List[str] = Field(default_factory=list)
    recovery_suggestions: List[str] = Field(default_factory=list)

class StartupEvaluationRequest(BaseModel):
    startup_name: str = Field(description="Name of the startup")
    startup_description: str = Field(description="Core pitch or parsed document text")
    founder_data: str = Field(default=None, description="Optional founder background context")
    target_stage: str = Field(default="Pre-seed", description="Stage used for weighting (Pre-seed, Seed, Series A)")

class HealthResponse(BaseModel):
    system_status: str
    groq_status: str
    vector_db_status: str
    pipeline_integrity: bool

class StartupProfile(BaseModel):
    startup_name: str
    target_stage: str

class EvaluationResults(BaseModel):
    innovation_score: float = Field(ge=0.0, le=100.0)
    market_score: float = Field(ge=0.0, le=100.0)
    scalability_score: float = Field(ge=0.0, le=100.0)
    founder_score: float = Field(ge=0.0, le=100.0)
    funding_readiness_score: float = Field(ge=0.0, le=100.0)

class FounderIntelligence(BaseModel):
    strengths: List[str]
    weaknesses: List[str]

class RiskAnalysis(BaseModel):
    risks: List[str]

class ConfidenceSummary(BaseModel):
    overall_confidence: float = Field(ge=0.0, le=100.0)

class StartupEvaluationResponse(BaseModel):
    pipeline_id: str
    startup_profile: StartupProfile
    evaluation_results: EvaluationResults
    founder_intelligence: FounderIntelligence
    risk_analysis: RiskAnalysis
    recommendations: List[str]
    confidence_summary: ConfidenceSummary
    execution_logs: List[str]
