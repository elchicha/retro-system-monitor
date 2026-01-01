

class RingBuffer:
    """A circular buffer implementation with fixed size"""

    def __init__(self, max_size):
        self.max_size = max_size
        self._data = []
        self._index = 0 # Where the next item will be inserted

    def __len__(self):
        """Return number of items currently in the buffer"""
        return len(self._data)

    def append(self, item):
        """Append an item to the buffer, overwriting oldest item if full"""
        if len(self._data) < self.max_size:
            self._data.append(item)
        else:
            self._data[self._index] = item

        # Move index forward, wrap around if needed
        self._index = (self._index + 1) % self.max_size

    def get_all(self):
        """Return all items currently in the buffer in order (oldest to newest)"""
        if len(self._data) < self.max_size:
            return self._data
        return self._data[self._index:] + self._data[:self._index]
