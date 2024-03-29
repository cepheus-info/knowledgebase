# 岗位交接计划

## 1. 简介

我将于 2023-09-22 日离任当前岗位，现将当前工作内容和未来规划做如下说明。

## 2. 目标

- 完成当前工作 [见：工作任务](#3-工作任务)

- 规划长期工作 [见：长期规划](#4-长期规划)

- 知识传递目标 [见：知识传递](#5-知识传递)

## 3. 工作任务

### 3.1. 数据库优化

- 附件死锁，读写分离和批量接口优化第一个版本

- 测试环境数据库查询慢`*`

  _`测试环境数据库查询较慢，与原先的环境相比，在配置上没有明显的差异，需要进一步排查。`_

- 现场环境资源共用部署`*`

  _`大规模环境迁移可能产生难以避免的故障，需要考虑应急方案。`_

- 基金流程和变动记录编辑死锁问题`*`

  _`基金流程吞吐量较低，且对变动记录表的批量更新操作较频繁和缓慢，与变动记录表的编辑操作冲突，容易导致死锁/锁定。`_

### 3.2. 应用优化

- 变动死信

- 性能测试(\*)

- 批量接口优化 Phase II

### 3.3. 数据一致性

- 通过 Event 状态限制执行新任务：变动，补扣发，编辑或删除后基金报表还有数据的问题(之前的解决方案版本测试未通过，已终止，需要找新的解决方案)

  长远来看，可以也仅可以通过[领域优化](#41-ddd-领域优化)来完成此目标。

### 3.4. 监控问题

- 运行监控

- 环境日志监控

### 3.5. 服务接口治理

- 网关自定义限流

## 4. 长期规划

### 4.1. DDD 领域优化

- 优化领域模型

  - 根据完成业务所需信息，优化领域模型

  例如：批量晋升时，Person Aggregate 需要包含用于计算晋升条件的信息，从而不需要查询除`配置表`以外的任何`业务表`（如：PersonWages，AnnualCheck 等）来完成晋升操作。

- 优化 CQRS 领域逻辑/视图逻辑

  - `基于数据库的业务逻辑` 迁移至 `基于 Aggregate / Domain Service 的领域逻辑`

  例如：基金生成时，需要对历史已生成基金，跨越生成基金等进行校验，这些校验逻辑应该放在领域层，而不是放在数据库层。

  - `直接由业务操作更新数据表` 迁移至 `由事件更新的数据表`

  例如：业务变动时，需要对当前人员状态进行更新，这些更新状态的操作应该由领域事件触发，并且在 Event Handler 中执行, 而不是直接由 Service 方法在数据库中更新。

- 优化事件处理一致性

  - 对同一事件的处理可能会分布在多个 Event Handler，甚至多个 Service 中，部分关键事件的处理应该保证一致性。

    例如：ChangeRecordedEvent 事件，需要保证对 PersonWages 表的更新和对 ChangeRecord 表、PersonSnapshot 表的插入是强一致的，同时需要保证对`mono-service`和`fund-service`中的更新是最终一致的。

```java
class PersonAggregate {

  private List<AnnualCheck> annualChecks;

    @CommandHandler
    public void handle(ChangeCommand command) {
      // 1. 校验
      // 2. 更新 PersonAggregate
      // 3. 发布 ChangeRecordedEvent
    }



    @EventSourcingHandler(ResumeChangeEvent event) {

    }
}
```

### 4.2. 框架版本升级

- 升级 Spring Boot 版本至 2.7.x

- 升级前端框架版本 Angular 16.x

- 升级 Axon framework 版本至 4.6.x

### 4.3. DevOps

- 优化 CI/CD 流程

- Docker Swarm 迁移 Kubernetes

## 5. 知识传递

### 5.1. 知识库

- [知识库地址：https://gitlab.sfdapp.com/generic/wiki/architecture](https://gitlab.sfdapp.com/generic/wiki/architecture)

- [Generic Lab 地址：https://gitlab.sfdapp.com/generic/lab](https://gitlab.sfdapp.com/generic/lab)

### 5.2. 说明

知识传递应当是一个持续且可沉淀的过程，因此我将利用公司内部的 GitLab 作为知识库，将工作中的疑难问题、解决方案、技术分享等内容沉淀到知识库中，以便后续的同事能够快速的获取到相关的知识。

## 6. 补充

### 6.1 数据一致性问题

### 6.2 Axon 未知实例

### 6.3 Axon 事件处理器无异常但不工作

### 6.4. 应用集群合并

AxonServer Reader -> Axon Server 1, 2, 3

Publish Message ->

AxonServer Writer -> Axon Server new

### 6.5. Mongo 事务未开启

### 6.6. 测算服务 Instance 数量 <-> PooledStream Processor 数量

全部指向同一个实例。

### 6.7. 国产化环境 部署环境管理

001（省直 Docker 部署)
002 (成都机关 jar 包部署)
003 (泸州版本 jar 包部署)

Docker -> jar 包
Docker: docker-compose.yml 配置环境变量
jar 包: external application.properties

解决方式：Jenkins CI 集成 jar 包发布
