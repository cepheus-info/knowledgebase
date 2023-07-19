# Use Sonarqube for lint and security check

## What is Sonarqube?

Sonarqube is a static code analysis tool. It can be used to check the code quality of the project. It can also be used to check the security of the project.

## How to use Sonarqube?

### Install Sonarqube plugin for Jenkins

1. Go to Jenkins > Manage Jenkins > Manage Plugins > Available

2. Search for Sonarqube Scanner

3. Install the plugin

### Configure Sonarqube in Jenkinsfile

1. Add the following code to the Jenkinsfile

```groovy
stage('Sonarqube') {
    steps {
        withSonarQubeEnv('sonarqube') {
            sh 'mvn sonar:sonar'
        }
    }
}
```

2. Add the following code to the Jenkinsfile

```groovy
environment {
    SONARQUBE_SCANNER_HOME = tool 'sonarqube'
}
```

3. Add the following code to the Jenkinsfile

```groovy
tools {
    maven 'maven'
    jdk 'jdk'
    sonarqube 'sonarqube'
}
```
