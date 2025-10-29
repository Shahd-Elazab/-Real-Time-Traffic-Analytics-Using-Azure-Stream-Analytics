# Kafka Commands Hands-On

### Display Topic Information
```bash
kafka-topics.sh --describe --zookeeper localhost:2181 --topic beacon
```
* Use case: You want to see how many partitions the `beacon` topic has, which broker is leading each partition, and the replication status.

* Example Output:
	```
	Topic: beacon  PartitionCount:6  ReplicationFactor:1
	Partition: 0  Leader: 1  Replicas: 1  Isr: 1
	Partition: 1  Leader: 1  Replicas: 1  Isr: 1
	```


### Add Partitions to a Topic
```bash
kafka-topics.sh --alter --zookeeper localhost:2181 --topic beacon --partitions 3
```

* Use case: Initially you started with 1 partition and traffic increased. You scale to 3 partitions for better throughput.

* **Warning:** Changing partition count affects message ordering if keys are used.


### Change Topic Retention Policy (Set SLA)
```bash
kafka-topics.sh --alter --zookeeper localhost:2181 --topic mytopic --config retention.ms=28800000


```
* Use case: You only want to retain logs for 8 hours due to storage limitations or regulatory reasons.

* **retention.ms=28800000** = 8 hours in milliseconds.


### Delete a Topic
```bash
kafka-run-class.sh kafka.admin.DeleteTopicCommand --zookeeper localhost:2181 --topic test
```
* Use case: You created a topic `test` for experimentation and now want to clean up.


### Create Topics
```bash
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic job_result
```
* Use case: You're building a job processing pipeline and create `job_result` to store job outputs.


### List All Topics
```bash
kafka-topics.sh --list --zookeeper localhost:2181
```
* Use case: You’re checking what topics already exist in the Kafka cluster.


### Produce Messages (Write to a Topic)
```bash
kafka-console-producer.sh --broker-list localhost:9092 --topic test
```
* Use case: You want to test Kafka by sending messages manually.

* Example usage:
	```
	>> Hello World
	>> {"event":"click","user":"user123"}
	```


### Consume Messages (Read from a Topic)
```bash
kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning
```
* Use case: You want to see all messages from the start of the `test` topic.


### Purge a Topic (Clear All Messages)
```bash
kafka-topics.sh --alter --zookeeper localhost:2181 --topic mytopic --config retention.ms=1000
sleep 60
kafka-topics.sh --alter --zookeeper localhost:2181 --topic mytopic --delete-config retention.ms
```
* Use case: Quickly clear a topic without deleting and recreating it.


### Get Earliest/Latest Offsets
```bash
# Earliest
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic mytopic --time -2

# Latest
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic mytopic --time -1
```
* Use case: You want to understand how much backlog is in a topic.


### Kafka Consumer Groups
```bash
# List consumer groups
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# Describe a specific group
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my_group
```
* Use case: Debug why a consumer group isn't catching up with messages or see what topics a group is consuming.


### Get Consumer Offsets
```bash
kafka-consumer-offset-checker.sh --zookeeper localhost:2181 --topic=mytopic --group=my_consumer_group
```
* Use case: Track where your consumers are in relation to the latest messages.


### Read Internal Offsets Topic
```bash
kafka-console-consumer.sh --consumer.config config/consumer.properties --from-beginning --topic __consumer_offsets --zookeeper localhost:2181 --formatter "kafka.coordinator.GroupMetadataManager$OffsetsMessageFormatter"
```
* Use case: Debug low-level consumer behavior by reading Kafka’s internal state about consumer groups.


### Read Last 5 Messages with `kafkacat`
```bash
kafkacat -C -b localhost:9092 -t mytopic -p 0 -o -5 -e
```
* Use case: You only want the last few records for quick inspection.


### Zookeeper Shell
```bash
zookeeper-shell.sh localhost:2181
```
* Use case: Directly interact with Zookeeper (e.g., view or edit Kafka metadata).

---

## Practical Example: E-Commerce Order Processing
Build an integration with an e-commerce site that uses Kafka to track orders from checkout to delivery.

**Create three topics:**
- `order_created`
- `payment_processed`
- `order_shipped`
```bash
# Creating topics
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic order_created
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic payment_processed
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic order_shipped
```
> Hint: More partitions = more parallelism.


**View Topics:**
```bash
# List all topics
kafka-topics.sh --list --zookeeper localhost:2181
```


**Simulate Order Events (Producers):**

Start a **producer** to simulate order creation:
```bash
kafka-console-producer.sh --broker-list localhost:9092 --topic order_created
```

Type messages manually:
```JSON
{"order_id":"101", "customer":"Mariam", "items":["book","pen"]}
{"order_id":"102", "customer":"Ali", "items":["laptop"]}
```

Start another producer for **payment processing**:
```bash
kafka-console-producer.sh --broker-list localhost:9092 --topic payment_processed
```

Example messages:
```JSON
{"order_id":"101", "status":"paid"}
{"order_id":"102", "status":"pending"}
```


**Read Events (Consumers):**

Start a **consumer** to listen for new orders:
```bash
kafka-console-consumer.sh --zookeeper localhost:2181 --topic order_created --from-beginning
```
Watch the messages appear in real time.


**Check Topic Details:**
```bash
kafka-topics.sh --describe --zookeeper localhost:2181 --topic order_created
```
See partitions, leaders, ISR (in-sync replicas).


**Purge Old Orders Quickly:**

Suppose you want to clear old messages from `order_created` topic:
```bash
kafka-topics.sh --alter --zookeeper localhost:2181 --topic order_created --config retention.ms=1000
sleep 60
kafka-topics.sh --alter --zookeeper localhost:2181 --topic order_created --delete-config retention.ms
```
