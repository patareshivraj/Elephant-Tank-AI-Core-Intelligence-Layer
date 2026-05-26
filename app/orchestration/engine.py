import asyncio
from typing import Dict, Any
from app.pipelines.startup_evaluation import StartupEvaluationPipeline

class AIOrchestrator:
    def __init__(self):
        self.startup_pipeline = StartupEvaluationPipeline()
        # self.semantic_pipeline = SemanticMatchingPipeline()
        # self.founder_pipeline = FounderPassportPipeline()
        
    async def run_startup_evaluation(self, file_path: str) -> Dict[str, Any]:
        """
        Triggers PIPELINE 1: The full end-to-end venture screening execution.
        """
        return await self.startup_pipeline.execute(file_path)

    async def run_semantic_matching(self, startup_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Triggers PIPELINE 2: Ecosystem discovery.
        """
        pass # Routes to isolated semantic pipeline

    async def run_founder_passport(self, resume_path: str) -> Dict[str, Any]:
        """
        Triggers PIPELINE 3: Founder analysis.
        """
        pass # Routes to isolated founder pipeline
