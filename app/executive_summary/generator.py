from app.reports.base_generator import BaseReportGenerator
from app.schemas.reporting import ExecutiveSummaryReport
from app.templates.report_prompts import EXEC_SUMMARY_PROMPT

class ExecSummaryGenerator(BaseReportGenerator):
    def generate(self, intelligence_payload: dict) -> ExecutiveSummaryReport:
        payload_str = str(intelligence_payload)
        raw_json = self.generate_narrative(payload_str, EXEC_SUMMARY_PROMPT, "EXEC_SUMMARY")
        return ExecutiveSummaryReport(**raw_json)
