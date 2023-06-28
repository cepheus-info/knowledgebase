# How Event-Driven Architecture resolves the challenges of complexity, scalability, and reliability

## Complexity

### Monolithic architecture

In a Monnolithic architecture, the scailability of the application is limited by the capacity of the server. If the server is overloaded, the application will crash. The only way to scale the application is to add more servers. This is not a good solution because it is expensive and it is not easy to manage.

The domain models were split into different modules, but the application is still monolithic. The modules are tightly coupled and they share the same database. The modules are not independent and they cannot be deployed independently.

The communication between the modules is done via the database, method calls. When an operation is invoked, the calling chains are very long. The application is very complex and it is difficult to understand the flow of the application.
A change in one module can affect other modules. The application is not flexible and it is difficult to add new features.

### Microservices architecture

In a Microservices architecture, the application is split into multiple services. Each service is a separate application and it can be deployed independently. The services are loosely coupled and they communicate via messages, rpc calls, rest APIs. The services are independent and they can be developed, deployed and scaled independently.

However, the Microservices architecture is more complex than the Monolithic architecture. The communication between the services is done via messages. Asynchronous and the flow of the application is not easy to understand. The application is distributed and it is difficult to debug and test.

### Event-Driven architecture

Let's explain a business scenario and implement it using a CRUD approach. The business scenario is about an Employee Salary Management application. The application has the following feature:

When a staff is created by a system administrator in an organization, the `StaffManagement` service will create the staff, persit all of the related information like Education Background, Position History, Working History, Annual Assessment History.

And then, a transaction history record will be created as well because we need to keep track of all the changes that are made to the staff member.

At the same time, an initial payroll record will be created because the fund needs to be allocated to the staff member.

In the end, a salary measurement is calculated and the records are persisted.

> After digging into the business scenario, we can find it is not a simple CRUD operation. It is a business process. The CRUD approach is not suitable for implementing this business scenario.

In CQRS, we can use the Aggregate to model the related entities. The Aggregate Root is the Staff entity. The Staff entity is responsible for creating the related entities and raising a Domain Event to tell other services that the staff is created. When an event sourcing approach is in place, we even don't need to persist the related entities. We can just store the Domain Event itself.

In other services, we can subscribe to the Domain Event and do whatever the Context cares about.
For example, the `TransactionHistory` service can subscribe to the `StaffCreated` event and create a transaction history record.
The `Payroll` service can subscribe to the `StaffCreated` event and create an initial payroll record.
The `SalaryMeasurement` service can subscribe to the `StaffCreated` event and calculate the salary measurement.
And the `StaffManagement` service itself can also subscribe to the `StaffCreated` event and do the persistence logic now.

The Domain Event itself is the source of truth. The Domain Event is immutable and it cannot be changed. Even if the `Payroll` service and `SalaryMeasurement` service is not implemented yet, the whole business process can still work. And as a plus, the business process is very easy to understand.

> The domain layer is cohesive and only cares about the core business, on the other hand, the read model is decoupled from the domain layer and only cares about the `Materialized View`. An Eventual Consistency approach is used to synchronize the read model with the domain layer. The default approach is via Retry. The read model will retry applying the domain event until it succeeds.

> In a more complex scenario, we can use a Saga to coordinate the business process, or use a technical distributed transaction to ensure the consistency of the data, such as the 2PC protocol, TCC.
