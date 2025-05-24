import unittest
from unittest.mock import patch, mock_open
from prompt_model.chat import Chat

class TestChat(unittest.TestCase):

    def setUp(self):
        self.test_json = {"dziedzina": "bezpieczeństwo",
                            "pytanie": "Czym?",
                            "odpowiedz": "Przeglądarka",
                            "chat": [
                                {
                                    "model_message": {
                                        "response": "Pytanie1"
                                    },
                                    "chatbot_answer": {
                                        "response": "Odpowiedz1",
                                        "user-id": "123",
                                        "conversation": "1",
                                        "trace-id": "2",
                                        "intents": None,
                                        "additional": ""
                                    }
                                },
                                {
                                    "model_message": {
                                        "response": "Pytanie2"
                                    },
                                    "chatbot_answer": {
                                        "response": "Odpowiedz2",
                                        "user-id": "123",
                                        "conversation": "1",
                                        "trace-id": "3",
                                        "intents": None,
                                        "additional": ""
                                    }
                                },
                                ]
                            }
        with patch('prompt_model.chat.os.path.exists') as os_path_exists_mock, \
            patch('prompt_model.chat.json.load') as load_mock, patch('prompt_model.chat.open', mock_open(read_data='{}')):
            load_mock.return_value = self.test_json
            self.chat = Chat('x/file.json')

    def test_init(self):

        with patch('prompt_model.chat.os.path.exists') as os_path_exists_mock:

            os_path_exists_mock.return_value = False
            
            with self.assertRaises(FileNotFoundError):
                Chat('file.json')

            os_path_exists_mock.assert_called_with('file.json')

        with patch('prompt_model.chat.os.path.exists') as os_path_exists_mock, \
        patch('prompt_model.chat.open', mock_open(read_data='{}')), \
        patch('prompt_model.chat.json.load') as json_mock:    
            json_mock.return_value = self.test_json.copy()
            os_path_exists_mock.return_value = True
            json_mock.return_value.get('chat', [])[0] = None

            with self.assertRaises(ValueError):
                Chat('file.json')
            
            json_mock.return_value.update({'chat' : None})

            with self.assertRaises(ValueError):
                Chat('file.json')

    def test_get_chat_topic_json(self):
        topic = self.chat.get_chat_topic_json()
        self.assertEqual(topic['field'], self.test_json['dziedzina'])
        self.assertEqual(topic['base_question'], self.test_json['pytanie'])
        self.assertEqual(topic['base_answer'], self.test_json['odpowiedz'])
    
    def test_get_chat_topic_string(self):
        topic = self.chat.get_chat_topic_string()

        test_topic = f'[DZIEDZINA] bezpieczeństwo\n[PYTANIE] Czym?\n[ODPOWIEDŹ] Przeglądarka'

        self.assertEqual(topic, test_topic)

    def test_iter(self):
        list_interaction = [x for x in self.chat]

        self.assertEqual(len(list_interaction), 2)

        test_interaction = '[PYTANIE] Pytanie1\n[ODPOWIEDŹ] Odpowiedz1'
        self.assertEqual(test_interaction, list_interaction[0])

        test_interaction = '[PYTANIE] Pytanie2\n[ODPOWIEDŹ] Odpowiedz2'
        self.assertEqual(test_interaction, list_interaction[1])

    def get_chat_file_path(self):
        file = self.chat.get_chat_file_path()
        self.assertEqual(file, 'file.json')
    
    def test_get_conversation_id(self):
        id = self.chat.get_conversation_id()
        self.assertEqual(id, '1')
        