#!/bin/bash

podman stop athross
podman rm athross
podman build -t athross -f build/Dockerfile .
podman run -d -p 8080:8080 --name athrros athross


exit 0