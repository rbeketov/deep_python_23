import re
from abc import abstractclassmethod


class BaseDescriptor:
    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not self.check_valid(value):
            raise ValueError("Invalid value")
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        delattr(instance, self.name)

    @classmethod
    @abstractclassmethod
    def check_valid(cls, value):
        pass


class IPDescriptor(BaseDescriptor):
    @classmethod
    def check_valid(cls, value):
        if not isinstance(value, str):
            return False
        pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        pattern += r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        pattern += r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        pattern += r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return re.match(pattern, value)


class PrimeNumberDescriptor(BaseDescriptor):
    @classmethod
    def check_valid(cls, value):
        if not isinstance(value, int):
            return False
        if value <= 1:
            return False
        if value <= 3:
            return True
        if value % 2 == 0 or value % 3 == 0:
            return False
        i = 5
        while i * i <= value:
            if value % i == 0 or value % (i + 2) == 0:
                return False
            i += 6
        return True


class PhoneDescriptor(BaseDescriptor):
    @classmethod
    def check_valid(cls, value):
        if not isinstance(value, str):
            return False
        return re.match(r"\+7-\d{3}-\d{3}-\d{4}", value)


class Data:
    ip = IPDescriptor()
    prime = PrimeNumberDescriptor()
    phone_number = PhoneDescriptor()

    def __init__(self, ip, prime, phone_number):
        self.ip = ip
        self.prime = prime
        self.phone_number = phone_number
