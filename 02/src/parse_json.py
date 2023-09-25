import json

INCORRECT_VALUES = "Некорректные аргументы"

def parse_json(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    if (
        not isinstance(json_str, str) or
        not isinstance(required_fields, (list, set)) or
        not isinstance(keywords, (list, set)) or
        not callable(keyword_callback)
    ):
        raise ValueError(INCORRECT_VALUES)
    
    json_doc = json.loads(json_str)

    for key in set(required_fields):
        if key in json_doc.keys():
            for word in set(keywords):
                if word in json_doc[key].split():
                    keyword_callback(word)

