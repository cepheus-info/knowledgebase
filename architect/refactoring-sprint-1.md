# Refactoring Sprint 1

## 1. Overview

Refactoring via Strangler Pattern is the only way to upgrade the system from 2.0 to 3.0. The following is the refactoring plan for the first sprint.

## 2. Refactoring Plan

### 2.1. Refactoring Scope

The scope of refactoring is limited to the following components:

- [ ] `core/smso-vnext` project

  This is the main component of the next version of the system. It is the core of the system and the most important part of the system. In Strangler Pattern, it is the new system that will replace the old system, and it will run in parallel with the old system for a period of time. Therefore, it is good to refactor this component first.

  This project is a gradle multi-project, which consists of the following projects and make use of buildSrc, common library, etc. to share common code, the following file structure is the same as the file structure of the project:

  > Note that we make use of the `smso-vnext.spring-conventions.groovy` file to share common code, which is a convention plugin for spring boot projects.

  ```bash
    smso-vnext
    ├── buildSrc
    │   ├── build.gradle
    │   └── src
    │       └── main
    │           └── groovy
    │               └── com
    │                   └── cepheus
    │                       └── smso
    │                           └── vnext
    │                               └── smso-vnext.spring-conventions.groovy
    ├── common
    │   ├── build.gradle
    │   └── src
    ├── common-auto-configure
    │   ├── build.gradle
    │   └── src
    ├── common-starter
    │   ├── build.gradle
    │   └── src
    ├── smso-person-management-service
    │   ├── build.gradle
    │   └── src
    ├── smso-transaction-history-service
    │   ├── build.gradle
    │   └── src
    ├── build.gradle
    └── settings.gradle
  ```

- [ ] `supporting/smso-maintainence` group of projects

  This is the component for maintaining the system, which is not used by end users. Therefore, it is safe to put in this component first.

  It will connect to the old system and the new system, and it will be used to maintain the system during the transition period. It consists of the following projects:

  - [ ] `supporting/smso-maintainence/smso-maintainence-service`

  - [ ] `supporting/smso-maintainence/smso-maintainence-frontend`

- [ ] `supporting/smso-auth` project

  This is the component for authentication and authorization, which do not have its own UI. But it supports all other components, including the parts that will be refactored in the next sprint. Therefore, it should be refactored first.

  It consists of the following modules:

  ```bash
    smso-auth
    ├── buildSrc
    ├── smso-auth-service
    │   ├── build.gradle
    │   └── src
    ├── smso-auth-inst-adapter
    |   ├── build.gradle
    |   └── src
    ├── smso-auth-org-adapter
    |   ├── build.gradle
    |   └── src
    ├── build.gradle
    └── settings.gradle
  ```

- [ ] `supporting/smso-organization` project

  This is the backend component for organization management, which is used by the smso-organization-app project. And it is also used by the smso-vnext / smso project. Therefore, it should be refactored first.

- [ ] `core/smso-organization-app` group of projects

  The core/smso-organization-app project is a core business component of the system, which is decoupled from the main component. It consists of the following projects:

  - [ ] `core/smso-organization-app/smso-organization-bff`
  - [ ] `core/smso-organization-app/smso-organization-frontend`

### 2.2. Refactoring Sequence and Plan

The refactoring sequence is as follows:

1. `supporting/smso-auth` project

Refactor the smso-auth project to a multi-modules project and provide the difference behavior via adapter pattern. The following is the refactoring plan:

- [ ] Refactor the smso-auth project to a multi-modules project
- [ ] Integrate the smso-auth-inst-adapter and smso-auth-org-adapter projects into the smso-auth project

2. `supporting/smso-organization` project

Omit this step for now.

3. `supporting/smso-maintainence` group of projects

Given that the smso-maintainence project is currently supporting smso-inst-backend, we need to refactor it to support both 

4. `core/smso-organization-app` group of projects
5. `core/smso-vnext` project
