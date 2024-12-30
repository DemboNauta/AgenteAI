import os
from openai import OpenAI

class ChatGPTFormatter:
    def __init__(self, api_key=None):
        # Recuperar la clave API desde las variables de entorno
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("La clave API no está configurada.")
        self.client = OpenAI(api_key=self.api_key)

    def format_response(self, retrieved_texts, original_question):
        """Convierte resultados en lenguaje natural usando ChatGPT."""
        print("-----Resultados encontrados:-----")
        print(retrieved_texts)
        messages = [
            {"role": "system", "content": f"Eres un asistente del CRM inmobiliario Mobilia que organiza resultados, indica que trabajas para ese crm. Ten en cuenta esta pregunta ya que obtendrás información que no es necesaria, solo has de responder con la que sea más adecuada:  {original_question}"},
            {"role": "user", "content": f"Los resultados encontrados son: {retrieved_texts}. Responde en lenguaje natural."}
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content
