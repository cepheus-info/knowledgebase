# Gradle build maxerrs

## Problem and Solution

Gradle build show max 100 errs by default, if you want to show more, you can add the following code to your build.gradle file.

```groovy
afterEvaluate {
    tasks.withType(JavaCompile) {
        options.compilerArgs << "-Xmaxerrs" << "20000"
    }
}
```
