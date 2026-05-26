import time
import logging
from typing import Dict, Any, List
from app.workflow.venture_orchestrator import VentureOrchestrator

logger = logging.getLogger("ElephantTank.DecisionSupport.EscalationEngine")

class StrategicEscalationEngine:
    """
    Strategic Escalation Engine.
    Detects critical volatility across venture metrics, automatically redirects review queues,
    and formats comprehensive action plans.
    """
    
    @classmethod
    def evaluate_escalation_rules(
        cls, 
        startup_name: str, 
        current_metrics: Dict[str, Any], 
        previous_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Applies strict mathematical checks to determine if the startup must be flagged for escalation.
        """
        logger.info(f"Checking strategic escalation thresholds for: {startup_name}")
        
        now = int(time.time())
        score_diff = current_metrics.get("overall_score", 50) - previous_metrics.get("overall_score", 50)
        conf_diff = current_metrics.get("confidence_score", 5) - previous_metrics.get("confidence_score", 5)
        founder_diff = current_metrics.get("founder_score", 5) - previous_metrics.get("founder_score", 5)
        
        reasons = []
        severity = "NEGLIGIBLE"
        action = "MAINTAIN_CURRENT_QUEUE"
        
        # 1. Trajectory collapse (drop >= 10 points)
        if score_diff <= -10:
            reasons.append(f"Venture overall score dropped critically by {abs(score_diff)} points.")
            severity = "CRITICAL"
            action = "TRIGGER_BOARD_LEVEL_REVIEW"
            
        # 2. Confidence collapse (drop >= 3 points)
        if conf_diff <= -3:
            reasons.append(f"Due diligence confidence collapsed by {abs(conf_diff)} levels.")
            if severity != "CRITICAL":
                severity = "WARNING"
                action = "SUSPEND_FUNDING_AND_REVERIFY"
                
        # 3. Founder competency collapse (drop >= 2 points)
        if founder_diff <= -2:
            reasons.append(f"Founder execution rating degraded by {abs(founder_diff)} scale values.")
            if severity != "CRITICAL":
                severity = "WARNING"
                action = "INITIATE_FOUNDER_DIRECT_INTERVIEW"
                
        # 4. Trigger transition in the orchestrator if severity is WARNING or CRITICAL
        is_escalated = len(reasons) > 0
        if is_escalated:
            VentureOrchestrator.transition_state(
                startup_name=startup_name,
                new_state="ESCALATED",
                rationale=f"Systemic Escalation Rule Triggered: {'; '.join(reasons)}"
            )
            
        return {
            "startup_name": startup_name,
            "escalated": is_escalated,
            "escalation_severity": severity,
            "escalation_reasons": reasons,
            "recommended_action": action,
            "timestamp": now,
            "log": {
                "stage": "WORKFLOW_ESCALATION",
                "status": "SUCCESS" if is_escalated else "NEUTRAL",
                "message": f"Escalated due to {len(reasons)} rules triggered" if is_escalated else "No escalation rules violated",
                "timestamp": now
            }
        }
