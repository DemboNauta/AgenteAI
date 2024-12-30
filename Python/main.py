from embeddings.generator import EmbeddingGenerator
from database.chroma import ChromaDatabase
from chatgpt.response_formatter import ChatGPTFormatter

# Inicialización
generator = EmbeddingGenerator()
db = ChromaDatabase()
formatter = ChatGPTFormatter()

# Paso 1: Generar embeddings para documentos más complejos
documents = [
    {"text": "Cuenca es una ciudad española famosa por sus casas colgantes.", "category": "turismo", "date": "2023-01-01"},
    {"text": "La Catedral de Cuenca es un icono del estilo gótico en España.", "category": "historia", "date": "2023-01-02"},
    {"text": "El puente de San Pablo en Cuenca ofrece vistas espectaculares.", "category": "arquitectura", "date": "2023-01-03"},
    {"text": "Cuenca es conocida también por su gastronomía tradicional.", "category": "gastronomía", "date": "2023-01-04"}
]

# Generar embeddings y añadir los documentos con metadatos a la base de datos
for i, doc in enumerate(documents):
    embedding = generator.generate_embeddings([doc["text"]])[0]
    db.add_documents(
        documents=[doc["text"]],
        ids=[f"doc_{i}"],
        metadatas=[{"category": doc["category"], "date": doc["date"]}]
    )

# Paso 2: Realizar una consulta avanzada
query = "Lugares turísticos en Cuenca"
query_embedding = generator.generate_embeddings([query])[0]

# Realizar una búsqueda híbrida (texto + metadatos)
results = db.query_similar(query_text=query, n_results=2)
retrieved_texts = results["documents"]

# Paso 3: Formatear respuesta con ChatGPT
response = formatter.format_response(retrieved_texts)
print("Respuesta sobre la consulta:")
print(response)

# Paso 4: Realizar una consulta basada en metadatos específicos
print("\n--- Búsqueda por categoría: Turismo ---")
category_results = db.query_similar(
    query_text="Turismo en Cuenca",
    n_results=2,
    filters={"category": "turismo"}
)
for result in category_results["documents"]:
    print(result)
