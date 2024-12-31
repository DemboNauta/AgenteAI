from embeddings.generator import EmbeddingGenerator
from database.chroma import ChromaDatabase
from chatgpt.response_formatter import ChatGPTFormatter

# Inicialización
generator = EmbeddingGenerator()
db = ChromaDatabase()
chatGPTformatter = ChatGPTFormatter()

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
    },
        {
        "text": (
            "Para crear una propiedad con múltiples características en Mobilia, ve a la sección 'Propiedades' y selecciona 'Nueva Propiedad'. "
            "Además de los campos básicos como dirección, precio y descripción, puedes incluir características avanzadas como número de plantas, "
            "si cuenta con estacionamiento, jardín, o si es apta para mascotas. Asegúrate de usar las etiquetas personalizadas que Mobilia permite "
            "para categorizar mejor la propiedad y hacerla más fácil de encontrar para potenciales clientes. Una vez ingresada toda la información, "
            "no olvides subir imágenes de calidad que resalten las mejores características de la propiedad. Guardarás la propiedad haciendo clic en 'Guardar'."
        ),
        "category": "funcionalidad",
        "date": "2023-01-05"
    },
    {
        "text": (
            "Para duplicar una propiedad existente en Mobilia, accede a la sección 'Propiedades' y selecciona la propiedad que deseas duplicar. "
            "Haz clic en el botón 'Duplicar' que aparece en el menú de acciones. Esto generará un nuevo registro con la misma información, incluyendo "
            "características, descripción y fotografías. Puedes editar este duplicado para actualizar la dirección, precio u otras características antes de guardarlo. "
            "Esta funcionalidad es útil cuando necesitas registrar propiedades similares con pequeños ajustes en su configuración."
        ),
        "category": "funcionalidad",
        "date": "2023-01-06"
    },
    {
        "text": (
            "Para asignar una propiedad a varios agentes en Mobilia, ve a la sección 'Propiedades', selecciona la propiedad deseada y accede a 'Asignar agentes'. "
            "Selecciona múltiples agentes desde el menú desplegable. Puedes especificar las responsabilidades de cada agente (como agente principal o de apoyo). "
            "Mobilia permite a los agentes colaborar en el seguimiento y cierre de ventas de manera más efectiva. Recuerda que debes tener permisos de administrador "
            "para realizar asignaciones múltiples."
        ),
        "category": "funcionalidad",
        "date": "2023-01-07"
    },
    {
        "text": (
            "Para asignar una categoría personalizada a un cliente en Mobilia, accede a la sección 'Clientes', selecciona el cliente y haz clic en 'Editar'. "
            "En la pestaña de 'Información Adicional', selecciona o crea una nueva categoría personalizada que describa al cliente, como 'Interesado en propiedades comerciales' "
            "o 'Comprador frecuente'. Esto permitirá una mejor segmentación al momento de enviar comunicaciones o realizar seguimiento personalizado."
        ),
        "category": "gestión",
        "date": "2023-01-08"
    },
    {
        "text": (
            "Puedes fusionar dos registros de clientes duplicados en Mobilia accediendo a la sección 'Clientes' y seleccionando ambos registros. "
            "Haz clic en 'Fusionar clientes', y Mobilia combinará automáticamente los datos, manteniendo la información más reciente o solicitando "
            "que elijas los valores correctos. Esta funcionalidad es útil para evitar confusiones y garantizar que toda la información sobre un cliente "
            "esté centralizada."
        ),
        "category": "gestión",
        "date": "2023-01-09"
    },
    {
        "text": (
            "Para enviar un correo masivo a tus clientes en Mobilia, ve a la sección 'Campañas de Correo'. Crea una nueva campaña y selecciona el grupo de clientes "
            "a los que deseas enviar el correo. Puedes usar filtros avanzados para segmentar por intereses, estado o historial de interacciones. Una vez creado el mensaje, "
            "puedes previsualizarlo y programarlo para enviarlo en una fecha y hora específicas. Mobilia también ofrece estadísticas sobre la tasa de apertura y clics del correo enviado."
        ),
        "category": "gestión",
        "date": "2023-01-10"
    },
    {
        "text": (
            "Si no puedes acceder a Mobilia desde tu red local, verifica primero si tienes conexión a internet. Si la conexión es estable pero el problema persiste, "
            "intenta acceder desde un dispositivo móvil o una red externa para descartar bloqueos de red. También asegúrate de que tu firewall o antivirus no esté bloqueando "
            "el acceso al sitio de Mobilia. Si nada de esto funciona, contacta al equipo de soporte proporcionando tu dirección IP y cualquier mensaje de error recibido."
        ),
        "category": "soporte",
        "date": "2023-01-11"
    },
    {
        "text": (
            "Para reportar un error en Mobilia, ve a la sección 'Ayuda' en el menú principal y selecciona 'Reportar un problema'. Describe el error con detalle, incluyendo "
            "las acciones realizadas antes de encontrar el problema. Mobilia te permite adjuntar capturas de pantalla o grabaciones de pantalla para facilitar el diagnóstico. "
            "El equipo de soporte te responderá a la brevedad con pasos para solucionar el problema o información sobre una actualización próxima."
        ),
        "category": "soporte",
        "date": "2023-01-12"
    },
    {
        "text": (
            "Si has olvidado tu contraseña en Mobilia, utiliza la opción de 'Recuperar Contraseña' en la página de inicio de sesión. Ingresa tu correo electrónico registrado "
            "y recibirás un enlace para restablecer tu contraseña. Si no recibes el correo en unos minutos, verifica tu carpeta de spam o contacta al soporte técnico para asegurarte "
            "de que la dirección de correo sea correcta y esté registrada en el sistema."
        ),
        "category": "soporte",
        "date": "2023-01-13"
    },
    {
        "text": (
            "Para generar un reporte de seguimiento de clientes en Mobilia, accede a la sección 'Reportes' y selecciona 'Seguimiento de Clientes'. "
            "Aplica filtros como el estado del cliente (activo, inactivo, prospecto), fechas de última interacción o agentes asignados. "
            "Mobilia generará un reporte visual que incluye gráficos de barras y datos detallados por cliente. Puedes exportar el reporte en formato PDF o Excel."
        ),
        "category": "reportes",
        "date": "2023-01-14"
    },
    {
        "text": (
            "Puedes automatizar la generación de reportes en Mobilia desde la sección 'Automatizaciones'. Configura una nueva tarea automatizada, eligiendo el tipo de reporte "
            "que deseas generar, como 'Informe de Ventas' o 'Seguimiento de Clientes'. Define la frecuencia (diaria, semanal, mensual) y selecciona los destinatarios. Mobilia "
            "enviará automáticamente el reporte a los correos indicados."
        ),
        "category": "reportes",
        "date": "2023-01-15"
    },
    {
        "text": (
            "Para analizar las tendencias de ventas en Mobilia, genera un reporte de 'Tendencias' desde la sección 'Reportes'. "
            "Selecciona un rango de fechas amplio y aplica filtros como tipo de propiedad, agente responsable y región. "
            "El reporte incluirá gráficos que muestran cómo han cambiado las ventas a lo largo del tiempo, ayudándote a identificar patrones y áreas de mejora."
        ),
        "category": "reportes",
        "date": "2023-01-16"
    },

]


