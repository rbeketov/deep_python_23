import io
from typing import List

BAD_INPUT_DATA = 'Неверный формат входных данных'


def read_and_filter_file_gen(file_input, search_words: List[str]):
    if (
        not isinstance(search_words, list) or
        not all(isinstance(word, str) for word in search_words)
    ):
        raise ValueError(BAD_INPUT_DATA)

    def process_file(file):
        for line in file:
            if any(word.lower() in line.lower().split() for word in search_words):
                yield line.strip()

    if isinstance(file_input, str):
        try:
            with open(file_input, 'r', encoding='utf-8') as file:
                yield from process_file(file)
        except FileNotFoundError as exc:
            raise NameError(f"Файл '{file_input}' не найден") from exc
    elif isinstance(file_input, io.IOBase):
        yield from process_file(file_input)
    else:
        raise ValueError(BAD_INPUT_DATA)
