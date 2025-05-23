import json
import traceback
import os

class ChatHistoryStorage:
    OUTPUT_DIRECTORY = os.path.abspath(r'output')
    FILE_NAME = 'chat_history'


    def __init__(self, starting_number=None, finish_number=None):
        self.current_number = starting_number
        self.starting_number = starting_number
        self.finish_number = finish_number

        self.history = {
                "dziedzina":"",
                "pytanie": "",
                "odpowiedz": "",
                "chat": []
        }

    def set_faq_question(self, question: str):
        if question:
            self.history['dziedzina'] = question.split("\n")[0].lstrip("[DZIEDZINA]").strip()
            self.history['pytanie'] = question.split("\n")[1].lstrip("[PYTANIE]").strip()
            self.history['odpowiedz'] = question.split("\n")[2].lstrip("[ODPOWIEDŹ]").strip()

    def save_dialog_fragment(self, model_message: str, chatbot_answer: dict[str, str | None], question: str = None):
        self.history['chat'].append({
            "model_message": {"response": model_message},
            "chatbot_answer": chatbot_answer
        })

    def get_number_of_files(self):
        if self.current_number is not None:
            if self.current_number > self.finish_number:
                raise ValueError("Current number exceeds finish number.")
            to_return = self.current_number
            self.current_number += 1
            return to_return
        existing_numbers = [
            int(fname[12:].rstrip(".json")) for fname in os.listdir(self.OUTPUT_DIRECTORY)
            if fname.startswith(self.FILE_NAME) and fname.endswith('.json')
        ]
        if not existing_numbers:
            return 0
        else:
            return max(existing_numbers)

    def save_to_file(self):
        os.makedirs(self.OUTPUT_DIRECTORY, exist_ok=True)

        max_num = self.get_number_of_files()

        next_num = max_num + 1
        file_name = f"{self.FILE_NAME}{next_num}.json"
        file_path = os.path.join(self.OUTPUT_DIRECTORY, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(self.history, file, ensure_ascii=False, indent=4)
            self.history['chat'] = []
        except Exception as e:
            print(f"Error saving chat history to file: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    chat_history_storage = ChatHistoryStorage()
    chat_history_storage.save_dialog_fragment("Test message", {"response": "Test response"})
    chat_history_storage.save_dialog_fragment("Test message2", {"response": "Test response2"})
    chat_history_storage.save_to_file()