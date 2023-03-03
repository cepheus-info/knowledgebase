# Getting started with Apache kafka

## 1. Overview

- [Apache Kafka](https://kafka.apache.org/) is a distributed streaming platform.

## 2. Customize docker-compose.yml

### 2.1. Old Version of kafka with zookeeper

1. Note that you should change the `build` line into image reference.
2. Set KAFKA_ADVERTISED_HOST_NAME to your own `host_ip`

- Below is a docker-compose.yml which is grabbed from [wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker).

```yml
version: "2"
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
  kafka:
    # change build: . to image: wurstmeister/kafka
    # build: .
    image: wurstmeister/kafka
    ports:
      - "9092"
    environment:
      DOCKER_API_VERSION: 1.22
      KAFKA_ADVERTISED_HOST_NAME: # your_host_ip
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

- A customized docker-compose.yml for kafka with zookeeper is as below.

```yml
version: "3.7"
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
    networks:
      KAFKA:
        aliases:
          - zookeeper
  kafka:
    image: wurstmeister/kafka
    ports:
      - "9092:9092"
      - "29092:29092"
    depends_on:
      - zookeeper
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:29092,EXTERNAL://0.0.0.0:9092
      # todo: also try kafka:29092 instead.
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://localhost:29092,EXTERNAL://192.168.2.84:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
      ALLOW_PLAINTEXT_LISTENER: "yes"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      KAFKA:
        aliases:
          - kafka
networks:
  KAFKA:
```

### 2.2. New Version of kafka without zookeeper

The latest version of kafka does not need zookeeper anymore. You can use the following docker-compose.yml to start a kafka instance.

```yml
version: "3.7"
services:
  kafka:
    image: "bitnami/kafka:latest"
    environment:
      KAFKA_ENABLE_KRAFT: "yes"
      KAFKA_CFG_PROCESS_ROLES: broker,controller
      KAFKA_CFG_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CFG_LISTENERS: CLIENT://:9092,EXTERNAL://:9093,CONTROLLER://:9094
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      KAFKA_CFG_ADVERTISED_LISTENERS: CLIENT://kafka:9092,EXTERNAL://10.39.1.225:9093
      KAFKA_CFG_INTER_BROKER_LISTENER_NAME: CLIENT
      KAFKA_BROKER_ID: 1
      KAFKA_CFG_CONTROLLER_QUORUM_VOTERS: 1@127.0.0.1:9094
      ALLOW_PLAINTEXT_LISTENER: "yes"
    volumes:
      - kafka:/bitnami/kafka
    networks:
      SMSO:
        aliases:
          - kafka
    ports:
      - 9092:9092
      - 9093:9093
      - 9094:9094

  kafdrop:
    image: obsidiandynamics/kafdrop
    restart: "no"
    environment:
      KAFKA_BROKERCONNECT: "kafka:9092"
      JVM_OPTS: "-Xms16M -Xmx48M -Xss180K -XX:-TieredCompilation -XX:+UseStringDeduplication -noverify"
    depends_on:
      - "kafka"
    networks:
      SMSO:
        aliases:
          - kafdrop
    ports:
      - 9095:9000

volumes:
  kafka:
networks:
  KAFKA:
```

## 3. Run kafka instance

- Run below command in wsl2/linux environment in a docker-compose.yml directory.

  ```bash
  docker-compose up -d
  ```

- Scale up a cluster

  ```bash
  docker-compose scale kafka=3
  ```

- Destroy a cluster

  ```bash
  docker-compose stop
  ```

- Check running container instances

  ```bash
  docker ps --format '{{ .Names }}' | grep kafka

  🐸smso-database-inst-kafka-1
  🐸kafka_zookeeper_1
  ```

- Check mapped port of container `smso-database-inst-kafka-1`

  ```bash
  docker inspect --format '{{ .NetworkSettings.Ports }}' smso-database-inst-kafka-1

  🐸map[9092/tcp:[{0.0.0.0 57844}]]
  ```

- Check the connection from the host to the Kafka broker

  ```bash
  nc -vz 0.0.0.0 57844
  # nc is a command from gnu-networkcap which you could install first or just ignore this step.
  ```

- Print out your topics

  ```bash
  docker exec -t smso-database-inst-kafka-1 \
  kafka-topics.sh \
  --bootstrap-server :9092 \
  --list

  # there should be no outputs since you have not create any topics yet.
  ```

- Create topic `t1`

  ```bash
  docker exec -t smso-database-inst-kafka-1 \
  kafka-topics.sh \
  --bootstrap-server :9092 \
  --create \
  --topic t1 \
  --partitions 3 \
  --replication-factor 1

  🐸Created topic t1.
  ```

- Describe topic t1

  ```bash
  docker exec -t kafka_kafka.1.yxgxcq98e09kwxazld69ys2z3 \
  kafka-topics.sh \
  --bootstrap-server :9092 \
  --describe \
  --topic BatchPromotion

  🐸Topic: t1       PartitionCount: 3       ReplicationFactor: 1    Configs: segment.bytes=1073741824
  🐸Topic: t1       Partition: 0    Leader: 1001    Replicas: 1001  Isr: 1001
  🐸Topic: t1       Partition: 1    Leader: 1001    Replicas: 1001  Isr: 1001
  🐸Topic: t1       Partition: 2    Leader: 1001    Replicas: 1001  Isr: 1001
  ```

- Connect with the Kafka console consumer in another terminal

  `Note your command line will not be ended cuz it's a continuas script.`

  ```bash
  docker exec -t smso-database-inst-kafka-1 \
  kafka-console-consumer.sh \
  --bootstrap-server :9092 \
  --group test-group \
  --topic t1
  ```

- Connect with the Kafka console producer in one terminal

  `Note your command line will not be ended cuz it's a continuas script.`

  ```bash
  docker exec -it smso-database-inst-kafka-1 \
  kafka-console-producer.sh \
  --broker-list :9092 \
  --topic t1
  ```

🤣 Now you have the magic to connect the 2 terminal's input & output.

## 4. Reference

As we have changed listeners config for docker environment, there's a detailed explaination below:
[https://www.confluent.io/blog/kafka-listeners-explained/](https://www.confluent.io/blog/kafka-listeners-explained/)

## 5. Troubleshooting

### 5.1. Use kafkacat as a debug tool

```bash
kafkacat -b 192.168.2.84:9092 -L
```

### 5.2. Cleanup kafka streams

```bash
docker exec -it smso-database-inst-kafka-1 \
kafka-streams-application-reset.sh --application-id com._3menchina.smso
```

### 5.3. Cleanup kafka topics

```bash
docker exec -it smso-database-inst-kafka-1 \
kafka-topics.sh \
--bootstrap-server :9092 \
--delete --topic BatchSubsidy
```

## 5.4. Reset Consumer offset

Use --to-latest --dry-run to test the operation
Note: Choose --to-latest or --to-earliest to keep up with / resetting consumer offset.

```bash
docker exec -it smso-database-inst-kafka-1 \
kafka-consumer-groups.sh --bootstrap-server localhost:9092  --group my-console-client  --topic keep-up-with-topic --reset-offsets --to-latest --dry-run
```

Use --execute to commit the operation:

```bash
docker exec -it smso-database-inst-kafka-1 \
kafka-consumer-groups.sh --bootstrap-server localhost:9092  --group my-console-client  --topic keep-up-with-topic --reset-offsets --to-latest --execute
```
