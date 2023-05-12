# Implement Dead Letter Queue in Axon Framework

## Introduction

In this article, we will learn how to implement a dead letter queue in Axon Framework. We will use the Axon Server as the message broker.

## What is a Dead Letter Queue?

A dead letter queue is a queue where messages that cannot be delivered to their destination are stored. The messages are stored in the dead letter queue until they are either manually removed or the time to live of the message expires.

## Why do we need a Dead Letter Queue?

As Axon Framework will retry to handle the Event Messages that are not handled successfully, we need a mechanism to handle the Event Messages that are not handled successfully after a certain number of retries. This is where the dead letter queue comes into the picture.

## How to implement a Dead Letter Queue in Axon Framework?

Axon Framework provides a mechanism to implement a dead letter queue. We can implement a dead letter queue by implementing the `DeadLetterHandler` interface. The `handle` method of the `DeadLetterHandler` interface is called when an Event Message is not handled successfully after a certain number of retries. The `handle` method takes a `DeadMessage` object as an argument. The `DeadMessage` object contains the Event Message that is not handled successfully and the exception that is thrown while handling the Event Message.

```java
public interface DeadLetterHandler {

    void handle(DeadMessage message);
}
```

We can register the `DeadLetterHandler` implementation using the `registerDeadLetterHandler` method of the `Configurer` interface.

```java
Configurer configurer = DefaultConfigurer.defaultConfiguration();
configurer.configureEventProcessing(
        eventProcessingConfigurer -> eventProcessingConfigurer.registerDeadLetterHandler(
                configuration -> new DeadLetterHandlerImpl()
        )
);
```

The `DeadLetterHandlerImpl` class is the implementation of the `DeadLetterHandler` interface. The `handle` method of the `DeadLetterHandlerImpl` class logs the Event Message that is not handled successfully and the exception that is thrown while handling the Event Message.

```java
public class DeadLetterHandlerImpl implements DeadLetterHandler {

    private static final Logger LOGGER = LoggerFactory.getLogger(DeadLetterHandlerImpl.class);

    @Override
    public void handle(DeadMessage message) {
        LOGGER.error("Event Message: {} is not handled successfully. Exception: {}",
                message.getEventMessage().getPayload(),
                message.getCause().getMessage()
        );
    }
}
```

Configuration in Spring boot application is done using the `@Configuration` annotation. The `@Configuration` annotation indicates that the class contains one or more bean methods annotated with the `@Bean` annotation. The `@Bean` annotation tells Spring that a method produces a bean that is managed by the Spring container. The `@Bean` annotation is a method-level annotation.

```java
@Configuration
public class AxonConfig {

    @Bean
    public DeadLetterHandler deadLetterHandler() {
        return new DeadLetterHandlerImpl();
    }
}
```

## Conclusion

In this article, we have learned how to implement a dead letter queue in Axon Framework. We have also learned why we need a dead letter queue and how to implement a dead letter queue in Axon Framework.

## References

- [Axon Framework Reference Guide](https://docs.axoniq.io/reference-guide/)

## Source Code

- [GitHub](https://github.com/ganeshkumarraja/medium/tree/master/axon/axon-implement-dead-letter-queue-in-axon-framework)

## Related Articles

- [Implement Event Replay in Axon Framework](https://medium.com/@ganeshkumarraja/implement-event-replay-in-axon-framework-4b0b0b2b8b0a)
