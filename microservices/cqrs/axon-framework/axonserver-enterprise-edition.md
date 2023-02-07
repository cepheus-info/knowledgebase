---
title: axonserver-enterprise-edition
description: 
published: true
date: 2021-10-12T11:30:44.752Z
tags: 
editor: markdown
dateCreated: 2021-10-12T11:30:42.981Z
---

---
A CQRS Framework
---

# AxonServer Enterprise Edition

A cluster is defined to guarantee high availability. 

Multiple connection points for (Axon Framework-based) client applications, and thus share the load of managing message delivery and event storage. Client applications will dynamically connect to a node in the cluster and automatically reconnect to another, should the node that they are currently connected to become unreachable.‌

Clustering and Multi-Context features are only available in Axon Server Enterprise Edition.

![Axon Server EE Cluster](<../../../assets/cqrs-architecture/image_(5).png>)



