from app.reports.base_generator import BaseReportGenerator
from app.schemas.reporting import InvestorReport
from app.templates.report_prompts import INVESTOR_REPORT_PROMPT

class InvestorReportGenerator(BaseReportGenerator):
    def generate(self, intelligence_payload: dict) -> InvestorReport:
        payload_str = str(intelligence_payload)
        raw_json = self.generate_narrative(payload_str, INVESTOR_REPORT_PROMPT, "ANALYST_REPORT")
        return InvestorReport(**raw_json)
