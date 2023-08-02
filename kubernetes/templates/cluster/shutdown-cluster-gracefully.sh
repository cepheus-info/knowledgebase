#!/bin/bash
# Get nodes
nodes=$(kubectl get nodes -o name)
# Drain nodes
for node in $nodes
do
    kubectl drain $node --ignore-daemonsets
done
# Shutdown nodes
for node in $nodes
do
    # In normal GUN/Linux, we can use shutdown -h now, but in alpine linux, we need to use poweroff
    # ssh $node sudo shutdown -h now
    ssh $node poweroff
done