# Generar embeddings y añadir los documentos con metadatos a la base de datos
for i, doc in enumerate(documents):
    embedding = generator.generate_embeddings([doc["text"]])[0]
    db.add_documents_safely(
        documents=[doc["text"]],
        ids=[f"doc_{i}"],
        metadatas=[{"category": doc["category"], "date": doc["date"]}]
    )

# Paso 2: Realizar una consulta sobre Mobilia
query = "¿Qué pasos debo seguir para asignar múltiples agentes a una propiedad?"
nombreCliente = "Edgar Milá"
print(f"\n---Consulta sobre Mobilia: {query}---")
query_embedding = generator.generate_embeddings([query])[0]

# Realizar una búsqueda híbrida (texto + metadatos)
print("\n--- Búsqueda Avanzada: Añadir un inmueble ---")
results = db.query_similar(query_text=query, n_results=2)
retrieved_texts = results["documents"]

# Paso 3: Formatear respuesta con ChatGPT
response = chatGPTformatter.format_response(retrieved_texts, query, nombreCliente)
print("\n---Respuesta sobre la consulta:---")
print(response)

# Paso 4: Realizar una consulta específica por categoría
print("\n--- Búsqueda por categoría: Funcionalidad ---")
category_results = db.query_similar(
    query_text="asignar múltiples agentes a una propiedad",
    n_results=2,
    filters={"category": "funcionalidad"}
)
for result in category_results["documents"]:
    print(result)
