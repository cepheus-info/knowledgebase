# Getting started with Apache kafka

## Customize docker-compose.yml
1. Note that you should change the `build` line into image reference.
2. Set KAFKA_ADVERTISED_HOST_NAME to your own `host_ip`
```yml
version: '2'
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

A new version as below:
```yml
version: '3.7'
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

## Run kafka instance

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

## Reference
As we have changed listeners config for docker environment, there's a detailed explaination below:
[https://www.confluent.io/blog/kafka-listeners-explained/](https://www.confluent.io/blog/kafka-listeners-explained/)

## Use kafkacat as a debug tool

```bash
kafkacat -b 192.168.2.84:9092 -L
```

## Cleanup kafka streams

```bash
docker exec -it smso-database-inst-kafka-1 \
kafka-streams-application-reset.sh --application-id com._3menchina.smso
```

## Cleanup kafka topics

```bash
docker exec -it smso-database-inst-kafka-1 \
kafka-topics.sh \
--bootstrap-server :9092 \
--delete --topic BatchSubsidy
```

## Reset Consumer offset

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