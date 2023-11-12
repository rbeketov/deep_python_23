from itertools import tee
from typing import List
from typing import Iterable

TYPE_ERROR_MESSAGE_ARIFMETIC = "Ожидается объект типа List[int] или CustomList[int]"
TYPE_ERROR_MESSAGE_COMPARE = "Ожидается объект типа CustomList[int]"
TYPE_ERROR_MESSAGE_NOT_ITERABLE = "Ожидается итерируемый объект"
TYPE_ERROR_MESSAGE_ONLY_INT = "Ожидается, что итерируемый объект имеет объекты типа int"


class CustomList(list):
    def __init__(self, input_list: Iterable[int]):
        if not isinstance(input_list, Iterable):
            raise TypeError(TYPE_ERROR_MESSAGE_NOT_ITERABLE)
        copy_iter_input_list, input_list = tee(input_list)
        if not all(isinstance(item, int) for item in input_list):
            raise TypeError(TYPE_ERROR_MESSAGE_ONLY_INT)
        super().__init__(copy_iter_input_list)

    def __add__(self, other: List[int]) -> 'CustomList':
        self.__check_correct_type_for_arithmetic(other)
        result = []
        min_len = min(len(other), len(self))
        for i in range(min_len):
            result.append(other[i] + self[i])

        if len(other) > len(self):
            result.extend(other[min_len:])
        elif len(other) < len(self):
            result.extend(self[min_len:])

        return CustomList(result)

    def __radd__(self, other: List[int]) -> 'CustomList':
        self.__check_correct_type_for_arithmetic(other)
        return self.__add__(other)

    def __sub__(self, other: List[int]) -> 'CustomList':
        self.__check_correct_type_for_arithmetic(other)
        return self.__add__([-x for x in other])

    def __rsub__(self, other: List[int]) -> 'CustomList':
        self.__check_correct_type_for_arithmetic(other)
        return CustomList([-x for x in self]).__add__(other)

    def __lt__(self, other: 'CustomList') -> bool:
        self.__check_correct_type_for_compare(other)
        return sum(self) < other._get_sum()

    def __le__(self, other: 'CustomList') -> bool:
        self.__check_correct_type_for_compare(other)
        return sum(self) <= other._get_sum()

    def __eq__(self, other: 'CustomList') -> bool:
        self.__check_correct_type_for_compare(other)
        return sum(self) == other._get_sum()

    def __ne__(self, other: 'CustomList') -> bool:
        self.__check_correct_type_for_compare(other)
        return not self.__eq__(other)

    def __gt__(self, other: 'CustomList') -> bool:
        self.__check_correct_type_for_compare(other)
        return not self.__le__(other)

    def __ge__(self, other: 'CustomList') -> bool:
        self.__check_correct_type_for_compare(other)
        return not self.__lt__(other)

    def __str__(self) -> str:
        return f"{super().__str__()}\nСумма элементов списка = {sum(self)}"

    def _get_sum(self) -> int:
        return sum(self)

    @staticmethod
    def __check_correct_type_for_arithmetic(object_):
        if not isinstance(object_, list) or not all(isinstance(x, int) for x in object_):
            raise TypeError(TYPE_ERROR_MESSAGE_ARIFMETIC)

    @staticmethod
    def __check_correct_type_for_compare(object_):
        if not isinstance(object_, CustomList):
            raise TypeError(TYPE_ERROR_MESSAGE_COMPARE)
