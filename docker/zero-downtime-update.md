# Zero Downtime update

## Update service via command line

Copy image files to remote server with below commands

```bash
scp docker-compose.inst.backend.yml.$version.tar.gz root@remote:/sfapp/docker/
```

Update specified service with start-first

```bash
docker service update --image cepheus990910/$image:$version --update-order start-first $service
```

## Update service via docker-compose.yml

Configure docker-compose.yml with below contents:

```yaml
version: "3.8"
services:
  service_name:
    image: image_name:version
    deploy:
      replicas: 3
      restart_policy:
        condition: any
        delay: 5s
        max_attempts: 3
        window: 120s
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
        failure_action: rollback
      rollback_config:
        parallelism: 0
        order: stop-first
```

Refer to template file in [docker-compose.yml](./templates/docker-compose.yml) for more information.

> The most important part is `update_config` and `rollback_config` in `deploy` section. With `order: start-first` we can start new containers before stopping old ones, so that we can achieve zero downtime update.
