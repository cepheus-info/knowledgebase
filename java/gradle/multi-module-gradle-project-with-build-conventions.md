# Multi module gradle project with build conventions & buildSrc

## 1. Introduction

Gradle is a build tool that can be used to build multi module projects. We need to define the root project and the sub projects. The root project is the parent project and the sub projects are the child projects. The sub projects can have dependencies on each other.

## 2. Project structure

### 2.1. File structure

The project structure is as follows:

```bash
    multi-module-gradle-project-with-build-conventions
    ├── buildSrc
    │   ├── build.gradle
    │   ├── settings.gradle
    │   └── src
    │       └── main
    │           └── groovy
    │               └── com.example.build-conventions.gradle
    ├── settings.gradle
    └── sub-project-1
        ├── build.gradle
        ├── settings.gradle
        └── src
            └── main
                └── java
                    └── com
                        └── example
                            └── subproject1
                                └── App.java
```

### 2.2. Root project

The root project is the parent project. It is defined in the `settings.gradle` file. The root project is defined as follows:

```groovy
rootProject.name = 'multi-module-gradle-project-with-build-conventions'
```

The build.gradle file of the root project is as follows(Optional, you can omit it if you can build the project without it):

```groovy
group 'com.example'
version '0.0.1-SNAPSHOT'
```

### 2.3. Sub projects

The sub projects are the child projects. They are defined in the `settings.gradle` file. The sub projects are defined as follows:

```groovy
rootProject.name = 'multi-module-gradle-project-with-build-conventions'
# append the sub projects
include 'sub-project-1'
```

## 3. Preparing Build conventions

The build conventions are defined in the `buildSrc` directory. The `buildSrc` directory is a special directory that is used to define the build conventions. The build conventions are defined in the `build.gradle` file and the `com.example.build-conventions.gradle` file.

### 3.1. buildSrc/build.gradle

The `build.gradle` file is as follows:

```groovy
plugins {
    id 'groovy-gradle-plugin'
}

repositories {
    mavenCentral()
    gradlePluginPortal()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-gradle-plugin:2.7.9'
    implementation 'io.spring.gradle:dependency-management-plugin:1.1.0'
    // org.graalvm.buildtools.native is not available in the Gradle Plugin Portal so we need to use the Maven Central repository
    // https://mvnrepository.com/artifact/org.graalvm.buildtools.native/org.graalvm.buildtools.native.gradle.plugin
    implementation 'org.graalvm.buildtools.native:org.graalvm.buildtools.native.gradle.plugin:0.9.18'
    implementation 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.10'
}
```

> Note that the dependencies here are only for the plugins that are used in build conventions.

### 3.2. buildSrc/src/main/groovy/com.example.build-conventions.gradle

The `build-conventions.gradle` file is as follows:

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot'
    id 'io.spring.dependency-management'
//  id 'org.graalvm.buildtools.native'
    id 'org.jetbrains.kotlin.jvm'
}

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter'
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.springframework.boot:spring-boot-configuration-processor'
    annotationProcessor 'org.projectlombok:lombok'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'

    implementation 'org.axonframework:axon-spring-boot-starter:4.7.0'
    implementation "org.jetbrains.kotlin:kotlin-stdlib"
}

tasks.named('test') {
    ignoreFailures = true
    useJUnitPlatform()
}
```

> Note that the dependencies here are used for sub projects which reference the build conventions plugin.

### 3.3. Naming convention

There are three ways to define the plugin id. The plugin id is used to reference the build conventions plugin in the sub projects.

#### 3.3.1. Use the default plugin id

The default plugin id is the name of the `build-conventions.gradle` file without `.gradle` part. For this example, the default plugin id is `com.example.build-conventions`.

#### 3.3.2. Define the plugin id in the `buildSrc/build.gradle` file

Every plugin must have a unique name. If you create your BuildConventionsPlugin as a class, the id of the plugin can be defined in the `buildSrc/build.gradle` file as follows:

```groovy
plugins {
    id 'groovy-gradle-plugin'
}

// ...omit other code

gradlePlugin {
    plugins {
        buildConventions {
            id = 'com.example.build-conventions'
            implementationClass = 'com.example.buildconventions.BuildConventionsPlugin'
        }
    }
}
```

#### 3.3.3. Define the plugin name in the `META-INF properties` file

You can also define the plugin name in the `buildSrc/resources/META-INF/gradle-plugins/com.example.build-conventions.properties` file as follows:

```properties
implementation-class=com.example.buildconventions.BuildConventionsPlugin
```

## 4. Using build conventions

The `sub-project-1` is the first sub project. It is defined in the `sub-project-1` directory. The `build.gradle` file is as follows:

```groovy
plugin {
    id 'com.example.build-conventions'
}

group = 'com.example'
version = '0.0.1-SNAPSHOT'

dependencies {
    developmentOnly 'org.springframework.boot:spring-boot-devtools'
    implementation 'org.springframework.boot:spring-boot-starter-data-r2dbc'
    implementation 'org.springframework.boot:spring-boot-starter-graphql'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
    runtimeOnly 'org.postgresql:postgresql'
    runtimeOnly 'org.postgresql:r2dbc-postgresql'
    testImplementation 'io.projectreactor:reactor-test'
    testImplementation 'org.springframework.graphql:spring-graphql-test'
    testImplementation 'org.springframework.security:spring-security-test'

// https://mvnrepository.com/artifact/org.axonframework/axon-spring-boot-starter
    implementation 'org.axonframework:axon-spring-boot-starter:4.7.1'
// https://mvnrepository.com/artifact/org.axonframework.extensions.reactor/axon-reactor-spring-boot-starter
    implementation 'org.axonframework.extensions.reactor:axon-reactor-spring-boot-starter:4.7.0'
}
```

> As you can see, we only declares the dependencies that are only applying to this sub project itself. The common dependencies are comming from pluginDSL block.

## 6. IDEA support

The IDEA support is not working well for the buildSrc project. I'm testing to add the following code to the `settings.gradle` file to make it work:

```groovy
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
    resolutionStrategy {
        eachPlugin {
            if (requested.id.id == 'com.example.build-conventions') {
                useModule("com.example:buildSrc:0.0.1-SNAPSHOT")
            }
        }
    }
}
```

> Note: above code is only for IDEA support. It's not required for the build. And we're not sure if it's a bug of IDEA or Gradle.

## 5. Conclusion

It's much more cleaner to organize your multi-module project with build-conventions provided by buildSrc now.

## 6. Reference

- [Gradle multi module project](https://docs.gradle.org/current/userguide/multi_project_builds.html)

- [Gradle buildSrc](https://docs.gradle.org/current/userguide/organizing_gradle_projects.html#sec:build_sources)

- [Custom Gradle Plugin](https://docs.gradle.org/current/userguide/custom_plugins.html)
