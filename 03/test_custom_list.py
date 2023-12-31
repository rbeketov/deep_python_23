import unittest

from custom_list import CustomList
from custom_list import TYPE_ERROR_MESSAGE_ARIFMETIC
from custom_list import TYPE_ERROR_MESSAGE_COMPARE
from custom_list import TYPE_ERROR_MESSAGE_ONLY_INT
from custom_list import TYPE_ERROR_MESSAGE_NOT_ITERABLE


class TestCustomList(unittest.TestCase):
    def test_correct_create(self):
        list_ = CustomList([1, 2, 3, 4, 5])
        self.assertIsInstance(list_, CustomList)

        self.assertEqual(list_[0], 1)
        self.assertEqual(list_[1], 2)
        self.assertEqual(list_[2], 3)
        self.assertEqual(list_[3], 4)
        self.assertEqual(list_[4], 5)

        self.assertEqual(len(list_), len([1, 2, 3, 4, 5]))

        list_.append(6)
        self.assertEqual(list_[5], 6)

    def trst_correct_create_from_iterator(self):
        iterator = iter([1, 2, 3, 4])
        custom_list_ = CustomList(iterator)
        self.assertEqual(custom_list_[0], 1)
        self.assertEqual(custom_list_[1], 2)
        self.assertEqual(custom_list_[2], 3)
        self.assertEqual(custom_list_[3], 4)
        self.assertEqual(len(custom_list_), len([1, 2, 3, 4]))

    def test_incorrect_create(self):
        with self.assertRaises(TypeError) as context:
            CustomList([1, 2, 3, 4, '5'])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ONLY_INT)

        with self.assertRaises(TypeError) as context:
            CustomList(['5'])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ONLY_INT)

        with self.assertRaises(TypeError) as context:
            CustomList(12)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_NOT_ITERABLE)

        with self.assertRaises(TypeError) as context:
            CustomList('12')
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ONLY_INT)

        with self.assertRaises(TypeError) as context:
            CustomList([1.2, 2.2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ONLY_INT)

    def test_add_positive_positive(self):
        left = CustomList([1, 2, 3])
        right = CustomList([1, 2, 3])
        real_result = left + right
        expected_result = CustomList([2, 4, 6])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(left), 3)
        self.assertEqual(len(right), 3)
        for res, exp in zip(left, [1, 2, 3]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3]):
            self.assertEqual(res, exp)

    def test_add_positive_negative(self):
        left = CustomList([1, 2, 3])
        right = [-1, 2, 3]
        real_result = left + right
        expected_result = CustomList([0, 4, 6])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertEqual(len(left), 3)
        for res, exp in zip(left, [1, 2, 3]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, list)
        self.assertEqual(len(right), 3)
        for res, exp in zip(right, [-1, 2, 3]):
            self.assertEqual(res, exp)

    def test_add_negative_negative(self):
        left = [-1, -2, -3]
        right = CustomList([-1, 2, 3])
        real_result = left + right
        expected_result = CustomList([-2, 0, 0])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, list)
        self.assertEqual(len(left), 3)
        for res, exp in zip(left, [-1, -2, -3]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(right), 3)
        for res, exp in zip(right, [-1, 2, 3]):
            self.assertEqual(res, exp)

    def test_add_with_dif_dim_left_bigger(self):
        left = [-1, -2, -3, 1, 1]
        right = CustomList([-1, 2, 3])
        real_result = left + right
        expected_result = CustomList([-2, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, list)
        self.assertEqual(len(left), 5)
        for res, exp in zip(left, [-1, -2, -3, 1, 1]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(right), 3)
        for res, exp in zip(right, [-1, 2, 3]):
            self.assertEqual(res, exp)

        left = CustomList([-1, -2, -3, 1, 1])
        right = [-1, 2, 3]
        real_result = left + right
        expected_result = CustomList([-2, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertEqual(len(left), 5)
        for res, exp in zip(left, [-1, -2, -3, 1, 1]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, list)
        self.assertEqual(len(right), 3)
        for res, exp in zip(right, [-1, 2, 3]):
            self.assertEqual(res, exp)

        left = CustomList([-1, -2, -3, 1, 1])
        right = CustomList([-1, 2, 3])
        real_result = left + right
        expected_result = CustomList([-2, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertEqual(len(left), 5)
        for res, exp in zip(left, [-1, -2, -3, 1, 1]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(right), 3)
        for res, exp in zip(right, [-1, 2, 3]):
            self.assertEqual(res, exp)

    def test_add_with_dif_dim_right_bigger(self):
        left = CustomList([-1, 2, 3])
        right = [-1, -2, -3, 1, 1]
        real_result = left + right
        expected_result = CustomList([-2, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertEqual(len(left), 3)
        for res, exp in zip(left, [-1, 2, 3]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, list)
        self.assertEqual(len(right), 5)
        for res, exp in zip(right, [-1, -2, -3, 1, 1]):
            self.assertEqual(res, exp)

        left = [-1, 2, 3]
        right = CustomList([-1, -2, -3, 1, 1])
        real_result = left + right
        expected_result = CustomList([-2, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, list)
        self.assertEqual(len(left), 3)
        for res, exp in zip(left, [-1, 2, 3]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(right), 5)
        for res, exp in zip(right, [-1, -2, -3, 1, 1]):
            self.assertEqual(res, exp)

        left = CustomList([-1, 2, 3])
        right = CustomList([-1, -2, -3, 1, 1])
        real_result = left + right
        expected_result = CustomList([-2, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertEqual(len(left), 3)
        for res, exp in zip(left, [-1, 2, 3]):
            self.assertEqual(res, exp)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(right), 5)
        for res, exp in zip(right, [-1, -2, -3, 1, 1]):
            self.assertEqual(res, exp)

    def test_incorrect_add(self):
        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) + ['1', 2, 3]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

        with self.assertRaises(TypeError) as context:
            res = ['1', 2, 3] + CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

        with self.assertRaises(TypeError) as context:
            res = [1.2, 2, 3] + CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) + [1, 2, 3.1]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

    def test_sub_positive_positive(self):
        left = CustomList([1, 2, 3])
        right = CustomList([1, 2, 3])
        real_result = left - right
        expected_result = CustomList([0, 0, 0])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(left), 3)
        self.assertEqual(len(right), 3)
        for res, exp in zip(left, [1, 2, 3]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3]):
            self.assertEqual(res, exp)

    def test_sub_positive_negative(self):
        left = CustomList([1, 2, 3])
        right = [-1, 2, 3]
        real_result = left - right
        expected_result = CustomList([2, 0, 0])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertIsInstance(right, list)
        self.assertEqual(len(left), 3)
        for res, exp in zip(left, [1, 2, 3]):
            self.assertEqual(res, exp)
        self.assertEqual(len(right), 3)
        for res, exp in zip(right, [-1, 2, 3]):
            self.assertEqual(res, exp)

        left = [-1, -2, -3]
        right = CustomList([-1, 2, 3])
        real_result = left - right
        expected_result = CustomList([0, -4, -6])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, list)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(left), 3)
        for res, exp in zip(left, [-1, -2, -3]):
            self.assertEqual(res, exp)
        self.assertEqual(len(right), 3)
        for res, exp in zip(right, [-1, 2, 3]):
            self.assertEqual(res, exp)

    def test_sub_with_dif_dim_right_bigger(self):
        left = CustomList([1, 2, 3])
        right = CustomList([1, 2, 3, 1, 1])
        real_result = left - right
        expected_result = CustomList([0, 0, 0, -1, -1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(left), 3)
        self.assertEqual(len(right), 5)
        for res, exp in zip(left, [1, 2, 3]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3, 1, 1]):
            self.assertEqual(res, exp)

        left = [1, 2, 3]
        right = CustomList([1, 2, 3, 1, 1])
        real_result = left - right
        expected_result = CustomList([0, 0, 0, -1, -1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, list)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(left), 3)
        self.assertEqual(len(right), 5)
        for res, exp in zip(left, [1, 2, 3]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3, 1, 1]):
            self.assertEqual(res, exp)

        left = CustomList([1, 2, 3])
        right = [1, 2, 3, 1, 1]
        real_result = left - right
        expected_result = CustomList([0, 0, 0, -1, -1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertIsInstance(right, list)
        self.assertEqual(len(left), 3)
        self.assertEqual(len(right), 5)
        for res, exp in zip(left, [1, 2, 3]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3, 1, 1]):
            self.assertEqual(res, exp)

    def test_sub_with_dif_dim_left_bigger(self):
        left = CustomList([1, 2, 3, 1, 1])
        right = CustomList([1, 2, 3])
        real_result = left - right
        expected_result = CustomList([0, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(left), 5)
        self.assertEqual(len(right), 3)
        for res, exp in zip(left, [1, 2, 3, 1, 1]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3]):
            self.assertEqual(res, exp)

        left = [1, 2, 3, 1, 1]
        right = CustomList([1, 2, 3])
        real_result = left - right
        expected_result = CustomList([0, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, list)
        self.assertIsInstance(right, CustomList)
        self.assertEqual(len(left), 5)
        self.assertEqual(len(right), 3)
        for res, exp in zip(left, [1, 2, 3, 1, 1]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3]):
            self.assertEqual(res, exp)

        left = CustomList([1, 2, 3, 1, 1])
        right = [1, 2, 3]
        real_result = left - right
        expected_result = CustomList([0, 0, 0, 1, 1])
        self.assertEqual(len(real_result), len(expected_result))
        for res, exp in zip(real_result, expected_result):
            self.assertEqual(res, exp)
        self.assertIsInstance(real_result, CustomList)

        self.assertIsInstance(left, CustomList)
        self.assertIsInstance(right, list)
        self.assertEqual(len(left), 5)
        self.assertEqual(len(right), 3)
        for res, exp in zip(left, [1, 2, 3, 1, 1]):
            self.assertEqual(res, exp)
        for res, exp in zip(right, [1, 2, 3]):
            self.assertEqual(res, exp)

    def test_incorrect_sub(self):
        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) - ['1', 2, 3]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

        with self.assertRaises(TypeError) as context:
            res = ['1', 2, 3] - CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

        with self.assertRaises(TypeError) as context:
            res = [1.2, 2, 3] - CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) - [1, 2, 3.1]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_ARIFMETIC)

    def test_compare(self):
        self.assertEqual(CustomList([1, 2, 3]), CustomList([1, 2, 3]))
        self.assertEqual(CustomList([1, 2, 3]), CustomList([1, 8, -3]))
        self.assertEqual(CustomList([-1, 6, 1]), CustomList([6, 0, 0, 0, 0]))
        self.assertEqual(CustomList([-1, 6, 1, 0]), CustomList([6]))

        self.assertLess(CustomList([1, 2, 2]), CustomList([1, 2, 3]))
        self.assertLess(CustomList([1, 2, -10]), CustomList([1, 2, 3]))
        self.assertLess(CustomList([1, 2, 1, 1, 1, -100]), CustomList([1, 2, 3]))
        self.assertLess(CustomList([-10]), CustomList([1, 2, 3]))
        self.assertLess(CustomList([5]), CustomList([1, 2, 3]))

        self.assertLessEqual(CustomList([5]), CustomList([1, 2, 3]))
        self.assertLessEqual(CustomList([6]), CustomList([1, 2, 3]))

        self.assertGreater(CustomList([1, 2, 4]), CustomList([1, 2, 3]))
        self.assertGreater(CustomList([1, -3, 10]), CustomList([1, 2, 3]))
        self.assertGreater(CustomList([10]), CustomList([1, 2, 3]))
        self.assertGreater(CustomList([10, 0, 0, 0, -1]), CustomList([1, 2, 3]))
        self.assertGreater(CustomList([10]), CustomList([1, 2, 3, 0, 0, 0]))

        self.assertGreaterEqual(CustomList([10]), CustomList([1, 2, 3, 0, 0, 0]))
        self.assertGreaterEqual(CustomList([10]), CustomList([1, 2, 3, 0, 4, 0]))

    def test_incorrect_compare(self):
        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) == [1, 2, 3]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = [1, 2, 3] == CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = [1, 2, 3] > CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) > [1, 2, 3]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = [1, 2, 3] >= CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) >= [1, 2, 3]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = [1, 2, 3] < CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) < [1, 2, 3]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = [1, 2, 3] <= CustomList([1, 2])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

        with self.assertRaises(TypeError) as context:
            res = CustomList([1, 2]) <= [1, 2, 3]
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE_COMPARE)

    def test_str_method(self):
        custom_list = CustomList([1, 2, 3])
        expected_result = "[1, 2, 3]\nСумма элементов списка = 6"
        result = str(custom_list)
        self.assertEqual(result, expected_result)

        custom_list = CustomList([1, -2, 3])
        expected_result = "[1, -2, 3]\nСумма элементов списка = 2"
        result = str(custom_list)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
