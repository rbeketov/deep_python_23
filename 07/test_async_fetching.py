import sys
import io
import unittest
import asyncio

from unittest.mock import MagicMock, AsyncMock, patch
from async_fetching import get_top_k_word_from_html
from async_fetching import fetch_url
from async_fetching import fetch_worker
from async_fetching import StatisticCounetr


TYPE_ERROR_MESSAGE = "Invalid data types"


class TestAsyncioFethcing(unittest.IsolatedAsyncioTestCase):
    async def test_get_top_k_word_from_html(self):
        html_content = "<p>This This, is a test. test. test.</p>"
        expected_result = {"test": 3}
        result = await get_top_k_word_from_html(html_content, top_count=1)
        self.assertEqual(result, expected_result)

        html_content = "<p>This This, is a test. test. test.</p>"
        expected_result = {"test": 3, "This": 2}
        result = await get_top_k_word_from_html(html_content, top_count=2)
        self.assertEqual(result, expected_result)

        html_content = "<p>This This, is a test. test. test.</p>"
        expected_result = {}
        result = await get_top_k_word_from_html(html_content, top_count=0)
        self.assertEqual(result, expected_result)

    async def test_fetch_url(self):
        html_content = "<p>This This, is a test. test. test.</p>"
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value = AsyncMock()
            mock_get.return_value.__aenter__.return_value.text.return_value = html_content
            with patch("async_fetching.get_top_k_word_from_html") as mock_parse:
                expected_result = {"test": 3, "This": 2}
                mock_parse.return_value = expected_result
                result = await fetch_url("example.com", 2)
                self.assertEqual(result, expected_result)
                calls = [unittest.mock.call(html_content, 2)]
                mock_parse.assert_has_calls(calls, any_order=False)

        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value = AsyncMock()
            mock_get.return_value.__aenter__.return_value.text.side_effect = Exception("ERROR!")
            with patch("async_fetching.get_top_k_word_from_html") as mock_parse:
                expected_result = {"Error": "ERROR!"}
                mock_parse.return_value = {"test": "test"}
                result = await fetch_url("example.com", 2)
                self.assertEqual(result, expected_result)
                calls = []
                mock_parse.assert_has_calls(calls, any_order=False)

    async def test_fetch_worker(self):
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

        que = asyncio.Queue()
        mock_logger = MagicMock(spec=StatisticCounetr)
        mock_logger.add.return_value = None
        mock_logger.__str__.return_value = "test"
        with patch("async_fetching.fetch_url") as mock_fetch:
            expected_result = {"Test": 5}
            mock_fetch.return_value = expected_result

            worker = asyncio.create_task(fetch_worker(que, 3, mock_logger))
            await que.put("example.com")
            await que.join()
            worker.cancel()

            self.captured_output.seek(0)
            output = self.captured_output.read()
            expected_output = "test\nUrl example.com:\n{\'Test\': 5}\n"
            self.assertEqual(expected_output, output)

            calls_fetch = [unittest.mock.call("example.com", 3)]
            mock_fetch.assert_has_calls(calls_fetch, any_order=False)

            mock_logger.add.assert_called_with()
            mock_logger.__str__.assert_called_with()

        sys.stdout = sys.__stdout__
        self.captured_output.close()

    async def test_invalid_value(self):
        with self.assertRaises(TypeError) as context:
            value = await get_top_k_word_from_html("test test test", -1)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await get_top_k_word_from_html(["test test test"], 10)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await get_top_k_word_from_html(-1, 10)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await get_top_k_word_from_html("test test test", "10")
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await fetch_url("url", "10")
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await fetch_url("url", -10)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await fetch_url(["url"], -10)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await fetch_worker(["url"], -10, 10)
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)

        with self.assertRaises(TypeError) as context:
            value = await fetch_worker("url", 10, "10")
        self.assertEqual(str(context.exception), TYPE_ERROR_MESSAGE)


if __name__ == "__main__":
    unittest.main()
