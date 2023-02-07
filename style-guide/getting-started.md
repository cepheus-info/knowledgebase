---
title: Style guide
description: 
published: true
date: 2022-04-22T05:34:08.220Z
tags: 
editor: markdown
dateCreated: 2022-04-22T05:27:29.625Z
---

# Development Style guide

## 1. File structure & File naming conventions

### Java应用

在Java应用中，优先使用模块化方式组织代码结构，在模块内部再考虑是否使用分层。示例：
```bash
├─basicInfo                     #业务模块
│  ├─api
│  ├─application
│  ├─assembler
│  ├─coreapi
│  └─infrastructure
├─batchSubsidy                  #业务模块
│  ├─api
│  ├─application
│  ├─assembler
│  ├─coreapi
│  └─infrastructure
├─changeRecord                  #业务模块
│  ├─application
│  ├─coreapi
│  └─infrastructure
├─coreapi                       #公用核心模块
├─promotion                     #业务模块
│  ├─api
│  ├─application
│  ├─coreapi
│  ├─infrastructure
│  └─specification
```

Why? 
- 优先使用模块的组织形式有利于保持整个模块的独立性，有利于架构演进过程中拆分为单独的服务和更好的移植。
- 模块内部使用分层可以在模块涉及业务较为复杂时适当的分离关注点，因此模块化应用与分层架构可以结合起来使用。

以约定名称后缀命名文件，如：
```java
Controller
Service
ServiceImpl
Strategy
Repository
CommandHandler
EventHandler
Interceptor
Request
Dto
Command
Event
```

### Angular应用

- 在Angular应用中，同样遵循组件化方式组织代码，但应当遵循文件命名原则如：
hero.component.ts|html|css|spec
hero.service.ts
hero.pipe.ts
hero.module.ts
hero.directive

- 对通用组件采取封装进library project的方式提高复用性。

Why?
- 组件是Angular中功能的最小单位，通常一个组件发挥的功能是内聚的。
- 组件可以以组件module的形式被其他组件所引用，通过Input、Output参数以及service的方式共享数据。

### React应用

- 在React应用中，区分按pages组织的代码以及按components组织的代码。

- 同一文件中只包含一个组件。

- 使用Pascal命名法命名文件。

## 2. Naming conventions

### Java应用

- 使用明确意图的名称

    特别对于DDD中，要明确Command、Event的含义：

    Command应使用动词来表示该动作是一个Intent意图。

    Event应使用过去分词来标识该事件是一个已发生的事实。
    
    例如: PromoteCommand、PromotedEvent

    同样，因为Command、Event在DDD中在特别含义，应在其他场合尽量避免使用该后缀以防止发生混淆。例如Web请求中的RequestBody则尽量命名为PromoteRequest、PromoteDto而非PromoteCommand。

- 使用较为生涩的名称时，对该类型定义处使用注释，但不要处处注释

    例如：
    ```java
    /**
    * 实际职级
    *
    * @author 作者
    * @since 0.1.0
    */
    @Table(name = "c_true_pro_rank")
    @EqualsAndHashCode(callSuper = true)
    @Data
    @Entity
    public class TrueProRankDto extends NaturalCodeDto {
        private String category;

        private Integer categoryIndex;
    }
    ```

- 避免使用较长的名称

    例如:

    ```java
    public interface BasisPerformanceRepository extends JpaRepository<BasisPerformanceDto, Integer> {
    BasisPerformanceDto findByPresentOccupationLevelAndTrueProRankLevelAndCadreAndSupremeAuditOrganizationIdAndJudgeProsecutors(
            Integer presentOccupationLevel, Integer trueProRankLevel, Boolean isCadre, String supremeAuditOrganizationId,Boolean judgeOrProsecutors);
    }
    ```
    当Repository方法中使用到3个以上参数时，通常不再适合使用自动生成方法来表示了，较难理解。

### React应用

- Reference Naming: 对React components使用PascalCase, 对引用实例使用camelCase.

    ```jsx
    // bad
    import reservationCard from './ReservationCard';
    // good
    import ReservationCard from './ReservationCard';
    // bad
    const ReservationItem = <ReservationCard />;
    // good
    const reservationItem = <ReservationCard />;
    ```

- Props Naming: 对属性名称使用camelCase，如果属性是React Component，则使用PascalCase.

    ```jsx
    // bad
    <Foo
    UserName="hello"
    phone_number={12345678}
    />
    // good
    <Foo
    userName="hello"
    phoneNumber={12345678}
    Component={SomeComponent}
    />
    ```

## 3. Source file structure

### Java应用

源文件应包含:

- License/copyright（如存在）
- Package声明
- Import声明
- 唯一一个顶层class
- 使用唯一一个空行来分割代码中的不同块.

### 3.1 No wildcard imports 不要使用通配符引入

### 3.2 Class内容顺序
Members、Initializers登放置顺序对Class的明确性有重要影响。没有放置顺序的唯一准则。
但每个Class应该有一个可以解释的明确逻辑顺序，例如: 新方法不是直接简单的添加在文件末尾，而是按照逻辑块成组的方式添加。

### 3.3 多个Overloads之间不要包含其他方法
这条规则同样应用到Constructor中。

