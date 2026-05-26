import os
import time
import logging
from app.utils.execution_logger import create_execution_log
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, Any

from app.contracts.api_schemas import StartupEvaluationRequest, StartupEvaluationResponse, MultiDocumentEvaluationRequest
from app.endpoints.evaluation import evaluate_startup
from app.reporting.executive_report import ExecutiveReportGenerator
from app.exports.json_export import JSONExportManager
from app.exports.markdown_export import MarkdownExportManager
from app.exports.pdf_export import PDFExportManager

# Sprint 6 Strategic Engines
from app.reasoning.long_context_orchestrator import LongContextOrchestrator
from app.reasoning.intelligence_synthesizer import IntelligenceSynthesizer
from app.reporting.institutional_memo import InstitutionalMemoEngine
from app.strategy.weakness_prioritizer import WeaknessPrioritizer
from app.strategy.moat_intelligence import MoatIntelligenceEngine
from app.strategy.market_timing import MarketTimingEngine
from app.strategy.trajectory_analysis import TrajectoryAnalysisEngine
from app.matching.founder_investor_fit import FounderInvestorFitEngine
from app.strategy.scalability_forecast import ScalabilityForecastEngine

logger = logging.getLogger("ElephantTank.API.StrategicIntelligence")
router = APIRouter()

REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "reports"))
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.post("/reports/generate-master", tags=["Strategic Venture Intelligence"])
async def generate_master_report(request: StartupEvaluationRequest):
    """
    Primary strategic intelligence endpoint.
    Orchestrates the entire due diligence lifecycle:
    1. Triggers core deterministic venture evaluation.
    2. Runs advanced founder, risk, market positioning, and ecosystem opportunity analyses.
    3. Sorts and ranks GTM/Founder risks prior to optimization recommendations.
    4. Generates and stores professional JSON, Markdown, and PDF reports locally.
    5. Returns the complete compiled master strategic intelligence payload.
    """
    logger.info(f"Received Master Venture Report request for: {request.startup_name}")
    
    # 1. Trigger the existing core evaluation logic
    try:
        eval_resp = await evaluate_startup(request)
        # Convert Pydantic response to dictionary for sub-engines
        eval_dict = eval_resp.model_dump()
    except Exception as e:
        logger.error(f"Core evaluation phase failed: {e}")
        raise HTTPException(status_code=500, detail=f"Venture evaluation failed: {str(e)}")
        
    # 2. Orchestrate Strategic Intelligence Compilation
    try:
        master_report = ExecutiveReportGenerator.generate_executive_report(
            evaluation_response=eval_dict,
            raw_description=request.startup_description,
            raw_founder_data=request.founder_data or ""
        )
    except Exception as e:
        logger.error(f"Strategic intelligence compilation phase failed: {e}")
        raise HTTPException(status_code=500, detail=f"Strategic report orchestration failed: {str(e)}")
        
    # 3. Formulate Export Filenames
    clean_name = "".join(c if c.isalnum() else "_" for c in request.startup_name).lower()
    timestamp = int(time.time())
    
    json_filename = f"{clean_name}_{timestamp}.json"
    md_filename = f"{clean_name}_{timestamp}.md"
    pdf_filename = f"{clean_name}_{timestamp}.pdf"
    
    json_path = os.path.join(REPORTS_DIR, json_filename)
    md_path = os.path.join(REPORTS_DIR, md_filename)
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
    
    # 4. Trigger Orchestrated Multi-format Exports
    try:
        JSONExportManager.export_to_json(master_report, json_path)
        MarkdownExportManager.export_to_markdown(master_report, md_path)
        PDFExportManager.export_to_pdf(master_report, pdf_path)
    except Exception as e:
        logger.error(f"Multi-format export failed: {e}")
        # Note: Bypassing strict exception raising here so the payload is still returned to Swagger
        
    # Enrich response with downloable URLs
    master_report["exported_files"] = {
        "json_report": f"/reports/download/{json_filename}",
        "markdown_report": f"/reports/download/{md_filename}",
        "pdf_report": f"/reports/download/{pdf_filename}"
    }
    
    return master_report

@router.get("/reports/download/{filename}", tags=["Strategic Venture Intelligence"])
async def download_report_file(filename: str):
    """
    Downloads compiled JSON, Markdown, or premium PDF report files from the local storage vault.
    """
    file_path = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Requested strategic report file not found.")
        
    # Secure download check: Prevent directory traversal attacks
    resolved_path = os.path.abspath(file_path)
    if not resolved_path.startswith(REPORTS_DIR):
        raise HTTPException(status_code=403, detail="Access denied.")
        
    return FileResponse(file_path, filename=filename)

