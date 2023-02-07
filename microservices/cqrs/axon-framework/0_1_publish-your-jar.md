---
title: Publish your shared library
description: Packaging and Publish your jar to maven Central
published: true
date: 2021-11-18T10:38:38.758Z
tags: 
editor: markdown
dateCreated: 2021-11-15T19:00:10.866Z
---

## Why?
Since I realized there would be so much infrastructure codes to write before I can config an Axon based service, I decided to wrap them into a common package.

## I. Create a library project

We created a library named cepheus_axon_extension in the following repository: [https://github.com/cepheus-info/cepheus_axon_extension](https://github.com/cepheus-info/cepheus_axon_extension).

### Project Structure
```
.
├── build.gradle
├── gradle
│   └── wrapper
│       └── gradle-wrapper.properties
├── gradle.properties
├── gradle.properties.sample
├── LICENSE
├── README.md
├── settings.gradle
└── src
    ├── main
    │   ├── kotlin
    │   │   └── info
    │   │       └── cepheus
    │   └── resources
    │       └── META-INF
    │           └── beans.xml
    └── test
        ├── kotlin
        └── resources
```
### How to?
The project was created with kotlin template, it's similar to a normal java library project.
```powershell
PS D:\Repos-Library> mkdir showcase_library

    Directory: D:\Repos-Library

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        2021-11-16   7:35 PM                showcase_library

PS D:\Repos-Library> cd .\showcase_library\
PS D:\Repos-Library\showcase_library> gradle init

Select type of project to generate:
  1: basic
  2: application
  3: library
  4: Gradle plugin
Enter selection (default: basic) [1..4] 3

Select implementation language:
  1: C++
  2: Groovy
  3: Java
  4: Kotlin
  5: Scala
  6: Swift
Enter selection (default: Java) [1..6] 4

Select build script DSL:
  1: Groovy
  2: Kotlin
Enter selection (default: Kotlin) [1..2] 1
```

The build.gradle was as below:
```groovy
import javax.naming.ConfigurationException

plugins {
    id 'java-library'
    id 'org.jetbrains.kotlin.jvm' version '1.5.31'
    id 'maven-publish'
    id 'signing'
    id 'org.jetbrains.dokka' version '1.5.31'
}

group = 'info.cepheus'
version = '0.0.1'
archivesBaseName = 'cepheus_axon_extension'

repositories {
    mavenCentral()
}

dependencies {
    implementation enforcedPlatform("${axonPlatformGroupId}:${axonPlatformArtifactId}:${axonPlatformVersion}")
    // omit dependencies...
}

ext {
    it.'signing.secretKeyRingFile' = project.findProperty('signing.secretKeyRingFile')
    it.'signing.password' = project.findProperty('signing.password')
    it.'signing.keyId' = project.findProperty('signing.keyId')
    it.ossrhUsername = project.findProperty('ossrhUsername')
    it.ossrhPassword = project.findProperty('ossrhPassword')
    it.ossrhStagingProfileId = project.findProperty('ossrhStagingProfileId')
}

task javadocJar(type: org.gradle.jvm.tasks.Jar) {
    group 'documentation'
    dependsOn dokkaHtml
    archiveClassifier.set('javadoc')
    from dokkaHtml.outputDirectory
}

publishing {
    publications {
        maven(MavenPublication) {
            groupId 'info.cepheus'
            artifactId 'cepheus_axon_extension'
            version '0.0.1'

            File pomAscFile = null
            pom {
                name = ''
                description = ''
                url = 'https://github.com/{organization}/{repo}'
                organization {
                    name = 'cepheus.info'
                    url = 'https://github.com/{organization}'
                }
                issueManagement {
                    system = 'GitHub'
                    url = 'https://github.com/{organization}/{repo}/issues'
                }
                licenses {
                    license {
                        name = 'MIT License'
                        url = 'https://github.com/{organization}/{repo}/blob/master/LICENSE'
                        distribution = 'repo'
                    }
                }
                developers {
                    developer {
                        id = ''
                        name = ''
                        email = ''
                    }
                }
                scm {
                    url = 'https://github.com/{organization}/{repo}'
                    connection = 'scm:git:git://github.com/{organization}/{repo}.git'
                    developerConnection = 'scm:git:ssh://git@github.com:{organization}/{repo}.git'
                }
            }

            pom.withXml {
                pomAscFile = signPomFile.signatureFiles[0]
            }

            artifacts {
                //noinspection GroovyAssignabilityCheck
                artifact jar
                //noinspection GroovyAssignabilityCheck
                artifact kotlinSourcesJar
                //noinspection GroovyAssignabilityCheck
                artifact javadocJar
                // pom-default.xml.asc
                pomAscFile
            }
        }
    }
    repositories {
        maven {
            name 'ossrh'
            url 'https://s01.oss.sonatype.org/service/local/staging/deploy/maven2/'
            credentials {
                username = ossrhUsername
                password = ossrhPassword
            }
        }
    }
}

/**
 * configure signing plugin including(pom-default.xml, libs/jar)
 */
signing {
    if (project.findProperty('signing.keyId') && project.findProperty('signing.password') && project.findProperty('signing.secretKeyRingFile')) {
        sign publishing.publications.maven
        sign configurations.archives
    } else {
        throw new ConfigurationException('No signing info found.')
    }
}

/**
 * sign pom-default.xml
 */
task signPomFile(type: Sign) {
    sign project.file("$buildDir/publications/maven/pom-default.xml")
    outputs.upToDateWhen { false }
}

/**
 * add dependencies for publishToMavenLocal
 */
tasks.withType(PublishToMavenLocal) {
    dependsOn project.tasks.javadocJar
    dependsOn project.tasks.signArchives
    dependsOn project.tasks.signMavenPublication
}

/**
 * add dependencies for publishMavenPublicationToYourRepository
 */
tasks.withType(PublishToMavenRepository) {
    dependsOn project.tasks.javadocJar
    dependsOn project.tasks.signArchives
    dependsOn project.tasks.signMavenPublication
    doFirst {
        if (!ossrhUsername) {
            throw new ConfigurationException('Please set the sonatype username with project property "ossrhUsername" ')
        }
        if (!ossrhPassword) {
            throw new ConfigurationException('Please set the sonatype password with project property "ossrhPassword" ')
        }
    }
}
```

1. We change id 'java' to 'java-library' in the plugins section.
2. We added 'maven-publish', 'signing', 'org.jetbrains.dokka' plugins.
3. We tweaked the whole publishing section, which specified the publishing repository, and credentials info.
4. The signing configuration should be treated carefully.

## II. Publish to mavenLocal
We can publish the jar to mavenLocal for some integration test.
There's a gradle task named publishToMavenLocal to do that.

Then in your client application, reference this package in your dependencies section, and exclude your library in remote repositories. That's because you have not publish it remotely yet, the build will fail regarding to this.

The build.gradle in your client application:
```groovy
repositories {
    mavenCentral() {
        content {
            excludeGroup("info.cepheus")
        }
    }
    mavenLocal()
}

dependencies {
		// omit other dependencies...

    implementation "info.cepheus:cepheus_axon_extension:0.0.1"
}
```

## III. Publish to mavenCentral
We can never publish to mavenCentral directly, instead, we need publishing to one of those proxyed repositories and our artifacts appear in the Central.

### 1) Sign up / Login to sonatype
First, [Create a Jira account](https://issues.sonatype.org/secure/Signup!default.jspa) if not yet.

Second, [Create a New Project ticket](https://issues.sonatype.org/secure/CreateIssue.jspa?issuetype=21&pid=10134) following the instructions.

Above steps can be found in the guide from [https://central.sonatype.org/publish/publish-guide/](https://central.sonatype.org/publish/publish-guide/).

### 2) Verify your domain name via TXT records
After created the New Project Issue, we can find the guidelines to verify the domain name or using Github prefixed groupId alternatively.
Note, You should create your TXT record with empty Hostname field.
And after created you might need to reopen the issue for further changes taken place.

### 3) GPG key
#### 1. Generate a gpg key pair if not yet:
```bash
gpg2 --full-generate-key
```
Select 4096 bits long and leave other items default.
```bash
gpg: directory '/home/wujuntao/.gnupg' created
gpg: keybox '/home/wujuntao/.gnupg/pubring.kbx' created
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.

GnuPG needs to construct a user ID to identify your key.

You selected this USER-ID:
    "Juntao Wu (wujuntaocn) <wujuntaocn@outlook.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
gpg: /home/wujuntao/.gnupg/trustdb.gpg: trustdb created
gpg: key 596526528E1AD2A8 marked as ultimately trusted
gpg: directory '/home/wujuntao/.gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '/home/wujuntao/.gnupg/openpgp-revocs.d/8EE94F34CE9218CC8393020F596526528E1AD2A8.rev'
public and secret key created and signed.

pub   rsa4096 2021-11-15 [SC]
      8EE94F34CE9218CC8393020F596526528E1AD2A8
uid   Juntao Wu (wujuntaocn) <wujuntaocn@outlook.com>
sub   rsa4096 2021-11-15 [E]
```
#### 2. Export the public parts into a text file:
```bash
gpg2 --armor --export 8EE94F34CE9218CC8393020F596526528E1AD2A8 > public.pgp
```

#### 3. Upload the public key to the well known pgp sites such as:
[https://keys.openpgp.org](https://keys.openpgp.org)
[https://keyserver.ubuntu.com](https://keyserver.ubuntu.com)

#### 4. Export the secring into a file:
```bash
gpg2 --export-secret-keys -o secring.key
```

#### 5. List the 8 chars short public key id with:
```bash
gpg2 --list-keys --keyid-format short

# which produces below content:
/home/wujuntao/.gnupg/pubring.kbx
---------------------------------
pub   rsa4096/8E1AD2A8 2021-11-15 [SC]
      8EE94F34CE9218CC8393020F596526528E1AD2A8
uid         [ultimate] Juntao Wu (wujuntaocn) <wujuntaocn@outlook.com>
sub   rsa4096/F2093848 2021-11-15 [E]
```

### 4) Modify ~/.gradle/gradle.properties for correct credentials

Create or update your global gradle.properties file rather than the project local properties. This is because we often add the gradle.properties into source control, which is risky for credentials.

The ~/.gradle/gradle.properties are like below:
```properties
signing.keyId=your-8-char-key-id
signing.password=your-signing-password
signing.secretKeyRingFile=C:\\Users\\wujun\\.gnupg\\secring.key

ossrhUsername=sonatype-username
ossrhPassword=sonatype-password
ossrhStagingProfileId=sonatype-staging-profile
```

### 5) Publish and check availabilities

5.1 Navigate to [https://s01.oss.sonatype.org/](https://s01.oss.sonatype.org/) to check if the publication successfully.

5.2 Once the contents has been published to the staging directory, use the close button for next.

5.3 If closing successfully, you can use the release button to publish the package now.

Check [https://central.sonatype.org/publish/release/#releasing-deployment-from-ossrh-to-the-central-repository-introduction](https://central.sonatype.org/publish/release/#releasing-deployment-from-ossrh-to-the-central-repository-introduction) for more information.

## IV. Check package availability

Remove your exclusion in client build.gradle, now it's time to check if the jar is publicly available.

You can further check other ways for sharing organization-wide library packages.
