import unittest
import json
from unittest import mock
from tests.json_generator import JSONGenerator
from src.parse_json import parse_json
from src.parse_json import INCORRECT_VALUES


class TestParseJSON(unittest.TestCase):
    def test_correct_callback_calls(self):
        generator = JSONGenerator()
        for _ in range(100):
            json_data, keys, words, callback_info = generator.create_json_keys_words(100)

            json_str = json.dumps(json_data)
            mock_callback = mock.Mock()
            parse_json(json_str, keys, words, mock_callback)

            expected_calls = [
                mock.call(word) for word, count in callback_info.items() for _ in range(count)
            ]

            expected_calls.sort()
            mock_callback.mock_calls.sort()
            self.assertEqual(expected_calls, mock_callback.mock_calls)

    def test_incorrect_input_value(self):
        with self.assertRaises(ValueError) as context:
            parse_json(None, None, None, None)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(None)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        generator = JSONGenerator()
        json_data, keys, words, callback_info = generator.create_json_keys_words(10)
        json_str = json.dumps(json_data)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, keys, words, None)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        mock_callback = mock.Mock()

        with self.assertRaises(ValueError) as context:
            parse_json(None, keys, words, mock_callback)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, None, words, mock_callback)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, keys, None, mock_callback)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, keys, words, 123)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

    def test_missing_field_non_callback(self):
        json_str = '{"age": "30", "city": "New York"}'
        required_fields = ['age', 'city']
        keywords = ['important']
        mock_callback = mock.Mock()

        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"age": "30", "city": "New York"}'
        required_fields = []
        keywords = []
        mock_callback = mock.Mock()

        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"age": "30", "city": "New York"}'
        required_fields = ['test']
        keywords = []
        mock_callback = mock.Mock()

        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"age": "30", "city": "New York"}'
        required_fields = []
        keywords = ['test']
        mock_callback = mock.Mock()

        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)


if __name__ == '__main__':
    unittest.main()
