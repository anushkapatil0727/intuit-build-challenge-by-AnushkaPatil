"""
this is a program for Unit tests for Producer-Consumer Pattern Implementation - This file contains a full pytest test suite to verify that the ProducerConsumer class
behaves correctly under different conditions. Each test focuses on a specific behavior like ordering, thread safety,queue behavior, handling of delays, 
and correct movement of items.
"""

import pytest
import time
from assignment1.producer_consumer import ProducerConsumer


class TestProducerConsumer:
    #this class test suite for the ProducerConsumer class.

    def test_basic_producer_consumer(self):
        """
        Basic test to verify the normal workflow:Producer should produce all items, Consumer should consume all items, it Output list should contain everything.
        This acts as a sanity check for the core logic.
        """
        source_data = list(range(10))  # Small dataset from 0 to 9
        pc = ProducerConsumer(source_data, max_queue_size=5)

        # Start both producer and consumer with tiny delays to simulate processing time
        pc.start(producer_delay=0.001, consumer_delay=0.001)
        pc.wait_completion()

        stats = pc.get_stats()

        # Verify that all items moved properly through the system
        assert stats['items_produced'] == 10
        assert stats['items_consumed'] == 10
        assert stats['destination_size'] == 10
        assert pc.destination_container == list(range(10))

    def test_order_preservation(self):
        """
        it Ensures that the consumer receives items in the exact same order as produced. FIFO behavior must remain consistent because the queue
        should not reorder anything.
        """
        source_data = list(range(20))
        pc = ProducerConsumer(source_data, max_queue_size=5)

        pc.start()
        pc.wait_completion()

        assert pc.destination_container == list(range(20))

    def test_empty_source(self):
        """
        it verifies behavior when no items are provided at all.
        the Producer should produce nothing, and consumer should finish immediately.
        """
        source_data = []
        pc = ProducerConsumer(source_data, max_queue_size=5)

        pc.start()
        pc.wait_completion()

        stats = pc.get_stats()

        assert stats['items_produced'] == 0
        assert stats['items_consumed'] == 0
        assert stats['destination_size'] == 0

    def test_single_item(self):
        
        # this tests the simplest non-empty case. It also ensures that the system correctly handles a single item and properly transfers it through the queue.
    
        source_data = [42]
        pc = ProducerConsumer(source_data, max_queue_size=1)

        pc.start()
        pc.wait_completion()

        assert pc.destination_container == [42]
        assert pc.get_stats()['items_consumed'] == 1

    def test_large_dataset(self):
        
        #Test scalability and correctness with a larger dataset. It ensures that no items are lost or duplicated, even under high load.
        
        source_data = list(range(100))
        pc = ProducerConsumer(source_data, max_queue_size=10)

        pc.start()
        pc.wait_completion()

        stats = pc.get_stats()

        assert stats['items_produced'] == 100
        assert stats['items_consumed'] == 100
        assert len(pc.destination_container) == 100

    def test_slow_consumer(self):
        """
        Tests behavior where the consumer is intentionally slower than the producer. This should cause the queue to fill up, forcing the producer to block temporarily.
        The final output order and item count should still be correct.
        """
        source_data = list(range(30))
        pc = ProducerConsumer(source_data, max_queue_size=5)

        pc.start(producer_delay=0.001, consumer_delay=0.005)
        pc.wait_completion()

        assert pc.destination_container == list(range(30))

    def test_slow_producer(self):
        """
        Opposite of the previous test: here the producer is slower than the consumer.
        Consumer should end up waiting for items, but final output must still match.
        """
        source_data = list(range(30))
        pc = ProducerConsumer(source_data, max_queue_size=5)

        pc.start(producer_delay=0.005, consumer_delay=0.001)
        pc.wait_completion()

        assert pc.destination_container == list(range(30))

    def test_queue_blocking_behavior(self):
        """
        Tests queue's blocking behavior:
        first, Small queue size (3)
        second, Fast producer, slow consumer
        The queue should never exceed its max capacity. This verifies that put() correctly blocks when the queue is full.
        """
        source_data = list(range(50))
        pc = ProducerConsumer(source_data, max_queue_size=3)

        pc.start(producer_delay=0.0001, consumer_delay=0.01)

        # Give some time for producer/consumer to start operating
        time.sleep(0.05)

        # this check that queue never exceeds maximum allowed size
        queue_size = pc.shared_queue.qsize()
        assert queue_size <= 3

        pc.wait_completion()

        assert pc.get_stats()['items_consumed'] == 50

    def test_thread_safety(self):
        """
        Ensures that increments to counters (items_produced/items_consumed) are thread-safe and reflect actual number of processed items.
        Also Lock the usage inside the class should guarantee this.
        """
        source_data = list(range(100))
        pc = ProducerConsumer(source_data)

        pc.start(producer_delay=0.0001, consumer_delay=0.0001)
        pc.wait_completion()

        assert pc.items_produced == len(pc.destination_container)
        assert pc.items_consumed == len(pc.destination_container)

    def test_string_data(self):
        """
        Verifies that the system works with string inputs as well.
        The logic should be fully data-type agnostic.
        """
        source_data = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']
        pc = ProducerConsumer(source_data, max_queue_size=3)

        pc.start()
        pc.wait_completion()

        assert pc.destination_container == source_data
        assert pc.get_stats()['items_consumed'] == 5

    def test_mixed_data_types(self):
        """
        Tests handling of mixed data types:integers, strings, floats, dicts, lists, booleans.
        this Queue-based designs should not care about the item type.
        """
        source_data = [1, 'two', 3.0, {'four': 4}, [5, 5], True]
        pc = ProducerConsumer(source_data)

        pc.start()
        pc.wait_completion()

        assert pc.destination_container == source_data
        assert pc.get_stats()['items_consumed'] == len(source_data)
