import unittest
from unittest import mock
import types
import io
from rf_gen import BAD_INPUT_DATA
from rf_gen import read_and_filter_file_gen


class TestReadAndFilterFileGen(unittest.TestCase):
    def test_file_not_found(self):
        with self.assertRaises(NameError) as context:
            list(read_and_filter_file_gen('non_existent_file.txt', ['word']))
        self.assertEqual(str(context.exception), "Файл 'non_existent_file.txt' не найден")

    def test_string_input(self):
        input_data = "test line 1\ntest line 2\ntest line 3"
        search_words = ['line']
        expected_result = ['test line 1', 'test line 2', 'test line 3']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))
        self.assertEqual(result, expected_result)

    def test_io_base_input(self):
        input_data = ["test line 1\n", "test line 2\n", "test line 3\n"]
        search_words = ['line']
        expected_result = ['test line 1', 'test line 2', 'test line 3']

        mock_io_base = mock.MagicMock(spec=io.IOBase)
        mock_io_base.__iter__.return_value = iter(input_data)

        result = list(read_and_filter_file_gen(mock_io_base, search_words))

        self.assertEqual(result, expected_result)

    def test_bad_input_data(self):
        with self.assertRaises(ValueError) as context:
            list(read_and_filter_file_gen(500, ['word']))
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)

    def test_is_generator(self):
        input_data = "test line 1\ntest line 2\ntest line 3"
        search_words = ['line']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            generator = read_and_filter_file_gen("test.txt", search_words)
            self.assertTrue(isinstance(generator, types.GeneratorType),
                            "Функция не является генератором")

            result = list(generator)
            expected_result = ['test line 1', 'test line 2', 'test line 3']
            self.assertEqual(result, expected_result, "Генератор возвращает неправильные строки")

            with self.assertRaises(StopIteration):
                next(generator)

    def test_empty_input_file(self):
        input_data = ""
        search_words = ['word']
        expected_result = []

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_empty_search_words(self):
        input_data = "test line 1\ntest line 2\ntest line 3"
        search_words = []
        expected_result = []

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_empty_lines_in_input_file(self):
        input_data = "\ntest line 1\n\ntest line 2\n\n\ntest line 3\n"
        search_words = ['line']
        expected_result = ['test line 1', 'test line 2', 'test line 3']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_no_matching_lines_in_input_file(self):
        input_data = "apple\nbanana\ncherry"
        search_words = ['grape']
        expected_result = []

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_permission_error(self):
        search_words = ['word']
        with mock.patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with self.assertRaises(PermissionError):
                list(read_and_filter_file_gen('file.txt', search_words))

    def test_case_insensitivity_in_input_data(self):
        input_data = "test lIne 1\ntest liNe 2\ntest LINE 3\n"
        search_words = ['line']
        expected_result = ['test lIne 1', 'test liNe 2', 'test LINE 3']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_case_insensitivity_in_search_words(self):
        input_data = "test line 1\ntest line 2\ntest line 3\n"
        search_words = ['LIne']
        expected_result = ['test line 1', 'test line 2', 'test line 3']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_case_insensitivity_in_search_words_and_input_data(self):
        input_data = "test lINe 1\ntest LinE 2\ntest LINE 3\n"
        search_words = ['LIne']
        expected_result = ['test lINe 1', 'test LinE 2', 'test LINE 3']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_word_boundaries(self):
        input_data = "Hello daddy\nHello mammy\nHello dad\n"
        search_words = ['dad', 'mam']
        expected_result = ['Hello dad']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_multiple_matches_in_one_line(self):
        input_data = "Hello daddy mammy and father\nHello mammy friend\nHello dad\n"
        search_words = ['daddy', 'mammy', 'friend']
        expected_result = ['Hello daddy mammy and father', 'Hello mammy friend']

        with mock.patch("builtins.open", mock.mock_open(read_data=input_data)):
            result = list(read_and_filter_file_gen('input.txt', search_words))

        self.assertEqual(result, expected_result)

    def test_incorrect_type_search_word(self):
        with self.assertRaises(ValueError) as context:
            list(read_and_filter_file_gen('input.txt', 123))
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)

        with self.assertRaises(ValueError) as context:
            list(read_and_filter_file_gen('input.txt', 'str'))
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)

        with self.assertRaises(ValueError) as context:
            list(read_and_filter_file_gen('input.txt', ['12', '12', 12]))
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)

        with self.assertRaises(ValueError) as context:
            list(read_and_filter_file_gen('input.txt', [12]))
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)


if __name__ == '__main__':
    unittest.main()
