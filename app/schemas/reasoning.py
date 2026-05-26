from typing import List, Dict
from pydantic import BaseModel, Field

class StartupEvaluationScores(BaseModel):
    innovation_score: int = Field(ge=1, le=10)
    market_potential_score: int = Field(ge=1, le=10)
    scalability_score: int = Field(ge=1, le=10)
    revenue_viability_score: int = Field(ge=1, le=10)
    founder_capability_score: int = Field(ge=1, le=10)
    competition_risk_score: int = Field(ge=1, le=10)
    funding_readiness_score: int = Field(ge=1, le=10)

class StartupEvaluationTraces(BaseModel):
    innovation_traces: List[str]
    market_potential_traces: List[str]
    scalability_traces: List[str]
    revenue_viability_traces: List[str]
    founder_capability_traces: List[str]
    competition_risk_traces: List[str]
    funding_readiness_traces: List[str]

class StartupReasoningResponse(BaseModel):
    dimension_scores: StartupEvaluationScores
    dimension_reasoning_traces: StartupEvaluationTraces
    strengths: List[str]
    weaknesses: List[str]
    due_diligence_questions: List[str]

class RiskRegistryItem(BaseModel):
    risk_category: str = Field(description="Operational, Financial, Market, Competitive, Regulatory, Execution")
    severity: str = Field(description="High, Medium, Low")
    explanation: str
    mitigation_suggestion: str

class RiskAnalysisResponse(BaseModel):
    risk_registry: List[RiskRegistryItem]
