import json
import os

class Chat:

    def __init__(self, chat_file_path):
        self.chat_file_path = chat_file_path
        if not os.path.exists(self.chat_file_path):
            raise FileNotFoundError(f"Plik nie istnieje: {self.chat_file_path}")

        with open(self.chat_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.base_question = data.get("pytanie")
        self.base_answer = data.get("odpowiedz")
        self.field = data.get("dziedzina")
        self.interactions = data.get("chat", [])
    
    def get_chat_topic_json(self):
        topic = {}
        topic["field"] = self.field
        topic["base_question"] = self.base_question
        topic["base_answer"] = self.base_answer
        return topic
    
    def get_chat_topic_string(self):
        return f'[DZIEDZINA] {self.field}\n[PYTANIE] {self.base_question}\n[ODPOWIEDŹ] {self.base_answer}'
    
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.interactions):
            raise StopIteration
        interaction = self.interactions[self.index]
        self.index += 1
        return f'[PYTANIE] {interaction['model_message']['response']}\n[ODPOWIEDŹ] {interaction['chatbot_answer']['response']}'
    
    def get_chat_file_path(self):
        return os.path.basename(self.chat_file_path)
    
def get_chats(folder_path):
    json_files = [
    f for f in os.listdir(folder_path)
    if f.endswith(".json") and os.path.isfile(os.path.join(folder_path, f))
    ]
    return [Chat(os.path.join(folder_path, file)) for file in json_files]