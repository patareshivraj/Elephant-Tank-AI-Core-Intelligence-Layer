import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.simulation.ecosystem_shock import EcosystemShockAnalysis
from app.intelligence.cascade_detection import EcosystemCascadeDetection
from app.knowledge_graph.venture_graph import VentureKnowledgeGraph

TEST_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

def setup_module():
    os.makedirs(os.path.join(TEST_UPLOADS, "knowledge_graph"), exist_ok=True)
    graph_path = os.path.join(TEST_UPLOADS, "knowledge_graph", "graph.json")
    if os.path.exists(graph_path):
        os.remove(graph_path)

def test_shock_and_cascade_scenarios():
    print("Executing shock and cascade detection tests...")
    
    st_metrics = {
        "startup_name": "Aether Space",
        "overall_score": 80.0,
        "sectors": ["SpaceTech", "SaaS"]
    }
    
    # 1. Shock analysis checks
    shock_res = EcosystemShockAnalysis.simulate_shock(st_metrics, "REGULATORY_SHIFT")
    assert shock_res["simulated_score"] == 65.0
    assert shock_res["survivability_index"] == 70.0
    assert shock_res["vulnerability_rating"] == "MEDIUM"
    
    # 2. Tech bonus shock checks
    ai_shock = EcosystemShockAnalysis.simulate_shock(st_metrics, "AI_DISRUPTION")
    assert ai_shock["simulated_score"] == 90.0
    assert ai_shock["survivability_index"] == 90.0
    assert ai_shock["vulnerability_rating"] == "LOW"
    
    # 3. Seed knowledge graph to check cascade logic
    VentureKnowledgeGraph.add_node("Aether Space", "STARTUP")
    VentureKnowledgeGraph.add_node("MedTech", "SECTOR")
    VentureKnowledgeGraph.add_edge("Aether Space", "MedTech", "OPERATES_IN")
    
    cascade_res = EcosystemCascadeDetection.evaluate_dependency_cascades()
    # Should have a Zero Founder warning since Aether Space was registered without founder node
    assert cascade_res["cascade_warnings_count"] >= 1
    assert any(c["cascade_type"] == "ZERO_FOUNDER_LINKAGE" for c in cascade_res["cascade_warnings"])
    
    print("[SUCCESS] Shock and cascade detection tests passed!")

if __name__ == "__main__":
    setup_module()
    test_shock_and_cascade_scenarios()
