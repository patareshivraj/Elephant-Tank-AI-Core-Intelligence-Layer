from app.llm.client import GroqReasoningClient
from app.templates.report_prompts import SYSTEM_WRITER_PROMPT
import json

class BaseReportGenerator:
    def __init__(self):
        self.client = GroqReasoningClient()

    def generate_narrative(self, payload_str: str, task_prompt_template: str, mode: str) -> dict:
        messages = [
            {"role": "system", "content": SYSTEM_WRITER_PROMPT},
            {"role": "user", "content": task_prompt_template.format(payload=payload_str)}
        ]
        
        # We reuse the LLM client but pass a mode like "EXEC_SUMMARY" to ensure a slightly higher temperature (0.4) for narrative prose
        return self.client.execute_prompt(messages, mode=mode)
