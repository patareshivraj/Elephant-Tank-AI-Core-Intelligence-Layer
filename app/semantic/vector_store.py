import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from app.semantic.embedding_generator import EmbeddingGenerator

logger = logging.getLogger("ElephantTank.Semantic.VectorStore")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db_store")
os.makedirs(DB_PATH, exist_ok=True)

class VectorStore:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            logger.info(f"Initializing ChromaDB Client at: {DB_PATH}")
            cls._client = chromadb.PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))
        return cls._client

    @classmethod
    def get_collection(cls, name: str):
        client = cls.get_client()
        # ChromaDB requires collections to be managed. Let's create if not exists
        return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})

    @classmethod
    def upsert_item(cls, collection_name: str, item_id: str, text: str, metadata: Dict[str, Any]):
        """
        Generates embedding and stores/updates an item in the specified collection.
        """
        try:
            collection = cls.get_collection(collection_name)
            embedding = EmbeddingGenerator.generate_embeddings(text)
            
            # Serialize list/dict values inside metadata because ChromaDB only accepts simple types
            cleaned_metadata = {}
            for k, v in metadata.items():
                if isinstance(v, (list, dict)):
                    cleaned_metadata[k] = str(v)
                else:
                    cleaned_metadata[k] = v
                    
            collection.upsert(
                ids=[item_id],
                embeddings=[embedding],
                metadatas=[cleaned_metadata],
                documents=[text]
            )
            logger.info(f"Successfully upserted item {item_id} inside namespace '{collection_name}'")
        except Exception as e:
            logger.error(f"Failed to upsert item {item_id} into '{collection_name}': {e}")
            raise

    @classmethod
    def search_similarity(
        cls, 
        collection_name: str, 
        query_text: str, 
        limit: int = 5, 
        where_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs semantic similarity search inside a collection and returns top-k documents with metadata & distances.
        """
        try:
            collection = cls.get_collection(collection_name)
            query_embedding = EmbeddingGenerator.generate_embeddings(query_text)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_metadata
            )
            
            hits = []
            if results and results.get("ids") and len(results["ids"][0]) > 0:
                for idx in range(len(results["ids"][0])):
                    # cosine similarity from cosine distance: similarity = 1 - distance
                    distance = results["distances"][0][idx] if results.get("distances") else 0.0
                    similarity = 1.0 - distance
                    
                    hits.append({
                        "id": results["ids"][0][idx],
                        "metadata": results["metadatas"][0][idx],
                        "document": results["documents"][0][idx],
                        "similarity": max(0.0, min(1.0, similarity))
                    })
            return hits
        except Exception as e:
            logger.error(f"Vector search failed inside collection '{collection_name}': {e}")
            return []

    @classmethod
    def delete_item(cls, collection_name: str, item_id: str):
        try:
            collection = cls.get_collection(collection_name)
            collection.delete(ids=[item_id])
            logger.info(f"Deleted item {item_id} from '{collection_name}'")
        except Exception as e:
            logger.error(f"Failed to delete item {item_id} from '{collection_name}': {e}")
