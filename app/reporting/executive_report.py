import logging
import time
from typing import Dict, Any
from app.utils.execution_logger import create_execution_log

from app.reporting.investment_memo import InvestmentMemoEngine
from app.reporting.founder_report import FounderReportEngine
from app.reporting.risk_report import RiskReportEngine
from app.strategy.recommendation_engine import RecommendationEngine
from app.strategy.market_positioning import MarketPositioningEngine
from app.strategy.ecosystem_opportunity import EcosystemOpportunityEngine

logger = logging.getLogger("ElephantTank.Reporting.ExecutiveReport")

class ExecutiveReportGenerator:
    """
    Executive Report Generator & Orchestrator.
    Aggregates investment memos, founder reports, risk intelligence, market positioning,
    ecosystem opportunities, and strategic recommendations into a unified, investor-grade master report.
    """
    
    @classmethod
    def generate_executive_report(
        cls, 
        evaluation_response: Dict[str, Any], 
        raw_description: str = "", 
        raw_founder_data: str = ""
    ) -> Dict[str, Any]:
        """
        Coordinates individual reporting engines to compile the Master Venture Intelligence Report.
        """
        logger.info("Orchestrating Executive VC Report compilation...")
        start_time = time.time()
        
        # 1. Base Variables
        profile = evaluation_response.get("startup_profile", {})
        startup_name = profile.get("startup_name", "Unknown Venture")
        target_stage = profile.get("target_stage", "Pre-seed")
        
        eval_results = evaluation_response.get("evaluation_results", {})
        overall_score = eval_results.get("overall_score", 50)
        innovation_score = eval_results.get("innovation_score", 5)
        market_score = eval_results.get("market_score", 5)
        funding_readiness = eval_results.get("funding_readiness_score", 5)
        
        # 2. Trigger Sub-Engines
        memo_report = InvestmentMemoEngine.generate_investment_memo(
            evaluation_response, raw_description, raw_founder_data
        )
        
        founder_report = FounderReportEngine.generate_founder_report(
            evaluation_response, raw_founder_data
        )
        
        risk_report = RiskReportEngine.generate_risk_report(
            evaluation_response
        )
        
        recs_report = RecommendationEngine.generate_recommendations(
            evaluation_response
        )
        
        positioning_report = MarketPositioningEngine.analyze_positioning(
            evaluation_response, raw_description
        )
        
        ecosystem_report = EcosystemOpportunityEngine.analyze_opportunities(
            evaluation_response, raw_description
        )
        
        # 3. Determine Funding Readiness Level (Deterministic)
        if funding_readiness >= 8 and overall_score >= 80:
            readiness_status = "INVESTMENT_GRADE"
        elif funding_readiness >= 5 and overall_score >= 60:
            readiness_status = "ROUND_PREPARATION"
        else:
            readiness_status = "EARLY_STAGE_INCUBATION"
            
        elapsed_time = time.time() - start_time
        logger.info(f"Master Executive Report compiled successfully in {elapsed_time:.3f}s.")
        
        return {
            "pipeline_id": evaluation_response.get("pipeline_id", "Unknown"),
            "startup_profile": {
                "startup_name": startup_name,
                "target_stage": target_stage,
                "overall_score": overall_score,
                "funding_readiness_level": readiness_status
            },
            "investment_memo": memo_report,
            "founder_intelligence": founder_report,
            "risk_analysis": risk_report,
            "market_positioning": positioning_report,
            "ecosystem_opportunity": ecosystem_report,
            "prioritized_recommendations": recs_report,
            "due_diligence_questions": evaluation_response.get("due_diligence_questions", []),
            "execution_logs": [
                create_execution_log(
                    stage="REPORT_GENERATION",
                    status="SUCCESS",
                    message=f"Successfully compiled master strategic venture intelligence report in {elapsed_time:.3f}s."
                )
            ]
        }
