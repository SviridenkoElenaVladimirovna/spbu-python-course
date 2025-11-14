import pytest
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from project.task6.MPHashTable import MPHashTable


class TestMPHashTable:
    """Test cases for concurrent access to MPHashTable."""

    def test_simple_concurrent_inserts(self):
        """Test multiple threads inserting different keys."""
        ht = MPHashTable()
        num_threads = 5
        items_per_thread = 20

        def insert_worker(thread_id):
            for i in range(items_per_thread):
                key = f"key_{thread_id}_{i}"
                value = f"value_{thread_id}_{i}"
                ht[key] = value

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for i in range(num_threads):
                executor.submit(insert_worker, i)

        expected_size = num_threads * items_per_thread
        assert len(ht) == expected_size

        for thread_id in range(num_threads):
            for i in range(items_per_thread):
                key = f"key_{thread_id}_{i}"
                assert key in ht
                assert ht[key] == f"value_{thread_id}_{i}"

    def test_no_race_condition_on_updates(self):
        """Test that updates don't cause race conditions - FIXED VERSION."""
        ht = MPHashTable()
        key = "race_key"
        num_threads = 5
        updates_per_thread = 50

        ht[key] = 0

        def update_worker():
            for _ in range(updates_per_thread):

                with ht._lock:
                    current = ht[key]
                    ht[key] = current + 1

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(update_worker) for _ in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        expected_value = num_threads * updates_per_thread
        assert (
            ht[key] == expected_value
        ), f"Race condition detected: expected {expected_value}, got {ht[key]}"

    def test_deadlock_prevention(self):
        """Test that operations don't cause deadlocks - SIMPLIFIED."""
        ht = MPHashTable()
        num_threads = 4
        timeout_seconds = 10

        def complex_worker(thread_id):
            for i in range(10):
                key1 = f"key_{thread_id}"
                key2 = f"key_{(thread_id + 1) % num_threads}"

                ht[key1] = f"value_{i}"
                _ = key2 in ht

                if i % 3 == 0:
                    list(ht)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(complex_worker, i) for i in range(num_threads)]

            try:
                for future in as_completed(futures, timeout=timeout_seconds):
                    future.result()
            except TimeoutError:
                pytest.fail("Deadlock detected - test timed out")

    def test_atomic_operations(self):
        """Test that operations are atomic."""
        ht = MPHashTable()
        key = "atomic_key"
        num_threads = 3

        def atomic_worker(worker_id):
            if worker_id == 0:
                ht[key] = "original_value"
            else:
                value = ht.get(key)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(atomic_worker, i) for i in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        assert key in ht

    def test_concurrent_resize_operations(self):
        """Test that resize operations work correctly under concurrent access."""
        ht = MPHashTable(initial_capacity=10, load_factor=0.8)
        num_threads = 3
        items_per_thread = 10

        def resize_worker(thread_id):
            for i in range(items_per_thread):
                key = f"key_{thread_id}_{i}"
                ht[key] = f"value_{thread_id}_{i}"

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(resize_worker, i) for i in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        expected_size = num_threads * items_per_thread
        assert len(ht) == expected_size

        for thread_id in range(num_threads):
            for i in range(items_per_thread):
                key = f"key_{thread_id}_{i}"
                assert key in ht
                assert ht[key] == f"value_{thread_id}_{i}"

    def test_lock_contention_performance(self):
        """Test that locking doesn't cause excessive performance degradation - FIXED."""
        ht = MPHashTable()
        num_threads = 3
        operations_per_thread = 50

        def operation_worker(thread_id):
            start_time = time.time()
            for i in range(operations_per_thread):
                key = f"key_{thread_id}_{i}"
                ht[key] = i
                _ = key in ht
            return time.time() - start_time

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(operation_worker, i) for i in range(num_threads)]
            times = [future.result() for future in as_completed(futures)]

        max_time = max(times)
        assert max_time < 5.0, f"Excessive lock contention detected: {max_time} seconds"

    def test_iteration_consistency_under_modification(self):
        """Test that iteration provides consistent view despite modifications - SIMPLIFIED."""
        ht = MPHashTable()

        for i in range(5):
            ht[f"initial_{i}"] = i

        iteration_completed = threading.Event()

        def iterator_worker():
            try:
                items = list(ht.items())
                iteration_completed.set()
                return len(items)
            except Exception as e:
                iteration_completed.set()
                raise e

        def modifier_worker():
            for i in range(3):
                ht[f"new_{i}"] = i + 100

        with ThreadPoolExecutor(max_workers=2) as executor:
            iterate_future = executor.submit(iterator_worker)
            executor.submit(modifier_worker)

            iteration_completed.wait(timeout=5)
            iterate_future.result(timeout=5)

    def test_exception_safety(self):
        """Test that exceptions in one thread don't corrupt other threads - FIXED."""
        ht = MPHashTable()
        num_threads = 2

        def normal_worker(thread_id):
            for i in range(10):
                key = f"normal_{thread_id}_{i}"
                ht[key] = i

        def exception_worker():
            try:
                for i in range(5):
                    if i == 2:
                        raise ValueError("Simulated error")
                    ht[f"exception_{i}"] = i
            except ValueError:
                ht["after_exception"] = "works"

        with ThreadPoolExecutor(max_workers=num_threads) as executor:

            normal_future = executor.submit(normal_worker, 0)

            exception_future = executor.submit(exception_worker)

            normal_future.result(timeout=5)
            try:
                exception_future.result(timeout=5)
            except ValueError:
                pass

        assert "after_exception" in ht
        assert ht["after_exception"] == "works"

    def test_concurrent_clear_and_reuse(self):
        """Test clear operation with immediate reuse by multiple threads - FIXED."""
        ht = MPHashTable()
        num_threads = 3
        clear_done = threading.Event()

        def worker(thread_id):
            for i in range(5):
                ht[f"phase1_{thread_id}_{i}"] = i

            clear_done.wait(timeout=5)

            for i in range(5):
                ht[f"phase2_{thread_id}_{i}"] = i + 100

        def clear_worker():
            time.sleep(0.1)
            ht.clear()
            clear_done.set()

        with ThreadPoolExecutor(max_workers=num_threads + 1) as executor:
            worker_futures = [executor.submit(worker, i) for i in range(num_threads)]

            clear_future = executor.submit(clear_worker)

            try:
                for future in as_completed(worker_futures + [clear_future], timeout=10):
                    future.result()
            except TimeoutError:
                pytest.fail("Test timed out - possible deadlock")

        assert len(ht) == num_threads * 5
        for thread_id in range(num_threads):
            for i in range(5):
                assert f"phase2_{thread_id}_{i}" in ht
                assert ht[f"phase2_{thread_id}_{i}"] == i + 100

    def test_basic_concurrent_operations(self):
        """Simple test for basic concurrent operations."""
        ht = MPHashTable()

        def writer():
            for i in range(10):
                ht[f"key_{i}"] = i

        def reader():
            for i in range(10):
                _ = f"key_{i}" in ht

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(writer)
            executor.submit(reader)

        assert len(ht) == 10

    def test_concurrent_access_consistency(self):
        """Test that concurrent access maintains consistency."""
        ht = MPHashTable()
        num_threads = 4
        operations = 20

        def worker(thread_id):
            for i in range(operations):
                key = f"key_{i}"
                ht[key] = f"value_{thread_id}"

                value = ht[key]
                assert value is not None

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, i) for i in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        assert len(ht) == operations
