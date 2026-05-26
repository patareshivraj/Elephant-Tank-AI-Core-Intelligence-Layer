import logging
from fastapi import APIRouter, BackgroundTasks
from app.contracts.api_schemas import StartupEvaluationRequest, ErrorResponse
from app.orchestration.engine import AIOrchestrator

logger = logging.getLogger("ElephantTank.API.Evaluation")
router = APIRouter()
orchestrator = AIOrchestrator()

@router.post("/evaluate-startup", tags=["Evaluation Pipeline"])
async def evaluate_startup(request: StartupEvaluationRequest):
    """
    Primary ingestion endpoint. Receives a startup profile, validates it, 
    and triggers the deterministic Phase 1 -> Phase 7 evaluation pipeline.
    """
    logger.info(f"Received Evaluation Request for: {request.startup_name}")
    
    # In a full production implementation, 'request.startup_description' would be saved to disk
    # or passed directly as a string into the orchestrator logic.
    # For architecture demonstration, we pass a simulated file path string identifier.
    
    try:
        pipeline_output = await orchestrator.run_startup_evaluation(file_path=request.startup_description)
        return pipeline_output
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        # This will be caught by the global_exception_handler if raised
        raise e
