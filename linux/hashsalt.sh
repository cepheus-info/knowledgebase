#!/bin/bash
# parameter 1: password
# parameter 2: salt
password=$1
salt=$2
# calc sha256 hash
echo $(echo -n $password | sha256sum | awk '{print $1}')$salt | sha256sum | awk '{print $1}'