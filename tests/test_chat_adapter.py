import json
import unittest
from unittest.mock import patch

from prompt_model.chat_adapter import ChatAdapter

class ChatAdapterTest(unittest.TestCase):

    def setUp(self):
        self.chat_adapter = ChatAdapter()
        self.raw_mock_response = json.dumps({
    "response": "Odebrana wiadomość\n===========\n\nIntents: ['Intencja']\nUser ID: 1337\nConversation: conv3rs4t10n\nTrace ID: 1234\ndisappointment: 1"
})


    @patch('subprocess.run')
    def test_send_message(self, mock_run):
        mock_message = "Testowa wiadomosc"

        mock_payload = json.dumps({"message": mock_message})
        
        mock_run.return_value.stdout = self.raw_mock_response
        result = mock_run.return_value

        response = self.chat_adapter.send_message(mock_message)

        mock_run.assert_called_with(["curl", "-X", "POST", "http://127.0.0.1:8000/send_message", "-H", "Content-Type: application/json",
                                     "-d", mock_payload], capture_output=True, text=True, encoding="utf-8")
        

    def test_transform_response(self):
        result = self.chat_adapter._transform_response(self.raw_mock_response)
        self.assertEqual(result["response"], "Odebrana wiadomość\n")
        self.assertEqual(result["intents"], "['Intencja']")
        self.assertEqual(result["user-id"], "1337")
        self.assertEqual(result["conversation"], "conv3rs4t10n")
        self.assertEqual(result["trace-id"], "1234")
        self.assertEqual(result["additional"], "disappointment: 1")



if __name__ == '__main__':
    unittest.main()    

    

