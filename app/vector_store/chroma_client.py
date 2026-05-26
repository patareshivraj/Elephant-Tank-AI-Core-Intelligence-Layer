import chromadb
import os

class ChromaDBManager:
    def __init__(self, db_path: str = "d:/STARTUP/chroma_db_store"):
        """
        Initializes the persistent local vector database.
        Prevents usage of complex cloud infrastructure per Phase 6 requirements.
        """
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Initialize isolated ecosystem collections
        # hnsw:space = cosine ensures accurate directional similarity scoring
        self.startups = self.client.get_or_create_collection(name="startups", metadata={"hnsw:space": "cosine"})
        self.investors = self.client.get_or_create_collection(name="investors", metadata={"hnsw:space": "cosine"})
        self.mentors = self.client.get_or_create_collection(name="mentors", metadata={"hnsw:space": "cosine"})
        self.incubators = self.client.get_or_create_collection(name="incubators", metadata={"hnsw:space": "cosine"})
        
    def get_collection(self, collection_name: str):
        """Retrieves the target semantic space."""
        return self.client.get_collection(name=collection_name)
