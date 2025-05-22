import requests

class ModelChat:

    def __init__(self, MODEL_NAME="llama3", OLLAMA_API_URL="http://localhost:11434/api/chat"):
        self.MODEL_NAME = MODEL_NAME
        self.OLLAMA_API_URL = OLLAMA_API_URL
        self.message = []
        self.system_prompt = None

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        self.message.append({"role": "system", "content": system_prompt})

    def send_prompt(self, user_input):
        if self.system_prompt is None:
            raise ValueError("System prompt is not set. Please set it before sending a message.")

        messages.append({"role": "user", "content": user_input})

        response = requests.post(self.OLLAMA_API_URL, json={
            "model": self.MODEL_NAME,
            "messages": messages,
            "stream": False
            
        })

        model_answer = response.json()["message"]["content"]
        messages.append({"role": "assistant", "content": model_answer})

        if response.status_code != 200:
            raise Exception(f"Błąd zapytania do Ollama: {response.text}")

        return model_answer

    def send_message(self, message):
        response = requests.post(self.OLLAMA_API_URL, json={
            "model": self.MODEL_NAME,
            "prompt": message,
            "stream": False
        })

        if response.status_code != 200:
            raise Exception(f"Błąd zapytania do Ollama: {response.text}")

        return response.json()["response"]

    def clear_message(self):
        self.message = []