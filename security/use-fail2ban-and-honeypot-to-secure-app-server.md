# Use fail2ban and honeypot to secure App server

## 1. Overview

[fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) is an intrusion prevention software framework that protects computer servers from brute-force attacks. It operates by monitoring log files (e.g. /var/log/auth.log) and banning IP addresses conducting too many failed login attempts.

[honeypot](<https://en.wikipedia.org/wiki/Honeypot_(computing)>) is a computer security mechanism set to detect, deflect, or, in some manner, counteract attempts at unauthorized use of information systems. Honeypots can be used to detect attempts at system or network intrusion and can buy time to investigate the incident and mount a defense.

## 2. Install and configure fail2ban

### 2.1. Install fail2ban

```bash
zypper install fail2ban
```

### 2.2 Configure fail2ban

Add nginx-4xx.conf to /etc/fail2ban/filter.d directory

```properties
[Definition]
failregex = ^<HOST>.*"(GET|POST|PATCH|PUT|DELETE|HEAD|OPTIONS|CONNECT|TRACE) ((?!\/magic).)* HTTP/1\.[01]" (4\d\d|200) .*$
ignoreregex = ^<HOST>.*"GET /magic .* HTTP/1\.[01]".*$
```

Change /etc/fail2ban/jail.d/defaults-debian.conf

```properties
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/secure
findtime = 60
maxretry = 2
bantime = 7200
[nginx-4xx]
enabled = true
port = http,https
filter = nginx-4xx
logpath = /var/log/nginx/access.log
findtime = 10
maxretry = 2
bantime = 7200
```

### 2.3 Restart fail2ban

```bash
systemctl restart fail2ban
```

### 2.4 Check fail2ban status

```bash
# Use below command to view fail2ban status
fail2ban-client status
# Use below command to view fail2ban banned ip list
fail2ban-client get nginx-4xx banned
# Use below command to mannually ban ip address
fail2ban-client set nginx-4xx banip <ip-address>
# Use below command to unban ip address(in all jails and database)
fail2ban-client unban <ip-address>
```

## 3. Install and configure honeypot

### 3.1. Use Hellpot to trick hackers

Hellpot is a honeypot that can be used to trick hackers. It can be used to detect hackers and block their ip address.

See [https://github.com/yunginnanet/HellPot](https://github.com/yunginnanet/HellPot) for more details.

Use below command to generage Hellpot config file

```bash
# Use below command to generate config file
./HellPot --genconfig
# Use below command to start Hellpot
./HellPot -c HellPot.toml &
```

### 3.2. Configure Hellpot

```toml
[deception]
server_name = 'nginx'

[http]
bind_addr = '127.0.0.1'
bind_port = '8080'
real_ip_header = 'X-Real-IP'
uagent_string_blacklist = ['Cloudflare-Traffic-Manager', 'curl']
unix_socket_path = '/var/run/hellpot'
unix_socket_permissions = '0666'
use_unix_socket = false

[http.router]
# Note we are use catchall to handle all requests
catchall = true
makerobots = false
# You can add more paths here if you are not using catchall
paths = []

[logger]
debug = true
directory = '/root/.local/share/HellPot/logs'
nocolor = false
trace = false
use_date_filename = true

[performance]
max_workers = 256
restrict_concurrency = false
```

### 3.3. Configure nginx to reflect Hellpot

```properties
server {
    listen 80;
    server_name example.com;
    location / {
        rewrite ^/(.*)$ /honeypot.html?uri=$request_uri break;
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /honeypot.html {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /robots.txt {
        return 200 "User-agent: *\nDisallow: /";
    }

    location /favicon.ico {
        return 200 "";
    }
}
```

### 3.4. Configure nginx to disable direct access to IP address

```properties
server {
    listen 80;
    listen [::]:80;
    server_name _;

    return 444;
}
```

## 4. References

- [https://www.fail2ban.org/wiki/index.php/Main_Page](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [https://en.wikipedia.org/wiki/Honeypot\_(computing)](<https://en.wikipedia.org/wiki/Honeypot_(computing)>)
