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
    private boolean idle;

    public ProcessorStatusEvent() {
    }

    public ProcessorStatusEvent(String processorId, boolean idle) {
        this.processorId = processorId;
        this.idle = idle;
    }

    public String getProcessorId() {
        return processorId;
    }

    public void setProcessorId(String processorId) {
        this.processorId = processorId;
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

#### 3.1.4. Step 4: Transform ActivityInitializedEvent Stream & ActivityCompletedEvent Stream to ProcessorStatusEvent Stream

This stream is used to track the status of the processor. When a processor is idle, an event will be published to this stream. Otherwise, no event will be published to this stream. We will use Spring cloud stream to transform ActivityInitializedEvent Stream & ActivityCompletedEvent Stream to ProcessorStatusEvent Stream.

Note: We can define a transformer with BiFunction<KStream<String, ActivityInitializedEvent>, KStream<String, ActivityCompletedEvent>, KStream<String, ProcessorStatusEvent>> transform() method. Each time when a new event is received from ActivityInitializedEvent Stream or ActivityCompletedEvent Stream, the transform() method will be called. We can use the received event to update the status of the processor. If the processor is idle, we can publish an event to ProcessorStatusEvent Stream. Otherwise, no event will be published to ProcessorStatusEvent Stream.

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
                                return aggregate;
                            },
                            Materialized.with(Serdes.String(), new JsonSerde<>(ProcessorStatusEvent.class))
                    )
                    .toStream()
                    .map((key, value) -> new KeyValue<>(key, value));

            return processorStatusEventStream.merge(processorStatusEventStream2);
        };
    }
}
```

#### 3.1.5. Step 5: Query the Processor Status Event Stream to get the latest status of the processor

The Processor Status Event Stream will emits many Processor Status Events. But we only need the latest Processor Status Event. So we will use the ProcessorStatusEventTransformer to transform the Processor Status Event Stream to Processor Status Event KTable. Then we can query the Processor Status Event KTable to get the latest Processor Status Event.

```java
@Component
public class ProcessorStatusTracker {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorStatusTracker.class);

        private final ProcessorStatusStream processorStatusStream;

        private final Map<String, Boolean> processorStatusMap = new ConcurrentHashMap<>();

        public ProcessorStatusTracker(ProcessorStatusStream processorStatusStream) {
            this.processorStatusStream = processorStatusStream;
        }

        @StreamListener(ProcessorStatusStream.INPUT)
        public void handleProcessorStatusEvent(ProcessorStatusEvent event) {
            LOGGER.info("Received processor status event: {}", event);
            processorStatusMap.put(event.getProcessorId(), event.isIdle());
        }

        public boolean isIdle(String processorId) {
            return processorStatusMap.getOrDefault(processorId, true);
        }
}
```

But there is another problem. When an ActivityInitializedEvent emits in a short period after idle, we'd rather not start a new processing. So we will need configure the ProcessorStatusTracker to ensure that the processor is idle for a period of time before starting a new processing.

```java
@Component
public class ProcessorStatusTracker {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProcessorStatusTracker.class);

        private final ProcessorStatusStream processorStatusStream;

        private final Map<String, Boolean> processorStatusMap = new ConcurrentHashMap<>();

        private final Map<String, Long> processorStatusTimestampMap = new ConcurrentHashMap<>();

        private final long idleTime;

        public ProcessorStatusTracker(ProcessorStatusStream processorStatusStream, @Value("${processor.idle.time}") long idleTime) {
            this.processorStatusStream = processorStatusStream;
            this.idleTime = idleTime;
        }

        @StreamListener(ProcessorStatusStream.INPUT)
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

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class ProcessorStatusTrackerTest {

    @Autowired
    private ProcessorStatusTracker processorStatusTracker;

    @Autowired
    private ProcessorStatusStream processorStatusStream;

    @Test
    public void testIsIdle() {
        String processorId = "processor-1";
        Assert.assertTrue(processorStatusTracker.isIdle(processorId));

        processorStatusStream.output().send(MessageBuilder.withPayload(new ProcessorStatusEvent(processorId, false)).build());
        Assert.assertFalse(processorStatusTracker.isIdle(processorId));

        processorStatusStream.output().send(MessageBuilder.withPayload(new ProcessorStatusEvent(processorId, true)).build());
        Assert.assertTrue(processorStatusTracker.isIdle(processorId));
    }

    @Test
    public void testIsBusyWhenActivityInitialized() {
        String processorId = "processor-1";
        Assert.assertTrue(processorStatusTracker.isIdle(processorId));

        processorStatusStream.output().send(MessageBuilder.withPayload(new ProcessorStatusEvent(processorId, false)).build());
        Assert.assertFalse(processorStatusTracker.isIdle(processorId));

        processorStatusStream.output().send(MessageBuilder.withPayload(new ProcessorStatusEvent(processorId, true)).build());
        Assert.assertTrue(processorStatusTracker.isIdle(processorId));

        // If the processor is idle for a period of time, it will be busy when an ActivityInitializedEvent emits
        processorStatusStream.output().send(MessageBuilder.withPayload(new ActivityInitializedEvent(processorId, "activity-1")).build());
        Assert.assertFalse(processorStatusTracker.isIdle(processorId));
    }

    @Test()
    public void testIsBusyWhenActivityCompleted() {
        String processorId = "processor-1";
        Assert.assertTrue(processorStatusTracker.isIdle(processorId));

        processorStatusStream.output().send(MessageBuilder.withPayload(new ProcessorStatusEvent(processorId, false)).build());
        Assert.assertFalse(processorStatusTracker.isIdle(processorId));

        processorStatusStream.output().send(MessageBuilder.withPayload(new ProcessorStatusEvent(processorId, true)).build());
        Assert.assertTrue(processorStatusTracker.isIdle(processorId));

        // If the processor is idle for a period of time, it will be busy when an ActivityCompletedEvent emits
        processorStatusStream.output().send(MessageBuilder.withPayload(new ActivityCompletedEvent(processorId, "activity-1")).build());
        Assert.assertTrue(processorStatusTracker.isIdle(processorId));
    }
}
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
