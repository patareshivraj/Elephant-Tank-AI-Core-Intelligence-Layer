import logging
from typing import Dict, Any, List
from app.memory.founder_memory import FounderMemoryEngine

logger = logging.getLogger("ElephantTank.Monitoring.FounderRiskMonitor")

class FounderRiskMonitor:
    """
    Founder Risk Escalation Intelligence.
    Monitors execution indices, flags leadership dependency risks, and detects technical capability drift.
    """
    
    @classmethod
    def evaluate_founder_risks(cls, founder_name: str) -> Dict[str, Any]:
        """
        Scans a founder's progression metrics to surface leadership alerts.
        """
        logger.info(f"Scanning competence metrics for founder: {founder_name}")
        
        history = FounderMemoryEngine.get_founder_history(founder_name)
        if not history or not history.get("progression_snapshots"):
            return {
                "founder_name": founder_name,
                "founder_risk_level": "NEGLIGIBLE",
                "risk_flags": [],
                "message": "Founder has no registered progression timeline history."
            }
            
        snapshots = history["progression_snapshots"]
        latest = snapshots[-1]
        
        flags = []
        
        # 1. Technical competence warning
        tech = latest.get("technical_competence", 6)
        if tech < 6:
            flags.append({
                "risk_type": "FOUNDER_DEPENDENCY_RISK",
                "message": f"Founder technical capability index is low ({tech}/10)."
            })
            
        # 2. Leadership warning
        lead = latest.get("leadership_index", 5)
        if lead < 5:
            flags.append({
                "risk_type": "LEADERSHIP_GAP",
                "message": f"Founder leadership competence rating is low ({lead}/10)."
            })
            
        # 3. Longitudinal execution instability checks
        if len(snapshots) >= 2:
            prev = snapshots[-2]
            t_diff = latest.get("technical_competence", 6) - prev.get("technical_competence", 6)
            l_diff = latest.get("leadership_index", 5) - prev.get("leadership_index", 5)
            
            if t_diff <= -2 or l_diff <= -2:
                flags.append({
                    "risk_type": "EXECUTION_INSTABILITY",
                    "message": "Founder capability indexes experienced a major drop between milestones."
                })
                
        severity = "HIGH" if len(flags) >= 2 else ("MEDIUM" if len(flags) == 1 else "NEGLIGIBLE")
        
        return {
            "founder_name": founder_name,
            "founder_risk_level": severity,
            "risk_flags": flags,
            "current_technical_rating": tech,
            "current_leadership_rating": lead
        }
