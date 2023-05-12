# Check event processor idle via Kafka Stream

## 1. Introduction

This document describes how to check if a processor is idle for a period time before processing any new task. Because we need to ensure there's no incompleted task executing when handling new tasks.

## 2. Original problem

When executing the fund operation, if all background processing is not waited, it may cause the number of fund statistics records to be incorrect.

## 3. Solution

We can use Apache Kafka Stream to track the status of the processor. If the processor is idle, we can process the event. Otherwise, we need to wait until the processor is idle.

### 3.1. Implementation

#### 3.1.1. Step 1: Define an Activity Initialized Event

This event is used to track the status of the processor. When a processor is started, an ActivityInitializedEvent will be published to the activity initialized event stream.

```java
public class ActivityInitializedEvent {

    private String activityId;
    private String processorId;

    public ActivityInitializedEvent() {
    }

    public ActivityInitializedEvent(String activityId, String processorId) {
        this.activityId = activityId;
        this.processorId = processorId;
    }

    public String getActivityId() {
        return activityId;
    }

    public void setActivityId(String activityId) {
        this.activityId = activityId;
    }

    public String getProcessorId() {
        return processorId;
    }

    public void setProcessorId(String processorId) {
        this.processorId = processorId;
    }

    @Override
    public String toString() {
        return "ActivityInitializedEvent{" +
                "processorId='" + processorId + '\'' +
                '}';
    }
}
```

In kotlin:

```kotlin
data class ActivityInitializedEvent(
    var activityId: String? = null,
    var processorId: String? = null
)
```

#### 3.1.2. Step 2: Define an Activity Completed Event

When an activity is completed, an event will be published to ActivityCompletedEventStream.

```java
public class ActivityCompletedEvent {

    private String activityId;
    private String processorId;

    public ActivityCompletedEvent() {
    }

    public ActivityCompletedEvent(String activityId, String processorId) {
        this.activityId = activityId;
        this.processorId = processorId;
    }

    public String getActivityId() {
        return activityId;
    }

    public void setActivityId(String activityId) {
        this.activityId = activityId;
    }

    public String getProcessorId() {
        return processorId;
    }

    public void setProcessorId(String processorId) {
        this.processorId = processorId;
    }

    @Override
    public String toString() {
        return "ActivityCompletedEvent{" +
                "processorId='" + processorId + '\'' +
                '}';
    }
}
```

In kotlin:

```kotlin
data class ActivityCompletedEvent(
    var activityId: String? = null,
    var processorId: String? = null
)
```

#### 3.1.3. Step 3. Define a Processor Status Event

This event is used to track the status of the processor. When a processor is idle, an event will be published to the processor status stream. Otherwise, no event will be published to the processor status stream.

```java
public class ProcessorStatusEvent {

    private String processorId;
    private String activityId;
    private boolean idle;

    public ProcessorStatusEvent() {
    }

    public ProcessorStatusEvent(String processorId, String activityId, boolean idle) {
        this.processorId = processorId;
        this.activityId = activityId;
        this.idle = idle;
    }

    public String getProcessorId() {
        return processorId;
    }

    public void setProcessorId(String processorId) {
        this.processorId = processorId;
    }

    public String getActivityId() {
        return activityId;
    }

    public void setActivityId(String activityId) {
        this.activityId = activityId;
    }

    public boolean isIdle() {
        return idle;
    }

    public void setIdle(boolean idle) {
        this.idle = idle;
    }

    @Override
    public String toString() {
        return "ProcessorStatusEvent{" +
                "processorId='" + processorId + '\'' +
                ", idle=" + idle +
                '}';
    }
}
```

#### Create a Kafka Stream Binder

We can use Spring cloud stream to create a Kafka Stream binder. We can define the Kafka Stream binder with the following code:

```java
public interface ProcessorStatusStream {

    String INPUT = "processor-status-in";
    String OUTPUT = "processor-status-out";

    @Input(INPUT)
    KStream<String, ProcessorStatusEvent> processorStatusIn();

    @Output(OUTPUT)
    KStream<String, ProcessorStatusEvent> processorStatusOut();
}
```

#### 3.1.4. Step 4: Transform ActivityInitializedEvent Stream & ActivityCompletedEvent Stream to ProcessorStatusEvent Stream

