import unittest
from unittest.mock import mock_open, patch
from prompt_model.scenario_parser import scenariusz_generator

class TestScenariuszGenerator(unittest.TestCase):

    def test_generator_multiple_scenarios(self):
        mock_content = (
            "### SCENARIUSZ\nScenario 1 description\n\n"
            "### SCENARIUSZ\nScenario 2 description\n\n"
            "### SCENARIUSZ\nScenario 3 description\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = list(scenariusz_generator("fake_path.md"))

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Scenario 1 description")
        self.assertEqual(result[1], "Scenario 2 description")
        self.assertEqual(result[2], "Scenario 3 description")

    def test_generator_ignores_empty_parts(self):
        mock_content = (
            "\n### SCENARIUSZ\nScenario 1\n"
            "### SCENARIUSZ\n\n"
            "### SCENARIUSZ\nScenario 2\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = list(scenariusz_generator("fake_path.md"))

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Scenario 1")

    def test_generator_scenario_with_multiline_description(self):
        mock_content = (
            "### SCENARIUSZ\nScenario 1 line 1\nScenario 1 line 2\n"
            "### SCENARIUSZ\nScenario 2 line 1\nScenario 2 line 2\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = list(scenariusz_generator("fake_path.md"))

        self.assertEqual(result[0], "Scenario 1 line 1\nScenario 1 line 2")
        self.assertEqual(result[1], "Scenario 2 line 1\nScenario 2 line 2")

    def test_generator_handles_file_with_only_marker(self):
        mock_content = "### SCENARIUSZ\n"

        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = list(scenariusz_generator("fake_path.md"))

        self.assertEqual(result, [])

    def test_generator_handles_marker_at_end_of_file(self):
        mock_content = (
            "### SCENARIUSZ\nScenario 1\n"
            "### SCENARIUSZ\nScenario 2\n"
            "### SCENARIUSZ\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = list(scenariusz_generator("fake_path.md"))

        self.assertEqual(result, ["Scenario 1", "Scenario 2"])