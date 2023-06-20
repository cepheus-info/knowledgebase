# Concurrent, Parallel, Asynchronous and Reactive

## Overview

These terms are often used interchangeably, but they are not the same thing. This article will explain the differences between them.

### Distinguishing between Concurrent, Parallel, Asynchronous and Reactive

#### Concurrent

Concurrent means that multiple operations are executing simultaneously, but it is possible that only one is executing at any given time. This requires a single processor or a single core in a processor. The operations may be started at different times, but they are all executing at the same time. This is usually implemented by using time-slicing, where each operation is given a short time to execute before it is interrupted and another operation is given a chance to execute.

Refer to [Multi-threading in Java](./multi-thread-in-java.md) for more details.

#### Parallel

Parallel means that multiple operations are executing simultaneously. This requires multiple processors or multiple cores in a processor. The operations may be started at different times, but they are all executing at the same time.

#### Asynchronous

Asynchronous means that the result of an operation is not immediately available. The operation is started, and the program continues to execute. The result of the operation may become available later, and a callback mechanism can be used to handle the result. This is also known as non-blocking.

#### Reactive

Reactive means that the result of an operation is not immediately available. The operation is started, and the program continues to execute. The result of the operation may become available later, and a callback mechanism can be used to handle the result. This is also known as non-blocking. The difference between Reactive and Asynchoronous is that Reactive is a programming model, while Asynchronous is an implementation detail. Reactive programming is a programming paradigm oriented around data flows and the propagation of change. This means that it should be possible to express static or dynamic data flows with ease in the programming languages used, and that the underlying execution model will automatically propagate changes through the data flow. It could also be expressed as a programming model for asynchronous data streams with non-blocking backpressure.
