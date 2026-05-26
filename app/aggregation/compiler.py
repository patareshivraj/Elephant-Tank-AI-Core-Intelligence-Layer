from typing import Dict, Any, List
from app.schemas.orchestration import UnifiedIntelligenceOutput, ExecutionLog

class IntelligenceCompiler:
    def compile_unified_output(
        self,
        pipeline_id: str,
        execution_logs: List[ExecutionLog],
        startup_profile: Dict[str, Any] = None,
        evaluation_results: Dict[str, Any] = None,
        founder_intelligence: Dict[str, Any] = None,
        risk_analysis: Dict[str, Any] = None,
        reports: Dict[str, Any] = None,
        semantic_matches: Dict[str, Any] = None
    ) -> UnifiedIntelligenceOutput:
        """
        Merges all isolated phase outputs into the master JSON contract.
        Handles missing components gracefully to support partial pipeline recovery.
        """
        # Centralize lists for ease of access
        recommendations = []
        if evaluation_results and "recommendations" in evaluation_results:
            recommendations.extend(evaluation_results.get("recommendations", []))
            
        confidence_summary = {
            "overall_confidence": evaluation_results.get("confidence_score", 0.0) if evaluation_results else 0.0
        }

        return UnifiedIntelligenceOutput(
            pipeline_id=pipeline_id,
            startup_profile=startup_profile or {},
            evaluation_results=evaluation_results or {},
            founder_intelligence=founder_intelligence or {},
            risk_analysis=risk_analysis or {},
            reports=reports or {},
            semantic_matches=semantic_matches or {},
            recommendations=recommendations,
            confidence_summary=confidence_summary,
            execution_logs=execution_logs
        )
