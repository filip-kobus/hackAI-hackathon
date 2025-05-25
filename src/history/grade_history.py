"""
Class for handling grading history and dumping it into json file.
"""


import json
import os
import traceback
import datetime

class GradeHistory:
    FILE_NAME = 'graded_chat'

    def __init__(self, output='graded_output'):
        self.OUTPUT_DIRECTORY = os.path.abspath(output)
        self.history = {
            "id": None,
            "topic": "",
            "chat": []
        }

    def set_chat_topic(self, topic: str):
        """Ustawia temat czatu (np. scenariusz lub pytanie FAQ)."""
        self.history['topic'] = topic
        
    def set_chat_id(self, id: int):
        """Ustawia id czatu"""
        self.history['id'] = id
        
    def split_q_and_a(self, q_and_a: str):
        q_and_a = q_and_a.split("\n")
        q = " ".join(q_and_a[0].split(" ")[1:])
        a = " ".join(" ".join(q_and_a[1:]).split(" ")[1:])
        q = f"user: {q}"
        a = f"chat: {a}"
        return q, a

    #def save_graded_answer(self, input_message: str, model_answer: str, thought_process: str, category: str, grade: int):
    def save_graded_answer(self, q_and_a: str, category: str, grade: int):
        question, answer = self.split_q_and_a(q_and_a)
        """Dodaje oceniony fragment czatu do historii."""
        self.history['chat'].append({
            "question": question,
            "answer": answer,
            "category": category,
            "grade": grade
        })

    def save_graded_chat(self, og_input_file: str):
        """Zapisuje całą historię ocenionego czatu do pliku JSON."""
        
        # Stworzeni folderu nadrzędnego, podrzędnych: 1-10 oraz 404
        os.makedirs(self.OUTPUT_DIRECTORY, exist_ok=True)
        for i in range(1,11):
            os.makedirs(os.path.join(self.OUTPUT_DIRECTORY, str(i)), exist_ok=True)
        os.makedirs(os.path.join(self.OUTPUT_DIRECTORY, "404"), exist_ok=True)
        
        # Ustal numer pliku na podstawie oryginalnego pliku wejściowego konwersacji dla danego pytania i timestamp'a
        score = self.pick_lowest_score()
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.OUTPUT_DIRECTORY, str(score), f"{og_input_file.replace(".json", "")}_{now}.json")
        try:
            with open(file_path, "w", encoding="utf-8") as file: 
                json.dump(self.history, file, ensure_ascii=False, indent=4)
            self.clear_history()
        except Exception as e:
            print(f"Error saving graded chat to file: {e}")
            traceback.print_exc()

    def clear_history(self):
        """Czyści historię po zapisie."""
        self.history = {
            "id": None,
            "topic": "",
            "chat": []
        }
        
    def pick_lowest_score(self):
        lowest = 10
        for item in self.history["chat"]:
            grade = int(item["grade"])
            if grade == 404:
                return 404
            elif grade < lowest:
                lowest = grade
        if grade < 1:
            return 1
        return lowest