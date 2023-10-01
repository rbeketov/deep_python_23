from model import SomeModel

EXCELLENT_CONST = 'отл'
FINE_CONST = 'норм'
FAILURE_CONST = 'неуд'
BAD_INPUT_DATA = 'Неверный формат входных данных'


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if (
        bad_thresholds > 1 or
        bad_thresholds < 0 or
        good_thresholds > 1 or
        good_thresholds < 0 or
        not isinstance(model, SomeModel)
    ):
        raise AttributeError(BAD_INPUT_DATA)
    predict = model.predict(message=message)
    if predict > good_thresholds:
        return EXCELLENT_CONST
    if predict < bad_thresholds:
        return FAILURE_CONST
    return FINE_CONST
