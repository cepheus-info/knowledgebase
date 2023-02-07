# Performance tuning

## Overview

There are many aspect of performance tuning.

## Process

### Database aspect

一般优化效果是从宏观到微观，因此可考虑如下优化顺序

| Type     | Name               | Priority | Description |
| -------- | ------------------ | -------- | ----------- |
| 架构优化 | 读写分离           | 1        | -           |
| 架构优化 | 分库分表           | 2        | -           |
| 配置优化 | 日志 缓存 连接数量 | 3        | -           |
| 查询优化 | 索引 查询          | 4        | -           |

### Application scaling

There are 2 kinds of scaling of application, vertical & horizontal.

#### Vertical Scaling

We can use vertical scaling first to make single server's extreme performance.

#### Horizontal Scaling

If vertical scaling is not enough to handle the requests, then we can use Application Cluster to load balance all the requests.
