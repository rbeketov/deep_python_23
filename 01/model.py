class SomeModel:
    def __init__(self):
        pass

    def predict(self, message: str) -> float:
        return abs(len(message)-6) * 0.5
