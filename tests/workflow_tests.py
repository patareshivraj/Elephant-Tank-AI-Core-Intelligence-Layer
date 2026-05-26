import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.workflow.venture_orchestrator import VentureOrchestrator

TEST_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

def setup_module():
    os.makedirs(os.path.join(TEST_UPLOADS, "workflow"), exist_ok=True)
    db_path = os.path.join(TEST_UPLOADS, "workflow", "workflows.json")
    if os.path.exists(db_path):
        os.remove(db_path)

def test_venture_orchestrator_flow():
    print("Executing workflow orchestration tests...")
    
    # 1. Enqueue startup
    init_log = VentureOrchestrator.initialize_pipeline("Zephyr AI", "IN_REVIEW")
    assert init_log["status"] == "SUCCESS"
    
    state_details = VentureOrchestrator.get_pipeline_state("Zephyr AI")
    assert state_details["workflow_state"] == "IN_REVIEW"
    
    # 2. State transition
    trans_log = VentureOrchestrator.transition_state("Zephyr AI", "DUE_DILIGENCE", "Passed initial filtering metrics.")
    assert trans_log["status"] == "SUCCESS"
    
    state_details = VentureOrchestrator.get_pipeline_state("Zephyr AI")
    assert state_details["workflow_state"] == "DUE_DILIGENCE"
    assert len(state_details["state_history"]) == 2
    
    # 3. List queues
    queue = VentureOrchestrator.list_queue("DUE_DILIGENCE")
    assert "Zephyr AI" in queue
    
    print("[SUCCESS] Workflow orchestrator tests passed!")

if __name__ == "__main__":
    setup_module()
    test_venture_orchestrator_flow()
