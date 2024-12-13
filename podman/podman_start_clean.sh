#!/bin/bash

# Stop and remove all containers
podman stop $(podman ps -aq)
podman rm $(podman ps -aq)

# Remove the pod
podman pod rm pod_fiware

# Clean up container storage
podman system prune -f

# Run docker-compose file
podman-compose up -d