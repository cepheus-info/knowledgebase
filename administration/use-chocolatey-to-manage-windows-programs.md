---
title: Use chocolatey to manage windows programs
description: 
published: true
date: 2022-11-08T08:16:20.756Z
tags: 
editor: markdown
dateCreated: 2022-11-08T08:16:20.756Z
---

# Use Chocolatey
Chocolatey is an open-sourcing tool to manage windows programs via command line.

## Install

Refer to [https://chocolatey.org/install](https://chocolatey.org/install) to install choco command.

1. Run Powershell with administrative rights.
2. Set Executing Policy
Run Get-ExecutionPolicy. If it returns Restricted, then run Set-ExecutionPolicy AllSigned or Set-ExecutionPolicy Bypass -Scope Process.
3. Run below command
```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
4. Run command to check installation
```bash
choco -?
```

## Usage (Install nvm)
1. Run command to install nvm
```bash
choco install nvm
```
2. Use nvm to install nodejs
```bash
nvm install lts
nvm install current
```
3. Start to use nvm to manage nodejs version