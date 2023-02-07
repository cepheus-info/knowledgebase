---
title: Getting Started of Quarkus
description: 
published: true
date: 2021-12-03T10:05:15.479Z
tags: 
editor: markdown
dateCreated: 2021-12-03T10:05:15.479Z
---

# Generate quarkus project

## I. Using maven command to generate project
You can use maven plugin to generate project with following steps.

### 1) Prepare environment
```powershell
# Install Chocolatey on windows.
# Install maven using Chocolatey on windows with Administrative rights.
choco install maven
```

### 2) Initialize a quarkus project
```powershell
mvn io.quarkus.platform:quarkus-maven-plugin:2.4.1.Final:create "-DbuildTool=gradle" "-Dextensions=resteasy,resteasy-jackson"
```
or
```powershell
mvn io.quarkus.platform:quarkus-maven-plugin:2.4.1.Final:create `
    -DprojectGroupId=my-groupId `
    -DprojectArtifactId=my-artifactId `
    -DprojectVersion=my-version `
    "-DclassName=org.my.group.MyResource" `
    "-Dextensions=resteasy,resteasy-jackson" `
    -DbuildTool=gradle
```

## II. Initialize using quarkus-cli

### 1) Install Jbang
```powershell
iex "& { $(iwr https://ps.jbang.dev) } app setup"
```

### 2) Install quarkus-cli

Powershell:
```powershell
# Use powershell if there's no network issue.
jbang app install --fresh --force quarkus@quarkusio
```

Bash with http_proxy
```bash
# For windows, exec in git bash for using of `export`
$ export JAVA_TOOL_OPTIONS="-Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=1080" && jbang app install --fresh --force quarkus@quarkusio
```

### 3) Create project & add extension

Command Prompt

3.1) create quarkus project:
```bash
# The quarkus create command can only work in Command Prompt for Windows
# quarkus create app --help for help
quarkus create app ^
info.cepheus:showcase_kotlin:0.0.1 --kotlin --gradle --wrapper --extension=resteasy,resteasy-jackson
```

3.2) add extensions:
```bash
# add neccesary extensions.
quarkus ext add agroal quarkus-jdbc-postgresql quarkus-hibernate-orm-panache-kotlin flyway smallrye-openapi
```

# Working with IDEA

## Install quarkus plugin

Search and install quarkus plugins

- [Quarkus Run Configs](https://plugins.jetbrains.com/plugin/14242-quarkus-run-configs)
- [Quarkus Tools](https://plugins.jetbrains.com/plugin/13234-quarkus-tools)