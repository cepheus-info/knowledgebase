---
title: Too many files opened
description: exception occurred when mongodb open too many files
published: true
date: 2021-12-02T04:45:46.374Z
tags: 
editor: markdown
dateCreated: 2021-12-02T04:45:46.374Z
---

# Trouble shooting current opened files
## command to get file counts opened by one container
```bash
docker ps -f name=<your-container-name> -q \
| xargs docker inspect --format '{{.State.Pid}}' \
| xargs lsof -p | wc -l
```

## command to get file counts opened by one process
```bash
lsof -p <your-pid> | wc -l
```

## Change system limit of opened files
todo: