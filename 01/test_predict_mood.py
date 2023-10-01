import unittest
from unittest import mock
from model import SomeModel
from predict_mood import predict_message_mood
from predict_mood import EXCELLENT_CONST, FINE_CONST
from predict_mood import FAILURE_CONST, BAD_INPUT_DATA


class TestPredictMessageMood(unittest.TestCase):
    def setUp(self):
        self.model = mock.MagicMock(spec=SomeModel)

    def test_valid_input(self):
        self.model.predict.return_value = 0.8
        self.assertEqual(predict_message_mood("Hello, world!", self.model), FINE_CONST)
        self.model.predict.assert_has_calls([mock.call(message="Hello, world!")])
        self.assertEqual(self.model.predict.call_count, 1)

        self.model.predict.return_value = 0.81
        self.assertEqual(predict_message_mood("Hello, world!", self.model), EXCELLENT_CONST)
        self.model.predict.assert_has_calls([mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!")])
        self.assertEqual(self.model.predict.call_count, 2)

        self.model.predict.return_value = 0.29
        self.assertEqual(predict_message_mood("Hello, world!", self.model), FAILURE_CONST)
        self.model.predict.assert_has_calls([mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!")])
        self.assertEqual(self.model.predict.call_count, 3)

        self.model.predict.return_value = 0.99
        self.assertEqual(predict_message_mood("Hello, world!", self.model), EXCELLENT_CONST)
        self.model.predict.assert_has_calls([mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!")])
        self.assertEqual(self.model.predict.call_count, 4)

        self.model.predict.return_value = 1
        self.assertEqual(predict_message_mood("Hello, world!", self.model), EXCELLENT_CONST)
        self.model.predict.assert_has_calls([mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!")])
        self.assertEqual(self.model.predict.call_count, 5)

        self.model.predict.return_value = 0.3
        self.assertEqual(predict_message_mood("Hello, world!", self.model), FINE_CONST)
        self.model.predict.assert_has_calls([mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!")])
        self.assertEqual(self.model.predict.call_count, 6)

        self.model.predict.return_value = 0
        self.assertEqual(predict_message_mood("Hello, world!", self.model), FAILURE_CONST)
        self.model.predict.assert_has_calls([mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!"),
                                             mock.call(message="Hello, world!")])
        self.assertEqual(self.model.predict.call_count, 7)

    def test_boundary_thresholds(self):
        self.model.predict.return_value = 0.
        self.assertEqual(predict_message_mood("Neutral message",
                                              self.model,
                                              bad_thresholds=0,
                                              good_thresholds=1), FINE_CONST)

        self.model.predict.return_value = 0.6
        self.assertEqual(predict_message_mood("Positive message",
                                              self.model,
                                              bad_thresholds=0.5,
                                              good_thresholds=0.59), EXCELLENT_CONST)

        self.model.predict.return_value = 0.1
        self.assertEqual(predict_message_mood("Negative message",
                                              self.model,
                                              bad_thresholds=0.11,
                                              good_thresholds=0.2), FAILURE_CONST)

    def test_invalid_thresholds(self):
        with self.assertRaises(AttributeError) as context:
            predict_message_mood("Test message",
                                 self.model,
                                 bad_thresholds=1.5,
                                 good_thresholds=0.8)
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)

        with self.assertRaises(AttributeError) as context:
            predict_message_mood("Test message",
                                 self.model,
                                 bad_thresholds=-0.1,
                                 good_thresholds=0.8)
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)

        with self.assertRaises(AttributeError) as context:
            predict_message_mood("Test message",
                                 self.model,
                                 bad_thresholds=0.2,
                                 good_thresholds=1.1)
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)

    def test_invalid_model_type(self):
        invalid_model = "This is not a SomeModel instance"
        with self.assertRaises(AttributeError) as context:
            predict_message_mood("Test message", invalid_model)
        self.assertEqual(str(context.exception), BAD_INPUT_DATA)


if __name__ == '__main__':
    unittest.main()
