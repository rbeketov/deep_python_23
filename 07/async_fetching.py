import asyncio
import re
import argparse
import time
from collections import Counter

import aiohttp
from bs4 import BeautifulSoup


TYPE_ERROR_MESSAGE = "Invalid data types"


class SingleTone(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class StatisticCounetr(metaclass=SingleTone):
    def __init__(self) -> None:
        self._total_count = 0

    def add(self) -> None:
        self._total_count += 1

    def __str__(self) -> str:
        return f"Poccesed {self._total_count} urls"


async def get_top_k_word_from_html(html_content: str, top_count: int) -> dict:
    if (
        not isinstance(html_content, str) or
        not isinstance(top_count, int) or
        top_count < 0
    ):
        raise TypeError(TYPE_ERROR_MESSAGE)

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    words = re.findall(r'\b\w+\b', text)
    word_count = dict(Counter(words).most_common(top_count))
    return word_count


async def fetch_url(url: str, top_count: int) -> dict:
    if (
        not isinstance(url, str) or
        not isinstance(top_count, int) or
        top_count < 0
    ):
        raise TypeError(TYPE_ERROR_MESSAGE)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html_content = await resp.text()
                result = await get_top_k_word_from_html(html_content, top_count)
                return result
    except Exception as err:
        return {"Error": f"{err}"}


async def fetch_worker(queue: asyncio.Queue,
                       top_count: int,
                       logger: StatisticCounetr) -> None:
    if (
        not isinstance(queue, asyncio.Queue) or
        not isinstance(top_count, int) or
        top_count < 0 or
        not isinstance(logger, StatisticCounetr)
    ):
        raise TypeError(TYPE_ERROR_MESSAGE)

    while True:
        url = await queue.get()
        try:
            result = await fetch_url(url, top_count)
            logger.add()
            print(f"{logger}\nUrl {url}:\n{result}")
        finally:
            queue.task_done()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Async URL fetcher with max concurrent")
    parser.add_argument("-c", type=int, default=10, help="Number of concurrent requests")
    parser.add_argument("-f", help="File containing URLs")
    parser.add_argument("-t", type=int, default=10, help="Top words count")

    logger = StatisticCounetr()
    args = parser.parse_args()
    total_concurrent = args.c
    top_count = args.t

    queue = asyncio.Queue(maxsize=total_concurrent)
    workers = [
        asyncio.create_task(fetch_worker(queue, top_count, logger))
        for _ in range(total_concurrent)
    ]

    with open(args.f, "r", encoding='utf-8') as file:
        for url in file:
            await queue.put(url.strip())

    await queue.join()
    for worker in workers:
        worker.cancel()


if __name__ == "__main__":
    time_1 = time.time()
    asyncio.run(main())
    time_2 = time.time()
    print(f"Total time {time_2 - time_1}")
