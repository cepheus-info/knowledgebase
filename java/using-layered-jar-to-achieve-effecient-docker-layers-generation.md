# Using layered jar to achieve efficient docker layers generation

## Problem

You want to push a docker image to a docker registry, but the image is too large. You want to reduce the size of the image.

As an example, we will use the [Dockerfile](./templates/Dockerfile) file to demonstrate how to use layered jar to achieve efficient docker push.

> Note: This is only for Spring Boot application as Quarkus has already implemented this feature via not using fat jar.

## Solution

### 1. Change the build.gradle

Add below config into build.gradle for your Spring Boot applications. You can configure it in your root-level build.gradle or [buildSrc conventions script](./templates/smso-vnext.java-conventions.gradle) as well.

```groovy
tasks.named('bootJar') {
    layered {
        enabled = true
        includeLayerTools = true
    }
}
```

### 2. Prepare the Dockerfile

```dockerfile
# Buildtime stage to package dockerize for HEALTHCHECK
FROM powerman/dockerize AS dockerize
RUN chmod a+x /usr/local/bin/dockerize

# Buildtime stage to extract the jar file and dependencies
FROM eclipse-temurin:17-jre-alpine AS builder
ARG JAR_FILE=build/libs/person-management-service-0.0.1-SNAPSHOT.jar
COPY ${JAR_FILE} application.jar
RUN java -Djarmode=layertools -jar application.jar extract

# Runtime stage to run the application
FROM eclipse-temurin:17-jre-alpine
RUN apk add --no-cache libstdc++

## Copy dockerize from buildtime stage
COPY --from=dockerize /usr/local/bin/dockerize /usr/bin/dockerize

## Copy the extracted application files
COPY --from=builder dependencies/ ./
COPY --from=builder snapshot-dependencies/ ./
COPY --from=builder spring-boot-loader/ ./
COPY --from=builder application/ ./

## Set the entrypoint to the spring boot loader
CMD java ${JAVA_OPTS} -Dspring.profiles.active=${SPRING_PROFILES_ACTIVE} "org.springframework.boot.loader.JarLauncher"

## Add a healthcheck to the container
HEALTHCHECK --start-period=60s --interval=5s --retries=12 --timeout=5s CMD ["dockerize", "-timeout", "5s", "-wait", "http://localhost:8080/actuator/health", "-exit-code", "1"]
```

> Note: The jre/jdk image were imported twice. The first one is for extracting the jar file and dependencies. The second one is for running the application.

> Note: the entrypoint is set to `org.springframework.boot.loader.JarLauncher` instead of a jar file as the jar file is extracted into the image.

## Conclusion

As Docker uses Layered File System, the network bandwidth is reduced when pushing the image to the registry.

The startup time is also reduced as the dependencies are extracted into the image.

## References

- [Spring Boot Reference Guide](https://docs.spring.io/spring-boot/docs/current/reference/html/appendix-executable-jar-format.html#executable-jar-layers)
