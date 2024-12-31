import chromadb
import os
from dotenv import load_dotenv

class ChromaDatabase:
    def __init__(self):
        load_dotenv()
        storage_path = os.getenv('STORAGE_PATH')
        self.client = chromadb.PersistentClient(
            path=storage_path
        )
        self.collection = self.client.get_or_create_collection("text_embeddings")

    def add_documents(self, documents, ids, metadatas=None):
        """Agrega documentos a la colección."""
        self.collection.add(documents=documents, ids=ids, metadatas=metadatas)

    def check_existing_ids(self, ids):
        """Verifica si los IDs ya están en la colección."""
        existing_ids = self.collection.get()["ids"]
        return [doc_id for doc_id in ids if doc_id in existing_ids]
    
    def add_documents_safely(self, documents, ids, metadatas=None):
        """Agrega documentos nuevos a la colección, evitando duplicados."""
        existing_ids = self.check_existing_ids(ids)  # Usamos self aquí
        new_ids = [doc_id for doc_id in ids if doc_id not in existing_ids]
        if new_ids:
            # Filtrar documentos y metadatos correspondientes a los nuevos IDs
            new_documents = [doc for doc, doc_id in zip(documents, ids) if doc_id in new_ids]
            new_metadatas = [meta for meta, doc_id in zip(metadatas, ids) if doc_id in new_ids]

            self.collection.add(documents=new_documents, ids=new_ids, metadatas=new_metadatas)
            print(f"Se han agregado {len(new_ids)} documentos nuevos.")
        else:
            print("No hay documentos nuevos para agregar.")

    def delete_documents(self, ids):
        """Elimina documentos de la colección."""
        self.collection.delete(ids=ids)

    def delete_all_documents(self):
        """Elimina todos los documentos de la colección."""
        self.collection.delete(delete_all=True)

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
