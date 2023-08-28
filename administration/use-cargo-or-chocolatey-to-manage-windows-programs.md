---
title: Use Cargo or Chocolatey to manage Windows programs
description:
published: true
date: 2022-11-08T08:16:20.756Z
tags:
editor: markdown
dateCreated: 2022-11-08T08:16:20.756Z
---

# Use Cargo or Chocolatey to manage Windows programs

## 1. Use Chocolatey

Chocolatey is an open-sourcing tool to manage windows programs via command line.

### 1.1. Install

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

### 1.2. Usage (Install nvm)

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

## 2. Use Cargo

Cargo is the package manager in Rust, supports Windows/Linux/MacOS at the same time.

### 2.1. Install via command line tool

Refer to [https://doc.rust-lang.org/cargo/getting-started/installation.html](https://doc.rust-lang.org/cargo/getting-started/installation.html) to install Rust and Cargo.

1. Download the installer [here](https://win.rustup.rs/) & `Proceed with installation`.
2. Run command to check installation

```bash
cargo --help
```

### 2.2. Usage (Install a tool)

1. Run command to install rendr

```bash
cargo install rendr
```

2. Use rendr to scaffold an application

```bash
rendr create --blueprint https://github.com/cepheus-info/cepheus_axon_extension.git --dir my-library-project
```
