import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Governance.GovernanceEngine")

class AIGovernanceEngine:
    """
    AI Governance Engine.
    Enforces operational policies, hallucination guardrails, and validation constraints.
    """
    
    @classmethod
    def audit_and_governance(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforces policy compliance on dynamic outputs.
        """
        startup = payload.get("startup_name", "Unknown")
        score = payload.get("overall_score")
        confidence = payload.get("confidence_score")
        
        violations = []
        
        # 1. Hallucination Guard: check overall score bounds
        if score is not None:
            score = float(score)
            if score < 0.0 or score > 100.0:
                violations.append({
                    "policy": "HALLUCINATION_GUARD",
                    "reason": f"Overall score {score} is out of boundary bounds (0-100)."
                })
                
        # 2. Confidence Boundary check
        if confidence is not None:
            confidence = int(confidence)
            if confidence < 1 or confidence > 10:
                violations.append({
                    "policy": "CONFIDENCE_BOUNDARY",
                    "reason": f"Confidence score {confidence} is out of structural limits (1-10)."
                })
                
        # 3. Decision Logic Check: high score with extremely low confidence
        if score is not None and confidence is not None:
            if score >= 85.0 and confidence <= 3:
                violations.append({
                    "policy": "INSUFFICIENT_EVIDENCE_POLICY",
                    "reason": f"Startup has high score ({score}) with unacceptably low evidence confidence ({confidence})."
                })
                
        status = "REJECTED_VIOLATION" if violations else "APPROVED_COMPLIANT"
        
        return {
            "startup_name": startup,
            "governance_status": status,
            "violations_detected": len(violations),
            "violations_list": violations
        }
