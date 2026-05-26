import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.monitoring.venture_monitor import VentureMonitor
from app.monitoring.readiness_monitor import InvestmentReadinessMonitor
from app.monitoring.founder_risk_monitor import FounderRiskMonitor
from app.memory.startup_memory import StartupMemoryEngine
from app.memory.founder_memory import FounderMemoryEngine

TEST_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

def setup_module():
    os.makedirs(os.path.join(TEST_UPLOADS, "memory"), exist_ok=True)
    for f in ["startups.json", "founders.json"]:
        path = os.path.join(TEST_UPLOADS, "memory", f)
        if os.path.exists(path):
            os.remove(path)

def test_monitoring_layers():
    print("Executing monitoring layer tests...")
    
    # Seed persistent memories
    StartupMemoryEngine.store_evaluation("Atlas SaaS", {"overall_score": 85, "risks": ["Short runway"]})
    # Update with decline and extra risk
    StartupMemoryEngine.store_evaluation("Atlas SaaS", {"overall_score": 75, "risks": ["Short runway", "High competition"]})
    
    # 1. Venture Monitor checks
    mon_res = VentureMonitor.monitor_startup("Atlas SaaS")
    assert mon_res["status"] == "ALERT_ACTIVE"
    assert len(mon_res["warnings"]) >= 2
    
    # 2. Investment Readiness checks
    readiness = InvestmentReadinessMonitor.evaluate_readiness({"startup_name": "Atlas SaaS", "overall_score": 82, "trajectory_score": 75})
    assert readiness["readiness_status"] == "HIGH_READINESS"
    
    # 3. Founder Risk checks
    FounderMemoryEngine.commit_founder_profile("David Webb", "Atlas SaaS", {"technical_competence": 5, "leadership_index": 4})
    founder_risk = FounderRiskMonitor.evaluate_founder_risks("David Webb")
    assert founder_risk["founder_risk_level"] == "HIGH"
    assert len(founder_risk["risk_flags"]) == 2
    
    print("[SUCCESS] Monitoring layer tests passed!")

if __name__ == "__main__":
    setup_module()
    test_monitoring_layers()
