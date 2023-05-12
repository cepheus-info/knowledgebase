# Using EFK to centralize logging

## Introduction

EFK is a combination of three open source projects: Elasticsearch, Fluentd, and Kibana. It is used to collect, index, and search, and visualize logs.

## Prerequisites

- [Docker](https://docs.docker.com/engine/install/)

## Setup

### Dockerfile for customized Fluentd

```dockerfile
# A new version is provided
FROM fluent/fluentd:v1.16-1
USER root
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "5.3.0"]
USER fluent
```

### Prepare fluentd.yml

Fluentd use a config file as below:

```conf
<source>
  @type forward
  port 24224
  bind
</source>
```

A yaml format is also supported:

```yml
config:
  # Receive events from 24224/tcp
  # This is used by log forwarding and the fluent-cat command
  - source:
      $type: forward
      port: 24224

  # http://<ip>:9880/myapp.access?json={"event":"data"}
  - source:
      $type: http
      port: 9880

  # Match events tagged with "myapp.access" and
  # store them to /var/log/fluent/access.%Y-%m-%d
  # Of course, you can control how you partition your data
  # with the time_slice_format option.
  - match:
      $tag: myapp.access
      $type: file
      path: /var/log/fluent/access

  - match:
      $type: elasticsearch
      host: localhost
      port: 9200
      logstash_format: true
      logstash_prefix: fluentd
      logstash_dateformat: "%Y%m%d"
      include_tag_key: true
      type_name: fluentd
      tag_key: @log_name
```

We can configure fluentd to collect logs from docker containers by using [fluent-plugin-docker](#fluent-plugin-docker).

### Configure docker to use fluentd logging driver

```sh
docker run --log-driver=fluentd --log-opt fluentd-address=localhost:24224 --log-opt tag="docker.{{.Name}}" nginx
```

A more convenient way is to use [docker-compose](https://docs.docker.com/compose/).

```yml
version: "3.7"
services:
  nginx:
    image: nginx
    container_name: nginx
    restart: always
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: docker.{{.Name}}
```

### Docker-compose file to start EFK

Refer to [docker-compose.efk.yml](./templates/docker-compose.efk.yml) for more information

```yml
version: "3.7"
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.7.1
    container_name: elasticsearch
    restart: always
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - elasticsearch:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
  kibana:
    image: docker.elastic.co/kibana/kibana:8.7.1
    container_name: kibana
    restart: always
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - 5601:5601
    depends_on:
      - elasticsearch
  fluentd:
    build: ./fluentd
    container_name: fluentd
    restart: always
    volumes:
      - ./fluentd/conf:/fluentd/etc
      - ./fluentd/log:/fluentd/log
      - /var/log/nginx:/var/log/nginx:ro
    ports:
      - 24224:24224
      - 24224:24224/udp
    depends_on:
      - elasticsearch
      - kibana
```
