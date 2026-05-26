import os
import time
import shutil
import logging
import re
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.pdf_parser import PDFExtractor
from app.ingestion.ppt_parser import PPTXExtractor
from app.processing.text_cleaner import TextCleaner
from app.processing.startup_structurer import StartupStructurer
from app.endpoints.evaluation import evaluate_startup
from app.contracts.api_schemas import StartupEvaluationRequest, StartupEvaluationResponse

from app.ingestion.resume_parser import ResumeExtractor

logger = logging.getLogger("ElephantTank.API.Ingestion")
router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-startup-documents", response_model=StartupEvaluationResponse, tags=["Document Intelligence Ingestion"])
async def upload_startup_documents(file: UploadFile = File(...)):
    """
    Accepts a pitch deck, PDF, PPTX, or txt file.
    Intelligently detects if it is a Resume or Pitch Deck, extracts text, structures the intelligence,
    and routes it to the deterministic evaluation pipeline.
    """
    logger.info(f"Received file upload: {file.filename}")
    
    ext = file.filename.split(".")[-1].lower()
    allowed_exts = ["pdf", "ppt", "pptx", "txt"]
    
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {ext}. Allowed: {allowed_exts}")
        
    # Save file locally
    file_path = os.path.join(UPLOAD_DIR, f"{int(time.time())}_{file.filename}")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save uploaded document.")
        
    # 1. Extraction Routing
    try:
        raw_text = ""
        if ext == "pdf":
            raw_text = PDFExtractor.extract_text(file_path)
        elif ext in ["ppt", "pptx"]:
            raw_text = PPTXExtractor.extract_text(file_path)
        elif ext == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
                
        if not raw_text.strip():
            raise ValueError("No text could be extracted from the document. The file might be an image-only PDF without OCR.")
            
    except Exception as e:
        logger.error(f"Document extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
        
    # 2. Text Cleaning Pipeline
    logger.info("Cleaning extracted document text...")
    clean_text = TextCleaner.clean(raw_text)
    
    # 3. Intelligent Ingestion Routing (Resume vs. Pitch Deck)
    filename_lower = file.filename.lower()
    is_resume = "resume" in filename_lower or "cv" in filename_lower or "curriculum" in filename_lower or len(re.findall(r"(experience|education|skills|employment|jobs)", clean_text.lower())) > 3
    
    structured_data = {}
    if is_resume:
        logger.info("Intelligent Router: Resume detected! Executing resume intelligence parser...")
        try:
            resume_data = ResumeExtractor.extract_founder_intelligence(clean_text)
            structured_data = {
                "startup_name": f"{resume_data.get('founder_name', 'Unknown')}'s Venture Initiative",
                "startup_description": resume_data.get("founder_summary", "Unverified project. Initiated via Resume/CV parsing profile."),
                "target_stage": "Pre-seed",
                "founder_data": f"Founder Name: {resume_data.get('founder_name')}. Skills: {', '.join(resume_data.get('technical_skills', []))}. History: {', '.join(resume_data.get('startup_history', []))}."
            }
        except Exception as e:
            logger.error(f"Resume parsing failed: {e}")
            raise HTTPException(status_code=500, detail=f"Resume intelligence parsing failed: {str(e)}")
    else:
        logger.info("Intelligent Router: Standard pitch deck or description detected. Executing structurer...")
        try:
            structured_data = StartupStructurer.structure_startup_text(clean_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Structuring failed: {str(e)}")
        
    # 4. Routing to Core Deterministic Evaluation Engine
    logger.info(f"Routing structured data to evaluation engine: {structured_data.get('startup_name')}")
    eval_req = StartupEvaluationRequest(
        startup_name=structured_data.get("startup_name", "Unknown Startup"),
        startup_description=structured_data.get("startup_description", ""),
        target_stage=structured_data.get("target_stage", "Pre-seed"),
        founder_data=structured_data.get("founder_data", "")
    )
    
    # Trigger the existing evaluation logic programmatically
    res = await evaluate_startup(eval_req)
    
    # 5. Dynamic Semantic Indexing
    try:
        from app.semantic.index_manager import IndexManager
        import uuid
        startup_id = f"st_{uuid.uuid4().hex[:12]}"
        IndexManager.index_startup(startup_id, structured_data)
        logger.info(f"Dynamically indexed startup '{structured_data.get('startup_name')}' as {startup_id}.")
    except Exception as e:
        logger.error(f"Failed to dynamically index startup into vector database: {e}")
        
    return res
