import unittest
import json


from time import sleep
from server import ServerMaster, WorkerProcessUrl
from unittest.mock import Mock, patch
from queue import Queue
from urllib.error import HTTPError
from server import ConstEnum

TYPE_ERROR_MESSAGE = "Invalid data types"


class TestServer(unittest.TestCase):
    def test_uncorrecr_config(self):
        with self.assertRaises(TypeError) as context:
            server = ServerMaster(host="192.102.2.2",
                                  port=8800,
                                  num_workers=-10,
                                  top_count=10)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            server = ServerMaster(host="192.102.2.2",
                                  port="100",
                                  num_workers=10,
                                  top_count=10)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            server = ServerMaster(host=123,
                                  port=8800,
                                  num_workers=10,
                                  top_count="10")
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            server = ServerMaster(host="0.0.0.0",
                                  port=8800,
                                  num_workers="sd",
                                  top_count=2)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

    def test_valid_parse_html(self):
        worker = WorkerProcessUrl(Queue(), 5)

        html_content = "<p>This is a test. test. test.</p>"
        expected_result = ['This', 'is', 'a', 'test', 'test', 'test']
        result = worker.parser_html(html_content)
        self.assertEqual(result, expected_result)

        html_content = ""
        expected_result = []
        result = worker.parser_html(html_content)
        self.assertEqual(result, expected_result)

        html_content = "<div><p></p><a href='example.com'></a></div>"
        expected_result = []
        result = worker.parser_html(html_content)
        self.assertEqual(result, expected_result)

        html_content = "<p>This is &amp; a test. &lt;Tag&gt;</p>"
        expected_result = ["This", "is", "a", "test", "Tag"]
        result = worker.parser_html(html_content)
        self.assertEqual(result, expected_result)

    def test_invalid_parse_html(self):
        worker = WorkerProcessUrl(Queue(), 5)

        with self.assertRaises(TypeError) as context:
            worker.parser_html(123)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            worker.parser_html(['12', '21'])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            worker.parser_html(12.124124)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

    def test_valid_url_response(self):
        worker = WorkerProcessUrl(Queue(), 5)
        worker.logger_statistic = Mock()
        with patch('urllib.request.urlopen') as mock_urlopen, \
             patch.object(worker, 'parser_html') as mock_parser_html:
            mock_response = Mock()
            mock_response.read.return_value = b'<p>This is a test. test. test.</p>'
            mock_urlopen.return_value.__enter__.return_value = mock_response
            url = 'http://example.com'
            expected_result = {'test': 3, 'This': 1, 'is': 1, 'a': 1}

            mock_parser_html.return_value = ['This', 'is', 'a', 'test', 'test', 'test']

            result = worker.process_url(url)

            mock_urlopen.assert_called_once_with(url)
            mock_response.read.assert_called_once_with()

            mock_parser_html.assert_called_once_with("<p>This is a test. test. test.</p>")            
            worker.logger_statistic.add_without_error.assert_called_once()
            self.assertEqual(result, expected_result)

    def test_empty_url_response(self):
        worker = WorkerProcessUrl(Queue(), 5)
        worker.logger_statistic = Mock()
        with patch('urllib.request.urlopen') as mock_urlopen, \
             patch.object(worker, 'parser_html') as mock_parser_html:
            mock_response = Mock()
            mock_response.read.return_value = b''
            mock_urlopen.return_value.__enter__.return_value = mock_response
            url = 'http://example.com'
            expected_result = {}

            mock_parser_html.return_value = []

            result = worker.process_url(url)

            mock_urlopen.assert_called_once_with(url)
            mock_response.read.assert_called_once_with()

            mock_parser_html.assert_called_once_with("")            
            worker.logger_statistic.add_without_error.assert_called_once()
            self.assertEqual(result, expected_result)

    def test_forbidden_url_response(self):
        worker = WorkerProcessUrl(Queue(), 5)
        worker.logger_statistic = Mock()
        with patch('urllib.request.urlopen') as mock_urlopen, \
             patch.object(worker, 'parser_html') as mock_parser_html:
            mock_urlopen.side_effect = HTTPError(url='',
                                                 code=403,
                                                 msg='forbidden!!!',
                                                 hdrs='',
                                                 fp=None)

            url = 'http://example.com'
            expected_result = {"Error": "HTTP Error 403: forbidden!!!"}

            mock_parser_html.return_value = []

            result = worker.process_url(url)

            mock_urlopen.assert_called_once_with(url)
            mock_parser_html.assert_not_called()

            worker.logger_statistic.add_with_error.assert_called_once()
            self.assertEqual(result, expected_result)

    def test_notfound_url_response(self):
        worker = WorkerProcessUrl(Queue(), 5)
        worker.logger_statistic = Mock()
        with patch('urllib.request.urlopen') as mock_urlopen, \
             patch.object(worker, 'parser_html') as mock_parser_html:
            mock_urlopen.side_effect = HTTPError(url='',
                                                 code=404,
                                                 msg='CHECK YOUR URL BOOOY!!',
                                                 hdrs='',
                                                 fp=None)

            url = 'hello my friend'
            expected_result = {"Error": "HTTP Error 404: CHECK YOUR URL BOOOY!!"}

            mock_parser_html.return_value = []

            result = worker.process_url(url)

            mock_urlopen.assert_called_once_with(url)
            mock_parser_html.assert_not_called()

            worker.logger_statistic.add_with_error.assert_called_once()
            self.assertEqual(result, expected_result)

    def test_invalid_url(self):
        worker = WorkerProcessUrl(Queue(), 5)

        with self.assertRaises(TypeError) as context:
            worker.process_url(123)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            worker.process_url(['12', '21'])
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            worker.process_url(12.124124)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

    def test_worker_start_and_process_url(self):
        queue = Queue()

        mock_socket = Mock()
        mock_socket.recv.return_value = "http://example.com".encode('utf-8')
        queue.put(mock_socket)

        worker = WorkerProcessUrl(queue, 5)
        worker.logger_statistic = Mock()

        with patch.object(worker, 'process_url') as mock_process_url, \
             patch('builtins.print') as mock_print:
            mock_process_url.return_value = {"test5": 5, "test3": 3}
            response_json = json.dumps({"test5": 5, "test3": 3})

            worker.start()
            sleep(2)
            worker.stop()
            worker.join()

            mock_socket.recv.assert_called_once_with(ConstEnum.BYTES)
            mock_process_url.assert_called_once_with("http://example.com")
            mock_socket.send.assert_called_once_with(response_json.encode('utf-8'))
            self.assertEqual(mock_print.call_count, 2)
            calls = [unittest.mock.call(f"{worker.name} started working"),
                     unittest.mock.call(worker.logger_statistic)
            ]
            mock_print.assert_has_calls(calls, any_order=False)
