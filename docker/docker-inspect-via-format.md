# Docker inspect via format

## Docker inspect via format

```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' <container_name>
```

## Docker ps via format

```bash
docker ps --format='{{.Names}}'
```

## Docker inspect all running containers via format

```bash
docker inspect --format='{{.Name}} {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)
```
