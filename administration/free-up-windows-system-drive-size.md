---
title: Free up Windows system drive size
description: 
published: true
date: 2022-11-07T06:47:58.449Z
tags: shrink
editor: markdown
dateCreated: 2022-01-30T07:43:24.463Z
---

# How to free up your Windows system drive
## Reduce Pagefile.sys size
Open Performance configuration via Searching `Adjust the appearance and performance of Windows` in Start menu.
Choose `Advanced tab` -> `Virtual memory panel` -> `Change Button`
Set a more proper size inside and confirm.
Restart computer.

## Optimize virtual disk file for Docker desktop
Turn on Windows feature `Hyper-V`
Below steps need you to shutdown docker & wsl as well. You can use command like:
```shell
wsl --list
wsl --terminate ubuntu-18.04
wsl --shutdown
```

Navigate to the vhdx path and open Powershell with Administrator Priviliges to execute command, a sample vhdx path here is C:\Users\your-user-name\AppData\Local\Docker\wsl\data
```shell
cd C:\Users\your-user-name\AppData\Local\Docker\wsl\data
Import-Module -Name Hyper-V
Optimize-VHD -Path .\ext4.vhdx -Mode full
```
