import argparse
import logging


FILE_FORMATER = "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
STREAM_FORMATER = "%(asctime)s - %(levelname)s - %(message)s"


class WordCountFilter(logging.Filter):
    def __init__(self, max_word_count):
        super().__init__()
        self.max_word_count = max_word_count

    def filter(self, record):
        message = record.getMessage()
        word_count = len(message.split())
        return word_count <= self.max_word_count


def _create_error_message(name: str, type: str) -> str:
    return f"\'{name}\' should be {type}"


class ListNode:
    def __init__(self, key: any, value: any) -> None:
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, limit: int) -> None:
        if not isinstance(limit, int) or limit <= 0:
            logging.critical(
                "When creating LRUCache the size of the incorrect type was passed: "
                "(should be positive int) "
                "\'limit\' = %s", limit
            )
            raise TypeError(_create_error_message(name="limit", type="positive int"))
        self.limit = limit
        self.newest = ListNode("newest", "newest")
        self.oldest = ListNode("oldest", "oldest")
        self.newest.prev = self.oldest
        self.oldest.next = self.newest
        self.cache = {}
        logging.info(
            "LRUCache was created, size = %s",
            self.limit
        )

    def get(self, key: any) -> any:
        if key not in self.cache:
            logging.error(
                "Requested key = \'%s\' does not exist in cache",
                key
            )
            return None
        self._delete(self.cache[key])
        self._insert(self.cache[key])
        logging.info(
            "\'get\' with key = \'%s\' executed successfully",
            key
        )
        return self.cache[key].value

    def _insert(self, node: 'ListNode'):
        logging.debug(
            "Attempt to insert ListNode with key = \'%s\', "
            "the node is located between \'%s\' and \'%s\'",
            node.key, self.newest.key, self.newest.prev.key
        )
        prev_newest, newest = self.newest.prev, self.newest
        prev_newest.next = node
        node.prev = prev_newest
        newest.prev = node
        node.next = newest
        logging.info(
            "key = \'%s\' increased in priority",
            node.key
        )

    def _delete(self, node: 'ListNode'):
        logging.debug(
            "Attempt to delete ListNode with key = \'%s\', "
            "the node is located between \'%s\' and \'%s\'",
            node.key, node.next.key, node.prev.key
        )
        prev_node, next_node = node.prev, node.next
        prev_node.next = next_node
        next_node.prev = prev_node

        logging.info(
            "key = \'%s\' deleted from cache",
            node.key
        )

    def set(self, key: any, value: any) -> None:
        logging.info(
            "Trying add key = \'%s\' in cache",
            key
        )
        if key in self.cache:
            logging.info(
                "key = \'%s\' is added that is already in cache",
                key
            )
            self._delete(self.cache[key])
        logging.debug(
            "Attempt to create ListNode with key = \'%s\' and value = \'%s\'",
            key, value
        )
        self.cache[key] = ListNode(key, value)
        logging.debug(
            "Created successfully ListNode with key = \'%s\' and value = \'%s\' ",
            key, value
        )
        self._insert(self.cache[key])
        logging.info(
            "Added successfully key = \'%s\' in cache",
            key
        )
        if len(self.cache) > self.limit:
            for_delete = self.oldest.next
            logging.warning(
                "The allowed size (%s) is exceeded "
                "the value will be displaced with key = \'%s\'",
                self.limit, for_delete.key
            )
            self._delete(for_delete)
            del self.cache[for_delete.key]


def config_log(args_):
    file_formater = logging.Formatter(FILE_FORMATER)
    file_handler = logging.FileHandler('cache.log')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formater)
    logger.addHandler(file_handler)

    if args_.s:
        stream_formater = logging.Formatter(STREAM_FORMATER)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_formater)
        logger.addHandler(stream_handler)

    if args_.f:
        max_len_4_filter = WordCountFilter(8)
        logger.addFilter(max_len_4_filter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LRUCache with logging configuration')
    parser.add_argument('-s', action='store_true', help='Log to stdout')
    parser.add_argument('-f', action='store_true', help='Apply custom filter')
    args = parser.parse_args()

    config_log(args)

    cache = LRUCache(limit=3)

    cache.set(1, 'one')  # set отсутствующего ключа
    cache.get(1)  # get существующего ключа
    cache.get(2)  # get отсутствующего ключа
    cache.set(2, 'two')  # set отсутствующего ключа
    cache.set(3, 'three')  # set отсутствующего ключа
    cache.set(4, 'four')  # set отсутствующего ключа + вытеснение (1, 'one')
    cache.get(1)  # get отсутствующего ключа
    cache.set(5, 'five')  # set отсутствующего ключа + вытеснение (2, 'two')
    cache.get(2)  # get отсутствующего ключа
    cache.set(3, 'new_three')  # set существующего ключа
    cache.set(6, 'six')  # set отсутствующего ключа + вытеснение (4, 'four')
    cache.get(4)  # get отсутствующего ключа
    cache.get(7)  # get отсутствующего ключа
