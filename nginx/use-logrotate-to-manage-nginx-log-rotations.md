# Use Logrotate to manage nginx log rotations

## Overview

Logrotate is a tool that rotates, compresses, and mails system logs. It is designed to simplify the administration of log files on a system which generates a lot of log files. Logrotate is a standard Linux tool and is available on most Linux distributions.

## Install Logrotate

### Install Logrotate on Ubuntu

```bash
sudo apt install logrotate
```

## Configure Logrotate to rotate nginx logs

### Create a logrotate configuration file

```bash
sudo nano /etc/logrotate.d/nginx
```

### Add the following content to the file

```bash
/var/log/nginx/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 640 nginx adm
    sharedscripts
    postrotate
        if [ -f /run/nginx.pid ]; then
            kill -USR1 `cat /run/nginx.pid`
        fi
    endscript
}
```

Note that the `postrotate` section is used to send a `USR1` signal to nginx to reopen the log files after rotation. This is necessary because nginx keeps the file descriptors open for the log files. If you don't do this, nginx will keep writing to the old log files after rotation.

## Conclusion

Use logrotate is a simple but effective way to manage nginx logs.