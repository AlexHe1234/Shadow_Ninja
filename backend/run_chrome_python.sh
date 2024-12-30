#!/bin/bash

# Check if X11 forwarding is properly set up (for GUI rendering)
if [ -z "$(xhost | grep 'LOCAL:' 2>/dev/null)" ]; then
    echo "Enabling access control for local X server..."
    xhost +LOCAL:
fi

# Determine the host's IP for DISPLAY (supports macOS and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    HOST_IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
else
    HOST_IP=$(hostname -I | awk '{print $1}')
fi

# Run Docker container without auto-launching Chrome
docker run -it --memory 8192mb \
    --cpus="4.0" \
    --sysctl net.ipv6.conf.all.disable_ipv6=1 \
    --sysctl net.ipv6.conf.default.disable_ipv6=1 \
    --platform linux/amd64 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=${HOST_IP}:0 \
    -v $HOME/Downloads:/root/Downloads \
    -v $HOME/.config/google-chrome/:/data \
    --name chrome-python \
    --entrypoint /bin/bash \
    chrome-python:latest