### 3.4 {}的使用 
#### 3.4.1 对if, else, for, do and while statements使用{}，即使是空行。

#### 3.4.2 对lambda表达式，{}可选。

#### 3.4.3 块format方式:
```java
return () -> {
  while (condition()) {
    method();
  }
};

return new MyClass() {
  @Override public void method() {
    if (condition()) {
      try {
        something();
      } catch (ProblemException e) {
        recover();
      }
    } else if (otherCondition()) {
      somethingElse();
    } else {
      lastThing();
    }
  }
};
```

#### 3.4.4 Empty Blocks 可以接受两种format方式
```java
 // 可以接受
  void doNothing() {}

  // 可以接受
  void doNothingElse() {
  }

  // 但不可接受混排方式
  try {
    doSomething();
  } catch (Exception e) {}
```

### 3.5 Column width: 100
限制单行宽度为100，对超出100列宽的代码使用折行，此规则对Package声明与Import声明例外。

### 3.6 折行规则
#### 3.6.1 示例：
1. When a line is broken at a non-assignment operator the break comes before the symbol. (此条规则只适用于Java)

    + 同样适用于 "operator-like" 符号:
        + dot separator (.)
        + method reference中的 :: (::)
        + type bound中的 & (<T extends Foo & Bar>)
        + catch block中的 | 符 (catch (FooException | BarException e)).
2. 含赋值操作符时，通常在 = 后折行. 此规则同样应用于高级for中。
3. 方法名应与后续的左括号(紧邻。
4. 逗号(,)应与前面的token相邻.
5. lamda箭头前不应该折行, 而应该选择折在 -> 之后：

```java
MyLambda<String, Long, Object> lambda =
    (String label, Long value, Object obj) -> {
        ...
    };

Predicate<String> predicate = str ->
    longExpressionInvolving(str);
```

## 4. Comments 注释

- 使用多行注释时 /**/
- 使用单行注释时 //

IDE中通常只会自动分析 /**/ 为Doc，因此对于Class注释，Method注释等应使用多行注释编写。
```java
    /**
     * Change Resume
     *
     * @param command    command to Change the whole Resume
     * @param eventStore @Autowired EventStore
     *
     * @return a ResumeDelta object representing Which fields had been changed
     */
    @CommandHandler
    public ResumeDelta handle(ResumeCommand command,
                       @Qualifier("eventStore") @Autowired EventStore eventStore
    ) {
      // ...
    }
```

Tips: 尽量在方法注释中描述清楚整个方法的意图，减少对代码内单行注释去描述语句的用法。例外是方法中存在多个逻辑块，需要对整个逻辑块的边界加以注释时：
```java
    /**
     * Change Resume
     *
     * @param command    command to Change the whole Resume
     * @param eventStore @Autowired EventStore
     *
     * @return a ResumeDelta object representing Which fields had been changed
     */
    @CommandHandler
    public ResumeDelta handle(ResumeCommand command,
                       @Qualifier("eventStore") @Autowired EventStore eventStore
    ) {
      //#region Guard a Resume is valid
      // do some steps to check if Resume valid
      //#endregion

      //#region process Resume calculation
      // ...
      //#endregion
    }

```
现代的编辑器通常支持#region注释块，Java中使用//#region //#endregion, Typescript中使用//region //endregion, C#中使用#region #endregion。但同时应当注意避免过大的逻辑块。

## 5. Javadoc
### 5.1 通用形式
例如:
```java
/**
 * Multiple lines of Javadoc text are written here,
 * wrapped normally...
 */
public int method(String p1) { ... }
... or in this single-line example:

/** An especially short bit of Javadoc. */
```

### 5.2 Javadoc使用场景
Javadoc应使用在每一个public class以及它们的每一个public/protected member中，只有少数例外。

#### 5.2.1 Exception: 自描述性members
对于简单方法例如getter, Javadoc是可选的。

#### 5.2.2 Exception: overrides
Override父类的方法，可选。

## 6. Transaction

最终一致性并非允许丢弃单体中的事务，相反，发送分布式消息应当遵循在每一个单体的处理器中用强一致性的用法。例如：
```java
/**
* bad style
**/
@Transactional
public void process() {
    // ... Persist当前Domain状态到Database
    repository.save();
    // ... 发送Command给其他服务处理
    commandGateway.send(new Command());
    // ... 其他逻辑处理过程
}
```
此种调用存在的问题是Transaction Manager将会因为process()方法中发生的异常而回滚，但Command已经在其他服务中异步执行，导致系统状态无法一致。

```java
/**
* proposed style
**/
public void process() {
    //#region 此方法将当前单体中应处理的逻辑过程进行封装
    service.doProcess();
    //#endregion
    
    // ... 发送Command给其他服务处理
    commandGateway.send(new Command());
}

@Transactional
public void doProcess() {
    // ... Persist当前Domain状态到Database
    repository.save();
    // ... 其他逻辑处理过程
    //#endregion
}
```
上述思路是确保sendCommand到达其他服务时，当前服务内的事务是已提交成功的状态，这样我们可以分别保证各服务自身是一致的，而全局状态则是最终一致的。（当其他服务中发生不可恢复异常时，需要额外的补偿机制对数据状态进行回滚）。

## 7. 单一职责原则

应该有且仅有一个原因引起类的变更。
