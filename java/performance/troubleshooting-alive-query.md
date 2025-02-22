We have a Java web application that uses Oracle jdbc to connect to the database. The application is running on Tomcat. The application maintains connections manually. Sometimes users get a connection unused for a long time. The connection is still open but a query might wait for a long time.

In our application, we have a DBAccess object created for every user's session and its pages. If the DBAccess object exists, we use the connection in the object. Every time we use the connection, we check if the connection is still alive. Previously, we executed a query against the particular connection directly, but sometimes the query took more than 15min to complete. If the alive query timed out, we rollback and close on the connection and create a new one. However, this approach is blocking for a long time. And even worse, the user cannot do anything during the blocking time. On the same browser, the user will reuse the same session and being blocked until the connection is reopened.

Recently, we designed a new approach to solve this problem. We submit the alive query to the connection in a ThreadPoolExecutor. If the query is not completed in 30 seconds(via Future.get), a TimeoutException is thrown. We rollback and close the connection and create a new one.

However, during the Performance Test, we found a huge performance degradation. The application was running slower than before. We suspect that the ThreadPoolExecutor is the bottleneck.

The ThreadPoolExecutor is created with the following configuration:

```java
new ThreadPoolExecutor(10, 20, 60L, TimeUnit.SECONDS, new ArrayBlockingQueue<>(200), new ThreadPoolExecutor.CallerRunsPolicy());
```

