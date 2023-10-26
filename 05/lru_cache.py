def _create_error_message(name: str, type: str) -> str:
    return f"\'{name}\' should be {type}"


class ListNode:
    def __init__(self, key: str, value: any) -> None:
        if not isinstance(key, str):
            raise TypeError(_create_error_message(name="key", type="str"))
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class LRUCache:
    def __init__(self, limit: int) -> None:
        if not isinstance(limit, int) or limit <= 0:
            raise TypeError(_create_error_message(name="limit", type="positive int"))
        self.limit = limit
        self.newest = ListNode("newest", "newest")
        self.oldest = ListNode("oldest", "oldest")
        self.newest.prev = self.oldest
        self.oldest.next = self.newest
        self.cache = {}

    def get(self, key: str) -> any:
        if not isinstance(key, str):
            raise TypeError(_create_error_message(name="key", type="str"))
        if key not in self.cache:
            return None
        self._delete(self.cache[key])
        self._insert(self.cache[key])
        return self.cache[key].value

    def _insert(self, node: 'ListNode'):
        prev_newest, newest = self.newest.prev, self.newest
        prev_newest.next = node
        node.prev = prev_newest
        newest.prev = node
        node.next = newest

    def _delete(self, node: 'ListNode'):
        prev_node, next_node = node.prev, node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def set(self, key: str, value: any) -> None:
        if not isinstance(key, str):
            raise TypeError(_create_error_message(name="key", type="str"))
        if key in self.cache:
            self._delete(self.cache[key])
        self.cache[key] = ListNode(key, value)
        self._insert(self.cache[key])

        if len(self.cache) > self.limit:
            for_delete = self.oldest.next
            self._delete(for_delete)
            del self.cache[for_delete.key]
