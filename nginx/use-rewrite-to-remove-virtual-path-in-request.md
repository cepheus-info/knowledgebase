# Use rewrite to remove virtual path in request

## Overview

We often use a virtual path to map different location to specified ip:port. And for many scenarios, we do not want those "path" sent to proxied server. We can make use of rewrite directive to change the default behavior.

## Configuration

```bash
location /custom-virtual-path {
    # rewrite here sends to app server without the /custom-virtual-path qualifier
    rewrite /custom-virtual-path(.*)$ $1 break;
    proxy_pass http://localhost:3304;
    proxy_set_header    X-Real-IP       $remote_addr;
    proxy_set_header    X-Forwarded-for $remote_addr;
    port_in_redirect off;
    proxy_http_version 1.1;
    chunked_transfer_encoding off;
    proxy_buffering off;
    proxy_cache off;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
    proxy_set_header Host $http_host;
}
```
