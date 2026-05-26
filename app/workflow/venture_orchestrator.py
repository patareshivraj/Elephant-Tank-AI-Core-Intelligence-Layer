import os
import json
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("ElephantTank.Workflow.VentureOrchestrator")

WORKFLOW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "workflow"))
os.makedirs(WORKFLOW_DIR, exist_ok=True)
WORKFLOWS_FILE = os.path.join(WORKFLOW_DIR, "workflows.json")

class VentureOrchestrator:
    """
    Venture Workflow Orchestrator.
    Manages operational startup review queues, tracks progression states,
    and structures lifecycle transitions deterministically.
    """
    
    @classmethod
    def _load_db(cls) -> Dict[str, Any]:
        if not os.path.exists(WORKFLOWS_FILE):
            return {}
        try:
            with open(WORKFLOWS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load workflow db: {e}")
            return {}
            
    @classmethod
    def _save_db(cls, db: Dict[str, Any]):
        try:
            with open(WORKFLOWS_FILE, "w") as f:
                json.dump(db, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save workflow db: {e}")

    @classmethod
    def initialize_pipeline(cls, startup_name: str, initial_stage: str = "IN_REVIEW") -> Dict[str, Any]:
        """
        Registers a startup in the pipeline review queue.
        """
        db = cls._load_db()
        key = startup_name.lower().strip()
        now = int(time.time())
        
        if key not in db:
            db[key] = {
                "startup_name": startup_name,
                "workflow_state": initial_stage,
                "state_history": [
                    {
                        "stage": initial_stage,
                        "timestamp": now,
                        "rationale": "Initial ingestion into Elephant Tank review queue."
                    }
                ],
                "last_modified": now
            }
            cls._save_db(db)
            
        return {
            "stage": "WORKFLOW_INITIALIZATION",
            "status": "SUCCESS",
            "message": f"Successfully enrolled '{startup_name}' into queue '{initial_stage}'.",
            "timestamp": now
        }

    @classmethod
    def transition_state(cls, startup_name: str, new_state: str, rationale: str) -> Dict[str, Any]:
        """
        Transitions the startup to a new operational lifecycle state.
        Valid states: IN_REVIEW, DUE_DILIGENCE, ESCALATED, APPROVED, REJECTED.
        """
        db = cls._load_db()
        key = startup_name.lower().strip()
        now = int(time.time())
        
        if key not in db:
            cls.initialize_pipeline(startup_name)
            db = cls._load_db()
            
        old_state = db[key]["workflow_state"]
        db[key]["workflow_state"] = new_state
        db[key]["last_modified"] = now
        db[key]["state_history"].append({
            "stage": new_state,
            "timestamp": now,
            "rationale": rationale
        })
        
        cls._save_db(db)
        logger.info(f"Transitioned {startup_name} from {old_state} -> {new_state}")
        
        return {
            "stage": "WORKFLOW_STATE_TRANSITION",
            "status": "SUCCESS",
            "message": f"Transitioned '{startup_name}' from '{old_state}' to '{new_state}'.",
            "timestamp": now
        }

    @classmethod
    def get_pipeline_state(cls, startup_name: str) -> Optional[Dict[str, Any]]:
        db = cls._load_db()
        return db.get(startup_name.lower().strip())

    @classmethod
    def list_queue(cls, stage: str) -> List[str]:
        db = cls._load_db()
        return [item["startup_name"] for item in db.values() if item["workflow_state"] == stage]
