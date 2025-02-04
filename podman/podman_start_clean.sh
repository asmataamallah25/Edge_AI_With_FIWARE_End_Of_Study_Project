#!/bin/bash

# Stop all containers
podman stop $(podman ps -aq)

# Remove all containers
podman rm -f $(podman ps -aq)

# Remove all pods
podman pod rm -f $(podman pod ls -q)

# Remove all volumes
podman volume prune -f
