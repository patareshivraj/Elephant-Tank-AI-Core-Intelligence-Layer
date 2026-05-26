import os
import json
import time
import logging
from groq import Groq
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.LLMClient")

class GroqReasoningClient:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("GROQ_API_KEY missing. LLM Client will fail in production.")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
        self.model = "llama-3.3-70b-versatile"
        
    def _get_temperature_for_mode(self, mode: str) -> float:
        if mode in ["STRICT_JSON", "RISK_ONLY", "STARTUP_EVALUATION"]:
            return 0.1  # Highly deterministic
        elif mode in ["ANALYST_REPORT", "EXEC_SUMMARY"]:
            return 0.4
        elif mode == "RECOMMENDATION_MODE":
            return 0.6
        return 0.2

    def execute_prompt(self, messages: list, mode: str = "STRICT_JSON", max_retries: int = 3) -> Dict[str, Any]:
        """
        Executes the prompt against the Groq API, enforcing JSON output.
        Implements exponential backoff for rate limits.
        """
        if not self.client:
            raise RuntimeError("Live API Key not configured. Cannot execute Phase 2 reasoning.")
            
        temperature = self._get_temperature_for_mode(mode)
        backoff = 2.0
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    response_format={"type": "json_object"},
                    max_tokens=4096
                )
                
                content = response.choices[0].message.content
                return json.loads(content)
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode LLM JSON: {e}")
                raise
            except Exception as e:
                logger.warning(f"Groq API Error (Attempt {attempt+1}): {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(backoff)
                backoff *= 2.0
