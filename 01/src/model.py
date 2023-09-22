class SomeModel:
    def predict(self, message: str) -> float:
        return abs(len(message)-6) * 0.5