from pydantic import BaseModel, Field
from typing import List

class FounderPassport(BaseModel):
    founder_name: str = Field(description="Name of the primary founder or team")
    leadership_score: int = Field(ge=0, le=100, description="Evidence-based leadership score")
    technical_capability_score: int = Field(ge=0, le=100)
    execution_readiness_score: int = Field(ge=0, le=100)
    startup_experience_score: int = Field(ge=0, le=100)
    domain_expertise_score: int = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0.0, le=100.0, description="Penalty-adjusted confidence metric")
    strengths: List[str] = Field(description="Verifiable capability strengths")
    weaknesses: List[str] = Field(description="Verifiable capability gaps")
    risk_flags: List[str] = Field(description="Critical execution risks (e.g. Solo Founder)")
    recommendations: List[str] = Field(description="Advisory or hiring recommendations")
