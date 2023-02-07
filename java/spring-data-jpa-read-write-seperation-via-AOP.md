# Spring Data JPA read write seperation via AOP

## 1. Overview

Read Write Seperation is a common strategy which make use of Multiple Data Sources to Load Balance the client requests to Database.

Spring Data JPA generally uses a AbstractRoutingDataSource class to achieve that purpose.

## 2. Steps & Details

### 2.1 Structure

We provide a simple example to demonstrate the implementations with a structure as below. Note: this only contains the src/main folder which is not a full versioned project.

```bash
.
├── java
│   └── info
│       └── cepheus
│           └── read_write_seperation_sample
│               ├── api
│               │   └── PersonInformationController.java
│               ├── application
│               │   ├── PersonInformationRepository.java
│               │   └── PersonInformationService.java
│               ├── config
│               │   ├── dynamicDataSource
│               │   │   ├── DynamicDataSourceAspect.java
│               │   │   ├── DynamicDataSourceConfig.java
│               │   │   ├── DynamicDataSourceHolder.java
│               │   │   ├── DynamicDataSource.java
│               │   │   └── TargetDataSource.java
│               │   ├── entityManager
│               │   │   └── EntityManagerFactoryConfig.java
│               │   └── pooledDataSource
│               │       ├── MultipleDataSourceProperties.java
│               │       └── MultipleSimpleDataSourceConfig.java
│               ├── domain
│               │   └── PersonInformation.java
│               └── ReadWriteSeperationSampleApplication.java
└── resources
    ├── application.properties
```

- api: contains Rest Controller
- application: contains application related services & interfaces
- config: contains spring boot configuration related classes
- domain: contains Entity classes

### 2.2 Configure SimpleDataSource for multiple connections

As we are using different connection to seperate read & write access, it must be configured before we could use.

MultipleDataSourceProperties.java is just a config placeholder for application.properties => spring.datasource part.
e.g. We can use multipleDataSourceProperties.write to represent spring.datasource.write object in application config.

```java
@Data
@Configuration
@ConfigurationProperties(prefix = "spring.datasource")
public class MultipleDataSourceProperties {
    private DataSourceProperties write = new DataSourceProperties();
    private DataSourceProperties read = new DataSourceProperties();
}
```

MultipleSimpleDataSourceConfig.java is a configuration class to define multiple DataSource Beans hold the physical connection. As we're not using connection pool in this demo, the connection might behaved differently than a normal AutoConfigured DataSource.

### 2.3 Configure AbstractRoutingDataSource

This part consists of below parts:

1. AbstractRoutingDataSource Bean
2. ThreadLocal based DynamicDataSourceHolder
3. Annotation & AOP

#### 2.3.1 AbstractRoutingDataSource Bean

To instantiate an AbstractRoutingDataSource Bean, we must make a implementation class of it first.

We just need to provide a determineCurrentLookupKey method to get the real context we are using.

DynamicDataSource.java:

```java
public class DynamicDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        // You can do 1 A simple load balancing strategy
        String lookupKey = DynamicDataSourceHolder.getDataSource();
        System.out.println("------------lookupKey---------"+lookupKey);
        return lookupKey;
    }

}
```

The AbstractRoutingDataSource Bean is defined in DynamicDataSourceConfig.java.
Please note that we just created a default DataSource router which contains a map of physical datasources & a method to determine key.
The abstract class itself will call our determine method to load the correct DataSource.

```java
@Configuration
public class DynamicDataSourceConfig {
    private final static String WRITE_DATASOURCE_KEY = "writeDataSource";
    private final static String READ_DATASOURCE_KEY = "readDataSource";

    @Bean
    public AbstractRoutingDataSource routingDataSource(
            @Qualifier(READ_DATASOURCE_KEY) DataSource readDataSource,
            @Qualifier(WRITE_DATASOURCE_KEY) DataSource writeDataSource
    ) throws Exception {
        DynamicDataSource dataSource = new DynamicDataSource();
        Map<Object, Object> targetDataSources = new HashMap();
        targetDataSources.put(WRITE_DATASOURCE_KEY, writeDataSource);
        targetDataSources.put(READ_DATASOURCE_KEY, readDataSource);
        dataSource.setTargetDataSources(targetDataSources);
        dataSource.setDefaultTargetDataSource(writeDataSource);
        return dataSource;
    }
}
```

#### 2.3.2 ThreadLocal based DynamicDataSourceHolder

The DynamicDataSourceHolder is the way to store current context information with ThreadLocal.

```java
/**
 * Dynamic DataSource Holder using ThreadLocal
 */
public class DynamicDataSourceHolder {
    // use ThreadLocal Binds the data source to the current thread
    private static final ThreadLocal<String> dataSources = new ThreadLocal<String>();

    public static void setDataSource(String dataSourceName) {
        dataSources.set(dataSourceName);
    }

    public static String getDataSource() {
        return (String) dataSources.get();
    }

    public static void clearDataSource() {
        dataSources.remove();
    }
}
```

#### 2.3.3 Annotation & AOP

We can make use of AOP to simplify the client code using dynamic datasource.

The Annotation: @TargetDataSource

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface TargetDataSource {
    String dataSource() default "";  // The data source
}
```

The Aspect: DynamicDataSourceAspect

> Set ThreadLocal variable lookupKey as the Annotated value

> Clear the value after proceeded method execution

> Implement the Ordered interface so that it will be executed before any @Transactional scope method and before the Session creation.

```java
@Aspect
@Component
public class DynamicDataSourceAspect implements Ordered {

    @Around("@annotation(info.cepheus.read_write_seperation_sample.config.dynamicDataSource.TargetDataSource)")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        MethodSignature methodSignature = (MethodSignature) pjp.getSignature();
        Method targetMethod = methodSignature.getMethod();
        if (targetMethod.isAnnotationPresent(TargetDataSource.class)) {
            String targetDataSource = targetMethod.getAnnotation(TargetDataSource.class).dataSource();
            System.out.println("---------- The data source is :" + targetDataSource + "------");
            DynamicDataSourceHolder.setDataSource(targetDataSource);
        }
        Object result = pjp.proceed();  // Execution method
        DynamicDataSourceHolder.clearDataSource();
        return result;
    }

    @Override
    public int getOrder() {
        return HIGHEST_PRECEDENCE;
    }
}
```

### 2.4 Client code uses the Annotation

The client code needed only simple changes with the AOP's help. And if we ignored these annotation for any methods, the default connection will be used, that is most case the Write-DataSource.

```java
    @TargetDataSource(dataSource = WRITE_DATASOURCE_KEY)
    @Transactional
    public Long create() {
        var person = new PersonInformation();
        person.setStaffName(UUID.randomUUID().toString());
        this.repository.save(person);
        return person.getId();
    }

    @TargetDataSource(dataSource = READ_DATASOURCE_KEY)
    @Transactional
    public PersonInformation find(Long id) {
        return this.repository.findById(id).orElse(null);
    }
```

## Conclusion

Spring Data JPA provided the clear way to use Multiple Datasource & a Routing mechinism to achieve Database load balancing.
We can find some other ways to , e.g.
    
- Hibernate focus on MultiTenantConnectionProvider and CurrentTenantIdentifierResolver (which is used by Quarkus framework).

- In MongoDB, we are considering a Sharding-Key way because it's document based (This is like the Horizontal Seperation)

## Reference

The reference project is hosts at: [lab/read-write-seperation-sample.git](http://gitlab.sfdapp.com/lab/read-write-seperation-sample.git)