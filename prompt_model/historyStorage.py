import json
import traceback
import os

class ChatHistoryStorage:
    OUTPUT_DIRECTORY = os.path.abspath(r'output')
    FILE_NAME = 'chat_history'

    def __init__(self):
        self.chat_history = []

    def save_dialog_fragment(self, model_message: str, chatbot_answer: dict[str, str | None]):
        self.chat_history.append({
            "model_message": {"response": model_message},
            "chatbot_answer": chatbot_answer
        })

    def save_to_file(self):
        os.makedirs(self.OUTPUT_DIRECTORY, exist_ok=True)

        existing_numbers = [
            int(fname[12:].rstrip(".json")) for fname in os.listdir(self.OUTPUT_DIRECTORY)
            if fname.startswith(self.FILE_NAME) and fname.endswith('.json')
        ]
        if not existing_numbers:
            max_num = 0
        else:
            max_num = max(existing_numbers)

        next_num = max_num + 1
        file_name = f"{self.FILE_NAME}{next_num}.json"
        file_path = os.path.join(self.OUTPUT_DIRECTORY, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(self.chat_history, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving chat history to file: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    chat_history_storage = ChatHistoryStorage()
    chat_history_storage.save_dialog_fragment("Test message", {"response": "Test response"})
    chat_history_storage.save_dialog_fragment("Test message2", {"response": "Test response2"})
    chat_history_storage.save_to_file()