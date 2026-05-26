from pydantic import BaseModel, Field
from typing import List, Dict, Any

class QAStatusReport(BaseModel):
    validation_status: str = Field(description="PASSED, FAILED, or WARNING")
    schema_validation: Dict[str, Any] = Field(description="Results of Pydantic type checking")
    hallucination_flags: List[str] = Field(description="Detected hallucinations between input and narrative output")
    confidence_validation: Dict[str, Any] = Field(description="Checks if missing data correctly triggered penalties")
    scoring_consistency: Dict[str, Any] = Field(description="Measures score drift against benchmark baselines")
    pipeline_integrity: Dict[str, Any] = Field(description="Validates if all stages executed correctly")
    recommendation_quality: Dict[str, Any] = Field(default_factory=dict)
    semantic_retrieval_quality: Dict[str, Any] = Field(default_factory=dict)
    execution_logs: List[str] = Field(default_factory=list)
