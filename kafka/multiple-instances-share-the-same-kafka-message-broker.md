# Multiple instances share the same Kafka cluster

## 1. Introduction

### 1.1. Background

In the past, we used to have an individual Kafka cluster for each application. However, this approach has some drawbacks:

- It is difficult to manage the Kafka cluster. For example, we need to monitor the health of each Kafka cluster, and we need to upgrade the Kafka cluster to the latest version.

- It is inefficient to use the Kafka cluster. For example, if we want to send a message from one application to another application, we need to send the message to the Kafka cluster of the first application, and then the first application needs to send the message to the Kafka cluster of the second application.

- It is difficult to scale the Kafka cluster. For example, if we want to scale the Kafka cluster, we need to scale each Kafka cluster individually.

### 1.2. Purpose

To solve the above problems, we want to share the same Kafka cluster among multiple applications.

## 2. Design

### 2.1. Kafka cluster

We will have a Kafka cluster for each environment (e.g. dev, test, prod). Each Kafka cluster will have multiple Kafka brokers. Each Kafka broker will have multiple Kafka topics. Each Kafka topic will have multiple Kafka partitions.

## 3. Problems

### 3.1. How to distinguish messages from different applications?

We can use the `application.id` property to distinguish messages from different applications.

For example (in `application.yml`):

```yml
spring:
  application:
    id: my-application
```

This will set the `application.id` property to `my-application`.

Q: Will the messages from different applications be mixed together in the same Kafka topic?

A: It depends on the `groupId` property of the Kafka listener. If the `groupId` property is the same, then the messages from different applications will be mixed together in the same Kafka topic. If the `groupId` property is different, then the messages from different applications will be separated in different Kafka topics.

Q: But how to set the `groupId` property dynamically? Say we start up multiple instances of the same application, but we use environment variables to set the `application.id` property. How to set the `groupId` property dynamically?

A: We can use the `application.id` property to set the `groupId` property dynamically. For example (in `application.yml`):

```yml
spring:
  application:
    id: my-application
  kafka:
    consumer:
      group-id: ${spring.application.id}
```

Q: How to set the `groupId` property dynamically in the Kafka listener?

A: We can use the `#{}` syntax to set the `groupId` property dynamically. For example (in `MyKafkaListener.java`):

```java
// A Kafka Listener for the "my-application" Kafka topic.
@KafkaListener(topics = "my-application", groupId = "#{spring.application.id}")
public void listen(String message) {
    // ...
}
```

Q: How to set the `groupId` property dynamically in the Kafka producer?

A: Kafka will set the topicId, we'll use KafkaTemplate to demonstrate this scenario, for example (in `MyKafkaProducer.java`):

```java
@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void send(String message) {
    kafkaTemplate.send("my-application", message);
}
```

However, if we want to set the `groupId` property dynamically in the Kafka producer, we can use the `#{}` syntax. For example (in `MyKafkaProducer.java`):

```java
@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void send(String message) {
    kafkaTemplate.send("#{spring.application.id}", "my-application", message);
}
```

Q: But we only have send method with signature send(String topicId, String key, String message), how to set the `groupId` property dynamically in the Kafka producer?

A: We can use the `#{}` syntax to set the `groupId` property dynamically. For example (in `MyKafkaProducer.java`):

```java

@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void send(String message) {
    kafkaTemplate.send("#{spring.application.id}", "my-application", message);
}
```

Q: Isn't it the same as the previous question?

A: No, it's not the same. The previous question is about how to set the `groupId` property dynamically in the Kafka listener. This question is about how to set the `groupId` property dynamically in the Kafka producer.

Q: But we only have send method with signature send(String topicId, String key, String message), how to set the `groupId` property dynamically in the Kafka producer?

A: Set the `groupId` property dynamically in the Kafka producer is not possible. Thus, once a message is sent to a Kafka topic, it will be mixed with other messages in the same Kafka topic. And handled by all Kafka listeners listening to the same Kafka topic. Each group of Kafka listeners will handle the message only once.

If we have below architecture, a kafka topic with 3 partitions, 2 applications with 2 instances each, and each instance has 2 listeners, then we will have 12 listeners in total, and each listener will handle the message only once.

```text
Kafka topic
    Partition 0
        Listener 0
        Listener 1
    Partition 1
        Listener 2
        Listener 3
    Partition 2
        Listener 4
        Listener 5
```

Q: But what if we want to send a message to a specific instance of a specific application, will a listener handle only messages from a group of messages?

A: Yes, a listener will handle only messages from a group of messages. For example, if we want to send a message to the first instance of the first application, we can use the `#{}` syntax to set the `groupId` property dynamically. For example (in `MyKafkaProducer.java`):

```java
@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void send(String message) {
    kafkaTemplate.send("#{spring.application.id}-0", "my-application", message);
}
```

Q: How to set topic name dynamically in the Kafka Listener?

A: We can use the `#{}` syntax to set the topic name dynamically. For example (in `MyKafkaListener.java`):

```java
// A Kafka Listener for the "my-application" Kafka topic.
@KafkaListener(topics = "#{spring.application.id}", groupId = "#{spring.application.id}")
public void listen(String message) {
    // ...
}
```

Q: How to set topic name dynamically in the Kafka producer?

A: We can use the `#{}` syntax to set the topic name dynamically. For example (in `MyKafkaProducer.java`):

```java
@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void send(String message) {
    var topic = "topicSubsidy";
    // SpEL expression to set topic name dynamically.
    kafkaTemplate.send("#{spring.application.id}" + topic, message);
}
```

Use Kafka Operations to send message to a specific partition, for example (in `MyKafkaProducer.java`):

```java
@Autowired
private KafkaOperations<String, String> kafkaOperations;

public void send(String message) {
    var topic = "topicSubsidy";
    var partition = 0;
    kafkaOperations.send(topic, partition, message);
}
```
