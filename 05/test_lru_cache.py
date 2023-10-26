import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_uncorrect_create(self):
        with self.assertRaises(TypeError) as context:
            lru_cache = LRUCache("test")
        self.assertEqual(str(context.exception), '\'limit\' should be positive int')

        with self.assertRaises(TypeError) as context:
            lru_cache = LRUCache(1.2)
        self.assertEqual(str(context.exception), '\'limit\' should be positive int')

        with self.assertRaises(TypeError) as context:
            lru_cache = LRUCache([])
        self.assertEqual(str(context.exception), '\'limit\' should be positive int')

        with self.assertRaises(TypeError) as context:
            lru_cache = LRUCache(-1)
        self.assertEqual(str(context.exception), '\'limit\' should be positive int')

    def test_main_logic(self):
        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k4"), None)
        cache.set("k4", "val4")
        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k4"), "val4")
        cache.set("k5", "val5")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k5"), "val5")
        cache.set("k6", "val6")
        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k6"), "val6")
        cache.set("k7", "val7")
        self.assertEqual(cache.get("k4"), None)
        self.assertEqual(cache.get("k7"), "val7")

    def test_any_value_in_cache(self):
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", 2)
        cache.set("k3", [1, 2, 3])
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k2"), 2)
        self.assertEqual(cache.get("k3"), [1, 2, 3])

    def test_limit_one(self):
        cache = LRUCache(1)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k3"), "val3")
        cache.set("k4", "val4")
        self.assertEqual(cache.get("k4"), "val4")
        self.assertEqual(cache.get("k3"), None)
        cache.set("k4", 1)
        self.assertEqual(cache.get("k4"), 1)

    def test_changing(self):
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")
        cache.set("k1", 1)
        cache.set("k2", 2)
        cache.set("k3", 3)
        self.assertEqual(cache.get("k1"), 1)
        self.assertEqual(cache.get("k2"), 2)
        self.assertEqual(cache.get("k3"), 3)
        cache.set("k1", [1])
        cache.set("k2", [2])
        cache.set("k3", [3])
        self.assertEqual(cache.get("k1"), [1])
        self.assertEqual(cache.get("k2"), [2])
        self.assertEqual(cache.get("k3"), [3])

    def test_uncorrect_key(self):
        cache = LRUCache(3)
        with self.assertRaises(TypeError) as context:
            cache.set(1, "12")
        self.assertEqual(str(context.exception), '\'key\' should be str')

        with self.assertRaises(TypeError) as context:
            cache.set([2], "12")
        self.assertEqual(str(context.exception), '\'key\' should be str')

        with self.assertRaises(TypeError) as context:
            cache.set(2.32, "12")
        self.assertEqual(str(context.exception), '\'key\' should be str')


if __name__ == "__main__":
    unittest.main()