This stream is used to track the status of the processor. When a processor is idle, an event will be published to this stream. Otherwise, no event will be published to this stream. We will use Spring cloud stream to transform ActivityInitializedEvent Stream & ActivityCompletedEvent Stream to ProcessorStatusEvent Stream.

Note: We can define a transformer with BiFunction<KStream<String, ActivityInitializedEvent>, KStream<String, ActivityCompletedEvent>, KStream<String, ProcessorStatusEvent>> transform() method. Each time when a new event is received from ActivityInitializedEvent Stream or ActivityCompletedEvent Stream, the transform() method will be called. We can use the received event to update the status of the processor.

```java
@EnableBinding({ProcessorStatusStream.class, ActivityInitializedEventStream.class, ActivityCompletedEventStream.class})
public class ProcessorStatusEventTransformer {

    public BiFunction<KStream<String, ActivityInitializedEvent>, KStream<String, ActivityCompletedEvent>, KStream<String, ProcessorStatusEvent>> transform() {
        return (activityInitializedEventStream, activityCompletedEventStream) -> {
            KStream<String, ProcessorStatusEvent> processorStatusEventStream = activityInitializedEventStream
                    .map((key, value) -> new KeyValue<>(value.getProcessorId(), value))
                    .groupByKey()
                    .aggregate(
                            ProcessorStatusEvent::new,
                            (key, value, aggregate) -> {
                                aggregate.setProcessorId(value.getProcessorId());
                                aggregate.setActivityId(value.getActivityId());
                                aggregate.setIdle(false);
                                return aggregate;
                            },
                            Materialized.with(Serdes.String(), new JsonSerde<>(ProcessorStatusEvent.class))
                    )
                    .toStream()
                    .map((key, value) -> new KeyValue<>(key, value));

            KStream<String, ProcessorStatusEvent> processorStatusEventStream2 = activityCompletedEventStream
                    .map((key, value) -> new KeyValue<>(value.getProcessorId(), value))
                    .groupByKey()
                    .aggregate(
                            ProcessorStatusEvent::new,
                            (key, value, aggregate) -> {
                                aggregate.setProcessorId(value.getProcessorId());
                                aggregate.setActivityId(value.getActivityId());
                                aggregate.setIdle(true);
                                return aggregate;
                            },
                            Materialized.with(Serdes.String(), new JsonSerde<>(ProcessorStatusEvent.class))
                    )
                    .toStream()
                    .map((key, value) -> new KeyValue<>(key, value));

            // Merge the Processor Status Event Stream
            return processorStatusEventStream.merge(processorStatusEventStream2);
        };
    }

    @Bean
    public Consumer<KStream<String, ProcessorStatusEvent>> process(@Autowired ProcessorStatusTracker processorStatusTracker) {
        return processorStatusEventStream -> processorStatusEventStream.foreach((key, value) -> processorStatusTracker.handleProcessorStatusEvent(value));
    }
}
```

#### 3.1.5. Step 5: Query the Processor Status Event Stream to get the latest status of the processor

The Processor Status Event Stream will emits many Processor Status Events. But we only need the latest Processor Status Event. So we will use the ProcessorStatusEventTransformer to transform the Processor Status Event Stream to Processor Status Event KTable. Then we can query the Processor Status Event KTable to get the latest Processor Status Event.

```java
@Component
public class ProcessorStatusTracker {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorStatusTracker.class);

        private final Map<String, Boolean> processorStatusMap = new ConcurrentHashMap<>();

        public ProcessorStatusTracker() {

        }

        public void handleProcessorStatusEvent(ProcessorStatusEvent event) {
            LOGGER.info("Received processor status event: {}", event);
            processorStatusMap.put(event.getProcessorId(), event.isIdle());
        }

        public boolean isIdle(String processorId) {
            return processorStatusMap.getOrDefault(processorId, true);
        }
}
```

