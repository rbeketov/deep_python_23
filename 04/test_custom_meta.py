import unittest
from custom_meta import CustomMeta


class TestCustomMetaClass(unittest.TestCase):
    def test_create_attr_class(self):
        class A(metaclass=CustomMeta):
            x = "x"
            _y = "y"
            __z = "z"

            def say(self):
                pass

            def __test__(self):
                pass

        self.assertFalse(hasattr(A, "x"))
        self.assertTrue(hasattr(A, "custom_x"))
        self.assertEqual(A.custom_x, "x")

        self.assertFalse(hasattr(A, "_y"))
        self.assertTrue(hasattr(A, "_custom_y"))
        self.assertEqual(A._custom_y, "y")

        self.assertFalse(hasattr(A, "_A__z"))
        self.assertTrue(hasattr(A, "_A__custom_z"))
        self.assertEqual(A._A__custom_z, "z")

        self.assertFalse(hasattr(A, "say"))
        self.assertTrue(hasattr(A, "custom_say"))

        self.assertFalse(hasattr(A, "custom__test__"))
        self.assertTrue(hasattr(A, "__test__"))

    def test_create_and_add_attr_instance(self):
        class A(metaclass=CustomMeta):
            def __init__(self, x, y, z):
                self.x = x
                self._y = y
                self.__z = z

        instance = A("x", "y", "z")

        self.assertFalse(hasattr(instance, "x"))
        self.assertTrue(hasattr(instance, "custom_x"))
        self.assertEqual(instance.custom_x, "x")

        self.assertFalse(hasattr(instance, "_y"))
        self.assertTrue(hasattr(instance, "_custom_y"))
        self.assertEqual(instance._custom_y, "y")

        self.assertFalse(hasattr(instance, "_A__z"))
        self.assertTrue(hasattr(instance, "_A__custom_z"))
        self.assertEqual(instance._A__custom_z, "z")

        instance.b = "b"
        self.assertFalse(hasattr(instance, "b"))
        self.assertTrue(hasattr(instance, "custom_b"))
        self.assertEqual(instance.custom_b, "b")


if __name__ == "__main__":
    unittest.main()
