from collections.abc import MutableMapping
from typing import Any, Optional, Iterator, List, Tuple, Union, MutableSequence, cast
from multiprocessing import Manager
from multiprocessing.managers import SyncManager
import threading

Entry = Union[None, Tuple[Any, Any], object]


class MPHashTable(MutableMapping):
    """
    Thread-safe hash table with open addressing and double hashing for collision resolution.

    Uses multiprocessing.Manager for shared state between processes.
    All operations are protected by locks to prevent race conditions.

    Attributes:
        _capacity: Current capacity of the internal table
        _load_factor: Load factor threshold for triggering resizing
        _table: Internal array for storing key-value pairs
        _size: Number of elements in the table
        _DELETED: Special marker for deleted entries
        _lock: Lock for thread synchronization
    """

    _DELETED = object()
    _shared_manager: Optional[SyncManager] = None

    @classmethod
    def get_manager(cls) -> SyncManager:
        """
        Get or create shared Manager instance.

        Returns:
            SyncManager: Shared manager for multiprocessing
        """
        if cls._shared_manager is None:
            cls._shared_manager = Manager()
        return cls._shared_manager

    def __init__(
        self,
        initial_capacity: int = 13,
        load_factor: float = 0.75,
        manager: Optional[SyncManager] = None,
    ) -> None:
        """
        Initialize the thread-safe hash table.

        Args:
            initial_capacity: Initial table capacity. Must be positive.
            load_factor: Load factor for determining when to resize.
                        Must be in range (0, 1).
            manager: Optional existing Manager instance for shared state

        Raises:
            ValueError: If initial_capacity <= 0 or load_factor not in (0, 1).
        """
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        if not 0 < load_factor < 1:
            raise ValueError("Load factor must be in range (0, 1)")

        if manager is None:
            manager = self.get_manager()

        self._manager = manager

        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._table_typed = cast(
            MutableSequence[Entry], manager.list([None] * initial_capacity)
        )
        self._size = 0
        self._lock = manager.RLock()

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

        for i in range(self._capacity):
            index = (start_index + i * self._hash2(key)) % self._capacity
            item = self._table_typed[index]

            if item is None:
                return (first_deleted, False) if first_deleted != -1 else (index, False)
            elif item is self._DELETED:
                if first_deleted == -1:
                    first_deleted = index
            elif isinstance(item, tuple) and item[0] == key:
                return (index, True)

        return (first_deleted, False) if first_deleted != -1 else (0, False)

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
        old_table = list(self._table_typed)
        old_capacity = self._capacity

        self._capacity = new_capacity
        self._table_typed[:] = [None] * new_capacity
        self._size = 0

        for item in old_table:
            if item is not None and item is not self._DELETED:
                if isinstance(item, tuple):
                    key, value = item
                    self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set key to value. Update value if key already exists.

        Args:
            key: Key to set or update
            value: Value to associate with the key
        """
        with self._lock:
            self._resize_if_needed()

            index: int
            found: bool
            index, found = self._find_index(key)

            if found:
                self._table_typed[index] = (key, value)
            else:
                if (
                    self._table_typed[index] is not None
                    and self._table_typed[index] is not self._DELETED
                ):
                    self._resize(self._capacity * 2 + 1)
                    index, found = self._find_index(key)
                    self._table_typed[index] = (key, value)
                    self._size += 1
                else:
                    self._table_typed[index] = (key, value)
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
        with self._lock:
            index: int
            found: bool
            index, found = self._find_index(key)

            if not found:
                raise KeyError(key)

            item = self._table_typed[index]
            if isinstance(item, tuple):
                return item[1]
            raise RuntimeError("Invalid table state")

    def __delitem__(self, key: Any) -> None:
        """
        Delete key-value pair from the table.

        Args:
            key: Key to delete

        Raises:
            KeyError: If key is not found
        """
        with self._lock:
            index: int
            found: bool
            index, found = self._find_index(key)

            if not found:
                raise KeyError(key)

            self._table_typed[index] = self._DELETED
            self._size -= 1

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exists in the table.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        with self._lock:
            _, found = self._find_index(key)
            return found

    def __iter__(self) -> Iterator[Any]:
        """
        Return iterator over all keys in the table.

        Yields:
            Iterator of all keys
        """
        with self._lock:
            for item in self._table_typed:
                if item is not None and item is not self._DELETED:
                    if isinstance(item, tuple):
                        yield item[0]

    def __len__(self) -> int:
        """
        Return number of elements in the table.

        Returns:
            Number of key-value pairs
        """
        with self._lock:
            return self._size

    def __repr__(self) -> str:
        """
        Return string representation of the table.

        Returns:
            String representation in dictionary format
        """
        with self._lock:
            items: List[str] = []
            for key in self:
                items.append(f"{key!r}: {self[key]!r}")
            return "MPHashTable({" + ", ".join(items) + "})"

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
        with self._lock:
            self._table_typed[:] = [None] * self._capacity
            self._size = 0

    @property
    def capacity(self) -> int:
        """Get current capacity (for testing purposes)."""
        return self._capacity