We need to aggregate all the Processor Status Events bind to the same processor to get the latest Processor Status Event. So we will change the ProcessorStatusTracker to group the Processor Status Events by processorId. Each ProcessorId will have multiple associated ActivityId and Idle status. To determine isIdle for processorId, we will check if all the associated ActivityId are idle. We want to use Map<String, Map<String, Boolean>> processorStatusMap to store the Processor Status Events. But the Map<String, Map<String, Boolean>> processorStatusMap is not thread safe. So we will use ConcurrentHashMap<String, Map<String, Boolean>> processorStatusMap to store the Processor Status Events.

    ```java
    @Component
    public class ProcessorStatusTracker {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorStatusTracker.class);

        private final Map<String, Map<String, Boolean>> processorStatusMap = new ConcurrentHashMap<>();

        public ProcessorStatusTracker() {

        }

        @StreamListener(ProcessorStatusStream.INPUT)
        public void handleProcessorStatusEvent(ProcessorStatusEvent event) {
            LOGGER.info("Received processor status event: {}", event);
            processorStatusMap.compute(event.getProcessorId(), (processorId, activityStatusMap) -> {
                if (activityStatusMap == null) {
                    activityStatusMap = new ConcurrentHashMap<>();
                }
                activityStatusMap.put(event.getActivityId(), event.isIdle());
                // to clean up the activityStatusMap, we will remove the activityStatusMap if all the activities are idle
                if (activityStatusMap.values().stream().allMatch(idle -> idle)) {
                    return null;
                }
                return activityStatusMap;
            });
        }

        public boolean isIdle(String processorId) {
            Map<String, Boolean> activityStatusMap = processorStatusMap.get(processorId);
            if (activityStatusMap == null || activityStatusMap.isEmpty()) {
                return true;
            }
            return activityStatusMap.values().stream().allMatch(idle -> idle);
        }
    }
    ```

But there is another problem. When an ActivityInitializedEvent emits in a short period after idle, we'd rather not start a new processing. So we will need configure the ProcessorStatusTracker to ensure that the processor is idle for a period of time before starting a new processing.

```java
@Component
public class ProcessorStatusTracker {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorStatusTracker.class);

        private final Map<String, Map<String, Boolean>> processorStatusMap = new ConcurrentHashMap<>();

        private final Map<String, Long> processorStatusTimestampMap = new ConcurrentHashMap<>();

        private final long idleTime;

        public ProcessorStatusTracker(@Value("${processor.idle.time}") long idleTime) {
            this.idleTime = idleTime;
        }

        public void handleProcessorStatusEvent(ProcessorStatusEvent event) {
            LOGGER.info("Received processor status event: {}", event);
            processorStatusMap.compute(event.getProcessorId(), (processorId, activityStatusMap) -> {
                if (activityStatusMap == null) {
                    activityStatusMap = new ConcurrentHashMap<>();
                }
                activityStatusMap.put(event.getActivityId(), event.isIdle());
                // to clean up the activityStatusMap, we will remove the activityStatusMap if all the activities are idle
                if (activityStatusMap.values().stream().allMatch(idle -> idle)) {
                    return null;
                }
                return activityStatusMap;
            });
            // Update the timestamp of the processor at the first time when the processor become idle
            if(event.isIdle()) {
                processorStatusTimestampMap.putIfAbsent(event.getProcessorId(), System.currentTimeMillis());
            }
        }

        public boolean isIdle(String processorId) {
            Map<String, Boolean> activityStatusMap = processorStatusMap.get(processorId);
            if (activityStatusMap == null || activityStatusMap.isEmpty()) {
                return true;
            }
            // Check if the processor is idle for a period of time
            Long timestamp = processorStatusTimestampMap.get(processorId);
            if(timestamp == null) {
                return false;
            }
            return System.currentTimeMillis() - timestamp > idleTime;
        }
}
```

Another component do not consider the activity status is as below:

