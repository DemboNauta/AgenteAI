# AgenteAI

AgenteAI es un proyecto que utiliza una base de datos vectorial (Chroma), embeddings generados con Sentence Transformers y ChatGPT para realizar búsquedas semánticas y generar respuestas en lenguaje natural.

## Características

- **Embeddings Multilingües**: Usa Sentence Transformers para generar representaciones vectoriales de textos.
- **Base de Datos Vectorial**: Utiliza Chroma para almacenar y consultar embeddings con filtros basados en metadatos.
- **ChatGPT**: Integra el modelo GPT-4 para generar respuestas detalladas en lenguaje natural.

## Requisitos Previos

- Python 3.9 o 3.10
- Clave API de OpenAI (puedes obtenerla en [OpenAI API](https://platform.openai.com/account/api-keys))

## Instalación

1. **Clona el Repositorio**:
   ```bash
   git clone https://github.com/DemboNauta/agente-ai.git
   cd agente-ai


## Crear env

python -m venv venv
source venv/bin/activate  # En Linux/macOS
.\venv\Scripts\Activate   # En Windows

## Instalar dependencias
pip install -r requirements.txt

## Configurar api_key

$env:OPENAI_API_KEY="tu-clave-api"

## Ejecutar
python main.py

## Resumen de comandos

![image](https://github.com/user-attachments/assets/9b62a367-1bb9-4ea6-abdd-4646cd1605f1)


## Ejemplos de respuesta al pedirle información sobre como añadir un inmueble:

![image](https://github.com/user-attachments/assets/fe62451e-aa0d-417d-8fdf-0267bfe14519)



