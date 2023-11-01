import unittest
import socket
from unittest.mock import patch, Mock, MagicMock
from queue import Queue
from client import WorkerSendUrls


class TestClient(unittest.TestCase):
    @patch('socket.socket', spec=socket)
    def test_worker_send_urls(self, mock_socket):
        mock_queue = MagicMock(spec=Queue)
        host = 'localhost'
        port = 8088

        mock_connection = Mock()
        mock_socket.return_value = mock_connection

        mock_queue.get.side_effect = [(1, "http://example.com"),
                                      (2, "http://example2.com"),
                                      (None, None)]

        expected_results = ["Result 1", "Result 2"]
        mock_connection.connect.side_effect = [None, None]
        mock_connection.send.side_effect = [None, None]
        mock_connection.recv.side_effect = [result.encode('utf-8') for result in expected_results]

        worker = WorkerSendUrls(mock_queue, host, port)

        worker.start()
        worker.join()

        expected_calls = [
            unittest.mock.call.connect((host, port)),
            unittest.mock.call.send(b"http://example.com"),
            unittest.mock.call.recv(1024).decode('utf-8'),
            unittest.mock.call.connect((host, port)),
            unittest.mock.call.send(b"http://example2.com"),
            unittest.mock.call.recv(1024).decode('utf-8')
        ]
        mock_connection.assert_has_calls(expected_calls, any_order=False)

        self.assertEqual(mock_queue.get.call_count, 4)
        mock_queue.put.assert_called_once_with((None, None))


if __name__ == "__main__":
    unittest.main()
