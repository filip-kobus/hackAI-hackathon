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
        
        self.conversation = None 
        if self.interactions:
            first_interaction = self.interactions[0]
            if isinstance(first_interaction, dict):
                chatbot_answer_dict = first_interaction.get('chatbot_answer')
                if isinstance(chatbot_answer_dict, dict):
                    self.conversation = chatbot_answer_dict.get('conversation')
            else:
                raise ValueError('Pierwsza interakcja nie jest słownikiem.')
        else:
            raise ValueError('Brak interakcji do pobrania ID konwersacji.')

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
        
        # Dodatkowe sprawdzenie, czy struktura jest poprawna przed próbą dostępu
        model_message_content = "Brak danych pytania"
        chatbot_answer_content = "Brak danych odpowiedzi"

        if isinstance(interaction, dict):
            model_message_dict = interaction.get('model_message')
            if isinstance(model_message_dict, dict):
                model_message_content = model_message_dict.get('response', "Brak treści pytania")
            
            chatbot_answer_dict = interaction.get('chatbot_answer')
            if isinstance(chatbot_answer_dict, dict):
                chatbot_answer_content = chatbot_answer_dict.get('response', "Brak treści odpowiedzi")
        else:
            print(f"Ostrzeżenie: Interakcja o indeksie {self.index -1} w pliku {self.chat_file_path} nie jest słownikiem.")
            
        return f'[PYTANIE] {model_message_content}\n[ODPOWIEDŹ] {chatbot_answer_content}'
    
    def get_chat_file_path(self):
        return os.path.basename(self.chat_file_path)

    def get_conversation_id(self):
        return self.conversation
    
def get_chats(folder_path):
    json_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".json") and os.path.isfile(os.path.join(folder_path, f))
    ]
    chats_list = []
    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            chats_list.append(Chat(file_path))
        except FileNotFoundError as e:
            print(f"Błąd przy przetwarzaniu pliku {file_name}: {e}")
        except json.JSONDecodeError as e:
            print(f"Błąd dekodowania JSON w pliku {file_name}: {e}")
        except Exception as e:
            print(f"Nieoczekiwany błąd przy przetwarzaniu pliku {file_name}: {e}")
    return chats_list

