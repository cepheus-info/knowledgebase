---
title: How does chmod affect files for OS
description: 
published: true
date: 2022-11-10T10:43:23.807Z
tags: 
editor: markdown
dateCreated: 2022-11-10T10:43:23.807Z
---

# How does chmod affect files
chmod +x: affect file in one OS or all OSes?

[Follow this stackoverflow question](https://unix.stackexchange.com/questions/437569/chmod-x-affect-file-in-one-os-or-all-oses) we can know that git kept only x attribute.

The rwx mode is used in Linux/Unix like OSs, but not the case in Windows. So we should note that how it will affect the file systems in your CI/CD environment.