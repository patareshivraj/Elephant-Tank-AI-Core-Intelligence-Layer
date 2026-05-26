from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MatchReasoning(BaseModel):
    matched_entity_id: str = Field(description="Unique identifier from ChromaDB")
    matched_entity_name: str
    similarity_score: float = Field(description="Deterministic cosine similarity score (0.0 to 1.0)")
    match_reasoning: List[str] = Field(description="AI-generated contextual explanation of the match")

class RecommendationOutput(BaseModel):
    recommended_entities: List[str]
    similarity_scores: List[float]
    matching_reasons: List[MatchReasoning]
    confidence_scores: List[float] = Field(description="Confidence metrics based on semantic distance")
    metadata_filters_applied: Dict[str, str] = Field(description="The deterministic strict filters utilized (e.g. stage, sector)")
