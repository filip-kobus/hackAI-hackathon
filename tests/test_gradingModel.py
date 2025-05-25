import unittest
from unittest.mock import patch, MagicMock
import sys

# === Mockowanie zależności z grade_executor ===
sys.modules['faq_parser'] = MagicMock()
sys.modules['scenario_parser'] = MagicMock()
sys.modules['chat_adapter'] = MagicMock()
sys.modules['ai_agent'] = MagicMock()
sys.modules['tools'] = MagicMock()
sys.modules['tools.tools'] = MagicMock()
sys.modules['historyStorage'] = MagicMock()
sys.modules['chat'] = MagicMock()
sys.modules['gradeHistory'] = MagicMock()

# Dopiero po mockowaniu importujemy grade_executor
from src.executors import grade_executor


class Testgrade_executor(unittest.TestCase):

    def test_split_message_parts_valid(self):
        sample = """
        PROCES_MYSLOWY: Model poprawnie ocenił wiadomość.
        KATEGORIA: Poprawna
        OCENA: 9
        """
        result = grade_executor._split_message_parts(sample)
        self.assertEqual(result, ("Model poprawnie ocenił wiadomość.", "Poprawna", "9"))

    def test_split_message_parts_invalid_format(self):
        invalid_sample = "Brak wymaganych sekcji w odpowiedzi."
        result = grade_executor._split_message_parts(invalid_sample)
        self.assertEqual(result, ("Blad dopasowywania wzorca", "Error", 404))

    @patch("src.executors.grade_executor.ModelChat")
    @patch("src.executors.grade_executor.get_chats")
    @patch("src.executors.grade_executor.GradeHistory")
    def test_main_execution(self, MockGradeHistory, mock_get_chats, MockModelChat):
        mock_agent = MockModelChat.return_value
        mock_agent.send_prompt.return_value = """
        PROCES_MYSLOWY: Testowe rozumowanie.
        KATEGORIA: Inne
        OCENA: 6
        """

        mock_chat = MagicMock()
        mock_chat.get_chat_topic_string.return_value = "Testowy temat"
        mock_chat.get_chat_topic_json.return_value = {"temat": "Test"}
        mock_chat.get_conversation_id.return_value = "abc123"
        mock_chat.get_chat_file_path.return_value = "/path/to/chat.json"
        mock_chat.__iter__.return_value = iter(["Pytanie i odpowiedź modelu."])

        mock_get_chats.return_value = [mock_chat]

        grade_executor.main()

        MockGradeHistory.return_value.save_graded_answer.assert_called_once()
        MockGradeHistory.return_value.save_graded_chat.assert_called_once()

if __name__ == '__main__':
    unittest.main()
