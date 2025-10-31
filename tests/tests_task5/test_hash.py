import pytest
from project.task5.hash import HashTable


class TestHashTable:
    """Test cases for HashTable implementation with double hashing."""

    def test_init_default_parameters(self):
        """Test initialization with default parameters."""
        ht = HashTable()
        assert len(ht) == 0
        assert ht._capacity == 13
        assert ht._load_factor == 0.75

    def test_init_custom_parameters(self):
        """Test initialization with custom parameters."""
        ht = HashTable(initial_capacity=17, load_factor=0.6)
        assert ht._capacity == 17
        assert ht._load_factor == 0.6
        assert len(ht) == 0

    def test_init_invalid_parameters(self):
        """Test initialization with invalid parameters."""
        with pytest.raises(ValueError, match="Initial capacity must be positive"):
            HashTable(initial_capacity=0)

        with pytest.raises(ValueError, match="Load factor must be in range"):
            HashTable(load_factor=0)

        with pytest.raises(ValueError, match="Load factor must be in range"):
            HashTable(load_factor=1.5)

    def test_get_nonexistent_key(self):
        """Test getting non-existent key raises KeyError."""
        ht = HashTable()
        with pytest.raises(KeyError):
            _ = ht["nonexistent"]

    def test_contains(self):
        """Test contains operation."""
        ht = HashTable()
        ht["key"] = "value"

        assert "key" in ht
        assert "nonexistent" not in ht

    def test_delete_existing_key(self):
        """Test deleting existing key."""
        ht = HashTable()
        ht["key1"] = "value1"
        ht["key2"] = "value2"

        del ht["key1"]
        assert "key1" not in ht
        assert "key2" in ht
        assert len(ht) == 1

    def test_delete_nonexistent_key(self):
        """Test deleting non-existent key raises KeyError."""
        ht = HashTable()
        with pytest.raises(KeyError):
            del ht["nonexistent"]

    def test_clear(self):
        """Test clearing the table."""
        ht = HashTable()
        ht["key1"] = "value1"
        ht["key2"] = "value2"

        ht.clear()
        assert len(ht) == 0
        assert "key1" not in ht
        assert "key2" not in ht

    def test_iteration_and_collection_methods(self):
        """Test iteration over keys and collection methods."""
        ht = HashTable()
        test_data = {"a": 1, "b": 2, "c": 3}

        for k, v in test_data.items():
            ht[k] = v

        keys = list(ht)
        assert set(keys) == set(test_data.keys())
        assert len(keys) == len(test_data)

        assert set(ht.keys()) == set(test_data.keys())
        assert set(ht.values()) == set(test_data.values())
        assert set(ht.items()) == set(test_data.items())

    def test_get_with_default(self):
        """Test get() method with default values."""
        ht = HashTable()
        ht["key"] = "value"

        assert ht.get("key") == "value"
        assert ht.get("nonexistent") is None
        assert ht.get("nonexistent", "default") == "default"

    def test_hash_functions(self):
        """Test hash functions return valid ranges."""
        ht = HashTable(initial_capacity=10)
        key = "test_key"

        h1 = ht._hash1(key)
        h2 = ht._hash2(key)

        assert 0 <= h1 < 10
        assert 1 <= h2 < 10

    def test_probe_sequence(self):
        """Test probe sequence generation."""
        ht = HashTable(initial_capacity=5)
        key = "test_key"
        start_index = ht._hash1(key)

        sequence = list(ht._probe_sequence(key, start_index))

        assert len(sequence) == 5
        assert all(0 <= idx < 5 for idx in sequence)
        assert start_index in sequence

    def test_collision_resolution(self):
        """Test collision resolution with double hashing."""
        ht = HashTable(initial_capacity=5, load_factor=0.8)

        keys = ["a", "b", "c", "d", "e"]
        for i, key in enumerate(keys):
            ht[key] = i

        for i, key in enumerate(keys):
            assert ht[key] == i

        assert len(ht) == len(keys)

    def test_resize_operation(self):
        """Test automatic resizing when load factor is exceeded."""
        ht = HashTable(initial_capacity=5, load_factor=0.6)
        original_capacity = ht._capacity

        for i in range(4):
            ht[f"key{i}"] = i

        assert ht._capacity > original_capacity
        for i in range(4):
            assert ht[f"key{i}"] == i

    def test_deleted_slot_reuse(self):
        """Test that deleted slots are reused for new insertions."""
        ht = HashTable(initial_capacity=5)

        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3
        original_size = len(ht)

        del ht["a"]
        assert len(ht) == original_size - 1
        assert "a" not in ht
        assert "b" in ht
        assert "c" in ht

        ht["d"] = 4
        assert ht["d"] == 4
        assert len(ht) == original_size

        assert "b" in ht
        assert "c" in ht
        assert "d" in ht
        assert "a" not in ht

        ht2 = HashTable(initial_capacity=3)
        ht2["x"] = 10
        ht2["y"] = 20
        del ht2["x"]

        ht2["z"] = 30
        assert "z" in ht2
        assert ht2._size == 2

    def test_different_key_types(self):
        """Test with different key types."""
        ht = HashTable()

        test_cases = [
            ("string_key", "string_value"),
            (123, "int_value"),
            (45.67, "float_value"),
            ((1, 2), "tuple_value"),
            (frozenset([1, 2, 3]), "frozenset_value"),
        ]

        for key, value in test_cases:
            ht[key] = value
            assert ht[key] == value

        assert len(ht) == len(test_cases)

    def test_large_number_of_operations(self):
        """Test with large number of operations."""
        ht = HashTable()
        n = 100

        for i in range(n):
            ht[f"key{i}"] = i

        assert len(ht) == n

        for i in range(n):
            assert ht[f"key{i}"] == i

        for i in range(0, n, 2):
            del ht[f"key{i}"]

        assert len(ht) == n // 2

        for i in range(1, n, 2):
            assert ht[f"key{i}"] == i

    def test_repr_string(self):
        """Test string representation."""
        ht = HashTable()
        ht["a"] = 1
        ht["b"] = 2

        repr_str = repr(ht)
        assert repr_str.startswith("HashTable({")
        assert "'a': 1" in repr_str
        assert "'b': 2" in repr_str
        assert repr_str.endswith("})")

    def test_double_hashing_distribution(self):
        """Test that double hashing provides good distribution."""
        ht = HashTable(initial_capacity=11)

        keys = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
        for key in keys:
            ht[key] = len(key)

        for key in keys:
            assert ht[key] == len(key)

    def test_update_existing_key_multiple_times(self):
        """Test updating an existing key once and multiple times."""
        ht = HashTable()

        ht["key"] = "value1"
        ht["key"] = "value2"
        assert ht["key"] == "value2"
        assert len(ht) == 1

        ht["counter"] = 0
        for i in range(1, 6):
            ht["counter"] = i
            assert ht["counter"] == i
        assert len(ht) == 2

    def test_resize_exact_load_factor(self):
        """Test resize when load factor is exactly reached."""
        ht = HashTable(initial_capacity=4, load_factor=0.75)

        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3

        assert ht._capacity > 4
        assert len(ht) == 3

    def test_full_table_with_only_deleted_slots(self):
        """Test behavior when table is full but only with DELETED markers."""
        ht = HashTable(initial_capacity=3, load_factor=0.99)

        ht["a"] = 1
        ht["b"] = 2
        ht["c"] = 3
        del ht["a"]
        del ht["b"]
        del ht["c"]

        assert len(ht) == 0
        ht["d"] = 4
        assert ht["d"] == 4

    def test_resize_preserves_deleted_slots_behavior(self):
        """Test that resize doesn't break deleted slots logic."""
        ht = HashTable(initial_capacity=4, load_factor=0.6)

        ht["a"] = 1
        ht["b"] = 2
        del ht["a"]

        ht["c"] = 3
        ht["d"] = 4

        ht["e"] = 5
        assert ht["e"] == 5
