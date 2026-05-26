import logging
from typing import Dict, Any, List
from app.memory.startup_memory import StartupMemoryEngine

logger = logging.getLogger("ElephantTank.Timeline.VentureTimeline")

class VentureTimelineIntelligence:
    """
    Venture Timeline Intelligence Engine.
    Structures comprehensive longitudinal milestone records, recommendation histories,
    and maps capital progress timelines.
    """
    
    @classmethod
    def get_timeline(cls, startup_name: str) -> Dict[str, Any]:
        """
        Retrieves the chronological milestone timeline for a given startup.
        """
        logger.info(f"Assembling strategic milestone timeline for: {startup_name}")
        
        history_data = StartupMemoryEngine.get_startup_history(startup_name)
        if not history_data or not history_data.get("evaluation_history"):
            return {
                "startup_name": startup_name,
                "milestone_events": [],
                "timeline_narrative": "No historical milestones registered for this venture."
            }
            
        events = []
        raw_history = history_data["evaluation_history"]
        sorted_history = sorted(raw_history, key=lambda x: x["timestamp"])
        
        for idx, snapshot in enumerate(sorted_history):
            events.append({
                "milestone_index": idx + 1,
                "timestamp": snapshot["timestamp"],
                "overall_score": snapshot["overall_score"],
                "confidence_score": snapshot["confidence_score"],
                "primary_risks": snapshot.get("risks", []),
                "recommendation_count": len(snapshot.get("recommendations", []))
            })
            
        first_score = sorted_history[0]["overall_score"]
        last_score = sorted_history[-1]["overall_score"]
        overall_progress = last_score - first_score
        
        narrative = (
            f"Venture timeline tracks {len(events)} milestones. Overall score shifted by "
            f"{overall_progress:+d} points (from {first_score} to {last_score})."
        )
        
        return {
            "startup_name": startup_name,
            "milestone_events": events,
            "timeline_narrative": narrative,
            "overall_progress_delta": overall_progress
        }
