# Guide to use caddy

## 1. Walkthrough basic json config

### 1.1. Install caddy

```bash
curl https://getcaddy.com | bash -s personal
```

### 1.2. Create caddy.json

```json
{
  "apps": {
    "http": {
      "servers": {
        "example": {
          "listen": [":2015"],
          "routes": [
            {
              "handle": [
                {
                  "handler": "static_response",
                  "body": "Hello, world!"
                }
              ]
            }
          ]
        }
      }
    }
  }
}
```

### 1.3. Run caddy

```bash
caddy run
```

### 1.4. Upload caddy.json to caddy server

```bash
curl -X POST -H "Content-Type: application/json" -d @caddy.json http://localhost:2019/load
```

### 1.5. Test caddy server

```bash
curl http://localhost:2015
```

## 2. Walkthrough Caddyfile

### 2.1. Create Caddyfile

```bash
touch Caddyfile
```

```Caddyfile
:2015

respond "Hello, world!"
```

### 2.2. Run caddy

```bash
caddy adapt --config Caddyfile
caddy run
```

### 2.3. Test caddy server

```bash
curl http://localhost:2015
```

## 3. Reload caddy server

```bash
caddy reload --config Caddyfile
```
