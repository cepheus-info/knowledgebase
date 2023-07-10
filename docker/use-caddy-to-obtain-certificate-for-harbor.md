# Use Caddy to obtain certificate for harbor

## 1. Overview

When we use `docker build`, `docker push` and `docker pull` commands to interact with harbor, we will get the following error:

```bash
x509: certificate signed by unknown authority
```

This is because the certificate of harbor is self-signed. We can use [Certbot](https://certbot.eff.org/) to obtain a certificate from [Let's Encrypt](https://letsencrypt.org/), and then use the certificate to replace the self-signed certificate of harbor.

However, this method is not recommended, because we need to expose port 80 to the internet, which is not posible in some cases. Like our ISP provider does not allow us to expose port 80 to the internet.

In this case, we can use [Caddy](https://caddyserver.com/) to obtain a certificate via [DNS-Challenge](https://caddyserver.com/docs/automatic-https#dns-challenge), which is the `only way` to obtain a certificate if port 80, 443 is not available.

## 2. Walk Through

### 2.1. Install Caddy

Refer to [Guide to use caddy](../caddy/guide-to-use-caddy.md) to install and learn some basics of Caddy.

### 2.2. Obtain certificate via DNS-Challenge

#### 2.2.1. Create a Caddyfile

```Caddyfile
{
    https_port 2143
    acme_dns alidns {
            access_key_id {your-id}
            access_key_secret {your-secret}
    }
}

harbor.sfdapp.com {
    reverse_proxy 127.0.0.1:8089
    tls wujuntaocn@outlook.com
}
```

#### 2.2.2. Run Caddy

```bash
caddy run --config Caddyfile
```

### 2.3. Modify external_url of harbor

```bash
# modify /data/harbor/harbor.yml
external_url: https://harbor.sfdapp.com:2143
```

> This is important as we need to access harbor via https port 2143 outside the server.

## 3. Conclusion

After you run Caddy, you will find that a certificate is generated in the `~/.local/share/caddy/certificates/harbor.sfdapp.com` folder. And the domain `harbor.sfdapp.com` is now available via https port 2143.
