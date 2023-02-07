---
title: Quarkus Integration with Axon Server
description: 
published: true
date: 2021-11-08T08:19:31.913Z
tags: 
editor: markdown
dateCreated: 2021-11-08T03:18:26.575Z
---

# Testing with axon-server-connector

## Prepare quarkus environment
quarkus-cli depends on maven, so we install maven globally first.
```shell
# Install Chocolatey on windows.
# Install maven using Chocolatey on windows with Administrative rights.
~$ choco install maven
```

## Initialize a quarkus project with command
```shell
~$ mvn io.quarkus.platform:quarkus-maven-plugin:2.4.1.Final:create "-DbuildTool=gradle" "-Dextensions=resteasy,resteasy-jackson"
```

## project dependency
add axon-server-connector dependency via build.gradle
```groovy
dependencies {
		// omit other dependencies
    implementation 'org.axonframework:axon-server-connector:4.5.4'
    
    // note this could also be done via .\gradlew addExtension --extensions=spring-boot-properties
    implementation 'io.quarkus:quarkus-spring-boot-properties'
}
```

## Test connectivity
	
We found that this property does not work when using in quarkus project.
After further investgating, we know this connector depends on spring boot properties configuration. So we rolled up a sample class exactly the same as AxonServerConfiguration.
  
```java
@Typed()
@ApplicationScoped
public class AxonConfiguration {
// omit other codes

    @Inject
    MyAxonServerConfiguration myAxonServerConfiguration;
}
```

This time we know the AxonServerConfiguration class does not contains a setEventCipher method, so the spring properties could not be loaded via quarkus function.

## Modify the axon-server-connector.jar

The implementation in axon referenced the concreted AxonServerConfiguration class, so the only way to change this behavior is to change the class and recompile it.

- Decompile the jar via fernflower
  1. Find java-decompiler.jar in \JetBrains\IntelliJ IDEA version\plugins\java-decompiler\lib
  2. Copy java-decompiler.jar to an empty folder and rename to fernflower.jar for a better readability.
  3. Create a decompile.cmd with content below, and then add this decompile.cmd foler into system environment.
  ```shell
	java -cp "%~dp0\fernflower.jar" org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -hdc=0 -dgs=1 -rsy=1 -rbr=1 -lit=1 -nls=1 -mpm=60 %~f1 %~f2
	powershell -Command "Rename-Item %~f2%~nx1 -NewName %~n1.zip "
	powershell -Command "Expand-Archive %~f2%~n1.zip %~f2 "
	powershell -Command "Remove-Item %~f2%~n1.zip "
  ```
  4. Run below command to decompile axon-server-connector.jar
  ```shell
  mkdir temp
  decompile.cmd .\axon-server-connector.jar .\temp\
  ```
  5. Create an empty java project with the pom.xml inside META-INF, copy the source code in .\temp\ into proper src\main\java.
  
     We need to modify some java files to build correctly.
  6. Build again via maven:jar plugin inside Maven panel.
  
## Publish modified jar to mavenLocal
  - Init project with gradle init
  ```shell
  gradle init
  ```
  - Publish to mavenLocal
  Refer to [https://www.jetbrains.com/help/idea/add-a-gradle-library-to-the-maven-repository.html](https://www.jetbrains.com/help/idea/add-a-gradle-library-to-the-maven-repository.html)

## Modify build.gradle in your application

Exclude module org.axonframework:axon-server-connector so that we could use a local package rather than the one in mavenCentral.
  ```groovy
  repositories {
      mavenLocal()
      mavenCentral {
          content {
              excludeModule("org.axonframework", "axon-server-connector")
          }
      }
  }
  ```
## Rerun application
  