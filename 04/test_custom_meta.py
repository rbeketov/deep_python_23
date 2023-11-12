import unittest
from custom_meta import CustomMeta


class TestCustomMetaClass(unittest.TestCase):
    def test_main_logic(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError) as context:
            CustomClass.x
        self.assertEqual(str(context.exception),
                         "type object 'CustomClass' has no attribute \'x\'")

        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        with self.assertRaises(AttributeError) as context:
            inst.x
        self.assertEqual(str(context.exception),
                         "\'CustomClass\' object has no attribute \'x\'")
        with self.assertRaises(AttributeError) as context:
            inst.val
        self.assertEqual(str(context.exception),
                         "\'CustomClass\' object has no attribute \'val\'")
        with self.assertRaises(AttributeError) as context:
            inst.line()
        self.assertEqual(str(context.exception),
                         "\'CustomClass\' object has no attribute \'line\'")
        with self.assertRaises(AttributeError) as context:
            inst.yyy
        self.assertEqual(str(context.exception),
                         "\'CustomClass\' object has no attribute \'yyy\'")

        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        assert inst.custom_dynamic == "added later"
        with self.assertRaises(AttributeError) as context:
            inst.dynamic
        self.assertEqual(str(context.exception),
                         "\'CustomClass\' object has no attribute \'dynamic\'")

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
