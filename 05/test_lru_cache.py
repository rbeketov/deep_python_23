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

    def test_task_logic(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIs(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIs(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

    def test_main_logic(self):
        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k4"), None)
        #
        cache.set("k4", "val4")
        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k4"), "val4")
        #
        cache.set("k5", "val5")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k5"), "val5")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k4"), "val4")
        #
        cache.set("k6", "val6")
        self.assertEqual(cache.get("k5"), None)
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k6"), "val6")
        self.assertEqual(cache.get("k4"), "val4")
        #

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

    def test_changing_with_exclusion(self):
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")
        cache.set("k2", 2)
        cache.set("k1", 1)
        cache.set("k4", "val4")
        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k4"), "val4")
        self.assertEqual(cache.get("k2"), 2)
        self.assertEqual(cache.get("k1"), 1)
        cache.set("k2", 22)
        cache.set("k1", 11)
        cache.set("k5", "val5")
        self.assertEqual(cache.get("k4"), None)
        self.assertEqual(cache.get("k2"), 22)
        self.assertEqual(cache.get("k1"), 11)

    def test_different_key(self):
        cache = LRUCache(2)
        cache.set(1, "val1")
        cache.set(2.2, [100])
        self.assertEqual(cache.get(1), "val1")
        self.assertEqual(cache.get(2.2), [100])
        cache.set('12', [100])
        self.assertEqual(cache.get(1), None)
        self.assertEqual(cache.get(2.2), [100])
        self.assertEqual(cache.get('12'), [100])


if __name__ == "__main__":
    unittest.main()
