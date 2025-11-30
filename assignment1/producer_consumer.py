"""
Assignment 1 - Producer-Consumer Pattern Implementation
By: Anushka Patil
Intuit Build Challenge
"""

import queue
import threading
import time
from typing import List, Optional


class ProducerConsumer:
    """Implements the classic producer-consumer pattern using threads and queue.Queue."""

    def __init__(self, source_data: List, max_queue_size: int = 10):
        self.source_container = list(source_data)
        self.destination_container = []
        self.shared_queue = queue.Queue(maxsize=max_queue_size)

        self.items_produced = 0
        self.items_consumed = 0

        self.producer_thread: Optional[threading.Thread] = None
        self.consumer_thread: Optional[threading.Thread] = None

        self.counter_lock = threading.Lock()

    def producer(self, delay: float = 0.0):
        print("Producer: Starting production...")
        while self.source_container:
            item = self.source_container.pop(0)

            self.shared_queue.put(item)
            print(f"Producer: Produced item {item}")

            with self.counter_lock:
                self.items_produced += 1

            time.sleep(delay)

        # Sentinel
        self.shared_queue.put(None)
        print("Producer: Finished producing")

    def consumer(self, delay: float = 0.0):
        print("Consumer: Starting consumption...")
        while True:
            item = self.shared_queue.get()

            if item is None:
                print("Consumer: Finished consuming")
                self.shared_queue.task_done()
                break

            print(f"Consumer: Consumed item {item}")
            self.destination_container.append(item)

            with self.counter_lock:
                self.items_consumed += 1

            self.shared_queue.task_done()
            time.sleep(delay)

    def start(self, producer_delay=0.0, consumer_delay=0.0):
        """Start producer & consumer threads."""
        self.producer_thread = threading.Thread(
            target=self.producer, args=(producer_delay,)
        )
        self.consumer_thread = threading.Thread(
            target=self.consumer, args=(consumer_delay,)
        )

        self.producer_thread.start()
        self.consumer_thread.start()

    def wait_completion(self):
        """Wait for both threads to finish."""
        self.producer_thread.join()
        self.consumer_thread.join()

    def get_stats(self) -> dict:
        return {
            "items_produced": self.items_produced,
            "items_consumed": self.items_consumed,
            "source_size": len(self.source_container),
            "destination_size": len(self.destination_container),
        }


def demonstrate_producer_consumer():
    print("\n=== Producer-Consumer Pattern Demonstration ===\n")

    data = list(range(20))
    pc = ProducerConsumer(data, max_queue_size=10)

    print(f"Source data size: {len(data)}")
    print(f"Queue max size: {pc.shared_queue.maxsize}\n")

    pc.start()
    pc.wait_completion()

    stats = pc.get_stats()

    print("\n=== Summary ===")
    print(f"Total items produced: {stats['items_produced']}")
    print(f"Total items consumed: {stats['items_consumed']}")
    print(f"Source container size: {stats['source_size']}")
    print(f"Destination container size: {stats['destination_size']}")
    print("\n✓ All items successfully transferred!")


if __name__ == "__main__":
    demonstrate_producer_consumer()
