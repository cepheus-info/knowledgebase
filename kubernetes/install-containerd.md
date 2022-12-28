# Getting started with containerd

Follow the instruction from [Getting started with containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md) to install containerd.

## Install containerd via binaries

### Step 1: Installing containerd

Download the containerd-`<VERSION`>-`<OS`>-`<ARCH`>.tar.gz archive from [https://github.com/containerd/containerd/releases](https://github.com/containerd/containerd/releases), verify its sha256sum, and extract it under /usr/local:

```bash
tar Cxzvf /usr/local containerd-1.6.2-linux-amd64.tar.gz
bin/
bin/containerd-shim-runc-v2
bin/containerd-shim
bin/ctr
bin/containerd-shim-runc-v1
bin/containerd
bin/containerd-stress
```

Download the containerd.service unit file from [https://raw.githubusercontent.com/containerd/containerd/main/containerd.service](https://raw.githubusercontent.com/containerd/containerd/main/containerd.service) into /usr/local/lib/systemd/system/containerd.service, and run the following commands:

```bash
systemctl daemon-reload
systemctl enable --now containerd
```

### Step 2: Installing runc

Download the runc.`<ARCH`> binary from [https://github.com/opencontainers/runc/releases](https://github.com/opencontainers/runc/releases), verify its sha256sum, and install it as /usr/local/sbin/runc.

```bash
install -m 755 runc.amd64 /usr/local/sbin/runc
```

### Step 3: Installing CNI plugins

Download the cni-plugins-<OS>-<ARCH>-<VERSION>.tgz archive from https://github.com/containernetworking/plugins/releases , verify its sha256sum, and extract it under /opt/cni/bin:

```bash
mkdir -p /opt/cni/bin
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.1.1.tgz
```

## Install Containerd via package manager

Note that use package manager will not install CNI plugins. You need to install CNI plugins manually.

Refer to docker document from [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

### Step 1: Remove old versions

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

### Step 2: Install using the repository

1. Upate the package index and install packages to allow apt to use a repository over HTTPS:

```bash
 sudo apt-get update
 sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

2. Add Docker’s official GPG key:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

3. Use the following command to set up the repository:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Step 3: Install Docker Engine
```bash
sudo apt-get update
```

```bash
 sudo chmod a+r /etc/apt/keyrings/docker.gpg
 sudo apt-get update
```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### Step 4: Verify that Docker Engine is installed correctly

```bash
sudo docker run hello-world
```

