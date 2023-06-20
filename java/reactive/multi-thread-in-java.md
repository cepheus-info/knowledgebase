# Multi Thread In Java

## 1. Overview

A thread is a thread of execution in a program. The Java Virtual Machine allows an application to have multiple threads of execution running concurrently.

Every thread has a priority. Threads with higher priority are executed in preference to threads with lower priority. Each thread may or may not also be marked as a daemon. When code running in some thread creates a new Thread object, the new thread has its priority initially set equal to the priority of the creating thread, and is a daemon thread if and only if the creating thread is a daemon.

When a Java Virtual Machine starts up, there is usually a single non-daemon thread (which typically calls the method named main of some designated class). The Java Virtual Machine continues to execute threads until either of the following occurs:

## 2. Thread States

A thread can be in one of the following states:

- NEW
  A thread that has not yet started is in this state.
- RUNNABLE
  A thread executing in the Java virtual machine is in this state.
- BLOCKED
  A thread that is blocked waiting for a monitor lock is in this state.
- WAITING
  A thread that is waiting indefinitely for another thread to perform a particular action is in this state.
- TIMED_WAITING
  A thread that is waiting for another thread to perform an action for up to a specified waiting time is in this state.
- TERMINATED
  A thread that has exited is in this state.

Above states are defined in `java.lang.Thread.State` enum.

How to get current thread state?

```java
Thread.State state = Thread.currentThread().getState();
```

How will a thread change its state?

- NEW -> RUNNABLE
  When a thread is created, it is in the NEW state. When `start()` method is called, it will change to RUNNABLE state.

- RUNNABLE -> BLOCKED
  When a thread is waiting for a monitor lock, it will change to BLOCKED state. When the thread gets the lock, it will change back to RUNNABLE state.

- RUNNABLE -> WAITING
  When a thread is waiting for another thread to perform a particular action, it will change to WAITING state. When the thread is notified, it will change back to RUNNABLE state.

- RUNNABLE -> TIMED_WAITING
  When a thread is waiting for another thread to perform a particular action for up to a specified waiting time, it will change to TIMED_WAITING state. When the thread is notified or the waiting time is over, it will change back to RUNNABLE state.

- RUNNABLE -> TERMINATED
  When a thread has exited, it will change to TERMINATED state.

### 2.1. Thread States Example

```java
public class ThreadStatesExample {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            System.out.println("Hello World!");
        });

        System.out.println("Thread state: " + thread.getState());

        thread.start();

        System.out.println("Thread state: " + thread.getState());

        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Thread state: " + thread.getState());
    }
}
```

Output:

```
Thread state: NEW
Thread state: RUNNABLE
Hello World!
Thread state: TERMINATED
```

### 2.2. Thread States Example 2

```java
public class ThreadStatesExample2 {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            synchronized (ThreadStatesExample2.class) {
                try {
                    Thread.sleep(1000);
                    ThreadStatesExample2.class.notify();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        System.out.println("Thread state: " + thread.getState());

        thread.start();

        System.out.println("Thread state: " + thread.getState());

        synchronized (ThreadStatesExample2.class) {
            try {
                ThreadStatesExample2.class.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println("Thread state: " + thread.getState());
    }
}
```

Output:

```
Thread state: NEW
Thread state: RUNNABLE
Thread state: TIMED_WAITING
```

### 2.3. synchronized & lock

#### 2.3.1. synchronized

synchronized is a keyword in Java. It is used to control access to a shared resource by multiple threads.

An example of synchronized:

```java
public class SynchronizedExample {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public static void main(String[] args) throws InterruptedException {
        SynchronizedExample example = new SynchronizedExample();

        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                example.increment();
            }
        });

        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                example.increment();
            }
        });

        thread1.start();
        thread2.start();

        thread1.join();
        thread2.join();

        System.out.println("Count: " + example.count);
    }
}
```

Output:

```
Count: 20000
```

#### 2.3.2. lock

Lock is an interface in Java. It is used to control access to a shared resource by multiple threads.

An example of lock:

```java
public class LockExample {
    private int count = 0;
    private Lock lock = new ReentrantLock();

    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        LockExample example = new LockExample();

        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                example.increment();
            }
        });

        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                example.increment();
            }
        });

        thread1.start();
        thread2.start();

        thread1.join();
        thread2.join();

        System.out.println("Count: " + example.count);
    }
}
```

Output:

```
Count: 20000
```

#### 2.3.3. synchronized vs lock

The main differences between synchronized and lock are:

- synchronized is a keyword in Java, while lock is an interface in Java.
- synchronized is a built-in feature in Java, while lock is not.
- synchronized is not extendable, while lock is extendable.
- synchronized is not interruptible, while lock is interruptible.
- synchronized is not fair, while lock is fair.
- synchronized is not able to try to acquire a lock, while lock is able to try to acquire a lock.
- synchronized is not able to acquire a lock with a timeout, while lock is able to acquire a lock with a timeout.

