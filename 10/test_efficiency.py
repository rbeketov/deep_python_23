import cjson
import ujson
import json
import time

from faker import Faker


def generate_random_json(len_list, len_json):
    fake = Faker()

    def generate_random_key():
        return fake.word()

    def generate_random_value():
        return fake.random_element(elements=(
            fake.random_int(),
            fake.random_number(),
            fake.word()
            )
        )

    json_list = []
    for _ in range(len_list):
        json_object = {generate_random_key(): generate_random_value() for _ in range(len_json)}
        json_list.append(json_object)
    return json_list


def test_efficiency():
    json_list = generate_random_json(1_000, 4_000)
    
    strart_cjson = time.time()
    for jsn in json_list:
        cjson.loads(cjson.dumps(jsn))
    end_cjson = time.time()

    strart_ujson = time.time()
    for jsn in json_list:
        ujson.loads(ujson.dumps(jsn))
    end_ujson = time.time()

    strart_json = time.time()
    for jsn in json_list:
        json.loads(json.dumps(jsn))
    end_json = time.time()

    print(f"\'cjson\' result: {end_cjson-strart_cjson} sec")
    print(f"\'ujson\' result: {end_ujson-strart_ujson} sec")
    print(f"\'json\' result: {end_json-strart_json} sec")


if __name__ == "__main__":
    test_efficiency()