from collections.abc import MutableMapping
from typing import Any, Optional, Iterator, List, Tuple


class HashTable(MutableMapping):
    """
    Hash table with open addressing and double hashing for collision resolution.

    Implements MutableMapping interface, providing dictionary-like functionality.
    Uses double hashing for probe sequence generation.

    Attributes:
        _capacity: Current capacity of the internal table
        _load_factor: Load factor threshold for triggering resizing
        _table: Internal array for storing key-value pairs
        _size: Number of elements in the table
        _DELETED: Special marker for deleted entries
    """

    _DELETED = object()

    def __init__(self, initial_capacity: int = 13, load_factor: float = 0.75) -> None:
        """
        Initialize the hash table.

        Args:
            initial_capacity: Initial table capacity. Must be positive.
            load_factor: Load factor for determining when to resize.
                        Must be in range (0, 1).

        Raises:
            ValueError: If initial_capacity <= 0 or load_factor not in (0, 1).
        """
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        if not 0 < load_factor < 1:
            raise ValueError("Load factor must be in range (0, 1)")

        self._capacity: int = initial_capacity
        self._load_factor: float = load_factor
        self._table: List[Optional[Tuple[Any, Any] | object]] = [None] * self._capacity
        self._size: int = 0

    def _hash1(self, key: Any) -> int:
        """
        Compute primary hash value for key.

        Args:
            key: Key to hash

        Returns:
            Primary hash index in range [0, capacity-1]
        """
        return hash(key) % self._capacity

    def _hash2(self, key: Any) -> int:
        """
        Compute secondary hash value for double hashing.

        Ensures the step size is never 0 and relatively prime to table capacity.

        Args:
            key: Key to hash

        Returns:
            Secondary hash value in range [1, capacity-1]
        """
        return 1 + (hash(key) % (self._capacity - 1))

    def _probe_sequence(self, key: Any, start_index: int) -> Iterator[int]:
        """
        Generate probe sequence using double hashing.

        Args:
            key: Key to generate probe sequence for
            start_index: Starting index for the probe sequence

        Yields:
            Sequence of indices to probe: (h1 + i * h2) % capacity
        """
        hash2: int = self._hash2(key)
        index: int = start_index

        for i in range(self._capacity):
            yield index
            index = (index + hash2) % self._capacity

    def _find_index(self, key: Any) -> Tuple[int, bool]:
        """
        Find index for key in the table using double hashing.

        Args:
            key: Key to find

        Returns:
            Tuple of (index, found) where:
            - index: Slot index in the table
            - found: True if key exists, False otherwise
        """
        start_index: int = self._hash1(key)
        first_deleted: int = -1

        for i, index in enumerate(self._probe_sequence(key, start_index)):
            if i >= self._capacity:
                break
            item = self._table[index]

            if item is None:
                return (first_deleted, False) if first_deleted != -1 else (index, False)
            elif item is self._DELETED:
                if first_deleted == -1:
                    first_deleted = index
            elif item[0] == key:
                return (index, True)

        if first_deleted != -1:
            return (first_deleted, False)

        for i in range(self._capacity):
            if self._table[i] is None:
                return (i, False)

        self._resize(self._capacity * 2 + 1)
        return self._find_index(key)

    def _resize_if_needed(self) -> None:
        """Check if table needs to be resized based on load factor."""
        if (self._size + 1) / self._capacity >= self._load_factor:
            self._resize(self._capacity * 2 + 1)

    def _resize(self, new_capacity: int) -> None:
        """
        Resize the table and rehash all elements.

        Args:
            new_capacity: New table capacity
        """
        old_table: List[Optional[Tuple[Any, Any] | object]] = self._table
        old_capacity: int = self._capacity

        self._capacity = new_capacity
        self._table = [None] * self._capacity
        self._size = 0

        for item in old_table:
            if item is not None and item is not self._DELETED:
                key, value = item
                self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set key to value. Update value if key already exists.

        Args:
            key: Key to set or update
            value: Value to associate with the key
        """
        self._resize_if_needed()

        index: int
        found: bool
        index, found = self._find_index(key)

        if found:
            self._table[index] = (key, value)
        else:
            self._table[index] = (key, value)
            self._size += 1

    def __getitem__(self, key: Any) -> Any:
        """
        Return value associated with key.

        Args:
            key: Key to search for

        Returns:
            Value associated with the key

        Raises:
            KeyError: If key is not found
        """
        index: int
        found: bool
        index, found = self._find_index(key)

        if not found:
            raise KeyError(key)

        return self._table[index][1]

    def __delitem__(self, key: Any) -> None:
        """
        Delete key-value pair from the table.

        Args:
            key: Key to delete

        Raises:
            KeyError: If key is not found
        """
        index: int
        found: bool
        index, found = self._find_index(key)

        if not found:
            raise KeyError(key)

        self._table[index] = self._DELETED
        self._size -= 1

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exists in the table.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        _, found = self._find_index(key)
        return found

    def __iter__(self) -> Iterator[Any]:
        """
        Return iterator over all keys in the table.

        Yields:
            Iterator of all keys
        """
        for item in self._table:
            if item is not None and item is not self._DELETED:
                yield item[0]

    def __len__(self) -> int:
        """
        Return number of elements in the table.

        Returns:
            Number of key-value pairs
        """
        return self._size

    def __repr__(self) -> str:
        """
        Return string representation of the table.

        Returns:
            String representation in dictionary format
        """
        items: List[str] = []
        for key in self:
            items.append(f"{key!r}: {self[key]!r}")
        return "HashTable({" + ", ".join(items) + "})"

    def keys(self) -> List[Any]:
        """
        Return list of all keys in the table.

        Returns:
            List of all keys
        """
        return [key for key in self]

    def values(self) -> List[Any]:
        """
        Return list of all values in the table.

        Returns:
            List of all values
        """
        return [self[key] for key in self]

    def items(self) -> List[Tuple[Any, Any]]:
        """
        Return list of all key-value pairs in the table.

        Returns:
            List of all (key, value) pairs
        """
        return [(key, self[key]) for key in self]

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Return value for key, or default if key not found.

        Args:
            key: Key to search for
            default: Default value to return if key not found

        Returns:
            Value if key exists, default otherwise
        """
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        """Remove all elements from the table."""
        self._table = [None] * self._capacity
        self._size = 0
