import unittest
from unittest.mock import patch, MagicMock
from src.executors import scenario_executor

class TestScenario_executor(unittest.TestCase):

    def test_format_response_removes_extra_newlines(self):
        response = "Line1\n\nLine2\n\n\nLine3"
        formatted = scenario_executor.format_response(response)
        self.assertEqual(formatted, "Line1\n\nLine2\n\n\nLine3")

    def test_format_response_strips_whitespace(self):
        response = "\n  Line1  \nLine2  \n"
        formatted = scenario_executor.format_response(response)
        self.assertEqual(formatted, "Line1  \nLine2")

    def test_get_system_prompt_contains_scenario(self):
        scenario = "Test scenario"
        prompt = scenario_executor._get_system_prompt(scenario)
        self.assertIn(scenario, prompt)
        self.assertIn("SCENARIUSZ_HACK:", prompt)
        self.assertIn("CEL:", prompt)
        self.assertIn("FORMAT_ODPOWIEDZI", prompt)

    def test_split_message_parts_invalid_component(self):
        agent_response = "BLA: cos\nODPOWIEDZ: cos\nOCENA: 7"
        with self.assertRaises(ValueError):
            scenario_executor._split_message_parts(agent_response)

    def test_split_message_parts_too_few_lines(self):
        agent_response = "PROCES_MYSLOWY: cos"
        with self.assertRaises(ValueError):
            scenario_executor._split_message_parts(agent_response)

    @patch('src.executors.scenario_executor.ModelChat')
    @patch('src.executors.scenario_executor.ChatAdapter')
    @patch('src.executors.scenario_executor.scenariusz_generator')
    @patch('src.executors.scenario_executor.ChatHistoryStorage')
    def test_main_runs(self, mock_history, mock_scenariusz, mock_adapter, mock_agent):
        # Setup mocks
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance
        mock_agent_instance.system_prompt = None
        mock_agent_instance.send_prompt.return_value = (
            "PROCES_MYSLOWY: test\nODPOWIEDZ: test\nOCENA: 5"
        )
        mock_adapter_instance = MagicMock()
        mock_adapter.return_value = mock_adapter_instance
        mock_adapter_instance.send_message.return_value = {'response': 'RESET SUCCESSFULL'}
        mock_scenariusz.return_value = ["Test scenario"]
        mock_history_instance = MagicMock()
        mock_history.return_value = mock_history_instance
        mock_history_instance.get_number_of_files.return_value = 0

        # Run main (should not raise)
        scenario_executor.main()

    def test_my_tool_prints(self):
        with patch('builtins.print') as mock_print:
            scenario_executor.my_tool("data")
            mock_print.assert_called_with("[MyTool] Narzędzie jeszcze niezaimplementowane.")

if __name__ == '__main__':
    unittest.main()