from pydantic import BaseModel, Field
from typing import List

class ExecutiveSummaryReport(BaseModel):
    executive_summary: str = Field(description="Concise 1-2 paragraph startup overview.")
    investment_potential: str = Field(description="VC-style analysis of the investment viability.")
    risk_summary: List[str]
    recommendations: List[str]
    due_diligence_questions: List[str]
    confidence_notes: List[str] = Field(description="Explicit notes on missing data or unverified assumptions.")

class InvestorReport(BaseModel):
    startup_overview: str
    problem_solution_analysis: str
    market_opportunity: str
    business_model_evaluation: str
    founder_intelligence: str
    risk_analysis: str
    competitive_intelligence: str
    funding_readiness: str
    recommendations: List[str]
    due_diligence_questions: List[str]
    confidence_notes: List[str]

class FounderReport(BaseModel):
    leadership_quality: str
    execution_readiness: str
    technical_capability: str
    domain_alignment: str
    strengths: List[str]
    weaknesses: List[str]
    confidence_notes: List[str]

class RiskReport(BaseModel):
    operational_risks: List[str]
    financial_risks: List[str]
    market_risks: List[str]
    competitive_risks: List[str]
    execution_risks: List[str]
    regulatory_risks: List[str]
    critical_mitigations: List[str]
