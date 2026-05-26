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
    innovation_score: int = Field(ge=1, le=10)
    market_score: int = Field(ge=1, le=10)
    scalability_score: int = Field(ge=1, le=10)
    founder_score: int = Field(ge=1, le=10)
    funding_readiness_score: int = Field(ge=1, le=10)
    overall_score: int = Field(ge=0, le=100, description="Calculated locally by deterministic Python logic")

class ReasoningTraces(BaseModel):
    innovation_reasoning: List[str]
    market_reasoning: List[str]
    scalability_reasoning: List[str]
    founder_reasoning: List[str]

class FounderIntelligence(BaseModel):
    strengths: List[str]
    weaknesses: List[str]

class RiskAnalysis(BaseModel):
    risks: List[str]

class ConfidenceSummary(BaseModel):
    overall_confidence: int = Field(ge=1, le=10)

class ExecutionLog(BaseModel):
    stage: str
    status: str
    message: str
    timestamp: int

class StartupEvaluationResponse(BaseModel):
    pipeline_id: str
    startup_profile: StartupProfile
    evaluation_results: EvaluationResults
    reasoning_traces: ReasoningTraces
    founder_intelligence: FounderIntelligence
    risk_analysis: RiskAnalysis
    recommendations: List[str]
    due_diligence_questions: List[str]
    confidence_summary: ConfidenceSummary
    execution_logs: List[ExecutionLog]
