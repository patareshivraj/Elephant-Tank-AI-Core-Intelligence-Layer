import sys
import os
import shutil

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.memory.startup_memory import StartupMemoryEngine
from app.memory.founder_memory import FounderMemoryEngine
from app.knowledge_graph.venture_graph import VentureKnowledgeGraph
from app.memory.evaluation_history import EvaluationHistoryTracker
from app.intelligence.evolution_analysis import StartupEvolutionAnalyzer
from app.knowledge_graph.ecosystem_mapper import EcosystemRelationshipMapper
from app.intelligence.drift_detector import IntelligenceDriftDetector
from app.intelligence.comparative_analysis import ComparativeStartupIntelligence
from app.intelligence.continuous_updates import ContinuousIntelligenceUpdateEngine
from app.timeline.venture_timeline import VentureTimelineIntelligence

TEST_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

def setup_module():
    # Make sure we clean or construct fresh test directories
    os.makedirs(os.path.join(TEST_UPLOADS, "memory"), exist_ok=True)
    os.makedirs(os.path.join(TEST_UPLOADS, "knowledge_graph"), exist_ok=True)
    for f in ["startups.json", "founders.json", "evaluations.json"]:
        path = os.path.join(TEST_UPLOADS, "memory", f)
        if os.path.exists(path):
            os.remove(path)
    graph_path = os.path.join(TEST_UPLOADS, "knowledge_graph", "graph.json")
    if os.path.exists(graph_path):
        os.remove(graph_path)

