from predict_mood import predict_message_mood
from model import SomeModel


def main():
    model = SomeModel()
    assert predict_message_mood("Чапаев и пустота", model) == "отл"
    assert predict_message_mood("Вулкан", model,) == "неуд"


if __name__ == "__main__":
    main()
