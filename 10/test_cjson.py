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

    def test_loads_ignore_unimportant_space(self):
        json_str = '{  "  hello  "   : 10 , "world  " : "v  alue", "  numb": -1.2}'
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(cjson_doc["  hello  "], 10)
        self.assertEqual(cjson_doc["world  "], "v  alue")
        self.assertEqual(cjson_doc["  numb"], -1.2)
        self.assertEqual(len(cjson_doc), 3)

    def test_loads_empty(self):
        json_str = '{}'
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(cjson_doc, {})
        self.assertEqual(len(cjson_doc), 0)

    def test_loads_invalid_input_value(self):
        with self.assertRaises(ValueError) as context:
            cjson.loads('}}')
        self.assertEqual(str(context.exception), "Invalid JSON format: Expected an object")
        with self.assertRaises(TypeError) as context:
            cjson.loads(123)
        self.assertEqual(str(context.exception), "Expected a string")
        with self.assertRaises(ValueError) as context:
            cjson.loads('{12: "23"}')
        self.assertEqual(str(context.exception), "Invalid JSON format: Expected a string key")
        with self.assertRaises(ValueError) as context:
            cjson.loads('{"12}')
        self.assertEqual(str(context.exception), "Invalid JSON format: Unclosed string key")
        with self.assertRaises(ValueError) as context:
            cjson.loads('{"12"     "23"}')
        self.assertEqual(
            str(context.exception),
            "Invalid JSON format: Expected a colon after the key"
        )
        with self.assertRaises(ValueError) as context:
            cjson.loads('{"12": 23"}')
        self.assertEqual(
            str(context.exception),
            "Invalid JSON format: Expected a comma or closing brace"
        )
        with self.assertRaises(ValueError) as context:
            cjson.loads('{"12": [23]}')
        self.assertEqual(
            str(context.exception),
            "Invalid JSON format: Expected a string or number value"
        )

    def test_dumps_valid_value(self):
        jsn_str = cjson.dumps({'12': -12.234, "ds": " 0 0 0 ", "[1]": 2})
        expected_result = '{"12": -12.234, "ds": " 0 0 0 ", "[1]": 2}'
        self.assertEqual(jsn_str, expected_result)
        self.assertEqual(len(jsn_str), len(expected_result))

    def test_dumps_empty_json(self):
        jsn_str = cjson.dumps({})
        self.assertEqual(jsn_str, "{}")
        self.assertEqual(len(jsn_str), len("{}"))

    def test_dumps_invalid_input_value(self):
        with self.assertRaises(TypeError) as context:
            cjson.dumps()
        self.assertEqual(str(context.exception), "Expected a dictionary")
        with self.assertRaises(TypeError) as context:
            cjson.dumps('}}')
        self.assertEqual(str(context.exception), "Argument must be a dictionary")

        with self.assertRaises(TypeError) as context:
            cjson.dumps({1.123: 123})
        self.assertEqual(str(context.exception), "Key must be a string")

        with self.assertRaises(TypeError) as context:
            cjson.dumps({"123": {"123": 1234}})
        self.assertEqual(str(context.exception), "Nested dictionaries are not supported")
        with self.assertRaises(TypeError) as context:
            cjson.dumps({"123": ["123"]})
        self.assertEqual(str(context.exception), "Unsupported value type")


if __name__ == "__main__":
    unittest.main()
