import logging
from typing import Dict, Any

from app.executive_summary.generator import ExecSummaryGenerator
from app.investor_reports.generator import InvestorReportGenerator
from app.schemas.evaluation import VentureIntelligenceOutput

logger = logging.getLogger("ElephantTank.ReportOrchestrator")

class ReportOrchestrator:
    def __init__(self):
        self.exec_generator = ExecSummaryGenerator()
        self.investor_generator = InvestorReportGenerator()

    def generate_report(self, intelligence: VentureIntelligenceOutput, mode: str = "EXEC_SUMMARY") -> Any:
        """
        Transforms the strict Phase 3 JSON output into a natural-language Pydantic report.
        """
        logger.info(f"Generating Phase 5 report in mode: {mode}")
        
        payload_dict = intelligence.dict()
        
        if mode == "EXEC_SUMMARY":
            return self.exec_generator.generate(payload_dict)
        elif mode == "INVESTOR_REPORT":
            return self.investor_generator.generate(payload_dict)
        else:
            raise ValueError(f"Unsupported report mode: {mode}")
