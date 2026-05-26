import logging
from typing import Dict, Any, List
from app.knowledge_graph.venture_graph import VentureKnowledgeGraph

logger = logging.getLogger("ElephantTank.Intelligence.CascadeDetection")

class EcosystemCascadeDetection:
    """
    Ecosystem Cascade Detection Engine.
    Detects dependency cascades, maps systemic chain reactions,
    and returns comprehensive risk propagation indicators.
    """
    
    @classmethod
    def evaluate_dependency_cascades(cls) -> Dict[str, Any]:
        """
        Scans graph structures to compile cascade risk indicators.
        """
        logger.info("Scanning graph sectors for dependency cascade exposures...")
        
        graph = VentureKnowledgeGraph._load_graph()
        nodes = graph.get("nodes", {})
        edges = graph.get("edges", [])
        
        cascades = []
        
        # 1. Map founder connections to startups
        for nid, details in nodes.items():
            if details.get("label") == "STARTUP":
                # Find connected founder nodes
                founders = []
                for edge in edges:
                    if edge["relation"] == "FOUNDED" and edge["target"] == nid:
                        founders.append(edge["source"])
                        
                # A startup with zero mapped founder links is a dependency cascade hazard
                if not founders:
                    cascades.append({
                        "cascade_type": "ZERO_FOUNDER_LINKAGE",
                        "affected_node": nid,
                        "severity": "MEDIUM",
                        "message": f"Venture '{nid}' operates with no registered founders in the knowledge graph. Governance hazard."
                    })
                    
        # 2. Check sector clustering densities
        sector_usage = {}
        for edge in edges:
            if edge["relation"] == "OPERATES_IN":
                sector_usage[edge["target"]] = sector_usage.get(edge["target"], 0) + 1
                
        # If a single sector contains more than 3 operating startups, it's a density crowd cascade zone
        for sec, count in sector_usage.items():
            if count >= 3:
                cascades.append({
                    "cascade_type": "SECTOR_CROWDING_CASCADE_HAZARD",
                    "affected_node": sec,
                    "severity": "HIGH",
                    "message": f"Sector '{sec}' is experiencing overcrowding ({count} startups). Sector contraction shock will propagate rapidly."
                })
                
        status = "CRITICAL_VOLATILITY" if any(c["severity"] == "HIGH" for c in cascades) else "STABLE"
        
        return {
            "ecosystem_cascade_status": status,
            "total_dependencies_checked": len(nodes),
            "cascade_warnings_count": len(cascades),
            "cascade_warnings": cascades
        }
