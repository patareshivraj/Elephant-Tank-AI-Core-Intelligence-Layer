import logging
import os
import json
from fastapi import APIRouter, HTTPException
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.contracts.api_schemas import StartupEvaluationRequest, ErrorResponse, StartupEvaluationResponse
from app.validation.json_repair import RobustJSONParser
from app.confidence.confidence_engine import DeterministicConfidenceEngine

logger = logging.getLogger("ElephantTank.API.Evaluation")
router = APIRouter()

@router.post("/evaluate-startup", response_model=StartupEvaluationResponse, tags=["Evaluation Pipeline"])
async def evaluate_startup(request: StartupEvaluationRequest):
    """
    Primary ingestion endpoint. Receives a startup profile, validates it, 
    and triggers a real Groq AI evaluation returning structured JSON.
    """
    logger.info(f"Received Evaluation Request for: {request.startup_name}")
    
    # 1. Validation Before Sending to Groq
    if not request.startup_description or len(request.startup_description) < 20:
        raise HTTPException(status_code=400, detail="Startup description is too short to evaluate.")
        
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable not set.")
        
    # 2. Setup Groq Client
    client = Groq(api_key=groq_api_key)
    
    # 3. Prompt Builder (Dynamic Loading)
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "startup_eval_v1.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except Exception as e:
        logger.error(f"Failed to load system prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error: Prompt configuration missing.")
        
    user_prompt = f"Startup Name: {request.startup_name}\nStage: {request.target_stage}\nFounder: {request.founder_data}\nDescription: {request.startup_description}"

    try:
        # 4. Groq Analysis
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        # 5. Structured JSON Parsing & Logging
        raw_json = response.choices[0].message.content
        logger.info(f"RAW GROQ RESPONSE:\n{raw_json}")
        
        try:
            parsed_data = RobustJSONParser.parse_and_repair(raw_json)
        except ValueError as ve:
            logger.error(f"JSON Repair Failed. {ve}")
            raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON.")
            
        # Ensure pipeline_id exists
        if "pipeline_id" not in parsed_data or not parsed_data["pipeline_id"]:
            import uuid
            parsed_data["pipeline_id"] = f"eval_{uuid.uuid4().hex[:8]}"
            
        # 6. DETERMINISTIC LOCAL PYTHON MATH ENGINE & NORMALIZATION
        # Extract base scores (1-10 scale)
        eval_res = parsed_data.get("evaluation_results", {})
        inv = eval_res.get("innovation_score", 0)
        mkt = eval_res.get("market_score", 0)
        scl = eval_res.get("scalability_score", 0)
        fnd = eval_res.get("founder_score", 0)
        frs = eval_res.get("funding_readiness_score", 0)
        
        # Normalization: Cap innovation if "wrapper" is detected in description
        desc_lower = request.startup_description.lower()
        if "wrapper" in desc_lower or "chatgpt wrapper" in desc_lower:
            inv = min(inv, 4)  # Hard cap on innovation for basic wrappers
            logger.info("Normalization Applied: Capped innovation score for AI wrapper.")
            
        # Normalization: Penalty for saturated markets
        if "food delivery" in desc_lower or "social media" in desc_lower:
            mkt = min(mkt, 6)
            logger.info("Normalization Applied: Capped market score for saturated industry.")
            
        # Update parsed data with normalized scores
        parsed_data["evaluation_results"]["innovation_score"] = inv
        parsed_data["evaluation_results"]["market_score"] = mkt
        
        # Calculate overall score dynamically based on stage (Scale 0-100)
        stage = request.target_stage.lower()
        if stage == "pre-seed":
            overall = (inv * 30 + fnd * 30 + mkt * 20 + scl * 10 + frs * 10) / 10
        elif stage == "seed":
            overall = (inv * 20 + mkt * 30 + scl * 20 + fnd * 20 + frs * 10) / 10
        else: # Series A
            overall = (inv * 10 + mkt * 20 + scl * 30 + fnd * 20 + frs * 20) / 10
            
        parsed_data["evaluation_results"]["overall_score"] = int(overall)
        
        # 7. DETERMINISTIC CONFIDENCE ENGINE
        raw_conf = parsed_data.get("confidence_summary", {}).get("overall_confidence", 5)
        try:
            base_conf = int(float(raw_conf))
        except (ValueError, TypeError):
            base_conf = 5
            
        final_conf = DeterministicConfidenceEngine.calculate_confidence(
            request.startup_description, 
            request.founder_data, 
            base_conf
        )
        if "confidence_summary" not in parsed_data:
            parsed_data["confidence_summary"] = {}
        parsed_data["confidence_summary"]["overall_confidence"] = final_conf
        
        # 8. STRUCTURED EXECUTION LOGGING
        import time
        parsed_data["execution_logs"] = [
            {
                "stage": "STARTUP_EVALUATION",
                "status": "SUCCESS",
                "message": "Qualitative reasoning generated by Groq. Deterministic scoring and confidence calculated locally.",
                "timestamp": int(time.time())
            }
        ]
        
        # 9. Validated Response (Pydantic enforces this exact output to Swagger)
        return StartupEvaluationResponse(**parsed_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
