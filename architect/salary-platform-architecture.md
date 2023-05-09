# Salary Platform architecture

## 1. Overview

The Salary Platform is a group of applications and services that allows users to manage, analyze and visualize their salary data. The platform is composed of the following domains:

工资平台是一个由多个应用和服务组成的平台，它允许用户管理、分析和可视化他们的工资数据。平台由以下域组成：

### 1.1. Core Domain (核心域)

The Core Domain is the main domain of the platform. It is responsible for provide business value directly to the users. It is composed of the following applications:

- [Salary Management Application(工资应用)](#)

- [Salary Measurement Application(测算应用)](#)

- [Salary Annual Report Application(年报应用)](#)

- [Organization & User Management Application(单位及用户管理)](#)

- [Console Application(用户控制台)](#)

- [Salary Data Visualization Application(工资及年报可视化)](#)

- [Finanical DataCenter Application(财政统发中心)](#)

- Components integrated in-app like Feedback & Notification, InApp Messaging, etc. (其他集成进控制台以应用形式提供给用户的组件: 反馈与通知、IM 消息等)

  > Note: 需要注意的是，这些组件可能是在核心域提供一个 wrapper，而实际的实现是在支撑域中，这样可以保证核心域的纯洁性，同时也可以保证支撑域的可替换性。例如：IM 消息的能力是由 Supporting Domains 的 QNA Application 实现的，但是在 Core Domain 中，我们可以提供一个 wrapper，将 QNA Application 的能力包装成一个 IM 消息的能力。

### 1.2. Supporting Domains (支撑域)

The Supporting Domains are responsible for provide support to the Core Domain. They are composed of the following applications:

#### 1.2.1. Gateway & Microservices Governance (网关与服务治理)

- [Application Gateway(应用网关)](#)

  The Application Gateway is the entry point of the platform. It is responsible for route the requests to the corresponding services.

- [Service Registry & Discovering(服务注册与发现)](#)

  The Service Registry & Discovering is responsible for register the services and provide the service discovering ability to the platform.

#### 1.2.2. Operations Portal (运维门户)

- [Operation & Maintenance Application(运维中心应用)](#)

  Operation & Maintenance Application is a web application that allows the platform administrators to manage the platform. It integrates other services' abilities to provide a unified management interface.

  - [Centralized Configuration Applications(面向业务系统的配置中心)](#)

  - [Maintenance Applications(面向运维角色的维护中心)](#)

  - [Deployment Applications(面向实施角色的部署中心)](#)

  - [QNA Applications(面向客服角色的问答中心)](#)

#### 1.2.3. Platform infrastructure Services (平台基础设施服务)

- [Security subdomain(安全子域)]

  - [认证服务(Authentication & Authorization Services)](#)

  - [认证适配器(Authentication & Authorization Adapters)](#)

- [Monitoring subdomain(监控子域)]

  - [监控与仪表盘 Monitoring & Dashboard Services)](#)

  - [告警服务(Alerts Services)](#)

  - [集中化日志服务(Centralized Logging Services)](#)

- [DevOps subdomain(DevOps 子域)]

  - [代码仓库(Code Repository Services)](#)

  - [持续交付(CI/CD Services)](#)

  - [应用启动配置管理(IaC Services)](#)

#### 1.2.4. Shared Information services (共享信息服务)

- [Basic Information subdomain(基础信息平台子域)]

  - [Organization Basic Information Services](#)

  - [Person Basic Information Services](#)

- [External Services subdomain(外部服务对接与适配)]

  - [Adapters for external services](#)

  - [AntiCorruption Layers for external services(防腐层)](#)

#### 1.2.5. Data Center Infrastructure (数据中心)

- [Data center infrastructure(数据中心基础设施)]

  - [Datawarehouse services(数据仓库)](#)

### 1.3. Generic Domains

The Generic Domains are responsible for provide generic services to the platform also to other development experiences. They are composed of the following components:

- [Common Spring boot auto-configuration & starters](#)

- [Common Frontend Scaffold](#)

- [Common UI Components](#)

- [File Storage Services & libraries](#)

- [Message Queue Services & libraries](#)
