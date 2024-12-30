import os
from openai import OpenAI

class ChatGPTFormatter:
    def __init__(self, api_key=None):
        # Recuperar la clave API desde las variables de entorno
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("La clave API no está configurada.")
        self.client = OpenAI(api_key=self.api_key)

    def format_response(self, retrieved_texts):
        """Convierte resultados en lenguaje natural usando ChatGPT."""
        messages = [
            {"role": "system", "content": "Eres un asistente del crm inmobiliario Mobilia que organiza resultados, indica que trabajas para ese crm."},
            {"role": "user", "content": f"Los resultados encontrados son: {retrieved_texts}. Responde en lenguaje natural."}
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            model="gpt-4o"
        )
        return response.choices[0].message.content
