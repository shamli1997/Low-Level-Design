# In-Memory Message Queue with Strategy and Observer Patterns

import threading
import time
import random
from collections import defaultdict
from abc import ABC, abstractmethod

# ========== Message ==========
class Message:
    def __init__(self, content):
        self.content = content


# ========== Strategy Pattern for Publishing ==========
class PublishStrategy(ABC):
    @abstractmethod
    def choose_partition(self, topic):
        pass

class RandomPartitionStrategy(PublishStrategy):
    def choose_partition(self, topic):
        return random.choice(topic.partitions)

class RoundRobinPartitionStrategy(PublishStrategy):
    def __init__(self):
        self.counter = defaultdict(int)

    def choose_partition(self, topic):
        idx = self.counter[topic.name] % len(topic.partitions)
        self.counter[topic.name] += 1
        return topic.partitions[idx]


# ========== Topic, Partition ==========
class Topic:
    def __init__(self, name, partition_count):
        self.name = name
        self.partitions = [Partition(i) for i in range(partition_count)]

class Partition:
    def __init__(self, pid):
        self.id = pid
        self.messages = []
        self.subscriber_offsets = defaultdict(int)
        self.lock = threading.Lock()
        self.subscribers = []

    def add_message(self, message):
        with self.lock:
            self.messages.append(message)
            for sub in self.subscribers:
                sub.notify()

    def register_subscriber(self, subscriber):
        self.subscriber_offsets[subscriber] = 0
        self.subscribers.append(subscriber)

    def get_next_message(self, subscriber):
        with self.lock:
            idx = self.subscriber_offsets[subscriber]
            if idx < len(self.messages):
                self.subscriber_offsets[subscriber] += 1
                return self.messages[idx]
            return None


# ========== Publisher ==========
class Publisher:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy

    def publish(self, topic, content):
        partition = self.strategy.choose_partition(topic)
        partition.add_message(Message(content))
        print(f"[{time.time()}] Publisher {self.name} published to Topic '{topic.name}' Partition {partition.id}: {content}")


# ========== Subscriber (Observer) ==========
class Subscriber:
    def __init__(self, name):
        self.name = name
        self.event = threading.Event()

    def notify(self):
        self.event.set()

    def subscribe(self, topic):
        for partition in topic.partitions:
            partition.register_subscriber(self)
            threading.Thread(target=self.consume, args=(partition,), daemon=True).start()

    def consume(self, partition):
        while True:
            self.event.wait()
            while True:
                msg = partition.get_next_message(self)
                if msg:
                    print(f"[{time.time()}] Subscriber {self.name} received from Partition {partition.id}: {msg.content}")
                else:
                    break
            self.event.clear()


# ========== Main Simulation ==========
if __name__ == "__main__":
    topic1 = Topic("Topic1", 3)
    topic2 = Topic("Topic2", 2)

    strategy1 = RandomPartitionStrategy()
    strategy2 = RoundRobinPartitionStrategy()

    pubA = Publisher("A", strategy1)
    pubB = Publisher("B", strategy2)

    sub1 = Subscriber("1")
    sub2 = Subscriber("2")

    sub1.subscribe(topic1)
    sub2.subscribe(topic1)

    pubA.publish(topic1, "Hello from A1")
    pubB.publish(topic1, "Hello from B1")
    pubA.publish(topic1, "Hello from A2")
    pubB.publish(topic1, "Hello from B2")

    time.sleep(2)

    sub1.subscribe(topic2)
    pubA.publish(topic2, "Topic2 msg1 from A")
    pubB.publish(topic2, "Topic2 msg2 from B")

    time.sleep(2)
    sub2.subscribe(topic2)
    pubA.publish(topic2, "Topic2 msg3 from A")

    time.sleep(5)
