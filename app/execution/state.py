import uuid
import time
from typing import List, Dict
from app.schemas.orchestration import ExecutionLog

class PipelineStateManager:
    def __init__(self, pipeline_name: str):
        self.pipeline_id = f"{pipeline_name}_{uuid.uuid4().hex[:8]}"
        self.current_stage = "INITIALIZED"
        self.status = "RUNNING"
        self.logs: List[ExecutionLog] = []

    def update_stage(self, stage_name: str, message: str = "Stage started"):
        self.current_stage = stage_name
        self._append_log("INFO", message)

    def log_success(self, message: str = "Stage completed successfully"):
        self._append_log("SUCCESS", message)

    def log_error(self, message: str):
        self.status = "FAILED"
        self._append_log("ERROR", message)

    def _append_log(self, status: str, message: str):
        from app.utils.execution_logger import create_execution_log
        log_data = create_execution_log(self.current_stage, status, message)
        self.logs.append(ExecutionLog(
            stage=log_data["stage"],
            status=log_data["status"],
            message=log_data["message"],
            timestamp_unix=log_data["timestamp_unix"],
            timestamp_readable=log_data["timestamp_readable"]
        ))
        
    def export_state(self) -> Dict:
        return {
            "pipeline_id": self.pipeline_id,
            "status": self.status,
            "current_stage": self.current_stage,
            "logs": [log.model_dump() for log in self.logs]
        }
