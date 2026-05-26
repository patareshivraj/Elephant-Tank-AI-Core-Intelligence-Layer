import json
import logging
from typing import Dict, Any, List
from elephant_tank.schemas import (
    RawStartupInput,
    LLMQualitativeOutput,
    UniversalVentureReport,
    DimensionMetric,
    RiskItem,
)
from elephant_tank.groq_client import GroqEngineClient
from elephant_tank.deterministic_logic import compute_final_scores

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ElephantTank.Orchestrator")

class VentureScreeningOrchestrator:
    def __init__(self):
        self.groq_client = GroqEngineClient()

    def run_screening_pipeline(self, raw_input: RawStartupInput) -> UniversalVentureReport:
        """
        Executes the entire Elephant Tank screening pipeline:
        1. Ingests and sanitizes raw input (hallucination control injection).
        2. Routes sanitized payload to the LLM for qualitative reasoning.
        3. Validates structural output from LLM using Pydantic.
        4. Runs local deterministic logic to compute weights, confidence, and risk penalties.
        5. Performs a final merge and returns a validated UniversalVentureReport.
        """
        logger.info(f"--- Starting Venture Screening Pipeline for: '{raw_input.name}' ---")
        
        # Step 1: Preprocess and Sanitize (Hallucination Control Key Injection)
        sanitized_payload = self._preprocess_and_sanitize(raw_input)
        payload_str = json.dumps(sanitized_payload, indent=2)
        
        # Step 2: Route to Groq API
        raw_llm_response = self.groq_client.execute_venture_screening(payload_str)
        
        # Step 3: Validate LLM Qualitative Output
        logger.info("Validating qualitative AI outputs against intermediate schema...")
        qualitative_assessment = LLMQualitativeOutput(**raw_llm_response)
        
        # Step 4: Local Deterministic Scoring & Confidence Calculation
        logger.info("Calculating stage-weighted scores, completeness confidence, and risk penalties locally...")
        final_score, confidence_score, weighted_dimensions = compute_final_scores(
            raw_input,
            qualitative_assessment.dimension_scores,
            qualitative_assessment.risk_registry
        )
        
        # Step 5: Merge and Assemble the Universal Venture Report
        logger.info("Assembling final venture screening report...")
        
        compiled_dimensions: Dict[str, DimensionMetric] = {}
        for key in qualitative_assessment.dimension_scores.keys():
            raw_val = qualitative_assessment.dimension_scores[key]
            weighted_val = weighted_dimensions.get(key, 0.0)
            reasoning = qualitative_assessment.dimension_reasonings.get(key, "No explanation provided.")
            evidence = qualitative_assessment.dimension_evidences.get(key, [])
            limitations = qualitative_assessment.dimension_limitations.get(key, [])
            
            compiled_dimensions[key] = DimensionMetric(
                qualitative_score=raw_val,
                weighted_score=weighted_val,
                reasoning=reasoning,
                evidence=evidence,
                limitations=limitations
            )
            
        report = UniversalVentureReport(
            startup_name=raw_input.name,
            stage=raw_input.current_stage,
            overall_score=final_score,
            confidence_score=confidence_score,
            dimension_scores=compiled_dimensions,
            risk_registry=qualitative_assessment.risk_registry,
            strengths=qualitative_assessment.strengths,
            weaknesses=qualitative_assessment.weaknesses,
            due_diligence_questions=qualitative_assessment.due_diligence_questions,
            recommendations=qualitative_assessment.recommendations
        )
        
        logger.info(f"--- Pipeline successfully completed. Overall Score: {final_score}/10, Confidence: {confidence_score}/10 ---")
        return report

    def _preprocess_and_sanitize(self, raw_input: RawStartupInput) -> Dict[str, Any]:
        """
        Scans all optional fields in the raw Pydantic input.
        Converts any None value to 'UNVERIFIED' to instruct the LLM
        not to speculate or hallucinate metrics, but to penalize cleanly.
        """
        raw_dict = raw_input.model_dump()
        
        # Helper to convert None values recursively
        def convert_none_to_unverified(data: Any) -> Any:
            if isinstance(data, dict):
                return {k: convert_none_to_unverified(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [convert_none_to_unverified(i) for i in data]
            elif data is None:
                return "UNVERIFIED"
            return data

        sanitized = convert_none_to_unverified(raw_dict)
        return sanitized
