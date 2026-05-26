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
        self.logs.append(ExecutionLog(
            stage=self.current_stage,
            status=status,
            message=message,
            timestamp=time.time()
        ))
        
    def export_state(self) -> Dict:
        return {
            "pipeline_id": self.pipeline_id,
            "status": self.status,
            "current_stage": self.current_stage,
            "logs": [log.model_dump() for log in self.logs]
        }
