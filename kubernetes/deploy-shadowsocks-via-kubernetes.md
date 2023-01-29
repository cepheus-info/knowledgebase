# Deploy Shadowsocks + V2ray-plugin + Nginx via kubernetes

## 1. Overview

Shadowsocks is a popular solution to provide a proxy to access other network. But it's unstable if we do not make some ssl trick here.

## 2. Prepare the host machines

### 2.1 Install CRI-O/Containerd as Container runtime

You can choose either CRI-O or Containerd as your container runtime, as they are both kubernetes compatible.

### 2.2 Install kubernetes environment

For High performance servers & virtual machines, a full featured kubernetes cluster is recommended. For personal usage & testing purpose, a k3s single master environment is enough.

## 3. Guide to install shadowsocks

### 3.1 Copy neccesary files into a hostPath

> Use below commands to create a temporary container and copy /usr/local/bin from docker container to local machine.

```bash
mkdir -p /home/shadowsocks
# create tmp config.json
cat <<EOF | sudo tee /home/shadowsocks/config.json
{
    "server": "localhost",
    "server_port": 8388,
    "password": "mypassword",
    "method": "aes-256-gcm"
}
EOF
# run tmp container
docker run --name ssserver-rust \
  --restart always \
  -p 8388:8388/tcp \
  -p 8388:8388/udp \
  -v /home/shadowsocks/config.json:/etc/shadowsocks-rust/config.json \
  -dit ghcr.io/shadowsocks/ssserver-rust:latest
```

Execute below command to copy:

```bash
# use docker cp to copy /usr/local/bin into /home/shadowsocks
docker cp containerId:/usr/local/bin /home/shadowsocks
```

Note: The reason to run this step is that in kubernetes, if we mount a container directory to hostPath, then the contents created via Dockerfile's COPY command will be covered by that hostPath. It become an issue as we will mount /usr/local/bin to a plugins volume.
The workaround here is use docker cp to manually copy these files into a hostPath.

