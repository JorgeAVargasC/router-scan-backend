#!/bin/bash

docker network rm router-scan-bridge-network
docker network create router-scan-bridge-network \
  --driver bridge \
  --subnet '192.168.1.0/24' \
  --gateway '192.168.1.254'

docker stop router-scan-backend
docker rm router-scan-backend
docker run \
  --name router-scan-backend \
  --network router-scan-bridge-network \
  --publish 5000:5000 \
  javargas1209/router-scan-backend