---
title: Using shadowsocks as a proxy via host machine
description: 
published: true
date: 2022-11-10T10:34:59.773Z
tags: 
editor: markdown
dateCreated: 2022-10-17T09:25:25.169Z
---

# Using shadow socks via host machine
- Configure your virtual network adpater connection as NAT
- Configure Shadowsocks client to "Allow other Devices to connect" in system tray.
- Check your ip address in your virtual machine, if your virtual machine's ip is 192.168.a.b, then your virtual host ip is 192.168.a.1
- Configure your proxy in vmware as:
ip address  | port | protocol 
----------- | ---- | --------
192.168.a.1 | 1080 | socks5
- Configure your /etc/environment file as below, or via system built-in proxy configuration.
  ```conf
  HTTP_PROXY=http://192.168.a.1:1080
  HTTPS_PROXY=http://192.168.a.1:1080
  NO_PROXY=localhost,machinename,127.0.0.1
  http_proxy=http://192.168.a.1:1080
  https_proxy=http://192.168.a.1:1080
  no_proxy=localhost,machinename,127.0.0.1
  ```
  > Note that the no_proxy only accepts extension rather than prefix. that means .com.cn is acceptable, neighter do www.google.
  So if we want to use NO_PROXY for all "IP Address" accessing, we can use below script to generate all numbers in {0..255}, and then paste the result into NO_PROXY value place.
  Some of distributions seems to accept a CIDR/format address, such as Fedora, etc.
 
   ```bash
   printf -v no_proxy '%s,' {0..255}
   echo $no_proxy
   ```
 