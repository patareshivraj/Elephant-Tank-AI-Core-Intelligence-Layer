from typing import Dict, Any, List

class HybridRetriever:
    def search(self, collection, query_vector: List[float], metadata_filters: Dict[str, Any] = None, top_k: int = 5) -> Dict[str, Any]:
        """
        Executes a hybrid semantic search.
        It finds the nearest semantic neighbors (query_vector) BUT strictly filters out 
        any results that do not match the deterministic metadata criteria (e.g., stage, geography).
        """
        # ChromaDB query payload
        query_payload = {
            "query_embeddings": [query_vector],
            "n_results": top_k,
            "include": ["metadatas", "documents", "distances"]
        }
        
        # Apply deterministic hard-filters to prevent logical matching failures
        if metadata_filters:
            if len(metadata_filters) == 1:
                query_payload["where"] = metadata_filters
            else:
                # Convert multiple dict keys into a ChromaDB $and payload
                and_filters = [{k: {"$eq": v}} for k, v in metadata_filters.items()]
                query_payload["where"] = {"$and": and_filters}
                
        results = collection.query(**query_payload)
        return results
