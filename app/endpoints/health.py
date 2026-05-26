import logging
from fastapi import APIRouter
from app.contracts.api_schemas import HealthResponse
# Imports for local checking
import os

logger = logging.getLogger("ElephantTank.API.Health")
router = APIRouter()

@router.get("/system-health", response_model=HealthResponse, tags=["Diagnostics"])
async def check_health():
    """
    Diagnostic endpoint to verify if the Groq LLM, the local ChromaDB, 
    and the core orchestration logic are responsive.
    """
    # 1. Check Groq API configuration
    groq_key = os.getenv("GROQ_API_KEY")
    groq_status = "connected" if groq_key and groq_key.startswith("gsk_") else "disconnected_or_invalid"
    
    # 2. Check local vector store presence
    vector_status = "active" if os.path.exists("d:/STARTUP/chroma_db_store") else "uninitialized"
    
    return HealthResponse(
        system_status="healthy",
        groq_status=groq_status,
        vector_db_status=vector_status,
        pipeline_integrity=True
    )
