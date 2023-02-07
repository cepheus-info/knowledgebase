---
title: Configure nginx to proxy pass https site
description: 
published: true
date: 2022-10-31T04:57:48.515Z
tags: 
editor: markdown
dateCreated: 2022-10-31T03:24:42.179Z
---

# Configure nginx to proxy pass https site

## Overview

As we know, nginx is a powerful web server. It can be used as a reverse proxy server to proxy pass http and https site. In this article, we will show you how to configure nginx to proxy pass https site.

## Prerequisites

- nginx
- openssl

## Step 1: Generate a self-signed certificate

First, we need to generate a self-signed certificate. We can use the following command to generate a self-signed certificate.

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
```

Then, we need to generate a certificate signing request (CSR). We can use the following command to generate a CSR.

```bash
openssl req -new -key /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.csr
```

Finally, we need to sign the certificate with the CSR. We can use the following command to sign the certificate.

```bash
openssl x509 -req -days 365 -in /etc/ssl/certs/nginx-selfsigned.csr -signkey /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
```

## Step 2: Generate a client certificate

We can use the following command to generate a client certificate.

```bash
openssl req -x509 -newkey rsa:4096 -keyout client.key -out client.pem -days 10000 -nodes
```

Copy the client certificate to the nginx server.

```bash
sudo mv client.key client.pem /etc/nginx/certs/
```

## Step 3: Configure nginx to proxy pass https site

First, we need to create a file named `example.conf` in the directory `/etc/nginx/conf.d/`. We can use the following command to create the file.

```bash
sudo touch /etc/nginx/conf.d/example.conf
```

Then, we need to edit the file. We can use the following command to edit the file.

```bash
sudo vim /etc/nginx/conf.d/example.conf
```

Next, we need to add the following content to the file.

```bash
server {
    listen      80;
    server_name www.example.com;
    #...

    location /upstream {
        proxy_pass                    https://backend.example.com;
        proxy_ssl_certificate         /etc/nginx/certs/client.pem;
        proxy_ssl_certificate_key     /etc/nginx/certs/client.key;
        proxy_ssl_protocols           TLSv1 TLSv1.1 TLSv1.2;
        proxy_ssl_ciphers             HIGH:!aNULL:!MD5;
        proxy_ssl_trusted_certificate /etc/nginx/trusted_ca_cert.crt;

        proxy_ssl_verify        on;
        proxy_ssl_verify_depth  2;
        proxy_ssl_session_reuse on;
    }
}
```

>Tips: Below is a concrete example configuration for a server that proxies to a kubenetes service. Note that sub_filter is used to modify the response content of the upstream server, as the script tag in kube-dashboard is hard-coded to use root path so we need a base tag to modify the path to the configured location.

```bash
server {
    listen 443 ssl;
    server_name  127.0.0.1 192.168.74.128;

    location /kubes/ {
        proxy_set_header Accept-Encoding "";
        proxy_pass https://127.0.0.1:10443/;
        proxy_ssl_certificate /etc/nginx/certs/client.pem;
        proxy_ssl_certificate_key /etc/nginx/certs/client.key;
        proxy_ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        proxy_ssl_ciphers HIGH:!aNULL:!MD5;
        proxy_ssl_trusted_certificate /etc/nginx/trusted_ca_cert.crt;

        proxy_ssl_verify off;

        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header "X-Accel-Buffering" no;
        proxy_buffering off;

        sub_filter_types text/html;
        sub_filter '</title>' '</title><base href="/kubes/">';
        sub_filter_once off;
    }

    ssl_certificate /etc/nginx/certs/client.pem;
    ssl_certificate_key /etc/nginx/certs/client.key;
}
```

Finally, we need to restart nginx. We can use the following command to restart nginx.

```bash
sudo systemctl restart nginx
```

## Conclusion

In this article, we have shown you how to configure nginx to proxy pass https site. We hope that this article can help you. If you have any questions, please feel free to leave a comment below.
