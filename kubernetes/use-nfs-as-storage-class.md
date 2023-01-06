# Use Nfs as Storage Class in kubernetes

## Overview

There are lots of options which can be used as storage class in kubernetes. One of them is NFS. This guide will help us setting up a usable environment to make use of [nfs-subdir-external-provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner/).

## Mannually Installation

### Get connection information for your NFS server

At least we should know the NFS server's connection information such as hostname, etc.

### Get the NFS Subdir External Provisioner files

Clone provided provisioner repository and navigate to deploy/ folder.

```bash
git clone https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner/
cd deploy
```

Now we can edit the deployment files to use our own NFS server.

### Setup authorization

If your cluster has RBAC enabled you must authorize the provisioner.

```bash
kubectl apply -f rbac.yaml
```

### Configure the NFS subdir external provisioner

Edit your deployment.yaml to customize NFS connection information.

However, we should notice that the image repository should be replaced with an accessible address instead of gcr.io in China.

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: nfs-client-provisioner
          image: kubesphere/nfs-subdir-external-provisioner:v4.0.2
          env:
            - name: NFS_SERVER
              value: 192.168.2.207
            - name: NFS_PATH
              value: /home/share/kubernetes
      volumes:
        - name: nfs-client-root
          nfs:
            server: 192.168.2.207
            path: /home/share/kubernetes
```

### Deploying your storage class

You can refer to [https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner) for more details.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner # or choose another name, must match deployment's env PROVISIONER_NAME'
parameters:
  pathPattern: "${.PVC.namespace}-${.PVC.name}"
  archiveOnDelete: "false"
```
