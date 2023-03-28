---
title: Disable ipv6 temporally
description: 
published: true
date: 2022-11-10T10:37:53.833Z
tags: 
editor: markdown
dateCreated: 2022-11-10T10:37:53.833Z
---

# Disable ipv6 temporally

You can use below command to disable ipv6 temporally
```bash
# Disable ipv6 temporally
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
```