import socket
import threading
import argparse
import json
import urllib.request
import re

from queue import Queue, Empty
from collections import Counter
from enum import IntEnum
from bs4 import BeautifulSoup


class ConstEnum(IntEnum):
    BYTES = 1024
    HOST_NUMBER = 0
    PORT_NUMBER = 1

class SingleTone(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class StatisticCounetr(metaclass=SingleTone):
    def __init__(self) -> None:
        self._total_count = 0
        self._count_with_error = 0

    def add_without_error(self) -> None:
        self._total_count += 1

    def add_with_error(self) -> None:
        self._total_count += 1
        self._count_with_error += 1

    def __str__(self) -> str:
        output = f"A total of {self._total_count} "
        output += f"of them were processed with an error of {self._count_with_error}"
        return output


class ServerMaster(threading.Thread):
    def __init__(self,
                 host: str,
                 port: int,
                 num_workers: int,
                 top_count: int) -> None:
        if (
            not isinstance(host, str) or
            not isinstance(port, int) or
            not isinstance(num_workers, int) or
            not isinstance(top_count, int) or
            top_count < 1 or
            num_workers < 1
        ):
            raise TypeError("Invalid data types")

        super().__init__()
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_count = top_count
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.queue = Queue()
        self._stop_event = threading.Event()
        self.socket.settimeout(5)

    def run(self) -> None:
        try:
            self._stop_event.clear()
            self.socket.listen()
            print(f"Server is listening on {self.host}:{self.port} with {self.num_workers} workers")
            workers = [WorkerProcessUrl(self.queue, self.top_count)
                       for _ in range(self.num_workers)]
            for worker in workers:
                worker.start()

            while True:
                if self._stop_event.is_set():
                    break
                try:
                    client_socket, client_address = self.socket.accept()
                except socket.timeout:
                    continue

                print(f"Accepted connection from {client_address}")
                self.queue.put(client_socket)

        except Exception as err:
            print(f"Error: {str(err)}")
        finally:
            print("Server closed")
            for worker in workers:
                worker.join()

    def stop(self):
        self._stop_event.set()


class WorkerProcessUrl(threading.Thread):
    def __init__(self,
                 queue: Queue,
                 top_count: int) -> None:
        if (
            not isinstance(queue, Queue) or
            not isinstance(top_count, int)
        ):
            raise TypeError("Invalid data types")

        super().__init__()
        self.queue = queue
        self.top_count = top_count
        self.logger_statistic = StatisticCounetr()
        self._stop_event = threading.Event()

    def run(self) -> None:
        thread = threading.current_thread()
        print(f"{thread.name} started working")
        self._stop_event.clear()
        while True:
            if self._stop_event.is_set():
                break
            try:
                client_socket = self.queue.get(timeout=2)
            except Empty:
                continue

            url = client_socket.recv(ConstEnum.BYTES).decode("utf-8").strip()
            word_count = self.process_url(url)
            response_json = json.dumps(word_count)
            try:
                client_socket.send(response_json.encode('utf-8'))
            except Exception as err:
                print(f"Error sending response to client: {err}")
                client_socket.close()
            finally:
                print(self.logger_statistic)

    def parser_html(self, html_content: str) -> str:
        if not isinstance(html_content, str):
            raise TypeError("Invalid data types")

        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text)
        return words

    def process_url(self, url: str) -> dict:
        if not isinstance(url, str):
            raise TypeError("Invalid data types")
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
            words = self.parser_html(content)
            word_count = dict(Counter(words).most_common(self.top_count))
            self.logger_statistic.add_without_error()
            return word_count
        except Exception as err:
            self.logger_statistic.add_with_error()
            return {"Error": f"{err}"}

    def stop(self):
        self._stop_event.set()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", type=int, help="Number of worker threads")
    parser.add_argument("-k", type=int, help="Top count of words")
    args = parser.parse_args()

    if args.w is None or args.k is None:
        parser.print_help()
        raise ValueError("Plese pass the configuration")

    with open('server-conf.txt', 'r', encoding="utf-8") as file:
        config_data = file.read().split('\n')

    host = config_data[ConstEnum.HOST_NUMBER]
    port = int(config_data[ConstEnum.PORT_NUMBER])
    server = ServerMaster(host, port, args.w, args.k)
    server.start()


if __name__ == "__main__":
    main()
