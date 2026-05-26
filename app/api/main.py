from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.endpoints.evaluation import router as eval_router
from app.endpoints.health import router as health_router
from app.middleware.error_handler import validation_exception_handler, global_exception_handler
import logging

# Configure base logging for the service layer
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def create_app() -> FastAPI:
    """Factory pattern to generate the master API instance."""
    app = FastAPI(
        title="Elephant Tank AI",
        description="Deterministic Startup Intelligence & Evaluation Engine",
        version="1.0.0"
    )
    
    # Bind custom error middleware
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
    
    # Bind routers
    from app.endpoints.ingestion import router as ingestion_router
    from app.endpoints.semantic_intelligence import router as semantic_router
    from app.endpoints.strategic_intelligence import router as strategic_router
    from app.endpoints.continuous_intelligence import router as continuous_router
    from app.endpoints.workflow_intelligence import router as workflow_router
    from app.endpoints.cross_ecosystem_simulation import router as simulation_router
    app.include_router(eval_router)
    app.include_router(ingestion_router)
    app.include_router(semantic_router)
    app.include_router(strategic_router)
    app.include_router(continuous_router)
    app.include_router(workflow_router)
    app.include_router(simulation_router)
    app.include_router(health_router)
    
    return app

# The standard entry point for Uvicorn (uvicorn app.api.main:app)
app = create_app()
