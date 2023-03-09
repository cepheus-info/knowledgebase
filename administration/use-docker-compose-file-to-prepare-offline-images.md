# Use docker-compose.yml to prepare offline docker images

## 1. Introduction

As we know, docker-compose is a tool for defining and running multi-container Docker applications. When you have to deploy your services on a machine without internet access, you can prepare offline docker images and then deploy them on the machine.

## 2. Prepare docker-compose.yml

You can use the following command to generate a docker-compose.yml file:

```powershell
docker-compose config > docker-compose.yml
```

## 3. Create a tarball via a custom script

You can use the shell script [docker-prepare.sh](./resources/docker-prepare.sh) to create a tarball containing all the docker images used by the docker-compose.yml file.

```bash
# A simple example
docker-prepare -c docker-compose.yml -e VERSION_TAG -v latest -o docker-images.tar
```

```bash
# Use docker-prepare --help for more information
docker-prepare -h
```

Note that this wrapper script makes use of the following tools:

- [docker](https://docs.docker.com/engine/reference/commandline/cli/)

- [docker-compose](https://docs.docker.com/compose/reference/overview/)

- dos2unix
