import time

class LeakyBucket:
    """Implements the Leaky Bucket algorithm for rate limiting."""
    
    def __init__(self, capacity: int, leak_rate: float):
        """
        :param capacity: The maximum number of messages the bucket can hold.
        :param leak_rate: The number of messages that "leak" (are processed) per second.
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self._current_level = 0.0
        self._last_leak_time = time.time()

    def _leak(self):
        """Internal method to simulate the 'leaking' of messages over time."""
        now = time.time()
        time_elapsed = now - self._last_leak_time
        leaked_amount = time_elapsed * self.leak_rate
        
        self._current_level = max(0, self._current_level - leaked_amount)
        self._last_leak_time = now

    def add_message(self, amount: int = 1) -> bool:
        """
        Tries to add a message to the bucket.
        :param amount: The 'size' of the message (default is 1).
        :return: True if the message was added, False if the bucket is full (spam).
        """
        self._leak()
        
        if self._current_level + amount <= self.capacity:
            self._current_level += amount
            return True
        else:
            return False