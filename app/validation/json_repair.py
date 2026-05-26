import json
import re
import logging

logger = logging.getLogger("ElephantTank.Validation.JSONRepair")

class RobustJSONParser:
    @staticmethod
    def parse_and_repair(raw_output: str) -> dict:
        """
        Attempts to parse LLM JSON output. If it fails, applies layered
        recovery strategies to fix markdown wrapping, trailing commas, and prefix text.
        """
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError as e:
            logger.warning(f"Standard JSON parse failed: {e}. Initiating repair layer 1.")
            
            # Layer 1: Strip Markdown block quotes (```json ... ```)
            repaired = re.sub(r"^```(?:json)?|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()
            
            # Layer 2: Remove conversational prefix/suffix text (find first { and last })
            start_idx = repaired.find('{')
            end_idx = repaired.rfind('}')
            if start_idx != -1 and end_idx != -1:
                repaired = repaired[start_idx:end_idx+1]
                
            # Layer 3: Handle trailing commas in objects or arrays
            repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
            
            try:
                parsed_data = json.loads(repaired)
                logger.info("JSON Repair successful via Layer 3.")
                return parsed_data
            except json.JSONDecodeError as final_e:
                logger.error(f"Fatal JSON Parse Error. Repair failed: {final_e}")
                raise ValueError("Irrecoverable JSON format from LLM.")
