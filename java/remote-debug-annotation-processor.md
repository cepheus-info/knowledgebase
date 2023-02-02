# Remote debug annotation processor

## Introduction
Annotation processors are used to process/generate code at compile time. This is a very useful feature, but it can be difficult to debug. This article will show you how to debug an annotation processor.

## Prerequisites
* IDE: IntelliJ IDEA
* Gradle: 7.5+
* JDK: 11+

## Create a project com.example.annotation which contains a custom annotation & annotation processor 
1. Create a new project with Gradle and Java.
2. File Structure is as below:
```
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── settings.gradle
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── example
    │               └── annotation
    │                   ├── DemoAnnotation.java
    │                   └── DemoAnnotationProcessor.java
    |                    
```
3. Create a class `DemoAnnotation.java` with following content:
```java
package com.example.demo;

import java.lang.annotation.*;

@Target(value = ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Constraint(validatedBy = {})
public @interface DemoAnnotation {
    String value() default "default";
}
```
4. Create a class `DemoAnnotationProcessor.java` with the following content:
```java
package com.example.demo;

import com.google.auto.service.AutoService;

import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.Element;
import javax.lang.model.element.ElementKind;
import javax.lang.model.element.PackageElement;
import javax.lang.model.element.TypeElement;
import javax.tools.Diagnostic;
import java.util.Properties;
import java.util.Set;

@AutoService(Processor.class)
@SupportedAnnotationTypes(value = {"com.example.demo.DemoAnnotation"})
@SupportedSourceVersion(SourceVersion.RELEASE_11)
public class DemoAnnotationProcessor extends AbstractProcessor {

    public DemoAnnotationProcessor() {
        super();
    }

    @Override
    public boolean process(Set<? extends TypeElement> annotations,
                           RoundEnvironment roundEnv) {
        String className = null;
        String packageName = null;
        String fqClassName = null;
        processingEnv.getMessager().printMessage(Diagnostic.Kind.ERROR, "Processing annotations...");
        // ... todo: the real processing logic
        // ...
        return false; // no further processing of this annotation type
    }
}
```
## Create a project named com.example.demo depends on com.example.annotation
1. File structure is as below:
```
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── settings.gradle
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── example
    │               └── demo
    │                   ├── DemoApplication.java
    │                   └── DemoService.java
    |                   
    |                    
```
2. Create class DemoService with below content:
```java
package com.example.demo;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.example.annotation;

@Slf4j
@Component
@RequiredArgsConstructor
public class DemoService {

    @DemoAnnotation
    public void process() {
        log.warn("process executed:");
    }
}
```

## Create remote debug configuration in IDEA
1. Choose Run -> Edit Configurations -> Add -> Remote Jvm Debug
![Remote Debug Configuration](images/remote-debug-configuration.png)

2. Set the port to 5005, and click OK

3. Set a breakpoint in DemoAnnotationProcessor.java

## Run the annotation processor via gradle
1. Run `./gradlew build` in the com.example root project
```bash
./gradlew build -Dorg.gradle.debug=true --no-daemon
```
The terminal will be suspended to wait for the remote debug connection.

2. Run the remote debug configuration in IDEA
You will see the following output:
```bash
> Task :com.example.demo:compileJava
Processing annotations...
```

And the breakpoint in `DemoAnnotationProcessor.java` will be hit.

## Conclusion
In this article, we have learned how to debug an annotation processor.