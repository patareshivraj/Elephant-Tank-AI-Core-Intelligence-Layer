import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
from app.utils.execution_logger import create_execution_log

logger = logging.getLogger("ElephantTank.Memory.StartupMemory")

MEMORY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "memory"))
os.makedirs(MEMORY_DIR, exist_ok=True)
STARTUPS_FILE = os.path.join(MEMORY_DIR, "startups.json")

class StartupMemoryEngine:
    """
    Persistent Startup Memory Engine.
    Handles storage and retrieval of structured evaluation histories, semantic profiles,
    and ecosystem parameters to enable longitudinal startup analysis.
    """
    
    @classmethod
    def _load_db(cls) -> Dict[str, Any]:
        if not os.path.exists(STARTUPS_FILE):
            return {}
        try:
            with open(STARTUPS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load startup memory db: {e}")
            return {}
            
    @classmethod
    def _save_db(cls, db: Dict[str, Any]):
        try:
            with open(STARTUPS_FILE, "w") as f:
                json.dump(db, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save startup memory db: {e}")

    @classmethod
    def store_evaluation(cls, startup_name: str, evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stores or appends a new structured startup evaluation into persistent memory.
        """
        logger.info(f"Storing evaluation history for startup: {startup_name}")
        db = cls._load_db()
        
        now = int(time.time())
        key = startup_name.lower().strip()
        
        # Prepare evaluation snapshot
        snapshot = {
            "timestamp": now,
            "overall_score": evaluation_results.get("overall_score", 50),
            "innovation_score": evaluation_results.get("innovation_score", 5),
            "market_score": evaluation_results.get("market_score", 5),
            "scalability_score": evaluation_results.get("scalability_score", 5),
            "founder_score": evaluation_results.get("founder_score", 5),
            "funding_readiness_score": evaluation_results.get("funding_readiness_score", 5),
            "risks": evaluation_results.get("risks", []),
            "recommendations": evaluation_results.get("recommendations", []),
            "confidence_score": evaluation_results.get("confidence_score", 7)
        }
        
        if key not in db:
            db[key] = {
                "startup_name": startup_name,
                "created_at": now,
                "last_updated": now,
                "current_profile": {
                    "target_stage": evaluation_results.get("target_stage", "Pre-seed"),
                    "sectors": evaluation_results.get("sectors", ["SaaS"])
                },
                "evaluation_history": []
            }
            
        db[key]["last_updated"] = now
        db[key]["current_profile"]["target_stage"] = evaluation_results.get("target_stage", db[key]["current_profile"]["target_stage"])
        db[key]["evaluation_history"].append(snapshot)
        
        cls._save_db(db)
        
        return create_execution_log(
            stage="STARTUP_MEMORY_UPDATE",
            status="SUCCESS",
            message=f"Successfully committed evaluation milestone for '{startup_name}' to persistence."
        )

    @classmethod
    def get_startup_history(cls, startup_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the complete profile and timeline history of a startup.
        """
        db = cls._load_db()
        return db.get(startup_name.lower().strip())
        
    @classmethod
    def list_all_startups(cls) -> List[str]:
        db = cls._load_db()
        return [item["startup_name"] for item in db.values()]
