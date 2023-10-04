import json

INCORRECT_VALUES = "Некорректные аргументы"


def parse_json(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    if (
        not isinstance(json_str, str) or
        not isinstance(required_fields, (list, set)) or
        not all(isinstance(field, str) for field in required_fields) or
        not isinstance(keywords, (list, set)) or
        not all(isinstance(keyword, str) for keyword in keywords) or
        not callable(keyword_callback)
    ):
        raise ValueError(INCORRECT_VALUES)

    json_doc = json.loads(json_str)

    for key in set(required_fields):
        if key in json_doc.keys():
            for word in set(keywords):
                if word.lower() in json_doc[key].lower().split():
                    keyword_callback(word)
