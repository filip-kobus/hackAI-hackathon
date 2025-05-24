import unittest
from unittest.mock import patch, MagicMock
from prompt_model.ai_agent import ModelChat

class TestModelChat(unittest.TestCase):

    def setUp(self):
        self.model_chat = ModelChat()

    def test_set_system_prompt(self):
        self.model_chat.set_system_prompt("You are a helpful assistant.")
        self.assertEqual(self.model_chat.system_prompt, "You are a helpful assistant.")
        self.assertEqual(self.model_chat.messages[0], {"role": "system", "content": "You are a helpful assistant."})

    def test_clear_history(self):
        self.model_chat.set_system_prompt("Test prompt")
        self.model_chat.clear_history()
        self.assertIsNone(self.model_chat.system_prompt)
        self.assertEqual(self.model_chat.messages, [])

    @patch('prompt_model.ai_agent.requests.post')
    def test_send_prompt_success(self, mock_post):
        self.model_chat.set_system_prompt("System prompt")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"content": "Hello, user!"}
        }
        mock_post.return_value = mock_response

        result = self.model_chat.send_prompt("Hi!")
        self.assertEqual(result, "Hello, user!")
        self.assertEqual(self.model_chat.messages[-1], {"role": "assistant", "content": "Hello, user!"})

    @patch('prompt_model.ai_agent.requests.post')
    def test_send_prompt_without_system_prompt_raises(self, mock_post):
        with self.assertRaises(ValueError):
            self.model_chat.send_prompt("Hi!")

    @patch('prompt_model.ai_agent.requests.post')
    def test_send_prompt_api_error(self, mock_post):
        self.model_chat.set_system_prompt("System prompt")
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.json.return_value = {
            "message": {"content": "Error"}
        }
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.model_chat.send_prompt("Hi!")
        self.assertIn("Błąd zapytania do Ollama", str(context.exception))

    @patch('prompt_model.ai_agent.requests.post')
    def test_send_message_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": "Assistant reply"
        }
        mock_post.return_value = mock_response

        result = self.model_chat.send_message("Hello!")
        self.assertEqual(result, "Assistant reply")

    @patch('prompt_model.ai_agent.requests.post')
    def test_send_message_api_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.model_chat.send_message("Hello!")
        self.assertIn("Błąd zapytania do Ollama", str(context.exception))

if __name__ == '__main__':
    unittest.main()