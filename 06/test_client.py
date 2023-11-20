import unittest
from unittest.mock import patch, MagicMock
from queue import Queue
from client import WorkerSendUrls


class TestClient(unittest.TestCase):
    @patch('socket.socket')
    def test_worker_send_urls(self, mock_socket):
        mock_queue = MagicMock(spec=Queue)
        host = 'localhost'
        port = 8088

        mock_connection = mock_socket.return_value
        mock_queue.get.side_effect = [
            (1, "http://example.com"),
            (2, "http://example2.com"),
            (None, None)
        ]

        expected_results = ["Result 1", "Result 2"]
        mock_connection.connect.return_value = None
        mock_connection.send.return_value = None
        mock_connection.recv.side_effect = [
            result.encode('utf-8') for result in expected_results
        ]

        worker = WorkerSendUrls(mock_queue, host, port)

        worker.start()
        worker.join()

        expected_connect_calls = [
            unittest.mock.call((host, port)),
            unittest.mock.call((host, port)),
        ]
        mock_socket.return_value.connect.assert_has_calls(expected_connect_calls, any_order=False)

        self.assertEqual(mock_queue.get.call_count, 3)
        mock_queue.put.assert_called_once_with((None, None))

        expected_send_calls = [
            unittest.mock.call(b"http://example.com"),
            unittest.mock.call(b"http://example2.com"),
        ]
        expected_recv_calls = [
            unittest.mock.call(1024),
            unittest.mock.call(1024),
        ]
        mock_connection.send.assert_has_calls(expected_send_calls, any_order=False)

        mock_connection.recv.assert_has_calls(expected_recv_calls, any_order=False)
        mock_connection.recv.return_value.decode.return_value = expected_results[0]

        expected_console_output = [
            unittest.mock.call("Url (number 1) http://example.com, result:\nResult 1"),
            unittest.mock.call("Url (number 2) http://example2.com, result:\nResult 2"),
        ]
        self.assertEqual(mock_connection.recv.call_count, 2)
        mock_connection.recv.assert_has_calls(expected_console_output, any_order=False)
