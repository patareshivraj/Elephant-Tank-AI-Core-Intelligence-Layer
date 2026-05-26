import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.HallucinationDetector")

class HallucinationDetector:
    def detect(self, original_profile: Dict[str, Any], final_report: str) -> List[str]:
        """
        Cross-references the deterministic input payload against the LLM's generated narrative.
        If a field was tagged as UNVERIFIED or missing, but the LLM hallucinates a number, this traps it.
        """
        flags = []
        
        # Example deterministic logic: Check Revenue
        raw_revenue = original_profile.get("revenue", "UNVERIFIED")
        
        if raw_revenue == "UNVERIFIED":
            # If input is UNVERIFIED, the output report should NOT contain standard currency markers $X.X 
            # (A simplistic but highly effective regex-style trap for financial hallucination)
            if "$" in final_report and ("ARR" in final_report or "MRR" in final_report or "Revenue" in final_report):
                flags.append("HALLUCINATION DETECTED: Revenue was UNVERIFIED in input, but LLM narrative includes monetary revenue figures.")
                
        # Check Team
        raw_team = original_profile.get("team", "UNVERIFIED")
        if raw_team == "UNVERIFIED" and ("exited founder" in final_report.lower() or "stanford" in final_report.lower()):
            flags.append("HALLUCINATION DETECTED: Team background was UNVERIFIED, but LLM inferred prestigious credentials.")
            
        if flags:
            logger.warning(f"Found {len(flags)} hallucination violations.")
            
        return flags
