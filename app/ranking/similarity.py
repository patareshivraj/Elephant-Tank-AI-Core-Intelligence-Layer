from typing import List, Dict, Any

class SimilarityRanker:
    def rank_and_filter(self, raw_results: Dict[str, Any], similarity_threshold: float = 0.65) -> List[Dict[str, Any]]:
        """
        Parses ChromaDB outputs. Converts vector distances to similarity scores (1.0 - distance).
        Aggressively filters out weak semantic matches below the threshold to prevent speculative recommendations.
        """
        filtered_matches = []
        
        if not raw_results or not raw_results.get("ids") or not raw_results["ids"][0]:
            return filtered_matches

        # Extract the first (and only) query result arrays
        ids = raw_results["ids"][0]
        distances = raw_results["distances"][0]
        metadatas = raw_results["metadatas"][0]
        documents = raw_results["documents"][0]
        
        for i in range(len(ids)):
            # Convert cosine distance to cosine similarity
            similarity_score = 1.0 - distances[i]
            
            if similarity_score >= similarity_threshold:
                filtered_matches.append({
                    "id": ids[i],
                    "similarity": round(similarity_score, 3),
                    "metadata": metadatas[i],
                    "document": documents[i]
                })
                
        # Return ranked by highest similarity first
        return sorted(filtered_matches, key=lambda x: x["similarity"], reverse=True)
