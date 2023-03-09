#!/usr/bin/env bash

usage="$(basename "$0") [-h] [-c] [-e] [-v] [-o] -- program to prepare docker deployment package

where:
    -h  show this help text
    -c  set the --compose-file (default: docker-compose.yml)
    -e  set the --env tag name (default: VERSION_TAG)
    -v  set the --version (default: latest)
    -o  set the --output (default: docker-compose.latest.tar.gz)"

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)
      echo "$usage"
      exit
      ;;
    -c|--compose-file)
      compose_file="$2"
      ;;
    -e|--env)
      env="$2"
      ;;
    -v|--version)
      version="$2"
      ;;
    -o|--output)
      output="$2"
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      echo "$usage"
      exit 1
  esac
  shift
  shift
done

compose_file="${compose_file:-docker-compose.yml}"
env="${env:-VERSION_TAG}"
version="${version:-latest}"
default_name=$compose_file.$version.tar.gz
removed_ext_name=${default_name//.yml/}
output=${output:-$removed_ext_name}

dos2unix $compose_file

export $env=$version && podman-compose -f $compose_file pull && \
cat $compose_file | grep 'image:' | awk '{print $2}' | sed s/\${$env}/$version/g | xargs -I{} echo {} && \
cat $compose_file | grep 'image:' | awk '{print $2}' | sed s/\${$env}/$version/g | dos2unix | xargs podman save | gzip > $output && \
echo the output file is: $output

# Previous way to filter images and docker save
# docker image ls | grep $version | awk '{print $1":"$2}' | xargs docker save | gzip > $output