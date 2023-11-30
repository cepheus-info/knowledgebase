# Use Aspectj in Non-Spring project

## 1. Overview

Aspectj is designed for general purpose instead of Spring. So we could use it in Non-Spring project as well.

## 2. Walkthrough

### 2.1. Concepts

#### 2.1.1. Compile-Time Weaving

Compile-Time Weaving is a mechanism which make use a compiler(ajc) to compile from source and produce woven class files as output. This is the simplest approach of weaving.

#### 2.1.2. Post-Compile Weaving

Post-Compile Weaving is also called binary weaving, which directly changes your byte-code to weave existing class files and JAR files. Compiler(ajc) is also in use.

#### 2.1.3. Load-Time Weaving

Load-Time Weaving is simply binary weaving defered until the point that a class loader loads a class file and defines the class to the JVM. Thus one or more "weaving class loaders", either provided explicitly by the run-time environment or enabled through a "weaving agent" are required.

### 2.2. Steps

Download ajc compiler jar package from [https://github.com/eclipse-aspectj/aspectj/releases](https://github.com/eclipse-aspectj/aspectj/releases), double click and install ajc.

Making chages to environment variables Path and CLASSPATH so ajc can be found. The CLASSPATH should include `aspectjrt.jar` in it. If we want to invoke ajc command in cmd.

#### 2.2.1. Compile-Time Weaving

1. Configure dependencies in pom.xml.

```xml
<properties>
    <aspectj.version>1.9.8.M1</aspectj.version> <!-- specify your version -->
</properties>
<!-- https://mvnrepository.com/artifact/org.aspectj/aspectjrt -->
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjrt</artifactId>
    <version>${aspectj.version}</version>
    <scope>runtime</scope>
</dependency>
```

2. Configure aspectj-maven-plugin in pom.xml.

> Note: If we do not configure maven-compiler-plugin to use dependency aspectj compiler, we might need the System Environment to contain ajc compiler pre-installed.

```xml
<build>
    <pluginManagement>
        <plugins>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>aspectj-maven-plugin</artifactId>
                <version>1.13.1</version>
            </plugin>
        </plugins>
    </pluginManagement>
    <plugins>
        <plugin>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <compilerId>aspectj</compilerId>
            </configuration>
            <dependencies>
                <dependency>
                    <groupId>org.codehaus.plexus</groupId>
                    <artifactId>plexus-compiler-aspectj</artifactId>
                    <version>2.11.1</version>
                  </dependency>
            </dependencies>
        </plugin>
        <plugin>
            <groupId>dev.aspectj</groupId>
            <artifactId>aspectj-maven-plugin</artifactId>
            <version>1.13.1</version>
            <dependencies>
                <dependency>
                    <groupId>org.aspectj</groupId>
                    <artifactId>aspectjtools</artifactId>
                    <version>1.9.7.M3</version>
                </dependency>
            </dependencies>
            <configuration>
                <complianceLevel>1.8</complianceLevel>
                <source>1.8</source>
                <target>1.8</target>
                <showWeaveInfo>true</showWeaveInfo>
                <verbose>true</verbose>
                <Xlint>ignore</Xlint>
                <encoding>UTF-8 </encoding>
                <sources>
                    <source>
                        <basedir>src/main/java</basedir>
                        <includes>
                            <include>**/TransationAspect.java</include>
                            <include>**/SecurityAspect.aj</include>
                        </includes>
                        <excludes>
                            <exclude>**/logging/*.aj</exclude>
                        </excludes>
                    </source>
                </sources>
            </configuration>
            <executions>
                <execution>
                    <id>compile</id>
                    <goals>
                        <goal>compile</goal>
                        <goal>test-compile</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

> Please note: Before version 1.13.1, this plugin by default depended on an AspectJ Compiler (AJC) version which was able to run on Java 8. Since 1.13.1 however, it depends on AspectJ 1.9.8.RC1 or higher, where AJC requires Java 11+. This requirement is inherited by the Eclipse Java Compiler (ECJ) which AJC is a fork of. If you wish to use an older AspectJ version (e.g. 1.9.8.M1, 1.9.7 or lower), please follow the description in section "Upgrading or downgrading AspectJ" on the "Usage" page. Then you can run the build on JDK 8 again.

#### 2.2.2. Post-Compile Weaving

The only difference in Post-Compile Weaving is the configuration section inside build.plugins.plugin.configuration. You could check pom.post-compile.xml for more details.

#### 2.2.3. Load-Time Weaving

##### 2.2.3.1. -javaagent option

You can use `-javaagent path/to/aspectj-weaver.jar` for Load-Time Weaving.

1. In Tomcat server, you can pass in JAVA_OPTS environment variable for that jvm option. Also, you can use startup script for this:

Windows cmd:

```bat
set "CATALINA_OPTS=%CATALINA_OPTS% -javaagent:<YourContrastJarPath>"
call <TomcatDirectory>\bin\startup.bat
```

Linux shell:

```bash
export CATALINA_OPTS="$CATALINA_OPTS -javaagent:<YourContrastJarPath>"
<TomcatDirectory>/bin/startup.sh
```

> Note: If we run Tomcat as a service, open the Tomcat service manager and change the JVM options to add the agent.

2. In SmartTomcat Plugin, you may need to set -javaagent:path\to\aspectjweaver.jar to VM options in your profile.

##### 2.2.3.2. META-INF/aop.xml

Configuring Load-time Weaving with aop xml files. Below is a example:

```xml
 <aspectj>
    <aspects>
        <!-- declare two existing aspects to the weaver -->
        <aspect name="com.MyAspect" />
        <aspect name="com.MyAspect.Inner" />
        <!-- define a concrete aspect inline -->
        <concrete-aspect name="com.xyz.tracing.MyTracing"
            extends="tracing.AbstractTracing"
            precedence="com.xyz.first, *">
            <pointcut name="tracingScope" expression="within(org.maw.*)" />
        </concrete-aspect>
        <!-- Of the set of aspects declared to the weaver
           use aspects matching the type pattern "com..*" for weaving. -->
        <include within="com..*" />
        <!-- Of the set of aspects declared to the weaver
           do not use any aspects with the @CoolAspect annotation for weaving -->
        <exclude within="@CoolAspect *" />
    </aspects>
    <weaver options="-verbose">
        <!-- Weave types that are within the javax.* or org.aspectj.*
           packages. Also weave all types in the foo package that do
           not have the @NoWeave annotation. -->
        <include within="javax.*" />
        <include within="org.aspectj.*" />
        <include within="(!@NoWeave foo.*) AND foo.*" />
        <!-- Do not weave types within the "bar" pakage -->
        <exclude within="bar.*" />
        <!-- Dump all types within the "com.foo.bar" package
           to the "./_ajdump" folder on disk (for diagnostic purposes) -->
        <dump within="com.foo.bar.*" />
        <!-- Dump all types within the "com.foo.bar" package and sub-packages,
           both before are after they are woven,
           which can be used for byte-code generated at runtime -->
        <dump within="com.foo.bar..*" beforeandafter="true" />
    </weaver>
</aspectj>
```