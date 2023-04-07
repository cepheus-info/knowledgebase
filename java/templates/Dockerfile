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
