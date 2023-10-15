import unittest
from descriptor import PrimeNumberDescriptor, IPDescriptor, PhoneDescriptor, Data


class TestDescriptors(unittest.TestCase):
    def test_functionality_base_descriptor(self):
        instance = Data("192.168.2.1", 7, "+7-904-704-8912")
        self.assertEqual(len(instance.__dict__), 3)
        self.assertEqual(instance.ip, "192.168.2.1")
        self.assertEqual(instance.prime, 7)
        self.assertEqual(instance.phone_number, "+7-904-704-8912")
        self.assertEqual(instance.__dict__["__ip"], "192.168.2.1")
        self.assertEqual(instance.__dict__["__prime"], 7)
        self.assertEqual(instance.__dict__["__phone_number"], "+7-904-704-8912")

        instance.prime = 17
        self.assertEqual(instance.prime, 17)
        self.assertEqual(instance.__dict__["__prime"], 17)

        instance.ip = "192.168.0.0"
        self.assertEqual(instance.ip, "192.168.0.0")
        self.assertEqual(instance.__dict__["__ip"], "192.168.0.0")

        instance.phone_number = "+7-902-704-8912"
        self.assertEqual(instance.phone_number, "+7-902-704-8912")
        self.assertEqual(instance.__dict__["__phone_number"], "+7-902-704-8912")

        with self.assertRaises(ValueError) as context:
            instance.prime = 4
        self.assertEqual(str(context.exception), "Invalid value")

        with self.assertRaises(ValueError) as context:
            instance.phone_number = "++++"
        self.assertEqual(str(context.exception), "Invalid value")

        with self.assertRaises(ValueError) as context:
            instance.ip = 4
        self.assertEqual(str(context.exception), "Invalid value")

    def test_prime_descriptor(self):
        prime_desc = PrimeNumberDescriptor()
        self.assertTrue(prime_desc.check_valid(2))
        self.assertTrue(prime_desc.check_valid(3))
        self.assertTrue(prime_desc.check_valid(7))
        self.assertTrue(prime_desc.check_valid(11))
        self.assertTrue(prime_desc.check_valid(151))
        self.assertTrue(prime_desc.check_valid(293))
        self.assertTrue(prime_desc.check_valid(7))

        self.assertFalse(prime_desc.check_valid(1))
        self.assertFalse(prime_desc.check_valid(0))
        self.assertFalse(prime_desc.check_valid(-1))
        self.assertFalse(prime_desc.check_valid(4))
        self.assertFalse(prime_desc.check_valid(9))
        self.assertFalse(prime_desc.check_valid(25))

    def test_ip_descriptor(self):
        ip_desc = IPDescriptor()
        self.assertTrue(ip_desc.check_valid("255.255.255.255"))
        self.assertTrue(ip_desc.check_valid("0.0.0.0"))
        self.assertTrue(ip_desc.check_valid("192.168.1.2"))
        self.assertTrue(ip_desc.check_valid("128.128.128.128"))

        self.assertFalse(ip_desc.check_valid("-1.128.128.128"))
        self.assertFalse(ip_desc.check_valid("128.-1.128.128"))
        self.assertFalse(ip_desc.check_valid("128.128.-1.128"))
        self.assertFalse(ip_desc.check_valid("128.128.128.-1"))
        self.assertFalse(ip_desc.check_valid("256.128.128.128"))
        self.assertFalse(ip_desc.check_valid("128.256.128.128"))
        self.assertFalse(ip_desc.check_valid("128.128.256.128"))
        self.assertFalse(ip_desc.check_valid("128.128.128.256"))

    def test_phone_descriptor(self):
        phone_desc = PhoneDescriptor()
        self.assertTrue(phone_desc.check_valid("+7-999-999-9999"))
        self.assertTrue(phone_desc.check_valid("+7-000-000-0000"))

        self.assertFalse(phone_desc.check_valid("+1-555-555-5555"))
        self.assertFalse(phone_desc.check_valid("+8-555-555-5555"))
        self.assertFalse(phone_desc.check_valid("+7-d55-555-5555"))
        self.assertFalse(phone_desc.check_valid("+7d55-555-5555"))
        self.assertFalse(phone_desc.check_valid("+7-abc-123-4567"))
        self.assertFalse(phone_desc.check_valid("+7-999-999-999"))
        self.assertFalse(phone_desc.check_valid(""))
        self.assertFalse(phone_desc.check_valid("999-999-9999"))


if __name__ == '__main__':
    unittest.main()
