from prompt_model.gradeHistory import GradeHistory
import unittest
from unittest.mock import patch, mock_open
import datetime
import os

class GradeHistoryTest(unittest.TestCase):

    def setUp(self):
        self.grade_history = GradeHistory()

    def test_set_topic(self):
        self.grade_history.set_chat_topic('Temat')

        self.assertEqual(self.grade_history.history['topic'], 'Temat')
    
    def test_set_chat_id(self):
        self.grade_history.set_chat_id('1')

        self.assertEqual(self.grade_history.history['id'], '1')
    
    def test_split_q_and_a(self):
        q_and_a = '[PYTANIE] pytanie\n[ODPOWIEDŹ] odpowiedź'
        q, a = self.grade_history.split_q_and_a(q_and_a)
        self.assertEqual(q, 'user: pytanie')
        self.assertEqual(a, 'chat: odpowiedź')

    def test_save_graded_answer(self):
        q_and_a = '[PYTANIE] pytanie\n[ODPOWIEDŹ] odpowiedź'
        category = 'inne'
        grade = 5
        self.grade_history.save_graded_answer(q_and_a, category, grade)

        self.assertEqual(self.grade_history.history['chat'][0]['question'], 'user: pytanie')
        self.assertEqual(self.grade_history.history['chat'][0]['answer'], 'chat: odpowiedź')
        self.assertEqual(self.grade_history.history['chat'][0]['category'], 'inne')
        self.assertEqual(self.grade_history.history['chat'][0]['grade'], 5)
        
        q_and_a = '[PYTANIE] pytanie1\n[ODPOWIEDŹ] odpowiedź1'
        category = 'inne1'
        grade = 10
        self.grade_history.save_graded_answer(q_and_a, category, grade)
        
        self.assertEqual(self.grade_history.history['chat'][1]['question'], 'user: pytanie1')
        self.assertEqual(self.grade_history.history['chat'][1]['answer'], 'chat: odpowiedź1')
        self.assertEqual(self.grade_history.history['chat'][1]['category'], 'inne1')
        self.assertEqual(self.grade_history.history['chat'][1]['grade'], 10)

    def test_clear_history(self):
        q_and_a = '[PYTANIE] pytanie\n[ODPOWIEDŹ] odpowiedź'
        category = 'inne'
        grade = 5
        self.grade_history.save_graded_answer(q_and_a, category, grade)
        self.grade_history.save_graded_answer(q_and_a, category, grade)

        self.grade_history.clear_history()

        self.assertEqual(self.grade_history.history['id'], None)
        self.assertEqual(self.grade_history.history['topic'], "")
        self.assertListEqual(self.grade_history.history['chat'], [])

    def test_pick_lowest_score(self):
        q_and_a = '[PYTANIE] pytanie\n[ODPOWIEDŹ] odpowiedź'
        category = 'inne'
        self.grade_history.save_graded_answer(q_and_a, category, 5)
        self.grade_history.save_graded_answer(q_and_a, category, 4)
        self.grade_history.save_graded_answer(q_and_a, category, 6)
        self.grade_history.save_graded_answer(q_and_a, category, 10)

        lowest = self.grade_history.pick_lowest_score()
        self.assertEqual(lowest, 4)

        self.grade_history.save_graded_answer(q_and_a, category, 1)
        lowest = self.grade_history.pick_lowest_score()
        self.assertEqual(lowest, 1)
        
        self.grade_history.save_graded_answer(q_and_a, category, 404)
        lowest = self.grade_history.pick_lowest_score()
        self.assertEqual(lowest, 404)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("json.dump")
    @patch("datetime.datetime")
    def test_save_graded_chat(self, mock_datetime, mock_json_dump, mock_makedirs, mock_file_open):
        # Utwórz instancję klasy
        gh = GradeHistory(output="test_output")

        # Dane testowe historii
        original_history = {
            "id": 123,
            "topic": "Test",
            "chat": [
                {"question": "Q", "answer": "A", "category": "cat", "grade": 5}
            ]
        }
        gh.history = original_history.copy()

        gh.pick_lowest_score = lambda: 5

        fake_now = datetime.datetime(2025, 5, 25, 15, 30, 0)
        mock_datetime.now.return_value = fake_now
        mock_datetime.strftime = datetime.datetime.strftime
        
        input_file = "input_file.json"
        timestamp = fake_now.strftime("%Y-%m-%d_%H-%M-%S")
        expected_path = os.path.join(gh.OUTPUT_DIRECTORY, "5", f"input_file_{timestamp}.json")

        gh.save_graded_chat(input_file)

        expected_dirs = [os.path.join(gh.OUTPUT_DIRECTORY, str(i)) for i in range(1, 11)] + [
            os.path.join(gh.OUTPUT_DIRECTORY, "404")
        ]
        mock_makedirs.assert_any_call(gh.OUTPUT_DIRECTORY, exist_ok=True)
        for d in expected_dirs:
            mock_makedirs.assert_any_call(d, exist_ok=True)

        mock_file_open.assert_called_once_with(expected_path, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(original_history, mock_file_open(), ensure_ascii=False, indent=4)

        self.assertEqual(gh.history, {"id": None, "topic": "", "chat": []})