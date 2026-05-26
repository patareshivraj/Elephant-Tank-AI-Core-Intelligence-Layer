import time
import logging
from typing import Dict, Any, List

from app.memory.startup_memory import StartupMemoryEngine
from app.memory.founder_memory import FounderMemoryEngine
from app.memory.evaluation_history import EvaluationHistoryTracker
from app.knowledge_graph.venture_graph import VentureKnowledgeGraph

logger = logging.getLogger("ElephantTank.Intelligence.ContinuousUpdates")

class ContinuousIntelligenceUpdateEngine:
    """
    Continuous Intelligence Update Engine.
    Unifies and coordinates write operations across startups, founders,
    historical runs, and knowledge graph layers to preserve strict systemic integrity.
    """
    
    @classmethod
    def update_venture_intelligence(
        cls, 
        startup_name: str, 
        evaluation_results: Dict[str, Any],
        founder_name: str = "",
        founder_metrics: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Transactional orchestrator updating persistent startup states,
        founder progression ratings, and semantic network edges.
        """
        logger.info(f"Initiating continuous intelligence cycle for: {startup_name}")
        now = int(time.time())
        logs = []
        
        # 1. Update Persistent Startup Memory
        log_mem = StartupMemoryEngine.store_evaluation(startup_name, evaluation_results)
        logs.append(log_mem)
        
        # 2. Update Evaluation History
        score = evaluation_results.get("overall_score", 50)
        metrics = {
            "innovation": evaluation_results.get("innovation_score", 5),
            "market": evaluation_results.get("market_score", 5),
            "scalability": evaluation_results.get("scalability_score", 5),
            "founder": evaluation_results.get("founder_score", 5)
        }
        recs = evaluation_results.get("recommendations", [])
        log_hist = EvaluationHistoryTracker.record_run(startup_name, score, metrics, recs)
        logs.append(log_hist)
        
        # 3. Update Founder Memory if provided
        if founder_name:
            metrics_founder = founder_metrics or {"technical_competence": 6, "leadership_index": 5, "execution_velocity": 5}
            log_founder = FounderMemoryEngine.commit_founder_profile(founder_name, startup_name, metrics_founder)
            logs.append(log_founder)
            
            # 4. Build Knowledge Graph edges
            # Link founder to startup
            log_edge_founder = VentureKnowledgeGraph.add_edge(founder_name, startup_name, "FOUNDED")
            logs.append(log_edge_founder)
            
        # Add Startup node and Sector nodes to KG
        VentureKnowledgeGraph.add_node(startup_name, "STARTUP", {
            "overall_score": score,
            "target_stage": evaluation_results.get("target_stage", "Pre-seed")
        })
        
        sectors = evaluation_results.get("sectors", ["SaaS"])
        for s in sectors:
            VentureKnowledgeGraph.add_node(s, "SECTOR")
            log_edge_sec = VentureKnowledgeGraph.add_edge(startup_name, s, "OPERATES_IN")
            logs.append(log_edge_sec)
            
        # Re-evaluate timing indicator link
        timing_verdict = evaluation_results.get("timing_verdict", "WELL_TIMED")
        VentureKnowledgeGraph.add_node(timing_verdict, "TIMING_INDICATOR")
        log_edge_timing = VentureKnowledgeGraph.add_edge(startup_name, timing_verdict, "HAS_TIMING")
        logs.append(log_edge_timing)
        
        return {
            "status": "SUCCESS",
            "message": f"Successfully completed continuous intelligence update cycle for '{startup_name}'.",
            "timestamp": now,
            "execution_logs": logs
        }
