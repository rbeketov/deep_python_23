import io

def read_and_filter_file_gen(file_input, search_words : list):
    if isinstance(file_input, str):
        try:
            with open(file_input, 'r') as file:
                for line in file:
                    if any(word in line for word in search_words):
                        yield line.strip()
        except FileNotFoundError:
            print(f"Файл '{file_input}' не найден.")

    elif isinstance(file_input, io.IOBase):
        for line in file_input:
            if any(word in line for word in search_words):
                yield line.strip()
    
    else:
        print("Неверный формат входных данных")