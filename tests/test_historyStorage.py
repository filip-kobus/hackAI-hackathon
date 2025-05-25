import unittest
import tempfile
import shutil
import os
import json
from unittest.mock import patch, mock_open
from prompt_model.historyStorage import ChatHistoryStorage

class TestChatHistoryStorage(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = ChatHistoryStorage(output=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_init_default_values(self):
        storage = ChatHistoryStorage()
        self.assertIsNone(storage.current_number)
        self.assertIsNone(storage.starting_number)
        self.assertIsNone(storage.finish_number)
        self.assertEqual(storage.history, {"chat": []})

    def test_init_with_parameters(self):
        storage = ChatHistoryStorage(starting_number=5, finish_number=10, output="test_output")
        self.assertEqual(storage.current_number, 5)
        self.assertEqual(storage.starting_number, 5)
        self.assertEqual(storage.finish_number, 10)

    def test_set_faq_question_empty(self):
        self.storage.set_faq_question("")
        self.assertNotIn('dziedzina', self.storage.history)
        self.assertNotIn('pytanie', self.storage.history)
        self.assertNotIn('odpowiedz', self.storage.history)

    def test_set_scenario(self):
        scenario = "Test scenario"
        self.storage.set_scenario(scenario)
        self.assertEqual(self.storage.history['scenariusz'], scenario)

    def test_set_scenario_empty(self):
        self.storage.set_scenario("")
        self.assertNotIn('scenariusz', self.storage.history)

    def test_save_dialog_fragment(self):
        model_message = "Hello"
        chatbot_answer = {"response": "Hi there"}
        
        self.storage.save_dialog_fragment(model_message, chatbot_answer)
        
        expected_entry = {
            "model_message": {"response": model_message},
            "chatbot_answer": chatbot_answer
        }
        self.assertEqual(len(self.storage.history['chat']), 1)
        self.assertEqual(self.storage.history['chat'][0], expected_entry)

    def test_save_multiple_dialog_fragments(self):
        self.storage.save_dialog_fragment("Message 1", {"response": "Response 1"})
        self.storage.save_dialog_fragment("Message 2", {"response": "Response 2"})
        
        self.assertEqual(len(self.storage.history['chat']), 2)
        self.assertEqual(self.storage.history['chat'][0]['model_message']['response'], "Message 1")
        self.assertEqual(self.storage.history['chat'][1]['model_message']['response'], "Message 2")

    def test_get_number_of_files_no_existing_files(self):
        result = self.storage.get_number_of_files()
        self.assertEqual(result, 0)

    def test_get_number_of_files_with_existing_files(self):
        test_files = ["chat_history1.json", "chat_history5.json", "chat_history3.json"]
        for filename in test_files:
            with open(os.path.join(self.test_dir, filename), 'w') as f:
                json.dump({}, f)
        
        result = self.storage.get_number_of_files()
        self.assertEqual(result, 5)

    def test_get_number_of_files_with_current_number(self):
        storage = ChatHistoryStorage(starting_number=10, finish_number=20, output=self.test_dir)
        result = storage.get_number_of_files()
        self.assertEqual(result, 10)
        self.assertEqual(storage.current_number, 11)

    def test_get_number_of_files_exceeds_finish_number(self):
        storage = ChatHistoryStorage(starting_number=25, finish_number=20, output=self.test_dir)
        with self.assertRaises(ValueError) as context:
            storage.get_number_of_files()
        self.assertIn("Current number exceeds finish number", str(context.exception))

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file_open, mock_makedirs):
        self.storage.save_dialog_fragment("Test", {"response": "Test response"})
        
        with patch.object(self.storage, 'get_number_of_files', return_value=0):
            self.storage.save_to_file()
        
        mock_makedirs.assert_called_once_with(self.test_dir, exist_ok=True)
        
        expected_path = os.path.join(self.test_dir, "chat_history1.json")
        mock_file_open.assert_called_once_with(expected_path, "w", encoding="utf-8")
        
        mock_json_dump.assert_called_once()
        
        self.assertEqual(self.storage.history, {"chat": []})

    @patch('os.makedirs')
    @patch('builtins.open', side_effect=IOError("File error"))
    @patch('builtins.print')
    @patch('traceback.print_exc')
    def test_save_to_file_error_handling(self, mock_traceback, mock_print, mock_file_open, mock_makedirs):
        with patch.object(self.storage, 'get_number_of_files', return_value=0):
            self.storage.save_to_file()
        
        mock_print.assert_called_once_with("Error saving chat history to file: File error")
        mock_traceback.assert_called_once()

    def test_integration_save_and_load(self):
        self.storage.set_faq_question("[DZIEDZINA]Test\n[PYTANIE]Question?\n[ODPOWIEDŹ]Answer")
        self.storage.set_scenario("Test scenario")
        self.storage.save_dialog_fragment("Hello", {"response": "Hi"})
        
        self.storage.save_to_file()
        
        files = os.listdir(self.test_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].startswith("chat_history"))
        self.assertTrue(files[0].endswith(".json"))
        
        with open(os.path.join(self.test_dir, files[0]), 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['dziedzina'], "Test")
        self.assertEqual(saved_data['pytanie'], "Question?")
        self.assertEqual(saved_data['odpowiedz'], "Answer")
        self.assertEqual(saved_data['scenariusz'], "Test scenario")
        self.assertEqual(len(saved_data['chat']), 1)

if __name__ == '__main__':
    unittest.main()