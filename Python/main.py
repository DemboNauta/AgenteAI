from embeddings.generator import EmbeddingGenerator
from database.chroma import ChromaDatabase
from chatgpt.response_formatter import ChatGPTFormatter

# Inicialización
generator = EmbeddingGenerator()
db = ChromaDatabase()
formatter = ChatGPTFormatter()

# Paso 1: Generar embeddings para documentos más complejos
documents = [
    {
        "text": (
            "Para agregar una nueva propiedad en Mobilia, ve a la sección 'Propiedades' en el menú principal. "
            "Haz clic en 'Nueva Propiedad'. Se abrirá un formulario donde puedes ingresar detalles como la dirección, "
            "el precio, la descripción, las características (número de habitaciones, baños, metros cuadrados, etc.), y "
            "fotografías de la propiedad. También puedes añadir información sobre el propietario, como su nombre, número "
            "de contacto y correo electrónico. Si necesitas asociar esta propiedad a un agente específico, puedes hacerlo "
            "desde el mismo formulario. Una vez completados los datos, asegúrate de guardar los cambios. Si encuentras problemas "
            "al guardar, verifica que todos los campos obligatorios estén llenos y que las fotografías cumplan con el tamaño máximo permitido."
        ),
        "category": "funcionalidad",
        "date": "2023-01-01"
    },
    {
        "text": (
            "La gestión de clientes en Mobilia se realiza desde la sección 'Clientes'. Aquí puedes ver una lista completa de todos los clientes "
            "registrados en tu sistema. Puedes agregar un nuevo cliente haciendo clic en 'Nuevo Cliente' y rellenando la información básica como nombre, "
            "número de teléfono, correo electrónico y preferencia de contacto. Además, puedes agregar notas relacionadas con sus intereses, como tipos de propiedades "
            "que busca, rangos de precios, y fechas tentativas para cerrar una compra. Mobilia también permite buscar clientes usando filtros avanzados, como su estado "
            "(activo, inactivo, prospecto), tipo de relación (comprador, vendedor, arrendatario) y fechas de registro. Esta funcionalidad es clave para mantener un seguimiento "
            "organizado y personalizado de cada cliente. Si necesitas actualizar datos, simplemente selecciona el cliente y edita la información deseada."
        ),
        "category": "gestión",
        "date": "2023-01-02"
    },
    {
        "text": (
            "Si tienes problemas para acceder a Mobilia, primero verifica tu conexión a internet. Una conexión inestable puede impedir que la plataforma cargue correctamente. "
            "Luego, asegúrate de que tus credenciales (nombre de usuario y contraseña) sean correctas. Si olvidaste tu contraseña, puedes usar la opción de 'Recuperar Contraseña' "
            "en la pantalla de inicio de sesión. Si el problema persiste, revisa si Mobilia está en mantenimiento. Los administradores suelen enviar correos o notificaciones previas "
            "cuando el sistema estará temporalmente fuera de servicio. También puedes intentar acceder desde otro navegador o dispositivo para descartar problemas locales. En caso de "
            "que el problema continúe, contacta al soporte técnico proporcionando detalles como el error que aparece en pantalla y las acciones que realizaste antes de encontrar el problema."
        ),
        "category": "soporte",
        "date": "2023-01-03"
    },
    {
        "text": (
            "La generación de informes de ventas en Mobilia es una herramienta poderosa para analizar el rendimiento de tu equipo. Para generar un informe, dirígete a la sección 'Informes' desde el menú principal. "
            "Selecciona la opción 'Informe de Ventas'. Esto abrirá una pantalla donde puedes personalizar el informe aplicando filtros como rango de fechas, agentes específicos, tipos de propiedades (venta o renta), y estados de las operaciones (cerrado, en proceso, cancelado). "
            "Una vez seleccionados los criterios, haz clic en 'Generar Informe'. Mobilia mostrará un resumen visual con gráficos interactivos y un desglose detallado de cada operación. Si necesitas compartir el informe, puedes exportarlo en formato PDF o Excel. "
            "En caso de que los datos no coincidan con tus expectativas, verifica que los filtros aplicados sean correctos y asegúrate de que todas las transacciones relevantes estén actualizadas en el sistema."
        ),
        "category": "reportes",
        "date": "2023-01-04"
    }
]


# Generar embeddings y añadir los documentos con metadatos a la base de datos
for i, doc in enumerate(documents):
    embedding = generator.generate_embeddings([doc["text"]])[0]
    db.add_documents(
        documents=[doc["text"]],
        ids=[f"doc_{i}"],
        metadatas=[{"category": doc["category"], "date": doc["date"]}]
    )

# Paso 2: Realizar una consulta sobre Mobilia
query = "¿Cómo puedo añadir un inmueble en Mobilia?"
query_embedding = generator.generate_embeddings([query])[0]

# Realizar una búsqueda híbrida (texto + metadatos)
print("\n--- Búsqueda Avanzada: Añadir un inmueble ---")
results = db.query_similar(query_text=query, n_results=2)
retrieved_texts = results["documents"]

# Paso 3: Formatear respuesta con ChatGPT
response = formatter.format_response(retrieved_texts)
print("Respuesta sobre la consulta:")
print(response)

# Paso 4: Realizar una consulta específica por categoría
print("\n--- Búsqueda por categoría: Funcionalidad ---")
category_results = db.query_similar(
    query_text="Agregar propiedades en Mobilia",
    n_results=2,
    filters={"category": "funcionalidad"}
)
for result in category_results["documents"]:
    print(result)
