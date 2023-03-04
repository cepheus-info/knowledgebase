# Use Podman to manage containers

## 1. Introduction

In this article, we will use Podman to manage containers. It should be noted that Podman is a daemonless container engine for developing, managing, and running OCI Containers on your Linux System. It is a drop-in replacement for Docker that requires no daemon. Podman provides a Docker-compatible command line that eases the transition from other container engines and allows the management of pods, containers, container images, and container volumes.

Compare to Docker-Desktop, Podman is more lightweight and can also be used on Windows. It is also a good choice for developers who want to use containers on Windows.

## 2. Install & Running Podman

### 2.1. Install Podman on Windows

Podman is also available on Windows. You can install it by following the [official guide](https://podman.io/getting-started/installation#windows).

### 2.2. Initialize Podman on Windows

After installing Podman, you need to initialize it by running the following command:

```powershell
podman machine init
```

### 2.3. Start Podman on Windows

```powershell
podman machine start
```

## 3. Use Podman to manage containers

### 3.1. Pull a container image

```powershell
podman pull docker.io/library/redis:latest
```

### 3.2. List all container images

```powershell
podman images
```

## 4. Use Podman-compose

### 4.1. Install Podman-compose

```powershell
# Note that you need to install python3 first.
pip install podman-compose
```

### 4.2. Use Podman-compose to start a container

This is much like what you do with docker-compose. You can use the following command to start a container.

```powershell
podman-compose up -d
```