Q: How to choose between synchronized and lock?

A: If you don't need to extend lock, don't need to interrupt lock, don't need to make lock fair, don't need to try to acquire a lock, don't need to acquire a lock with a timeout, then use synchronized. Otherwise, use lock.

Q: Does synchronized use lock?

A: Yes, synchronized uses lock internally. The lock used by synchronized is called monitor lock.

Q: What is monitor lock?

A: Monitor lock is a lock that is used by synchronized internally. It is implemented by wait/notify mechanism.

Q: Will a thread release monitor lock when it is interrupted?

A: No, a thread will not release monitor lock when it is interrupted. It will throw InterruptedException instead. If you want to release monitor lock when a thread is interrupted, you need to use lock.

Q: How to handle InterruptedException gracefully?

A: You can either re-interrupt the thread or restore the interrupt status of the thread. For example:

```java
public class InterruptedExceptionExample {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
                // Restore the interrupt status of the thread.
                Thread.currentThread().interrupt();
            }
        });

        thread.start();

        thread.interrupt();

        thread.join();
    }
}
```

Q: What is the use case of interrupting a thread?

A: Interrupting a thread is used to cancel a thread. For example:

```java
public class InterruptingThreadExample {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                System.out.println("Hello World!");
            }
        });

        thread.start();

        Thread.sleep(1000);

        thread.interrupt();

        thread.join();
    }
}
```

Q: What is the use case of join()?

A: join() is used to wait for a thread to finish. For example:

```java
public class JoinExample {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

        thread.start();

        thread.join();
    }
}
```

## 3. Thread Usage

There are two ways to create a thread in Java:

- Extend Thread class.

```java
public class ThreadExample extends Thread {
    @Override
    public void run() {
        System.out.println("Hello World!");
    }

    public static void main(String[] args) {
        ThreadExample thread = new ThreadExample();
        thread.start();
    }
}
```

- Implement Runnable interface.

```java
public class ThreadExample implements Runnable {
    @Override
    public void run() {
        System.out.println("Hello World!");
    }

    public static void main(String[] args) {
        Thread thread = new Thread(new ThreadExample());
        thread.start();
    }
}
```

## 4. Thread Pool

Thread pool is a pool of threads that can be reused to execute tasks.

There are two ways to create a thread pool in Java:

- Use Executors helper class.

```java
public class ThreadPoolExample {
    public static void main(String[] args) {
        // Create a single thread pool.
        // ExecutorService executorService = Executors.newSingleThreadExecutor();
        // Create a thread pool with 10 threads.
        ExecutorService executorService = Executors.newFixedThreadPool(10);
        // Create a thread pool with as many threads as needed.
        // ExecutorService executorService = Executors.newCachedThreadPool();

        executorService.submit(() -> {
            System.out.println("Hello World!");
        });

        executorService.shutdown();
    }
}
```

> This is not recommended because Executors helper class does not provide a lot of flexibility. For example, you cannot specify the maximum number of threads in the thread pool.

- Use ThreadPoolExecutor.

```java
public class ThreadPoolExample {
    public static void main(String[] args) {
        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
                10, // corePoolSize
                10, // maximumPoolSize
                0,  // keepAliveTime
                TimeUnit.MILLISECONDS,  // unit
                new LinkedBlockingQueue<>(),  // workQueue
                Executors.defaultThreadFactory(),  // threadFactory
                new ThreadPoolExecutor.AbortPolicy()  // handler
        );

        threadPoolExecutor.submit(() -> {
            System.out.println("Hello World!");
        });

        threadPoolExecutor.shutdown();
    }
}
```

> However, this is not recommended either because it is too verbose. You can use ThreadPoolBuilder to build a thread pool instead.

- Use ThreadPoolBuilder.

```java
public class ThreadPoolExample {
    public static void main(String[] args) {
        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolBuilder()
                .setCorePoolSize(10)
                .setMaximumPoolSize(10)
                .setKeepAliveTime(0)
                .setUnit(TimeUnit.MILLISECONDS)
                .setWorkQueue(new LinkedBlockingQueue<>())
                .setThreadFactory(Executors.defaultThreadFactory())
                .setHandler(new ThreadPoolExecutor.AbortPolicy())
                .build();

        threadPoolExecutor.submit(() -> {
            System.out.println("Hello World!");
        });

        threadPoolExecutor.shutdown();
    }
}
```

## 5. Future, CompletableFuture, and CompletionService

### 5.1. Future

Future is a placeholder for a result that will be available in the future.

```java
public class FutureExample {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        Future<String> future = executorService.submit(() -> {
            Thread.sleep(1000);
            return "Hello World!";
        });

        System.out.println(future.get());

        executorService.shutdown();
    }
}
```