```java
@Component
public class ProcessorStatusTracker {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorStatusTracker.class);

        private final Map<String, Boolean> processorStatusMap = new ConcurrentHashMap<>();

        private final Map<String, Long> processorStatusTimestampMap = new ConcurrentHashMap<>();

        private final long idleTime;

        public ProcessorStatusTracker(@Value("${processor.idle.time}") long idleTime) {
            this.idleTime = idleTime;
        }

        public void handleProcessorStatusEvent(ProcessorStatusEvent event) {
            LOGGER.info("Received processor status event: {}", event);
            processorStatusMap.put(event.getProcessorId(), event.isIdle());
            // Update the timestamp of the processor at the first time when the processor become idle
            if(event.isIdle()) {
                processorStatusTimestampMap.putIfAbsent(event.getProcessorId(), System.currentTimeMillis());
            } else {
                processorStatusTimestampMap.remove(event.getProcessorId());
            }
        }

        /**
         * Check if the processor is idle for a period of time
         * @param processorId
         * @return true if the processor is idle for a period of time, otherwise false
         */
        public boolean isIdle(String processorId) {
            if (processorId == null) {
                return true;
            }

            if (!processorStatusMap.getOrDefault(processorId, true)) {
                return false;
            }

            Long timestamp = processorStatusTimestampMap.get(processorId);
            // If the processor is idle but the timestamp is null, it means that the processor has never been idle
            if (timestamp == null) {
                return false;
            }
            // If the processor is idle for a period of time, return true
            return System.currentTimeMillis() - timestamp > idleTime;
        }
}
```

#### 3.1.6. Step 6: Unit Test for ProcessorStatusTracker

As EnableBinding and StreamListener are deprecated, we will use a functional style to implement the ProcessorStatusStream.

Unit Test via KafkaTemplate to send the ProcessorStatusEvent to the Spring Cloud Stream.

```java
@ExtendWith(SpringExtension.class)
@SpringBootTest
@EmbeddedKafka(partitions = 1, topics = {ProcessorStatusStream.INPUT})
public class ProcessorStatusTrackerTest {

    @Autowired
    private KafkaTemplate<String, ProcessorStatusEvent> kafkaTemplate;

    @Autowired
    private ProcessorStatusTracker processorStatusTracker;

    @Test
    public void testProcessorStatusTracker() throws InterruptedException {
        String processorId = "processor-1";
        String activityId = "activity-1";
        ProcessorStatusEvent processorStatusEvent = new ProcessorStatusEvent(processorId, activityId, true);
        kafkaTemplate.send(ProcessorStatusStream.INPUT, processorStatusEvent);
        Thread.sleep(1000);
        assertTrue(processorStatusTracker.isIdle(processorId));
    }

    // test the processor is not idle if the activity is not idle
    @Test
    public void testProcessorStatusTracker2() throws InterruptedException {
        String processorId = "processor-1";
        String activityId = "activity-1";
        ProcessorStatusEvent processorStatusEvent = new ProcessorStatusEvent(processorId, activityId, false);
        kafkaTemplate.send(ProcessorStatusStream.INPUT, processorStatusEvent);
        Thread.sleep(1000);
        assertFalse(processorStatusTracker.isIdle(processorId));
    }

    // test the processor is not idle if the activity is idle but the processor is not idle for a period of time
    @Test
    public void testProcessorStatusTracker3() throws InterruptedException {
        String processorId = "processor-1";
        String activityId = "activity-1";
        ProcessorStatusEvent processorStatusEvent = new ProcessorStatusEvent(processorId, activityId, true);
        kafkaTemplate.send(ProcessorStatusStream.INPUT, processorStatusEvent);
        Thread.sleep(1000);
        assertFalse(processorStatusTracker.isIdle(processorId));
    }

    // test the processor is idle if the activity is idle and the processor is idle for a period of time
    @Test
    public void testProcessorStatusTracker4() throws InterruptedException {
        String processorId = "processor-1";
        String activityId = "activity-1";
        ProcessorStatusEvent processorStatusEvent = new ProcessorStatusEvent(processorId, activityId, true);
        kafkaTemplate.send(ProcessorStatusStream.INPUT, processorStatusEvent);
        Thread.sleep(1000);
        assertTrue(processorStatusTracker.isIdle(processorId));
    }

    // test the processor is not idle if one of the activities is not idle
    @Test
    public void testProcessorStatusTracker5() throws InterruptedException {
        String processorId = "processor-1";
        String activityId1 = "activity-1";
        String activityId2 = "activity-2";
        ProcessorStatusEvent processorStatusEvent1 = new ProcessorStatusEvent(processorId, activityId1, true);
        ProcessorStatusEvent processorStatusEvent2 = new ProcessorStatusEvent(processorId, activityId2, false);
        kafkaTemplate.send(ProcessorStatusStream.INPUT, processorStatusEvent1);
        kafkaTemplate.send(ProcessorStatusStream.INPUT, processorStatusEvent2);
        Thread.sleep(1000);
        assertFalse(processorStatusTracker.isIdle(processorId));
    }

    // test via ActivityInitializedEvent & ActivityCompletedEvent
    @Test
    public void testProcessorStatusTracker6() throws InterruptedException {
        String processorId = "processor-1";
        String activityId = "activity-1";
        ActivityInitializedEvent activityInitializedEvent = new ActivityInitializedEvent(processorId, activityId);
        ActivityCompletedEvent activityCompletedEvent = new ActivityCompletedEvent(processorId, activityId);
        kafkaTemplate.send(ActivityInitializedStream.INPUT, activityInitializedEvent);
        kafkaTemplate.send(ActivityCompletedStream.INPUT, activityCompletedEvent);
        Thread.sleep(1000);
        assertTrue(processorStatusTracker.isIdle(processorId));
    }
}
```

