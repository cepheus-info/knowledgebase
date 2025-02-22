# README

## Install V2Ray on Linux Server

### 1. Install V2Ray

```bash
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
```

### 2. Configure V2Ray

Configure `/usr/local/etc/v2ray/config.json` with content from [server/config.json](./server/config.json).

> Note: windows inbound support for socks5 is not working well, you can use `http` instead.

### 3. Start V2Ray

```bash
systemctl start v2ray
```

### 4. Firewall

Allow port `10087` and `10088` for V2Ray. Ubuntu 24.04 enabled `ufw` by default.

```bash
sudo ufw allow 10087
sudo ufw allow 10088
```
