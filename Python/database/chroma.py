import chromadb

class ChromaDatabase:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("text_embeddings")

    def add_documents(self, documents, ids, metadatas=None):
        """Agrega documentos a la colección."""
        self.collection.add(documents=documents, ids=ids, metadatas=metadatas)
    
    def query_similar(self, query_text, n_results=5, filters=None):
        """
        Realiza una consulta de similitud en la base de datos.
        Puede incluir filtros basados en metadatos.
        """
        if filters:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=filters  # Chroma usa `where` para filtrar por metadatos
            )
        else:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )            
        return results
