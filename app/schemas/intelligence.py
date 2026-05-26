from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field

class ExtractedField(BaseModel):
    value: Any = Field(description="The extracted data value, or 'UNVERIFIED' if absent.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score of the extraction.")
    verified: bool = Field(description="True if extracted deterministically or successfully mapped.")
    source_chunk: Optional[str] = Field(None, description="The chunk ID or slide where this was found.")

class StartupProfile(BaseModel):
    startup_name: ExtractedField
    sector: ExtractedField
    stage: ExtractedField
    headquarters: ExtractedField

class ProblemSolution(BaseModel):
    problem_statement: ExtractedField
    solution_overview: ExtractedField
    product_description: ExtractedField

class MarketInformation(BaseModel):
    tam_usd: ExtractedField
    sam_usd: ExtractedField
    som_usd: ExtractedField
    target_customers: ExtractedField

class TractionMetrics(BaseModel):
    mrr_usd: ExtractedField
    arr_usd: ExtractedField
    growth_rates: ExtractedField
    user_counts: ExtractedField

class FounderIntelligence(BaseModel):
    name: ExtractedField
    role: ExtractedField
    experience: ExtractedField
    technical_capability: ExtractedField

class StartupIntelligenceOutput(BaseModel):
    startup_profile: StartupProfile
    problem_and_solution: ProblemSolution
    market_information: MarketInformation
    traction_metrics: TractionMetrics
    founder_profiles: List[FounderIntelligence]
    missing_information: List[str] = Field(default_factory=list, description="Keys that were tagged as UNVERIFIED.")
    confidence_registry: Dict[str, float] = Field(default_factory=dict, description="Aggregate extraction confidence scores.")
