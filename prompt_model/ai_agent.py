import requests

class ModelChat:

    def __init__(self, MODEL_NAME="llama3", OLLAMA_API_URL="http://localhost:11434/api/chat"):
        self.MODEL_NAME = MODEL_NAME
        self.OLLAMA_API_URL = OLLAMA_API_URL

    def send_prompt(self, system_prompt, user_input):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        response = requests.post(self.OLLAMA_API_URL, json={
            "model": self.MODEL_NAME,
            "messages": messages,
            "stream": False
            
        })

        if response.status_code != 200:
            raise Exception(f"Błąd zapytania do Ollama: {response.text}")

        return response.json()["message"]["content"]
    def send_message(self, message):
        response = requests.post(self.OLLAMA_API_URL, json={
            "model": self.MODEL_NAME,
            "prompt": message,
            "stream": False
        })

        if response.status_code != 200:
            raise Exception(f"Błąd zapytania do Ollama: {response.text}")

        return response.json()["response"]