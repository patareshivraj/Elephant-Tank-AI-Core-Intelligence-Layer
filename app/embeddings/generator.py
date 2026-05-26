from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingGenerator:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        """
        Initializes the local embedding model. 
        bge-small operates entirely offline and is optimized for retrieval tasks.
        """
        # Load the model once into memory
        self.model = SentenceTransformer(model_name)
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a dense numerical vector representation of the text.
        """
        # encode() returns a numpy array, we convert to standard float list for ChromaDB
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()
