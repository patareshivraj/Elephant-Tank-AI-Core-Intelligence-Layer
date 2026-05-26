import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.decision_support.escalation_engine import StrategicEscalationEngine
from app.workflow.venture_orchestrator import VentureOrchestrator

TEST_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

def setup_module():
    os.makedirs(os.path.join(TEST_UPLOADS, "workflow"), exist_ok=True)
    db_path = os.path.join(TEST_UPLOADS, "workflow", "workflows.json")
    if os.path.exists(db_path):
        os.remove(db_path)

def test_escalation_rules_trigger():
    print("Executing strategic escalation tests...")
    
    # Register in orchestrator first
    VentureOrchestrator.initialize_pipeline("Sigma Tech", "IN_REVIEW")
    
    # 1. Test critical score collapse drop (>= 10 points)
    esc_result = StrategicEscalationEngine.evaluate_escalation_rules(
        startup_name="Sigma Tech",
        current_metrics={"overall_score": 68, "confidence_score": 7, "founder_score": 8},
        previous_metrics={"overall_score": 82, "confidence_score": 7, "founder_score": 8}
    )
    
    assert esc_result["escalated"] is True
    assert esc_result["escalation_severity"] == "CRITICAL"
    assert esc_result["recommended_action"] == "TRIGGER_BOARD_LEVEL_REVIEW"
    
    # Verify State transitioned inside the orchestrator
    state_details = VentureOrchestrator.get_pipeline_state("Sigma Tech")
    assert state_details["workflow_state"] == "ESCALATED"
    
    print("[SUCCESS] Strategic escalation tests passed!")

if __name__ == "__main__":
    setup_module()
    test_escalation_rules_trigger()
