# Spring Boot Best Practices

## 1. Project Structure

- Do create resuable modules for common functionalities, you can use a spring-boot like naming convention for modules, e.g. `common`, `common-autoconfigure`, `common-starter`.

  - `common` module for common functionalities
  - `common-autoconfigure` module for auto-configuration of common functionalities
  - `common-starter` module for starter of common functionalities

  > This is the most important magic of spring-boot, to make a project and its dependencies easy to use.

- Do use `@ConfigurationProperties` to bind properties to POJOs.

- Do use mono-repo for high cohesion microservices, you can use multi-module project and git submodule to achieve this.

- Do extract build.conventions to built-in module buildSrc or custom specific module for common build logic.
  Add common dependencies in your conventions file, rather than add dependencies in each module or parent module.

- Do use dependency management for 3rdparty dependencies.

- Do not commit application-local.properties{yml} to git, use application-local.properties{yml}.template instead.

- Do use Clean Architecture to design your module structure.

  - `api` package for service interfaces layer
  - `application` package for application layer
  - `domain` package for domain layer
  - `infrastructure` package for infrastructure layer
  - `coreapi` package for core api layer
  - `config` package for configuration
  - `util` package for utilities
  - `exception` package for exceptions
  - `constant` package for constants
  - ..., etc.

  And for high cohesion, you can feel free to add portable packages inside each layer.

- Do use package-by-feature for high cohesion microservices and do not use package-by-layer.
  N-layer architecture is not suitable for microservices.

- Do Use layered jar for build image and deployment.
  This is because a docker image is a layered filesystem, the dependencies of your application should be in its own layer, so that you can reuse the layer when you build another version of image. So do the snapshot dependencies.

## 2. Divide

- Choose below Microservice Design Patters carefully and use them effeciently for complex microservices:

  - Domain Driven Design to design your domain model. (DDD)

  - Event Driven Architecture. (EDA)

  - Command and Query Responsibility Seperation. (CQRS)

  - Event Sourcing. (ES)

  > Note that, you should consider the cost of using these patterns, and choose the right one for your project. For simple CRUD microservices, it's not necessary to use these patterns.

- Modeling your business into below subdomains:

  - Core Domain: the most important domain of your business, it's the core of your business, and it's the most valuable domain of your business.

  - Supporting Domain: the domain that supports your core domain, it's not the core of your business, but it's necessary for your business.

  - Generic Domain: the domain that is generic for your business, it's not the core of your business, and it's not necessary for your business.

## 3. Conquer

- Conquer your business with below patterns:

  - Service Discovery and Registration: use docker swarm or kubernetes you can easily achieve this.

  - Resilience: use resilience4j.

    - Retry: retry with exponential backoff for idempotent operations & possibly successful operations.

    - Timeout: use timeout for all asynchronous operations, this is very important for microservices.

    - Bulkhead: use bulkhead to limit the number of concurrent requests and to keep the system stable.

    - Circuit Breaker: use circuit breaker to limit the number of failed requests and to fail fast.

    - Rate Limiter: use rate limiter to limit the number of requests per second to achieve more thoughput.

    - Throttling: use throttling to limit the number of requests per user to achieve more thoughput.

    - Fallback: use fallback to provide default value or default behavior when the main operation fails.

  - Distributed Tracing: use zipkin or jaeger.

  - Distributed Lock: use redis or zookeeper.

  - Distributed Cache: use redis or hazelcast.

  - Distributed Message: use kafka or rabbitmq.

  - Distributed Transaction: choose different solutions for different scenarios.

    - Saga: use saga for long running transactions. (This involves a lot of work, so you should consider the cost of using this solution)

    - TCC: use tcc for short running transactions. (This is a good solution for much of scenarios, it's a balance between cost and benefit)

    - XA: use xa for transactions that involve multiple relational databases. (There might be some performance issues when chosen the original XA solution)

    - 2PC: there's an AT mode in Seata framework, it's an improved version of XA, you can use it for transactions that involve multiple relational databases. (Undo log is used for compensation, so there is a performance boost when compared to XA)

## 4. Database considerations

- Do use relational database for transactional data.

- Do use NoSQL database for non-transactional data.

- Do use distributed database for high availability.

- Do use database sharding for high scalability.

- Do use database replication for high availability.

- Do use database cache for high performance.

- Do use database index for high performance.

### 4.1. Transactions

Transaction isolation levels:

- Read Uncommitted: dirty read, non-repeatable read, phantom read.

- Read Committed: non-repeatable read, phantom read.

- Repeatable Read: phantom read.
  Note: In MySQL Innodb, the default isolation level is Repeatable Read. And the phantom read is avoided by gap lock.

- Serializable: no dirty read, no non-repeatable read, no phantom read. (This is the highest isolation level, and it's not recommended to use this level in production environment, because it will cause a lot of performance issues.)

Locks:

- Shared Lock: read lock, multiple shared locks can be held on the same resource.

- Exclusive Lock: write lock, only one exclusive lock can be held on the same resource.

- Gap Lock: gap lock is a kind of shared lock, it's used to avoid phantom read.

- Next-Key Lock: next-key lock is a kind of gap lock, it's used to avoid phantom read.

- Record Lock: record lock is a kind of exclusive lock, it's used to avoid dirty read and non-repeatable read.

- Insert Intention Lock: insert intention lock is a kind of shared lock, it's used to avoid phantom read.

- Auto-Increment Lock: auto-increment lock is a kind of exclusive lock, it's used to avoid phantom read.
