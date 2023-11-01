import socket
import threading
from sys import argv
from queue import Queue
from enum import IntEnum


class ConstEnum(IntEnum):
    EXECTED_ARGUMENT_COUNT = 3
    BYTES = 1024
    NUM_WORKER_NUMBER = 1
    FILE_NUMBER = 2
    HOST_NUMBER = 0
    PORT_NUMBER = 1


class ClientSendUrls:
    def __init__(self,
                 host: str,
                 port: int,
                 num_workers: int,
                 file_with_urls: str) -> None:
        if (
            not isinstance(host, str) or
            not isinstance(port, int) or
            not isinstance(num_workers, int) or
            not isinstance(file_with_urls, str) or
            num_workers < 1
        ):
            raise TypeError("Invalid data types")

        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.que = Queue(self.num_workers)
        self.file_with_urls = file_with_urls

    def start(self) -> None:
        try:
            workers = [WorkerSendUrls(self.que,
                                      self.host,
                                      self.port)
                       for _ in range(self.num_workers)]
            for worker in workers:
                worker.start()
            self.load_urls()
        except Exception as err:
            print(f"Error: {str(err)}\n")
        finally:
            for worker in workers:
                worker.join()
            print("Join completed")

    def load_urls(self) -> None:
        try:
            print(f"Open...\'{self.file_with_urls}\'")
            with open(self.file_with_urls, "r", encoding="utf-8") as data_urls:
                for i, url in enumerate(data_urls):
                    correct_url = url.strip() + '\n'
                    self.que.put((i, correct_url))
                    print(f"Uploaded url number {i}")
        except Exception as err:
            raise RuntimeError(f"Error while try upload urls: {str(err)}") from err
        finally:
            self.que.put((None, None))


class WorkerSendUrls(threading.Thread):
    def __init__(self,
                 queue: Queue,
                 host: str,
                 port: int) -> None:
        if (
            not isinstance(queue, Queue) or
            not isinstance(host, str) or
            not isinstance(port, int)
        ):
            raise TypeError("Invalid data types")

        super().__init__()
        self.queue = queue
        self.host = host
        self.port = port

    def run(self) -> None:
        thread = threading.current_thread()
        print(f"{thread.name} started working")
        while True:
            try:
                number, url = self.queue.get()
                if not url:
                    self.queue.put((None, None))
                    break

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
                    connection.connect((self.host, self.port))
                    connection.send(url.encode())
                    result = connection.recv(ConstEnum.BYTES).decode("utf-8")
                    print(f"Url (number {number}) {url.strip()}, result:\n{result}")

            except Exception as err:
                print(f"Error while try process url number {number}: {str(err)}")


def main() -> None:
    if len(argv) != ConstEnum.EXECTED_ARGUMENT_COUNT:
        print("Usage: python client.py \'num_workers\' \'file\'")
        raise ValueError("Plese pass the configuration")

    num_workers = int(argv[ConstEnum.NUM_WORKER_NUMBER])
    file = argv[ConstEnum.FILE_NUMBER]
    with open('server-conf.txt', 'r', encoding="utf-8") as file_config:
        config_data = file_config.read().split('\n')
    host = config_data[ConstEnum.HOST_NUMBER]
    port = int(config_data[ConstEnum.PORT_NUMBER])

    client = ClientSendUrls(host, port, num_workers, file)
    client.start()


if __name__ == "__main__":
    main()
