import os
import json
import time
import logging
from typing import Dict, Any, List, Set, Tuple

logger = logging.getLogger("ElephantTank.KnowledgeGraph.VentureGraph")

KG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "knowledge_graph"))
os.makedirs(KG_DIR, exist_ok=True)
GRAPH_FILE = os.path.join(KG_DIR, "graph.json")

class VentureKnowledgeGraph:
    """
    Venture Knowledge Graph Layer.
    Models, traverses, and tracks ecosystem networks connecting founders,
    startups, mentors, technologies, sectors, and institutional investors.
    """
    
    @classmethod
    def _load_graph(cls) -> Dict[str, Any]:
        if not os.path.exists(GRAPH_FILE):
            return {"nodes": {}, "edges": []}
        try:
            with open(GRAPH_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load knowledge graph: {e}")
            return {"nodes": {}, "edges": []}
            
    @classmethod
    def _save_graph(cls, graph: Dict[str, Any]):
        try:
            with open(GRAPH_FILE, "w") as f:
                json.dump(graph, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save knowledge graph: {e}")

    @classmethod
    def add_node(cls, node_id: str, label: str, properties: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Adds a semantic entity node to the graph.
        """
        logger.info(f"Adding Knowledge Graph node: {node_id} ({label})")
        graph = cls._load_graph()
        
        nid = node_id.lower().strip()
        graph["nodes"][nid] = {
            "node_id": node_id,
            "label": label,
            "properties": properties or {},
            "timestamp": int(time.time())
        }
        
        cls._save_graph(graph)
        return {"status": "SUCCESS", "node_id": nid}

    @classmethod
    def add_edge(cls, source_id: str, target_id: str, relation: str, properties: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Creates a directed semantic relationship edge between two entities.
        """
        src = source_id.lower().strip()
        tgt = target_id.lower().strip()
        
        logger.info(f"Adding Knowledge Graph edge: {src} --[{relation}]--> {tgt}")
        graph = cls._load_graph()
        
        # Verify node existence, create placeholder if missing
        if src not in graph["nodes"]:
            graph["nodes"][src] = {"node_id": source_id, "label": "UNSPECIFIED", "properties": {}, "timestamp": int(time.time())}
        if tgt not in graph["nodes"]:
            graph["nodes"][tgt] = {"node_id": target_id, "label": "UNSPECIFIED", "properties": {}, "timestamp": int(time.time())}
            
        # Add edge if not already exists
        edge_exists = False
        for edge in graph["edges"]:
            if edge["source"] == src and edge["target"] == tgt and edge["relation"] == relation:
                edge_exists = True
                break
                
        if not edge_exists:
            graph["edges"].append({
                "source": src,
                "target": tgt,
                "relation": relation,
                "properties": properties or {},
                "timestamp": int(time.time())
            })
            
        cls._save_graph(graph)
        return {
            "stage": "KNOWLEDGE_GRAPH_UPDATE",
            "status": "SUCCESS",
            "message": f"Linked {source_id} to {target_id} via '{relation}'.",
            "timestamp": int(time.time())
        }

    @classmethod
    def traverse_relations(cls, node_id: str) -> List[Dict[str, Any]]:
        """
        Traverses relationships for a given node to find direct neighbors and relations.
        """
        nid = node_id.lower().strip()
        graph = cls._load_graph()
        
        results = []
        for edge in graph["edges"]:
            if edge["source"] == nid:
                results.append({
                    "direction": "OUTGOING",
                    "neighbor": graph["nodes"].get(edge["target"], {}).get("node_id", edge["target"]),
                    "neighbor_label": graph["nodes"].get(edge["target"], {}).get("label", "Unknown"),
                    "relation": edge["relation"],
                    "properties": edge["properties"]
                })
            elif edge["target"] == nid:
                results.append({
                    "direction": "INCOMING",
                    "neighbor": graph["nodes"].get(edge["source"], {}).get("node_id", edge["source"]),
                    "neighbor_label": graph["nodes"].get(edge["source"], {}).get("label", "Unknown"),
                    "relation": edge["relation"],
                    "properties": edge["properties"]
                })
        return results

    @classmethod
    def discover_sector_subgraph(cls, sector_name: str) -> Dict[str, Any]:
        """
        Discovers all startups and technology links clustered under a specific sector.
        """
        sec = sector_name.lower().strip()
        graph = cls._load_graph()
        
        relevant_nodes = set()
        relevant_edges = []
        
        # 1. Find all startups operating in this sector
        for edge in graph["edges"]:
            if edge["relation"] == "OPERATES_IN" and edge["target"] == sec:
                relevant_nodes.add(edge["source"])
                relevant_edges.append(edge)
                
        # 2. Add edges connected to these startups (founders, technology)
        for edge in graph["edges"]:
            if edge["source"] in relevant_nodes or edge["target"] in relevant_nodes:
                relevant_nodes.add(edge["source"])
                relevant_nodes.add(edge["target"])
                if edge not in relevant_edges:
                    relevant_edges.append(edge)
                    
        return {
            "nodes": {nid: graph["nodes"][nid] for nid in relevant_nodes if nid in graph["nodes"]},
            "edges": relevant_edges
        }
