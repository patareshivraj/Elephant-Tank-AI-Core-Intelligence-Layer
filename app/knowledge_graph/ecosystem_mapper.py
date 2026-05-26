import logging
from typing import Dict, Any, List
from app.knowledge_graph.venture_graph import VentureKnowledgeGraph

logger = logging.getLogger("ElephantTank.KnowledgeGraph.EcosystemMapper")

class EcosystemRelationshipMapper:
    """
    Ecosystem Relationship Mapper.
    Exposes explainable venture networks, maps target market adjacencies,
    and uncovers subtle overlaps across sectors, technologies, and institutional investors.
    """
    
    @classmethod
    def map_competitive_overlaps(cls, startup_name: str) -> Dict[str, Any]:
        """
        Scans direct and indirect knowledge graph boundaries to find competing ventures.
        """
        logger.info(f"Mapping competitor ecosystems for: {startup_name}")
        
        # Get immediate neighbors
        relations = VentureKnowledgeGraph.traverse_relations(startup_name)
        
        direct_competitors = []
        shared_sectors = []
        shared_investors = []
        
        # 1. Inspect direct links
        for r in relations:
            if r["relation"] == "COMPETES_WITH":
                direct_competitors.append(r["neighbor"])
            elif r["relation"] == "OPERATES_IN":
                shared_sectors.append(r["neighbor"])
                
        # 2. Traverse shared sectors to find peer startups
        peer_startups = set()
        for sec in shared_sectors:
            sec_relations = VentureKnowledgeGraph.traverse_relations(sec)
            for sr in sec_relations:
                if sr["direction"] == "INCOMING" and sr["neighbor"].lower() != startup_name.lower():
                    peer_startups.add(sr["neighbor"])
                    
        return {
            "target_startup": startup_name,
            "direct_competitors": direct_competitors,
            "associated_sectors": shared_sectors,
            "peer_sector_startups": list(peer_startups),
            "ecosystem_overlap_narrative": f"Mapped {len(direct_competitors)} direct competitors and {len(peer_startups)} peer startups under sectors {shared_sectors}."
        }
