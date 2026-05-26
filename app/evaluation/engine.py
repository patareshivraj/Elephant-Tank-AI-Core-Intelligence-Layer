import json
import logging
from typing import Dict, Any

from app.routing.router import PromptRouter
from app.llm.client import GroqReasoningClient
from app.schemas.reasoning import StartupReasoningResponse, RiskAnalysisResponse

logger = logging.getLogger("ElephantTank.EvaluationEngine")

class ReasoningEngine:
    def __init__(self):
        self.router = PromptRouter()
        self.client = GroqReasoningClient()

    def evaluate_startup(self, structured_startup_json: str) -> StartupReasoningResponse:
        """
        Executes the Phase 2 Startup Evaluation task.
        Takes structured JSON from Phase 1, runs VC analysis, and validates against Pydantic.
        """
        logger.info("Initializing STARTUP_EVALUATION reasoning loop...")
        
        # 1. Route and Hydrate Prompt
        messages = self.router.route_task(
            task_name="startup_evaluation",
            startup_json=structured_startup_json
        )
        
        # 2. Execute against LLM (Strict Mode)
        raw_output = self.client.execute_prompt(messages, mode="STARTUP_EVALUATION")
        
        # 3. Pydantic Contract Validation
        logger.info("Validating AI response against strict reasoning schemas...")
        try:
            validated_response = StartupReasoningResponse(**raw_output)
            return validated_response
        except Exception as e:
            logger.error(f"Schema validation failed. AI Output broke structural constraints: {e}")
            raise ValueError("LLM Output breached structured schema contracts.") from e

    def execute_custom_task(self, task_name: str, mode: str, schema_class, **kwargs):
        """
        Generic evaluation pipeline for Founders, Risk, or Executive Summaries.
        """
        messages = self.router.route_task(task_name=task_name, **kwargs)
        raw_output = self.client.execute_prompt(messages, mode=mode)
        
        if schema_class:
            return schema_class(**raw_output)
        return raw_output
