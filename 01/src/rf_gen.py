import io

BAD_INPUT_DATA = 'Неверный формат входных данных'


def read_and_filter_file_gen(file_input, search_words: list):
    if isinstance(file_input, str):
        try:
            with open(file_input, 'r', encoding='utf-8') as file:
                for line in file:
                    if any(word in line for word in search_words):
                        yield line.strip()
        except FileNotFoundError as exc:
            raise NameError(f"Файл '{file_input}' не найден") from exc
    elif isinstance(file_input, io.IOBase):
        for line in file_input:
            if any(word in line for word in search_words):
                yield line.strip()
    else:
        raise AttributeError(BAD_INPUT_DATA)
