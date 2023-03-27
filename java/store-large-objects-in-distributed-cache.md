# Store large objects in distributed cache

## Problem

You want to store large objects in the distributed cache. Each object like a few megabytes in size.

It's slow to store and retrieve objects and deserialize them. You want to store and retrieve them as fast as possible.

## Solution

Redis is not designed for storing large objects. It's designed for storing small objects. It's not a good idea to store large objects in Redis.

You can use DataAccessFileCache and Protobuf to store large objects in the distributed cache.

## Example

### Create a Protobuf message

Create a Protobuf message to store the large object.

```protobuf
syntax = "proto3";

package com.example;

message LargeObject {
    string id = 1;
    bytes data = 2;
}
```

### Create a Protobuf message handler

Create a Protobuf message handler to store and retrieve the large object.

```java
import com.example.LargeObject;
import com.example.LargeObjectHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Optional;

public class LargeObject {

        private String id;
        private byte[] data;

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public byte[] getData() {
            return data;
        }

        public void setData(byte[] data) {
            this.data = data;
        }
}

@Component
public class LargeObjectCache {

    private final LargeObjectHandler largeObjectHandler;

    @Autowired
    public LargeObjectCache(LargeObjectHandler largeObjectHandler) {
        this.largeObjectHandler = largeObjectHandler;
    }

    public void store(LargeObject largeObject) {
        largeObjectHandler.store(largeObject);
    }

    public Optional<LargeObject> get(String id) {
        return largeObjectHandler.get(id);
    }
}

public class LargeObjectHandler {

        private final RedisTemplate<String, byte[]> redisTemplate;

        public LargeObjectHandler(RedisTemplate<String, byte[]> redisTemplate) {
            this.redisTemplate = redisTemplate;
        }

        public void store(LargeObject largeObject) {
            redisTemplate.opsForValue().set(largeObject.getId(), largeObject.getData().toByteArray());
        }

        public Optional<LargeObject> get(String id) {
            byte[] data = redisTemplate.opsForValue().get(id);
            if (data == null) {
                return Optional.empty();
            }
            return Optional.of(LargeObject.newBuilder().setId(id).setData(data).build());
        }
}
```

Note: The Protobuf message handler is not thread-safe. You need to synchronize the access to the Protobuf message handler.

### Create a Protobuf message handler configuration

Create a Protobuf message handler configuration to configure the Protobuf message handler.

```java
import com.example.LargeObjectHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.RedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class LargeObjectHandlerConfiguration {

    @Bean
    public RedisTemplate<String, byte[]> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisTemplate<String, byte[]> redisTemplate = new RedisTemplate<>();
        redisTemplate.setConnectionFactory(redisConnectionFactory);
        redisTemplate.setKeySerializer(new StringRedisSerializer());
        redisTemplate.setValueSerializer(RedisSerializer.none());
        redisTemplate.setHashKeySerializer(new StringRedisSerializer());
        redisTemplate.setHashValueSerializer(RedisSerializer.none());
        return redisTemplate;
    }

    @Bean
    public LargeObjectHandler largeObjectHandler(RedisTemplate<String, byte[]> redisTemplate) {
        return new LargeObjectHandler(redisTemplate);
    }
}
```

### Create a Protobuf Serializer and Deserializer

Create a Protobuf Serializer and Deserializer to serialize and deserialize the large object.

```java
import com.example.LargeObject;
import org.springframework.data.redis.serializer.RedisSerializer;
import org.springframework.data.redis.serializer.SerializationException;

public class LargeObjectSerializer implements RedisSerializer<LargeObject> {

    @Override
    public byte[] serialize(LargeObject largeObject) throws SerializationException {
        return largeObject.toByteArray();
    }

    @Override
    public LargeObject deserialize(byte[] bytes) throws SerializationException {
        return LargeObject.parseFrom(bytes);
    }
}
```