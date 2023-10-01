import sys
import io
import unittest
import time

from mean_k_calls import time_mean_last_k_calls
from mean_k_calls import INCORRECT_VALUES


class TestMeanTimeLastKCalls(unittest.TestCase):
    def setUp(self):
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__
        self.captured_output.close()

    def test_k_equal_to_1(self):
        @time_mean_last_k_calls(1)
        def decorated_function():
            time.sleep(0.5)

        decorated_function()

        self.captured_output.seek(0)
        output = self.captured_output.read()
        self.assertIn("Среднее время выполнения последних k = 1 вызовов:", output)

    def test_cnt_calls_less_k(self):
        @time_mean_last_k_calls(10)
        def decorated_function():
            time.sleep(0.5)

        for _ in range(5):
            decorated_function()

        self.captured_output.seek(0)
        output = self.captured_output.read()

        expected_output = [
            f"Среднее время выполнения последних k = {k} вызовов:" for k in range(1, 6)
        ]

        for line in expected_output:
            self.assertIn(line, output)

    def test_cnt_calls_more_k(self):
        @time_mean_last_k_calls(2)
        def decorated_function():
            time.sleep(0.5)

        for _ in range(4):
            decorated_function()

        self.captured_output.seek(0)
        output = self.captured_output.read()

        expected_output = [
            "Среднее время выполнения последних k = 1 вызовов:",
            "Среднее время выполнения последних k = 2 вызовов:"
        ]
        not_expected_output = [
            "Среднее время выполнения последних k = 3 вызовов:",
            "Среднее время выполнения последних k = 4 вызовов:"
        ]

        for line in expected_output:
            self.assertIn(line, output)
        for line in not_expected_output:
            self.assertNotIn(line, output)

        expected_lines = 4
        actual_lines = len(output.splitlines())
        self.assertEqual(expected_lines, actual_lines)

    def test_incorrect_k_value(self):
        with self.assertRaises(ValueError) as context:
            @time_mean_last_k_calls(-1)
            def decorated_function_1():
                time.sleep(0.5)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            @time_mean_last_k_calls("123")
            def decorated_function_2():
                time.sleep(0.5)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

        with self.assertRaises(ValueError) as context:
            @time_mean_last_k_calls(0)
            def decorated_function_3():
                time.sleep(0.5)
        self.assertEqual(str(context.exception), INCORRECT_VALUES)

    def test_decorator_name(self):
        @time_mean_last_k_calls(4)
        def decorated_function():
            time.sleep(0.5)
        self.assertEqual(decorated_function.__name__, "decorated_function")


if __name__ == '__main__':
    unittest.main()
