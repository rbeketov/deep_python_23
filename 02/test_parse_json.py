import unittest
import json
from unittest import mock
from json_generator import JSONGenerator
from parse_json import parse_json
from parse_json import INCORRECT_VALUES


class TestParseJSON(unittest.TestCase):
    def test_correct_callback_calls(self):
        generator = JSONGenerator()
        for _ in range(100):
            json_data, keys, words, callback_info = generator.create_json_keys_words(100)

            json_str = json.dumps(json_data)
            mock_callback = mock.Mock()
            parse_json(json_str, keys, words, mock_callback)

            expected_calls = [
                mock.call(key, word) for (key, word), count in callback_info.items()
                for _ in range(count)
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
        json_data, keys, words, _ = generator.create_json_keys_words(10)
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

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, keys, [12, '12'], print)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, [12, '12'], words, print)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, '123', words, print)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, keys, 'word', print)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            parse_json(json_str, 1, 'word', print)
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

    def test_case_insensitivity_in_keywords(self):
        json_str = '{"AGe": "30", "city": "New York"}'
        required_fields = ['age', 'city']
        keywords = ['30']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"age": "30", "city": "New York"}'
        required_fields = ['AGE', 'cIty']
        keywords = ['30', 'new']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"aGe": "30", "cIty": "New York"}'
        required_fields = ['AgE', 'city']
        keywords = ['30', 'new']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"age": "citY", "city": "New York"}'
        required_fields = ['age', 'city']
        keywords = ['City']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
             mock.call("age", "City")
        ]
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"age": "CITY", "city": "New York"}'
        required_fields = ['age', 'city']
        keywords = ['city', 'new']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
            mock.call("age", "city"),
            mock.call("city", 'new'),
        ]
        self.assertEqual(expected_calls.sort(), mock_callback.mock_calls.sort())

        json_str = '{"age": "city ON BridGE", "city": "New York no OLD York"}'
        required_fields = ['age', 'city']
        keywords = ['city', 'new', 'bridge', 'oLd', 'NO', 'yOrK']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
            mock.call("age", "city"),
            mock.call("age", "bridge"),
            mock.call("city", 'new'),
            mock.call("city", 'yOrK'),
            mock.call("city", 'oLd'),
            mock.call("city", 'NO'),
        ]
        self.assertEqual(expected_calls.sort(), mock_callback.mock_calls.sort())

    def test_word_boundaries(self):
        json_str = '{"age": "304", "city": "New York"}'
        required_fields = ['age', 'city']
        keywords = ['30']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

        json_str = '{"age": "304", "city": "News York"}'
        required_fields = ['age', 'city']
        keywords = ['30', 'new']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = []
        self.assertEqual(expected_calls, mock_callback.mock_calls)

    def test_several_found_keywords_and_required_field(self):
        json_str = '{"age": "30 hello test", "city": "New York and heLLO juiCe"}'
        required_fields = ['age', 'city']
        keywords = ['30', 'Hello', 'juice']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
            mock.call("age", "30"),
            mock.call("age", "Hello"),
            mock.call("city", 'Hello'),
            mock.call("city", 'juice'),
        ]
        self.assertEqual(expected_calls.sort(), mock_callback.mock_calls.sort())

        json_str = '{"age": "30 hello test", "city": "New York"}'
        required_fields = ['age', 'city']
        keywords = ['30', 'Hello', 'juice', 'test']
        mock_callback = mock.Mock()
        parse_json(json_str, required_fields, keywords, mock_callback)
        expected_calls = [
            mock.call("age", "30"),
            mock.call("age", "Hello"),
            mock.call("age", "test"),
        ]
        self.assertEqual(expected_calls.sort(), mock_callback.mock_calls.sort())


if __name__ == '__main__':
    unittest.main()
