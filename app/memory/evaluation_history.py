import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
from app.utils.execution_logger import create_execution_log

logger = logging.getLogger("ElephantTank.Memory.EvaluationHistory")

MEMORY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "memory"))
os.makedirs(MEMORY_DIR, exist_ok=True)
EVAL_HISTORY_FILE = os.path.join(MEMORY_DIR, "evaluations.json")

class EvaluationHistoryTracker:
    """
    Historical Evaluation Tracker.
    Registers, versions, and tracks detailed startup valuation runs, strategic milestones,
    and supports delta comparisons between historical due diligence runs.
    """
    
    @classmethod
    def _load_history(cls) -> Dict[str, List[Dict[str, Any]]]:
        if not os.path.exists(EVAL_HISTORY_FILE):
            return {}
        try:
            with open(EVAL_HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load evaluation history db: {e}")
            return {}
            
    @classmethod
    def _save_history(cls, db: Dict[str, List[Dict[str, Any]]]):
        try:
            with open(EVAL_HISTORY_FILE, "w") as f:
                json.dump(db, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save evaluation history db: {e}")

    @classmethod
    def record_run(cls, startup_name: str, score: int, metrics: Dict[str, int], recommendations: List[str]) -> Dict[str, Any]:
        """
        Appends a timestamped evaluation milestone run snapshot.
        """
        logger.info(f"Recording historical run for startup: {startup_name}")
        db = cls._load_history()
        
        now = int(time.time())
        key = startup_name.lower().strip()
        
        run_record = {
            "timestamp": now,
            "overall_score": score,
            "metrics": metrics,
            "recommendations": recommendations,
            "run_version": len(db.get(key, [])) + 1
        }
        
        if key not in db:
            db[key] = []
            
        db[key].append(run_record)
        cls._save_history(db)
        
        return create_execution_log(
            stage="EVALUATION_HISTORY_UPDATE",
            status="SUCCESS",
            message=f"Recorded run v{run_record['run_version']} for '{startup_name}'."
        )

    @classmethod
    def compare_runs(cls, startup_name: str, run_v1: int, run_v2: int) -> Dict[str, Any]:
        """
        Compares two evaluation runs for a given startup.
        """
        key = startup_name.lower().strip()
        db = cls._load_history()
        runs = db.get(key, [])
        
        r1 = next((r for r in runs if r["run_version"] == run_v1), None)
        r2 = next((r for r in runs if r["run_version"] == run_v2), None)
        
        if not r1 or not r2:
            return {
                "error": "One or both run versions not found in history.",
                "v1_found": r1 is not None,
                "v2_found": r2 is not None
            }
            
        score_delta = r2["overall_score"] - r1["overall_score"]
        
        # Calculate metric deltas
        metric_deltas = {}
        for m, val in r2["metrics"].items():
            if m in r1["metrics"]:
                metric_deltas[m] = val - r1["metrics"][m]
                
        return {
            "startup_name": startup_name,
            "comparison_window": {
                "earlier_version": run_v1,
                "later_version": run_v2,
                "time_span_seconds": r2["timestamp"] - r1["timestamp"]
            },
            "score_shift": {
                "v1_score": r1["overall_score"],
                "v2_score": r2["overall_score"],
                "delta": score_delta
            },
            "metric_shifts": metric_deltas,
            "recommendations_evolution": {
                "previous": r1["recommendations"],
                "current": r2["recommendations"]
            }
        }
