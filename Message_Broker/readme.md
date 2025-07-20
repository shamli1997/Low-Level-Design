# 📩 In-Memory Message Queue System (Kafka-like)

## 🚦 Design Thinking + LLD Breakdown


## 🔍 Step 1: Understand Requirements
### ✅ Functional Requirements:
- Support multiple **Topics**.
- Each Topic has multiple **Partitions** (scalable & ordered message queues).
- Multiple **Publishers** send messages to topics.
- Multiple **Subscribers** consume messages from topics.
- Ensure **exactly-once delivery**, **in-order delivery within partition**, and **concurrency**.

### ❌ Non-Functional Requirements:
- High throughput
- Low latency
- Thread-safe reads/writes
- Maintainability + Extensibility

---

## 🎭 Step 2: Identify Key Actors (Use Cases)

| Actor      | Responsibilities                                         |
|------------|----------------------------------------------------------|
| Publisher  | Publish message to topic                                 |
| Subscriber | Subscribe to topic and consume messages                  |
| Topic      | Logical category managing message partitions             |
| Partition  | Stores ordered messages and tracks subscriber offsets    |
| Strategy   | Decides how to publish messages to partitions            |
| Observer   | Subscribes to changes in partitions (push-based model)   |

---

## 🧱 Step 3: Relationship Mapping

### Composition vs Aggregation:
| Class A           | Has-a B          | Relationship Type | Why? |
|------------------|------------------|--------------------|------|
| Topic            | Partitions       | Composition        | Partitions do not exist without Topic. |
| Partition        | Messages         | Composition        | Messages exist within specific Partition. |
| Partition        | Subscribers      | Aggregation        | Subscribers can exist independently. |
| Topic            | Strategy         | Aggregation        | Strategy object is injected (replaceable). |

---

## 📊 Step 4: Class Design Evolution

### 🔹 Topic
- ❌ `List<Partition>`: No topic ID mapping.
- ✅ `Map<TopicName, List<Partition>>`: Logical grouping by name.

### 🔹 Partition
- ✅ Holds messages in a thread-safe list.
- ✅ Tracks per-subscriber offset.
- ✅ Composed inside Topic.

### 🔹 Publisher
- ❌ Naive: Direct message push with random choice.
- ✅ Optimized: Use **Strategy Pattern** to choose partition.

### 🔹 Subscriber
- ✅ Uses threads to consume messages.
- ✅ Subscribed via Observer model.

---

## 💡 Design Patterns Used

| Pattern     | Why We Used It                                                |
|-------------|---------------------------------------------------------------|
| Strategy    | Choose partition dynamically while publishing.                |
| Observer    | Push model for message consumption per subscriber.            |

---

## ✅ SOLID Principles

| Principle | How We Followed It |
|-----------|--------------------|
| S - SRP   | Each class has a single job (Publisher, Subscriber, etc.) |
| O - OCP   | Easily plug new strategies (e.g. hash-based, sticky-partition). |
| L - LSP   | Strategies and observers are replaceable implementations. |
| I - ISP   | No bloated interfaces, only essential methods. |
| D - DIP   | Strategy and observer logic are interface-driven. |

---

## ♻️ Message Flow (with Optimizations)

### 🗭 Publishing:
1. Publisher → selects partition using strategy.
2. Message appended to partition.
3. All subscribers of partition notified (Observer pattern).

### 📅 Consumption:
1. Each partition has offset tracking per subscriber.
2. Thread checks for new messages.
3. Delivers exactly once, in order.

---

## 📈 Optimizations (With Reasoning)

| Concern        | Naive Design                        | Optimized Design                                  |
|----------------|--------------------------------------|---------------------------------------------------|
| Message Insert | Pick random partition manually       | Strategy pattern → plug any smart logic           |
| Read Model     | Loop over partitions                 | Each partition has threads, offsets, observer     |
| Delivery       | No control on delivery semantics     | Per-subscriber offset map for exactly-once        |
| Concurrency    | Shared mutable list                  | `Queue`/`synchronized list` for thread safety      |

---

## 🛠️ Future Improvements
- Consumer groups
- Retry + DLQ (Dead Letter Queue)
- Persistent queues using disk/Redis
- Monitoring + Alerting + Replay

---

## 📦 Sample Use Case
- Topic: `Topic1` with 2 partitions.
- Publisher A & B → send messages concurrently.
- Subscriber 1 & 2 → consume from all partitions.
- ✅ Messages are consumed in order, without loss, and without duplication.

---

## 🛠️ Future Extensions
- ✅ Consumer groups
- ✅ Persistent queues (Redis, Disk)
- ✅ Retry & DLQ (Dead Letter Queue)
- ✅ Metrics & Monitoring


---

## 🧠 Conclusion
This implementation demonstrates real-world message queue design using key OOP and design pattern concepts. It’s minimal yet scalable and a solid base to expand into more production-grade features.

---

