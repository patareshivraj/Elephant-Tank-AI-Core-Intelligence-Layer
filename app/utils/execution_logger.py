import time
from datetime import datetime

class ExecutionLogger:
    """
    Centralized execution logging utility for Elephant Tank AI.
    Generates dynamic Unix integer timestamps and timezone-aware ISO human-readable timestamps.
    """
    
    @classmethod
    def create_execution_log(cls, stage: str, status: str, message: str) -> dict:
        """
        Creates a structured, dynamically timestamped execution log.
        """
        return {
            "stage": stage,
            "status": status,
            "message": message,
            "timestamp_unix": int(time.time()),
            "timestamp_readable": datetime.now().astimezone().isoformat()
        }

def create_execution_log(stage: str, status: str, message: str) -> dict:
    """
    Module level convenience function.
    """
    return ExecutionLogger.create_execution_log(stage, status, message)
