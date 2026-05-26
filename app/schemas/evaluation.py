from typing import List, Dict
from pydantic import BaseModel, Field

class EvaluatedDimension(BaseModel):
    raw_score: float = Field(description="Qualitative LLM score (1-10)")
    weighted_score: float = Field(description="Calculated deterministic score")
    reasoning_traces: List[str] = Field(description="Evidence backing the score")

class FundingReadiness(BaseModel):
    classification: str = Field(description="Idea, Pre-Seed Ready, Seed Ready, Series A Ready, Growth")
    justification: str

class RiskItem(BaseModel):
    category: str
    severity: str
    business_impact: str
    mitigation: str

class VentureIntelligenceOutput(BaseModel):
    startup_name: str
    overall_score: float = Field(ge=0.0, le=100.0, description="Final risk-adjusted weighted score")
    confidence_score: float = Field(ge=0.0, le=100.0, description="Completeness grading")
    funding_readiness: FundingReadiness
    scoring_interpretation: str = Field(description="Verbal classification of the 0-100 score")
    
    dimension_scores: Dict[str, EvaluatedDimension]
    risk_registry: List[RiskItem]
    
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    due_diligence_questions: List[str]
