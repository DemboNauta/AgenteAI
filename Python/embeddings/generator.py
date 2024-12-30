from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name='distiluse-base-multilingual-cased-v2'):
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, texts):
        """Convierte una lista de textos en embeddings."""
        return self.model.encode(texts)
