from pydantic import BaseModel, Field
from typing import Dict, Any, List

class OptimizationReport(BaseModel):
    pipeline_latency: Dict[str, float] = Field(description="Millisecond latency breakdowns per module")
    groq_performance: Dict[str, Any] = Field(description="Token usage, API response times, and model routing choices")
    embedding_performance: Dict[str, Any] = Field(description="ChromaDB and SentenceTransformer retrieval times")
    cache_statistics: Dict[str, Any] = Field(description="Hit/Miss ratios and storage metrics")
    memory_usage: Dict[str, Any] = Field(description="Peak RAM utilization during the pipeline run")
    bottlenecks: List[str] = Field(description="Identified modules exceeding target latency thresholds")
    optimization_recommendations: List[str] = Field(description="Automated suggestions for improving throughput")
    system_health: Dict[str, Any] = Field(default_factory=dict)