Since @EmbeddedKafka is in used, we need to add the following dependency in the build.gradle.

```groovy
testImplementation 'org.springframework.kafka:spring-kafka-test'
```

### 3.2. Optimizing the usage of the Processor Tracker via AOP

The Processor Tracker is used in many places. We can use AOP to simplify the usage of the Processor Tracker.

#### 3.2.1. Step 1: Create the annotation @ProcessorTracker

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface ProcessorTracker {

    /**
     * The id of the processor
     * @return
     */
    String value();
}
```

#### 3.2.2. Step 2: Create the aspect ProcessorTrackerAspect

```java
@Aspect
@Component
public class ProcessorTrackerAspect {

    private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorTrackerAspect.class);

    private final ProcessorStatusTracker processorStatusTracker;

    public ProcessorTrackerAspect(ProcessorStatusTracker processorStatusTracker) {
        this.processorStatusTracker = processorStatusTracker;
    }

    @Around("@annotation(processorTracker)")
    public Object around(ProceedingJoinPoint joinPoint, ProcessorTracker processorTracker) throws Throwable {
        String processorId = processorTracker.value();
        LOGGER.info("Checking if the processor {} is idle", processorId);
        if (processorStatusTracker.isIdle(processorId)) {
            return joinPoint.proceed();
        } else {
            LOGGER.info("The processor {} is busy", processorId);
            return null;
        }
    }
}
```

Above code will not wait for the processor to be idle. If the processor is busy, it will return null immediately. If we want to wait for the processor to be idle, we can use the following code.

```java
@Aspect
@Component
public class ProcessorTrackerAspect {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorTrackerAspect.class);

        private final ProcessorStatusTracker processorStatusTracker;

        public ProcessorTrackerAspect(ProcessorStatusTracker processorStatusTracker) {
            this.processorStatusTracker = processorStatusTracker;
        }

        @Around("@annotation(processorTracker)")
        public Object around(ProceedingJoinPoint joinPoint, ProcessorTracker processorTracker) throws Throwable {
            String processorId = processorTracker.value();
            LOGGER.info("Checking if the processor {} is idle", processorId);
            while (!processorStatusTracker.isIdle(processorId)) {
                LOGGER.info("The processor {} is busy, waiting for it to be idle", processorId);
                Thread.sleep(1000);
            }
            return joinPoint.proceed();
        }
}
```

There is an reactive way via Coroutine in kotlin. We can use the following code. delay is a suspend function, so we need to add suspend to the method around. This method will not block the thread.

```kotlin
@Aspect
@Component
class ProcessorTrackerAspect(private val processorStatusTracker: ProcessorStatusTracker) {

    companion object {
        private val LOGGER = LoggerFactory.getLogger(ProcessorTrackerAspect::class.java)
    }

    @Around("@annotation(processorTracker)")
    suspend fun around(joinPoint: ProceedingJoinPoint, processorTracker: ProcessorTracker): Any? {
        val processorId = processorTracker.value
        LOGGER.info("Checking if the processor {} is idle", processorId)
        while (!processorStatusTracker.isIdle(processorId)) {
            LOGGER.info("The processor {} is busy, waiting for it to be idle", processorId)
            delay(1000)
        }
        return joinPoint.proceed()
    }
}
```

## 4. Conclusion

In this article, we have learned how to use Kafka Streams to implement a stateful stream processing. We have also learned how to use Spring Cloud Stream to simplify the development of Kafka Streams applications.