def test_memory_and_continuous_intelligence_pipeline():
    print("========================================")
    print(" ELEPHANT TANK - MEMORY & CONTINUOUS INTELLIGENCE")
    print("========================================")
    
    # 1. Persistent Startup Memory Checks
    print("[1] Verifying Startup Memory Engine...")
    eval_data = {
        "overall_score": 75,
        "innovation_score": 8,
        "market_score": 7,
        "scalability_score": 7,
        "founder_score": 8,
        "funding_readiness_score": 7,
        "risks": ["High initial CAC"],
        "recommendations": ["Optimize B2B conversion"],
        "confidence_score": 8,
        "target_stage": "Seed",
        "sectors": ["SaaS", "FinTech"]
    }
    
    log_mem = StartupMemoryEngine.store_evaluation("Alpha SaaS", eval_data)
    assert log_mem["status"] == "SUCCESS"
    
    history = StartupMemoryEngine.get_startup_history("Alpha SaaS")
    assert history is not None
    assert history["startup_name"] == "Alpha SaaS"
    assert len(history["evaluation_history"]) == 1
    assert history["evaluation_history"][0]["overall_score"] == 75
    print("  [OK] Startup evaluation persistence validated.")
    print("----------------------------------------")
    
    # 2. Founder Memory Integrity Checks
    print("[2] Verifying Founder Memory Engine...")
    metrics = {"technical_competence": 8, "leadership_index": 7, "execution_velocity": 8}
    log_founder = FounderMemoryEngine.commit_founder_profile("Sarah Jenkins", "Alpha SaaS", metrics)
    assert log_founder["status"] == "SUCCESS"
    
    # Verify duplicates avoidance
    FounderMemoryEngine.commit_founder_profile("Sarah Jenkins", "Alpha SaaS", {"technical_competence": 9})
    f_hist = FounderMemoryEngine.get_founder_history("Sarah Jenkins")
    assert f_hist is not None
    assert len(f_hist["venture_history"]) == 1, "Should avoid duplicate venture listings."
    assert f_hist["current_technical_rating"] == 9, "Should update current competence rating."
    print("  [OK] Founder identity deduplication and ratings verified.")
    print("----------------------------------------")
    
    # 3. Knowledge Graph Traversal
    print("[3] Verifying Knowledge Graph Layer...")
    VentureKnowledgeGraph.add_node("Alpha SaaS", "STARTUP")
    VentureKnowledgeGraph.add_node("Sarah Jenkins", "FOUNDER")
    log_edge = VentureKnowledgeGraph.add_edge("Sarah Jenkins", "Alpha SaaS", "FOUNDED")
    assert log_edge["status"] == "SUCCESS"
    
    relations = VentureKnowledgeGraph.traverse_relations("Sarah Jenkins")
    assert len(relations) >= 1
    assert relations[0]["neighbor"] == "Alpha SaaS"
    assert relations[0]["relation"] == "FOUNDED"
    print("  [OK] Graph relationship traversal validated.")
    print("----------------------------------------")
    
    # 4. Historical Evaluation Comparisons
    print("[4] Verifying Historical Tracker Comparisons...")
    EvaluationHistoryTracker.record_run("Alpha SaaS", 70, {"innovation": 7, "market": 6}, ["Previous Recommendation"])
    EvaluationHistoryTracker.record_run("Alpha SaaS", 82, {"innovation": 9, "market": 8}, ["Current Recommendation"])
    
    comparison = EvaluationHistoryTracker.compare_runs("Alpha SaaS", 1, 2)
    assert comparison["score_shift"]["delta"] == 12
    assert comparison["metric_shifts"]["innovation"] == 2
    print("  [OK] Run-to-run metric shift comparisons validated.")
    print("----------------------------------------")
    
    # 5. Startup Evolution Analyzer
    print("[5] Verifying Startup Evolution Analyzer...")
    runs = [
        {"timestamp": 1000, "overall_score": 60},
        {"timestamp": 2000, "overall_score": 75}
    ]
    evo = StartupEvolutionAnalyzer.analyze_evolution(runs)
    assert evo["evolution_status"] == "RAPIDLY_SCALING"
    assert evo["score_trajectory"]["absolute_shift"] == 15
    print("  [OK] Startup evolution scaling metrics validated.")
    print("----------------------------------------")
    
    # 6. Ecosystem Overlaps Mapping
    print("[6] Verifying Ecosystem Overlap Mapping...")
    # Add peer startup operating in same sector
    VentureKnowledgeGraph.add_node("Beta SaaS", "STARTUP")
    VentureKnowledgeGraph.add_node("SaaS", "SECTOR")
    VentureKnowledgeGraph.add_edge("Alpha SaaS", "SaaS", "OPERATES_IN")
    VentureKnowledgeGraph.add_edge("Beta SaaS", "SaaS", "OPERATES_IN")
    
    overlaps = EcosystemRelationshipMapper.map_competitive_overlaps("Alpha SaaS")
    assert "Beta SaaS" in overlaps["peer_sector_startups"]
    print("  [OK] Peer startup sector overlap mapping validated.")
    print("----------------------------------------")
    
    # 7. Intelligence Drift Detection
    print("[7] Verifying Drift Detection...")
    drift = IntelligenceDriftDetector.calculate_drift(
        {"overall_score": 80, "metrics": {"innovation": 8}},
        {"overall_score": 65, "metrics": {"innovation": 6}}
    )
    assert drift["drift_status"] == "CRITICAL_DOWNWARD_DRIFT"
    assert drift["drift_severity"] == "HIGH"
    print("  [OK] Critical downward score drift validated.")
    print("----------------------------------------")
    
    # 8. Comparative Startup Analysis
    print("[8] Verifying Startup-vs-Startup delta matrices...")
    comp = ComparativeStartupIntelligence.compare_startups(
        {"startup_name": "Alpha SaaS", "overall_score": 85, "innovation_score": 9},
        {"startup_name": "Beta SaaS", "overall_score": 70, "innovation_score": 7}
    )
    assert comp["comparison_matrix"]["overall_scores"]["delta"] == 15
    print("  [OK] Startup comparison matrices validated.")
    print("----------------------------------------")
    
    # 9. Continuous Intelligence Update orchestrator
    print("[9] Verifying Continuous Update Engine...")
    update_log = ContinuousIntelligenceUpdateEngine.update_venture_intelligence(
        startup_name="Alpha SaaS",
        evaluation_results={
            "overall_score": 88,
            "innovation_score": 9,
            "sectors": ["SaaS", "Cloud"],
            "timing_verdict": "WELL_TIMED"
        },
        founder_name="Sarah Jenkins",
        founder_metrics={"technical_competence": 10, "leadership_index": 9}
    )
    assert update_log["status"] == "SUCCESS"
    print("  [OK] Continuous update engine transactional execution validated.")
    print("----------------------------------------")
    
    # 10. Timeline Milestone logs
    print("[10] Verifying Timeline Intelligence...")
    timeline = VentureTimelineIntelligence.get_timeline("Alpha SaaS")
    assert len(timeline["milestone_events"]) >= 1
    assert timeline["overall_progress_delta"] is not None
    print("  [OK] Longitudinal venture milestone timeline verified.")
    print("========================================")
    print("[SUCCESS] ALL MEMORY & CONTINUOUS INTELLIGENCE TESTS PASSED!")

if __name__ == "__main__":
    try:
        setup_module()
        test_memory_and_continuous_intelligence_pipeline()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
