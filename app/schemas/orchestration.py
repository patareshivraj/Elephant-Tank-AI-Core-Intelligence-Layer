from pydantic import BaseModel, Field
from typing import Dict, Any, List

class ExecutionLog(BaseModel):
    stage: str
    status: str
    message: str
    timestamp: float

class UnifiedIntelligenceOutput(BaseModel):
    pipeline_id: str = Field(description="Unique UUID for this execution run")
    startup_profile: Dict[str, Any] = Field(default_factory=dict)
    evaluation_results: Dict[str, Any] = Field(default_factory=dict)
    founder_intelligence: Dict[str, Any] = Field(default_factory=dict)
    risk_analysis: Dict[str, Any] = Field(default_factory=dict)
    reports: Dict[str, Any] = Field(default_factory=dict)
    semantic_matches: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    confidence_summary: Dict[str, Any] = Field(default_factory=dict)
    execution_logs: List[ExecutionLog] = Field(default_factory=list)
