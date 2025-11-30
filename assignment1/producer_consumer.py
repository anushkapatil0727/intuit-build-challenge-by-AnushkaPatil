"""
Assignment 1 - Producer-Consumer Pattern Implementation
By Anushka Patil
Intuit Build Challenge - This assignment demonstrates how multithreading works in Python by implementing the classic Producer Consumer problem. The goal is to show controlled data sharing between two threads using a thread-safe queue.
"""

import queue          # it Provides a thread-safe FIFO queue used for communication between threads
import threading      # it is used to create and manage separate producer and consumer threads
import time           # it is used for optional delays to simulate real-world processing time
from typing import List, Optional


class ProducerConsumer:
    """
    This class encapsulates the full producer–consumer logic.
    It uses: A shared queue (buffer), A producer thread that creates items, A consumer thread that processes items, Locks for safe updates to shared counters
    """

    def __init__(self, source_data: List, max_queue_size: int = 10):
        """
        Constructor initializes all required data structures.

        source_data: The initial list of items that the producer will process.
        max_queue_size: Maximum number of items allowed in the shared queue at once.

        We convert source_data into a standalone list to avoid modifying the original.
        """
        self.source_container = list(source_data)  # this will Input data that producer will push into the queue
        self.destination_container = []            # Where the consumer stores processed items
        self.shared_queue = queue.Queue(maxsize=max_queue_size)  # Thread-safe queue acting as the buffer

        self.items_produced = 0     # Its the counter for how many items producer created
        self.items_consumed = 0     # Counter for how many items consumer processed

        # These will store the actual Thread objects once started
        self.producer_thread: Optional[threading.Thread] = None
        self.consumer_thread: Optional[threading.Thread] = None

        # A lock ensures increments to counters are safe when accessed by multiple threads
        self.counter_lock = threading.Lock()

    def producer(self, delay: float = 0.0):
        """
        The producer thread:
        1. Pulls items from source_container
        2. Pushes them into the shared queue
        3. it optionally sleeps to simulate slower production

        When done, the producer sends a sentinel value (None) to signal the consumer to stop.
        """
        print("Producer: Starting production...")

        while self.source_container:
            # it takes the next item from the source list
            item = self.source_container.pop(0)

            # it puts the item into the shared queue (this blocks if queue is full)
            self.shared_queue.put(item)
            print(f"Producer: Produced item {item}")

            # this will update production count safely
            with self.counter_lock:
                self.items_produced += 1

            time.sleep(delay)  # Optional delay to mimic real production time

        # After producing all items, send a sentinel value to tell consumer “this is the end”
        self.shared_queue.put(None)
        print("Producer: Finished producing")

    def consumer(self, delay: float = 0.0):
        """
        The consumer thread: Continuously takes items from the shared queue, Processes (here: appends to destination_container, Stops when it receives the sentinel value (None)
        """
        print("Consumer: Starting consumption...")

        while True:
            # it will retrieve next item (blocks until something is available)
            item = self.shared_queue.get()

            # If producer sends sentinel, we break the loop and finish
            if item is None:
                print("Consumer: Finished consuming")
                self.shared_queue.task_done()
                break

            # "Process" the item, here we simply store it
            print(f"Consumer: Consumed item {item}")
            self.destination_container.append(item)

            # Safely update consumer count
            with self.counter_lock:
                self.items_consumed += 1

            # Mark the item as processed
            self.shared_queue.task_done()
            time.sleep(delay)

    def start(self, producer_delay=0.0, consumer_delay=0.0):
        """
        Starts both producer and consumer threads. This simply creates the threads and starts running them.
        """
        self.producer_thread = threading.Thread(
            target=self.producer, args=(producer_delay,)
        )
        self.consumer_thread = threading.Thread(
            target=self.consumer, args=(consumer_delay,)
        )

        # Begin thread execution
        self.producer_thread.start()
        self.consumer_thread.start()

    def wait_completion(self):
        """
        Joins both threads. This ensures the main program waits until both threads fully finish before moving forward.
        """
        self.producer_thread.join()
        self.consumer_thread.join()

    def get_stats(self) -> dict:
        """
        Returns a summary of how many items were produced and consumed. I used this practice for debugging and verifying correctness.
        """
        return {
            "items_produced": self.items_produced,
            "items_consumed": self.items_consumed,
            "source_size": len(self.source_container),
            "destination_size": len(self.destination_container),
        }


def demonstrate_producer_consumer():
    """
    This function demonstrates the full producer–consumer workflow.
    It:Creates a dataset, Initializes the class, Starts the threads, Waits for completion and Prints a summary
    """
    print("\n=== Producer-Consumer Pattern Demonstration ===\n")

    # Dummy dataset (0–19) for production
    data = list(range(20))

    # this create the ProducerConsumer system with queue size of 10
    pc = ProducerConsumer(data, max_queue_size=10)

    print(f"Source data size: {len(data)}")
    print(f"Queue max size: {pc.shared_queue.maxsize}\n")

    # Start producer and consumer threads
    pc.start()

    # Wait until both threads complete execution
    pc.wait_completion()

    # Retrieve final statistics
    stats = pc.get_stats()

    print("\n=== Summary ===")
    print(f"Total items produced: {stats['items_produced']}")
    print(f"Total items consumed: {stats['items_consumed']}")
    print(f"Source container size: {stats['source_size']}")
    print(f"Destination container size: {stats['destination_size']}")
    print("\n✓ All items successfully transferred!")


# it will run the demonstration only when this file is executed directly
if __name__ == "__main__":
    demonstrate_producer_consumer()
