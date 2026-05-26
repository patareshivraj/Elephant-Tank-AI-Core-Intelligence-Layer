import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Recovery")

class RecoveryHandler:
    def handle_failure(self, stage: str, exception: Exception, state_manager) -> Dict[str, Any]:
        """
        Traps fatal pipeline errors (e.g., Groq API timeout, Pydantic validation breach).
        Logs the failure into the state manager and returns a graceful partial-payload
        so the orchestrator can output whatever data was compiled prior to the crash.
        """
        error_msg = f"Fatal Execution Error in {stage}: {str(exception)}"
        logger.error(error_msg)
        
        state_manager.log_error(error_msg)
        
        # Return an explicit failure payload to block downstream math
        return {
            "error": True,
            "failed_stage": stage,
            "exception": str(exception),
            "recovered": False
        }
