# Override docker entrypoint

## Problem

You want to override the entrypoint of a docker image. For example, you want to run a command in a container that has a default entrypoint.

## Solution

### Override entrypoint via command line argument

You can override the entrypoint by using the `--entrypoint` flag.

```bash
docker run --entrypoint /bin/bash -it ubuntu
```

### Override entrypoint via docker-compose.yml

You can override the entrypoint by using the `entrypoint` key in the `docker-compose.yml` file.

```yaml
version: "3.7"
services:
  myservice:
    image: ubuntu
    entrypoint: /bin/bash
```

However, this will not work if the image has a `CMD` instruction in its `Dockerfile`. In that case, you need to use the `command` key in the `docker-compose.yml` file.

```yaml
version: "3.7"
services:
  myservice:
    image: ubuntu
    entrypoint: /bin/bash
    command: -c "echo hello world"
```

```yaml
version: "3.7"
services:
  myservice:
    image: ubuntu
    entrypoint: tail -f /dev/null
```

## Example

When we run the following [docker-compose.goaccess.yml](../nginx/templates/docker-compose.goaccess.yml) file, we will see how this override work.

```yaml
version: "3.7"
services:
  goaccess:
    image: allinurl/goaccess
    # Ommit the entrypoint to use the default entrypoint
    command: -f /goaccess/log/nginx/access.log -o /goaccess/www/html/index.html --log-format='%h %^[%d:%t %^] "%r" %s %b "%R" "%u" "%^" %T %^ %^' --date-format='%d/%b/%Y' --time-format='%H:%M:%S' --tz='Asia/Shanghai' --real-time-html --ws-url=ws://localhost:7890
```
