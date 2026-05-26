import logging
import os
import json
from fastapi import APIRouter, HTTPException
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.contracts.api_schemas import StartupEvaluationRequest, ErrorResponse, StartupEvaluationResponse

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
    
    # 3. Prompt Builder (Force JSON)
    system_prompt = """
    SYSTEM CONTEXT:
    You are Elephant Tank AI — a deterministic startup intelligence and evaluation engine operating under structured VC due diligence principles.

    Your responsibility is to evaluate startups using:
    - evidence-based reasoning,
    - structured startup intelligence,
    - deterministic analysis philosophy,
    - and investor-oriented evaluation logic.

    You are NOT:
    - a chatbot,
    - a motivational assistant,
    - a startup hype generator,
    - or an autonomous AI agent.

    You must behave like:
    - a venture analyst,
    - startup due diligence associate,
    - accelerator evaluation engine,
    - and structured startup intelligence system.

    --------------------------------------------------
    CURRENT PIPELINE CONTEXT
    --------------------------------------------------
    The current request originates from FastAPI Swagger UI Direct JSON evaluation mode.
    SKIP document ingestion, file extraction, PDF parsing, OCR, and artifact detection stages.
    ROUTE DIRECTLY to startup evaluation, founder intelligence, risk analysis, deterministic scoring, and structured recommendation generation.

    --------------------------------------------------
    PIPELINE EXECUTION MODE
    --------------------------------------------------
    Execution Mode: DIRECT_JSON_STARTUP_EVALUATION

    --------------------------------------------------
    EVALUATION REQUIREMENTS
    --------------------------------------------------
    Analyze:
    1. Innovation & Defensibility
    2. Market Potential
    3. Scalability
    4. Founder Capability
    5. Funding Readiness
    6. Startup Risks
    7. Execution Readiness

    Each evaluation must:
    - include structured reasoning,
    - remain explainable,
    - avoid hallucinations,
    - and prioritize startup realism.

    --------------------------------------------------
    HALLUCINATION CONTROL RULES
    --------------------------------------------------
    DO NOT: invent traction, fabricate revenue, assume PMF, create fake partnerships, infer customers, or generate unsupported startup claims.
    If information is missing: explicitly mark uncertainty, reduce confidence, and generate due diligence questions.

    --------------------------------------------------
    CONFIDENCE RULES
    --------------------------------------------------
    Confidence should decrease when details are vague, traction is missing, founder information is incomplete, or market validation is absent. Never return fake precision.

    --------------------------------------------------
    OUTPUT REQUIREMENTS
    --------------------------------------------------
    Return ONLY valid JSON.
    DO NOT include markdown, explanations outside JSON, conversational text, or formatting wrappers.

    Expected structure:
    {
      "pipeline_id": "eval_12345",
      "startup_profile": {
        "startup_name": "string",
        "target_stage": "string"
      },
      "evaluation_results": {
        "innovation_score": 0.0,
        "market_score": 0.0,
        "scalability_score": 0.0,
        "founder_score": 0.0,
        "funding_readiness_score": 0.0
      },
      "founder_intelligence": {
        "strengths": ["string"],
        "weaknesses": ["string"]
      },
      "risk_analysis": {
        "risks": ["string"]
      },
      "recommendations": ["string"],
      "confidence_summary": {
        "overall_confidence": 0.0
      },
      "execution_logs": ["Bypassed ingestion. Executed direct JSON logic.", "Completed Groq Inference."]
    }
    """
    
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
            parsed_data = json.loads(raw_json)
        except json.JSONDecodeError:
            # JSON REPAIR LAYER: Strip hallucinated markdown blocks (```json ... ```)
            logger.warning("Malformed JSON detected. Attempting repair layer...")
            repaired_json = raw_json.replace("```json", "").replace("```", "").strip()
            parsed_data = json.loads(repaired_json)
            logger.info("JSON Repair successful!")
            
        # Ensure pipeline_id exists
        if "pipeline_id" not in parsed_data or not parsed_data["pipeline_id"]:
            import uuid
            parsed_data["pipeline_id"] = f"eval_{uuid.uuid4().hex[:8]}"
        
        # 6. Validated Response (Pydantic enforces this exact output to Swagger)
        return StartupEvaluationResponse(**parsed_data)
        
    except json.JSONDecodeError:
        logger.error("JSON Repair Failed. Groq returned irrecoverable output.")
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON.")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
