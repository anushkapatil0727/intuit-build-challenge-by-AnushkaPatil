"""
Unit tests for Producer-Consumer Pattern Implementation
"""

import pytest
import time
from assignment1.producer_consumer import ProducerConsumer


class TestProducerConsumer:
    """Test suite for ProducerConsumer class"""
    
    def test_basic_producer_consumer(self):
        """Test basic producer-consumer with small dataset"""
        source_data = list(range(10))
        pc = ProducerConsumer(source_data, max_queue_size=5)
        
        pc.start(producer_delay=0.001, consumer_delay=0.001)
        pc.wait_completion()
        
        stats = pc.get_stats()
        
        assert stats['items_produced'] == 10
        assert stats['items_consumed'] == 10
        assert stats['destination_size'] == 10
        assert pc.destination_container == list(range(10))

    def test_order_preservation(self):
        """Test that items are consumed in the same order they were produced"""
        source_data = list(range(20))
        pc = ProducerConsumer(source_data, max_queue_size=5)
        
        pc.start()
        pc.wait_completion()
        
        assert pc.destination_container == list(range(20))
    
    def test_empty_source(self):
        """Test producer-consumer with empty source"""
        source_data = []
        pc = ProducerConsumer(source_data, max_queue_size=5)
        
        pc.start()
        pc.wait_completion()
        
        stats = pc.get_stats()
        
        assert stats['items_produced'] == 0
        assert stats['items_consumed'] == 0
        assert stats['destination_size'] == 0
    
    def test_single_item(self):
        """Test producer-consumer with single item"""
        source_data = [42]
        pc = ProducerConsumer(source_data, max_queue_size=1)
        
        pc.start()
        pc.wait_completion()
        
        assert pc.destination_container == [42]
        assert pc.get_stats()['items_consumed'] == 1
    
    def test_large_dataset(self):
        """Test producer-consumer with larger dataset"""
        source_data = list(range(100))
        pc = ProducerConsumer(source_data, max_queue_size=10)
        
        pc.start()
        pc.wait_completion()
        
        stats = pc.get_stats()
        
        assert stats['items_produced'] == 100
        assert stats['items_consumed'] == 100
        assert len(pc.destination_container) == 100
    
    def test_slow_consumer(self):
        """Test with slow consumer (consumer slower than producer)"""
        source_data = list(range(30))
        pc = ProducerConsumer(source_data, max_queue_size=5)
        
        pc.start(producer_delay=0.001, consumer_delay=0.005)
        pc.wait_completion()
        
        assert pc.destination_container == list(range(30))
    
    def test_slow_producer(self):
        """Test with slow producer (producer slower than consumer)"""
        source_data = list(range(30))
        pc = ProducerConsumer(source_data, max_queue_size=5)
        
        pc.start(producer_delay=0.005, consumer_delay=0.001)
        pc.wait_completion()
        
        assert pc.destination_container == list(range(30))
    
    def test_queue_blocking_behavior(self):
        """Test that queue properly blocks when full"""
        source_data = list(range(50))
        pc = ProducerConsumer(source_data, max_queue_size=3)
        
        pc.start(producer_delay=0.0001, consumer_delay=0.01)
        
        time.sleep(0.05)
        
        queue_size = pc.shared_queue.qsize()
        assert queue_size <= 3
        
        pc.wait_completion()
        
        assert pc.get_stats()['items_consumed'] == 50
    
    def test_thread_safety(self):
        """Test that counter increments happen safely"""
        source_data = list(range(100))
        pc = ProducerConsumer(source_data)
        
        pc.start(producer_delay=0.0001, consumer_delay=0.0001)
        pc.wait_completion()
        
        assert pc.items_produced == len(pc.destination_container)
        assert pc.items_consumed == len(pc.destination_container)
    
    def test_string_data(self):
        """Test with string inputs"""
        source_data = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']
        pc = ProducerConsumer(source_data, max_queue_size=3)
        
        pc.start()
        pc.wait_completion()
        
        assert pc.destination_container == source_data
        assert pc.get_stats()['items_consumed'] == 5
    
    def test_mixed_data_types(self):
        """Test with mixed data types"""
        source_data = [1, 'two', 3.0, {'four': 4}, [5, 5], True]
        pc = ProducerConsumer(source_data)
        
        pc.start()
        pc.wait_completion()
        
        assert pc.destination_container == source_data
        assert pc.get_stats()['items_consumed'] == len(source_data)
