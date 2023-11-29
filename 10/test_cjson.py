import unittest
import json
import ujson
import cjson


class TestCJSON(unittest.TestCase):
    def test_from_task(self):
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(json_doc, ujson_doc)
        self.assertEqual(ujson_doc, cjson_doc)
        self.assertEqual(json_str, cjson.dumps(cjson.loads(json_str)))


if __name__ == "__main__":
    unittest.main()
