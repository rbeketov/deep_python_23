import random
from collections import Counter
from faker import Faker


class JSONGenerator:
    def __init__(self):
        self.faker = Faker()

    def create_json_keys_words(self, num_items, probability_keys=0.5, probability_words=0.15):
        json_data = {}
        keys = set()
        words = set()
        callback_info = Counter()

        for _ in range(num_items):
            # генерируем случайный ключ
            key = self.faker.word()
            # если ключ уже существует в наборе ключей, пропускаем итерацию
            # чтобы не затереть предыдущий
            if key in keys:
                continue
            value = self.__generate_random_string()
            json_data[key] = value

            # добавляем ключ в множество ключей с вероятностью p_k
            if random.random() < probability_keys:
                keys.add(key)
                # перебираем слова, которые уже были добавлены
                # и считаем их вхождение в сгениррированную строку
                for word in words:
                    if word in value.split():
                        callback_info[word] += 1

                # хотим с вероятностью p_w добавить слово из новой строки
                # в set для поиска, поэтому идём по строке
                for word in value.split():
                    if random.random() < probability_words:
                        # не прибовляем значения в счётчике,
                        # если это слово уже было в words,
                        # т.к. тогда мы его посчитали forом выше...
                        if word not in words:
                            words.add(word)
                            for key_ in keys:
                                if word in json_data[key_].split():
                                    callback_info[word] += 1

        return json_data, keys, words, callback_info

    def __generate_random_string(self):
        length = random.randint(5, 15)
        random_words = [self.faker.word() for _ in range(length)]
        return ' '.join(random_words)