@router.post("/reports/generate-institutional", tags=["Strategic Venture Intelligence"])
async def generate_institutional_report(request: MultiDocumentEvaluationRequest):
    """
    Advanced Long-Context Institutional Reasoning endpoint.
    Coordinates:
    1. Multi-document context merging and cleaning via LongContextOrchestrator.
    2. Conflict metric resolution and signal combining via IntelligenceSynthesizer.
    3. Core deterministic startup evaluation.
    4. Multi-engine Advanced Strategic Analysis (Moat, Timing, Trajectory, Weakness Prioritization, Scalability, and Investor Fit).
    5. High-fidelity multi-format JSON, Markdown, and PDF report compilation.
    """
    logger.info(f"Received Institutional Strategic request for startup: {request.startup_name}")
    start_time = time.time()
    
    # 1. Long-Context Orchestration
    docs_list = [{"source_type": doc.source_type, "content": doc.content} for doc in request.documents]
    orchestrated = LongContextOrchestrator.orchestrate_context(docs_list)
    
    # 2. Multi-Document Intelligence Synthesis
    synthesis = IntelligenceSynthesizer.synthesize_intelligence(orchestrated)
    consolidated_desc = f"{synthesis.get('synthesized_diligence_narrative')} ARR Baseline: {synthesis.get('resolved_revenue_baseline')}"
    founder_summary = synthesis.get("reconciled_founders_summary", "")
    
    # 3. Formulate standard request and trigger Core Evaluation
    core_req = StartupEvaluationRequest(
        startup_name=request.startup_name,
        startup_description=consolidated_desc,
        founder_data=founder_summary,
        target_stage=request.target_stage
    )
    
    try:
        eval_resp = await evaluate_startup(core_req)
        eval_dict = eval_resp.model_dump()
    except Exception as e:
        logger.error(f"Core evaluation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Venture evaluation failed: {str(e)}")
        
    # Extract overall metrics
    eval_results = eval_dict.get("evaluation_results", {})
    overall_score = eval_results.get("overall_score", 50)
    innovation_score = eval_results.get("innovation_score", 5)
    
    # 4. Run Advanced Strategic Intelligence Modules
    moat = MoatIntelligenceEngine.analyze_moat(consolidated_desc, innovation_score)
    timing = MarketTimingEngine.analyze_timing(consolidated_desc)
    
    # Extract execution readiness from core evaluation strengths/weaknesses
    founder_readiness = "OPERATIONAL_STABLE"
    founder_intel = eval_dict.get("founder_intelligence", {})
    if founder_intel.get("weaknesses"):
        founder_readiness = "VULNERABLE"
        
    trajectory = TrajectoryAnalysisEngine.analyze_trajectory(overall_score, founder_readiness, moat["moat_index"])
    
    # Merge and prioritize all qualitative weaknesses using our deterministic Urgency Prioritizer
    all_weaknesses = []
    all_weaknesses.extend(eval_dict.get("founder_intelligence", {}).get("weaknesses", []))
    all_weaknesses.extend(eval_dict.get("risk_analysis", {}).get("risks", []))
    if not all_weaknesses:
        all_weaknesses = ["No structural execution weaknesses identified."]
        
    prioritized_weaknesses = WeaknessPrioritizer.prioritize_weaknesses(all_weaknesses)
    
    # Run Scalability and Investor Fit matching
    scalability = ScalabilityForecastEngine.forecast_scalability(consolidated_desc)
    
    domains_list = ["AI SaaS", "Deep Tech"] if "ai" in consolidated_desc.lower() or "quantum" in consolidated_desc.lower() else ["Software SaaS"]
    fit = FounderInvestorFitEngine.evaluate_fit(
        startup_stage=request.target_stage,
        startup_domains=domains_list,
        founder_risk_appetite="Balanced",
        investor_profile=request.investor_profile
    )
    
    # 5. Compile Master Institutional VC Memo
    memo = InstitutionalMemoEngine.generate_institutional_memo(
        synthesis_data=synthesis,
        overall_score=overall_score,
        moat_data=moat,
        timing_data=timing,
        trajectory_data=trajectory,
        scalability_data=scalability,
        fit_data=fit
    )
    
    # Assemble master report data structure
    master_report = {
        "pipeline_id": eval_dict.get("pipeline_id", "eval_inst"),
        "startup_profile": {
            "startup_name": request.startup_name,
            "target_stage": request.target_stage,
            "overall_score": overall_score,
            "resolved_revenue_baseline": synthesis.get("resolved_revenue_baseline")
        },
        "investment_memo": memo,
        "strategic_moat_intelligence": moat,
        "market_timing_analysis": timing,
        "trajectory_analysis": trajectory,
        "prioritized_weakness_matrix": prioritized_weaknesses,
        "scalability_forecasting": scalability,
        "investor_fit_profile": fit,
        "due_diligence_questions": eval_dict.get("due_diligence_questions", []),
        "execution_logs": [
            orchestrated.get("execution_log"),
            synthesis.get("execution_log"),
            memo.get("execution_log"),
            create_execution_log(
                stage="LONG_CONTEXT_REASONING",
                status="SUCCESS",
                message=f"Successfully completed advanced institutional reasoning pipeline in {time.time() - start_time:.3f}s."
            )
        ]
    }
    
    # 6. Formulate export paths and compile reports
    clean_name = "".join(c if c.isalnum() else "_" for c in request.startup_name).lower()
    timestamp = int(time.time())
    
    json_filename = f"inst_{clean_name}_{timestamp}.json"
    md_filename = f"inst_{clean_name}_{timestamp}.md"
    pdf_filename = f"inst_{clean_name}_{timestamp}.pdf"
    
    json_path = os.path.join(REPORTS_DIR, json_filename)
    md_path = os.path.join(REPORTS_DIR, md_filename)
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
    
    try:
        # Save JSON copy
        JSONExportManager.export_to_json(master_report, json_path)
        # Create standard report dictionary mapping for printing reports using standard templates
        std_format_report = ExecutiveReportGenerator.generate_executive_report(
            evaluation_response=eval_dict,
            raw_description=consolidated_desc,
            raw_founder_data=founder_summary
        )
        MarkdownExportManager.export_to_markdown(std_format_report, md_path)
        PDFExportManager.export_to_pdf(std_format_report, pdf_path)
    except Exception as e:
        logger.error(f"Multi-format institutional export failed: {e}")
        
    master_report["exported_files"] = {
        "json_report": f"/reports/download/{json_filename}",
        "markdown_report": f"/reports/download/{md_filename}",
        "pdf_report": f"/reports/download/{pdf_filename}"
    }
    
    return master_report
