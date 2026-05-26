import logging
from typing import Dict, Any, List
from app.knowledge_graph.venture_graph import VentureKnowledgeGraph

logger = logging.getLogger("ElephantTank.Alerts.EcosystemAlerts")

class EcosystemOpportunityAlerts:
    """
    Ecosystem Opportunity Alert Engine.
    Monitors sector node clusters, highlights market timing opportunities,
    and surfaces underserved sector gaps for venture capitalists.
    """
    
    @classmethod
    def scan_for_opportunities(cls) -> List[Dict[str, Any]]:
        """
        Evaluates graph parameters to compile actionable venture opportunity alert structures.
        """
        logger.info("Scanning Knowledge Graph for emerging clusters and sector gaps...")
        
        graph = VentureKnowledgeGraph._load_graph()
        nodes = graph.get("nodes", {})
        edges = graph.get("edges", [])
        
        alerts = []
        
        # 1. Underserved Sector Gaps (Sectors with <= 1 operating startups)
        sectors = [nid for nid, details in nodes.items() if details.get("label") == "SECTOR"]
        
        for s in sectors:
            # Count operating startups
            startup_count = 0
            for edge in edges:
                if edge["relation"] == "OPERATES_IN" and edge["target"] == s:
                    startup_count += 1
                    
            if startup_count <= 1:
                alerts.append({
                    "alert_type": "UNDERSERVED_SECTOR_GAP",
                    "target_entity": nodes[s]["node_id"],
                    "severity": "MEDIUM",
                    "rationale": f"Sector '{nodes[s]['node_id']}' is underserved. Only {startup_count} active startups mapped here. High whitespace potential."
                })
                
        # 2. Timing Advantage Matches
        for nid, details in nodes.items():
            if details.get("label") == "STARTUP":
                # Find if linked to WELL_TIMED timing indicator
                is_well_timed = False
                for edge in edges:
                    if edge["source"] == nid and edge["relation"] == "HAS_TIMING" and edge["target"] == "well_timed":
                        is_well_timed = True
                        break
                        
                if is_well_timed:
                    alerts.append({
                        "alert_type": "TIMING_ADVANTAGE_MATCH",
                        "target_entity": details["node_id"],
                        "severity": "HIGH",
                        "rationale": f"Venture '{details['node_id']}' operates with extreme sector timing relevance. Immediate pipeline integration advised."
                    })
                    
        return alerts
