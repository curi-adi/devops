#!/bin/bash

# Collect logs every 5 seconds
while true; do
    docker logs flask-app | tail -n 10 >> access.log
    echo "Logs updated: $(date)"
    sleep 5
done