See [discussion here](https://discuss.kubernetes.io/t/inside-containers-mount-path-folder-no-file-present-only-lost-found-directory/9262/6) for more information.

<i>You need to copy data into the volume. Whatever path you mount it on will be hidden inside your running container, regardless of whether your image has data there. Docker tries to be clever and copy files there, but Kubernetes does not - too many edge cases. You made a volume, you have to initialize it. Only you know what that really means for your app.</i>

### 3.2 Shadowsocks config

#### 3.2.1 config.yaml

Below is a sample config.yaml and some tips here:

> service_port is the port which can be accessed externally, here we choose 32001 as we will bind a k8s service nodePort to 32001
> plugin_opts will be passed to v2ray-plugin

- If we want ss_client -> nginx(tls) -> ss_server, then we can just use:

```yaml
plugin_opts: server;path=/custom-virtual-path
```

- If we want ss_client -> ss_server(tls), then we need to use below config, and mount certificates into a specified location:

```yaml
plugin_opts: server;path=/custom-virtual-path;tls;host=domain-name;cert=/etc/cert/fullchain.pem;key=/etc/cert/privkey.pem
```

Please note the certificates should be chmod a+r first.

```bash
# This privkey.pem is obtained before we setup shadowsocks app.
# Please refer to the nginx part to obtain a correct certificate
chmod a+r /etc/cert/privkey.pem
```

> The sample config.yaml

```yaml
servers:
  - fast_open: true
    method: aes-256-gcm
    mode: tcp_and_udp
    password: your_password
    server:
      - "::"
      - 127.0.0.1
    server_port: 8388
    service_port: 32001
    plugin: v2ray-plugin
    # Note: if you need to use tls for ssserver directly,
    # Replace with plugin_opts: server;path=/custom-virtual-path;tls;host=domain-name;cert=/etc/cert/fullchain.pem;key=/etc/cert/privkey.pem
    # And the certificate should be chmod a+r first
    plugin_opts: server;path=/custom-virtual-path
```

#### 3.2.2 config.json

We can use yq command line tool to convert yaml to json

```bash
# use below command to convert yaml to json
yq config.yaml --tojson > config.json
# use below command to convert json to yaml
yq --prettyPrint config.json > config.yaml
```

### 3.3 Shadowsocks-rust.yaml

Below is a full kubernetes yaml with some tips here, note you can find an original version from [https://github.com/shadowsocks/shadowsocks-rust/blob/master/k8s/shadowsocks-rust.yaml](https://github.com/shadowsocks/shadowsocks-rust/blob/master/k8s/shadowsocks-rust.yaml)

> The config.json in shadowsocks-rust.yaml is copied from above prepared json block

> The service type is set as NodePort for convenience:

```yaml
spec:
  type: NodePort
  ports:
    - name: ss-8388
      targetPort: 8388
      protocol: TCP
      port: 8388
      nodePort: 32001
```

> We copied initContainers from [https://github.com/shadowsocks/shadowsocks-rust/blob/master/k8s/chart/templates/deployment.yaml](https://github.com/shadowsocks/shadowsocks-rust/blob/master/k8s/chart/templates/deployment.yaml), this is for downloading v2ray_plugins into containers:/usr/local/bin, which is mounted as plugins volume.

```yaml
initContainers:
  - name: plugin-downloader
    image: busybox
    command:
      - sh
      - -c
      - |
        TAG=$(wget -qO- https://api.github.com/repos/shadowsocks/v2ray-plugin/releases/latest | grep tag_name | cut -d '"' -f4)
        wget https://github.com/shadowsocks/v2ray-plugin/releases/download/$TAG/v2ray-plugin-linux-amd64-$TAG.tar.gz
        tar -xf *.gz
        rm *.gz
        mv v2ray* /usr/local/bin/v2ray-plugin
        chmod +x /usr/local/bin/v2ray-plugin

        TAG=$(wget -qO- https://api.github.com/repos/teddysun/xray-plugin/releases/latest | grep tag_name | cut -d '"' -f4)
        wget https://github.com/teddysun/xray-plugin/releases/download/$TAG/xray-plugin-linux-amd64-$TAG.tar.gz
        tar -xf *.gz
        rm *.gz
        mv xray* /usr/local/bin/xray-plugin
        chmod +x /usr/local/bin/xray-plugin
    volumeMounts:
      - name: plugins
        mountPath: /usr/local/bin
```

> The plugins volume is created as hostPath rather than emptyDir, because it's sharing the docker-entrypoint.sh & ssserver directory declared in Dockerfile. If we use emptyDir, these files will be covered. So we are mounting it as a hostPath and copying these files manually.

```yaml
volumes:
  - name: config
    configMap:
      name: shadowsocks-rust
  - name: plugins
    hostPath:
      path: /home/ubuntu/shadowsocks/bin
```

> Shadowsocks-rust.yaml

```yaml
---
# Source: shadowsocks-rust/templates/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: shadowsocks-rust
  labels:
    helm.sh/chart: shadowsocks-rust-0.1.0
    app.kubernetes.io/name: shadowsocks-rust
    app.kubernetes.io/instance: shadowsocks-rust
    app.kubernetes.io/version: "1.x.x"
    app.kubernetes.io/managed-by: Helm
---
# Source: shadowsocks-rust/templates/config.yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: shadowsocks-rust
  labels:
    helm.sh/chart: shadowsocks-rust-0.1.0
    app.kubernetes.io/name: shadowsocks-rust
    app.kubernetes.io/instance: shadowsocks-rust
    app.kubernetes.io/version: "1.x.x"
    app.kubernetes.io/managed-by: Helm
data:
  config.json: |
    {
      "servers":
        [
          {
            "fast_open": true,
            "method": "aes-256-gcm",
            "mode": "tcp_and_udp",
            "password": "opensuse",
            "server": ["::", "127.0.0.1"],
            "server_port": 8388,
            "service_port": 32001,
            "plugin": "v2ray-plugin",
            "plugin_opts": "server;path=/custom-virtual-path;host=domain-name"
          }
        ]
    }
---
# Source: shadowsocks-rust/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: shadowsocks-rust
  labels:
    helm.sh/chart: shadowsocks-rust-0.1.0
    app.kubernetes.io/name: shadowsocks-rust
    app.kubernetes.io/instance: shadowsocks-rust
    app.kubernetes.io/version: "1.x.x"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  ports:
    - name: ss-8388
      targetPort: 8388
      protocol: TCP
      port: 8388
      nodePort: 32001
  selector:
    app.kubernetes.io/name: shadowsocks-rust
    app.kubernetes.io/instance: shadowsocks-rust
---
# Source: shadowsocks-rust/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shadowsocks-rust
  labels:
    helm.sh/chart: shadowsocks-rust-0.1.0
    app.kubernetes.io/name: shadowsocks-rust
    app.kubernetes.io/instance: shadowsocks-rust
    app.kubernetes.io/version: "1.x.x"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: shadowsocks-rust
      app.kubernetes.io/instance: shadowsocks-rust
  template:
    metadata:
      labels:
        app.kubernetes.io/name: shadowsocks-rust
        app.kubernetes.io/instance: shadowsocks-rust
    spec:
      serviceAccountName: shadowsocks-rust
      securityContext: {}
      volumes:
        - name: config
          configMap:
            name: shadowsocks-rust
        - name: plugins
          hostPath:
            path: /home/ubuntu/shadowsocks/bin
      initContainers:
        - name: plugin-downloader
          image: busybox
          command:
            - sh
            - -c
            - |
              TAG=$(wget -qO- https://api.github.com/repos/shadowsocks/v2ray-plugin/releases/latest | grep tag_name | cut -d '"' -f4)
              wget https://github.com/shadowsocks/v2ray-plugin/releases/download/$TAG/v2ray-plugin-linux-amd64-$TAG.tar.gz
              tar -xf *.gz
              rm *.gz
              mv v2ray* /usr/local/bin/v2ray-plugin
              chmod +x /usr/local/bin/v2ray-plugin

              TAG=$(wget -qO- https://api.github.com/repos/teddysun/xray-plugin/releases/latest | grep tag_name | cut -d '"' -f4)
              wget https://github.com/teddysun/xray-plugin/releases/download/$TAG/xray-plugin-linux-amd64-$TAG.tar.gz
              tar -xf *.gz
              rm *.gz
              mv xray* /usr/local/bin/xray-plugin
              chmod +x /usr/local/bin/xray-plugin
          volumeMounts:
            - name: plugins
              mountPath: /usr/local/bin
      containers:
        - name: shadowsocks-rust
          securityContext: {}
          image: "ghcr.io/shadowsocks/ssserver-rust:latest"
          imagePullPolicy: IfNotPresent
          volumeMounts:
            - name: config
              mountPath: /etc/shadowsocks-rust
              readOnly: true
            - name: plugins
              mountPath: /usr/local/bin
          ports:
            - name: ss-8388
              containerPort: 8388
              protocol: TCP
          livenessProbe:
            tcpSocket:
              port: 8388
            failureThreshold: 3
            initialDelaySeconds: 1
            timeoutSeconds: 1
          readinessProbe:
            tcpSocket:
              port: 8388
            initialDelaySeconds: 2
          resources:
            limits:
              cpu: 100m
              memory: 128Mi
            requests:
              cpu: 20m
              memory: 32Mi
---
# Source: shadowsocks-rust/templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "shadowsocks-rust-test-connection"
  labels:
    helm.sh/chart: shadowsocks-rust-0.1.0
    app.kubernetes.io/name: shadowsocks-rust
    app.kubernetes.io/instance: shadowsocks-rust
    app.kubernetes.io/version: "1.x.x"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ["wget"]
      args: ["shadowsocks-rust:"]
  restartPolicy: Never
```

### 3.4 Apply shadowsocks-rust.yaml

Now you can use below command to apply kubernetes yaml file:

```bash
kubectl apply -f shadowsocks-rust.yaml
```

### 3.5 Use Nginx to reverse proxy ssserver

After setup nginx, the network topology will be ssclient -> nginx -> ssserver. And it looks like we are accessing a normal website via https. After all, people accessing this domain-name name will get a normal website response, only if we use v2ray_plugin + correct password + correct path (/custom-virtual-path here) will connect to the real ssserver.

```properties
server {
    listen 80;

    server_name domain-name;

    root /home/www/public-html;

    error_page  404              /404.html;

    location = /404.html {
        root /usr/share/nginx/html;
    }

    location /custom-virtual-path {
        proxy_pass http://localhost:32001;
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
}
```

### 3.6 Setup DNS A records at your Cloud Provider's console

Setup DNS A records for your domain-name & ip address. After this step, we can access the website normally. And if we're not use tls in ssclient, the ssclient -> nginx -> ssserver connection should work as well, but without ssl.

### 3.7 Use certbot to apply certificate

Install certbot as [https://certbot.eff.org/instructions](https://certbot.eff.org/instructions), and issue a correct certificate for your domain-name.

### 3.8 Use tls plugin_opts in your ssclient config

```json
{
  "server": "domain-name",
  "server_port": 443,
  "password": "your-password",
  "method": "aes-256-gcm",
  "plugin": "v2ray-plugin_windows_amd64",
  "plugin_opts": "tls;host=domain-name;path=/custom-virtual-path;",
  "remarks": "server-remarks",
  "timeout": 5,
  "warnLegacyUrl": false
}
```

## 4. Conclusion

It's not that easy to run multiple individual components as a solution without neccesary experience and practices.
