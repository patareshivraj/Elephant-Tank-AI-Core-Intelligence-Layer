import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.contracts.api_schemas import ErrorResponse

logger = logging.getLogger("ElephantTank.API.ErrorHandler")

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Traps FastAPI payload validation errors and forces them into our deterministic contract."""
    errors = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    
    error_payload = ErrorResponse(
        error_type="PAYLOAD_VALIDATION_ERROR",
        message="The provided JSON payload does not match the required schema.",
        module="API_ROUTER",
        validation_errors=errors,
        recovery_suggestions=["Ensure all required keys are present and data types are correct."]
    )
    logger.warning(f"Validation failure on {request.url}")
    return JSONResponse(status_code=422, content=error_payload.model_dump())

async def global_exception_handler(request: Request, exc: Exception):
    """Traps uncaught backend exceptions (e.g., pipeline crashes, Groq timeouts) gracefully."""
    error_payload = ErrorResponse(
        error_type="INTERNAL_SYSTEM_ERROR",
        message="The intelligence pipeline encountered an unrecoverable failure.",
        module="CORE_ENGINE",
        validation_errors=[str(exc)],
        recovery_suggestions=["Check API keys, database connectivity, or system logs."]
    )
    logger.error(f"System crash on {request.url}: {str(exc)}")
    return JSONResponse(status_code=500, content=error_payload.model_dump())
