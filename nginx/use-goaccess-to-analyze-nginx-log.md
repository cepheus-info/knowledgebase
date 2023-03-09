# Use GoAccess to analyze nginx log

## Introduction

[GoAccess](https://goaccess.io/) is a real-time web log analyzer and interactive viewer that runs in a terminal in \*nix systems or through your browser. It provides fast and valuable HTTP statistics for system administrators that require a visual server report on the fly.

## Use GoAccess via Docker/Podman

### Execute GoAccess

```bash
docker run --rm -it -v /var/log/nginx:/var/log/nginx allinurl/goaccess:latest -f /var/log/nginx/access.log -o /var/log/nginx/report.html --log-format=COMBINED --real-time-html
```

### only get the report

```bash
# Use docker
cat access.log | docker run --rm -i -e LANG=$LANG allinurl/goaccess -a -o html --log-format COMBINED - > report.html
# Use podman
cat access.log | podman run --rm -i -e LANG=$LANG allinurl/goaccess -a -o html --log-format COMBINED - > report.html
```

### Get realtime report

```bash
# Use docker
tail -F access.log | docker run -p 7890:7890 --rm -i -e LANG=$LANG allinurl/goaccess -a -o html --log-format COMBINED --real-time-html - > report.html
# Use Podman
tail -F access.log | podman run -p 7890:7890 --rm -i -e LANG=$LANG allinurl/goaccess -a -o html --log-format COMBINED --real-time-html - > report.html
```
