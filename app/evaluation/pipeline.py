import logging
from typing import Dict, Any, List
from app.scoring.engine import ScoringEngine
from app.risk_engine.analyzer import RiskAnalyzer
from app.confidence.calculator import ConfidenceCalculator
from app.funding_readiness.classifier import ReadinessClassifier
from app.schemas.evaluation import (
    VentureIntelligenceOutput,
    EvaluatedDimension,
    FundingReadiness,
    RiskItem
)

logger = logging.getLogger("ElephantTank.IntelligenceEngine")

class VentureIntelligencePipeline:
    def __init__(self):
        self.scoring = ScoringEngine()
        self.risk = RiskAnalyzer()
        self.confidence = ConfidenceCalculator()
        self.readiness = ReadinessClassifier()

    def generate_intelligence_report(
        self, 
        startup_name: str,
        stage: str,
        raw_llm_scores: Dict[str, float],
        llm_reasoning_traces: Dict[str, List[str]],
        risk_registry_payload: List[Dict[str, str]],
        missing_fields: List[str],
        strengths: List[str],
        weaknesses: List[str],
        recommendations: List[str],
        due_diligence_questions: List[str]
    ) -> VentureIntelligenceOutput:
        """
        Orchestrates Phase 3: Transforms LLM qualitative reasoning into deterministic numerical reality.
        """
        logger.info("Executing Deterministic Intelligence Aggregation...")
        
        # 1. Deterministic Scores (0-100 scale)
        base_weighted_score, weighted_breakdown = self.scoring.compute_weighted_aggregate(raw_llm_scores, stage)
        
        # 2. Compile Risk Deductions
        risk_penalty = self.risk.calculate_risk_penalty(risk_registry_payload)
        
        # 3. Compile Confidence Completeness Score
        confidence_score = self.confidence.calculate_confidence(missing_fields)
        
        # 4. Final Aggregation
        final_overall_score = max(0.0, min(100.0, base_weighted_score - risk_penalty))
        interpretation = self.scoring.interpret_score(final_overall_score)
        
        # 5. Funding Readiness Classification
        maturity = self.readiness.determine_funding_readiness(final_overall_score, confidence_score, stage)
        
        # Assemble Structured Output
        compiled_dimensions = {}
        for dim, raw_val in raw_llm_scores.items():
            compiled_dimensions[dim] = EvaluatedDimension(
                raw_score=raw_val,
                weighted_score=weighted_breakdown.get(dim, 0.0),
                reasoning_traces=llm_reasoning_traces.get(dim, [])
            )
            
        compiled_risks = [RiskItem(**r) for r in risk_registry_payload]
        
        report = VentureIntelligenceOutput(
            startup_name=startup_name,
            overall_score=final_overall_score,
            confidence_score=confidence_score,
            funding_readiness=FundingReadiness(**maturity),
            scoring_interpretation=interpretation,
            dimension_scores=compiled_dimensions,
            risk_registry=compiled_risks,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            due_diligence_questions=due_diligence_questions
        )
        
        logger.info(f"Phase 3 Pipeline Complete. Final Score: {final_overall_score}/100")
        return report
