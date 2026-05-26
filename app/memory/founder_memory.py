import os
import json
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("ElephantTank.Memory.FounderMemory")

MEMORY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "memory"))
os.makedirs(MEMORY_DIR, exist_ok=True)
FOUNDERS_FILE = os.path.join(MEMORY_DIR, "founders.json")

class FounderMemoryEngine:
    """
    Founder Memory System.
    Tracks founder histories, execution capability metrics, leadership development,
    and prevents duplicate identities in a persistent, longitudinal database.
    """
    
    @classmethod
    def _load_db(cls) -> Dict[str, Any]:
        if not os.path.exists(FOUNDERS_FILE):
            return {}
        try:
            with open(FOUNDERS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load founder memory db: {e}")
            return {}
            
    @classmethod
    def _save_db(cls, db: Dict[str, Any]):
        try:
            with open(FOUNDERS_FILE, "w") as f:
                json.dump(db, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save founder memory db: {e}")

    @classmethod
    def commit_founder_profile(cls, name: str, startup_name: str, capability_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Commits founder capabilities, B2B/tech expertise, and tracks history.
        """
        logger.info(f"Registering founder progression records for: {name}")
        db = cls._load_db()
        
        now = int(time.time())
        key = name.lower().strip()
        
        snapshot = {
            "timestamp": now,
            "associated_startup": startup_name,
            "technical_competence": capability_metrics.get("technical_competence", 6),
            "leadership_index": capability_metrics.get("leadership_index", 5),
            "execution_velocity": capability_metrics.get("execution_velocity", 5)
        }
        
        if key not in db:
            db[key] = {
                "founder_name": name,
                "first_seen": now,
                "current_technical_rating": capability_metrics.get("technical_competence", 6),
                "current_leadership_rating": capability_metrics.get("leadership_index", 5),
                "venture_history": [startup_name],
                "progression_snapshots": []
            }
            
        # Append snapshot and update ratings
        db[key]["current_technical_rating"] = capability_metrics.get("technical_competence", db[key]["current_technical_rating"])
        db[key]["current_leadership_rating"] = capability_metrics.get("leadership_index", db[key]["current_leadership_rating"])
        if startup_name not in db[key]["venture_history"]:
            db[key]["venture_history"].append(startup_name)
            
        db[key]["progression_snapshots"].append(snapshot)
        
        cls._save_db(db)
        
        return {
            "stage": "FOUNDER_MEMORY_UPDATE",
            "status": "SUCCESS",
            "message": f"Successfully updated founder progression timeline for '{name}'.",
            "timestamp": now
        }

    @classmethod
    def get_founder_history(cls, name: str) -> Optional[Dict[str, Any]]:
        db = cls._load_db()
        return db.get(name.lower().strip())
