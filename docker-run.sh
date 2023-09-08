#!/bin/bash

docker network create traefik-public

export USERNAME=admin
export PASSWORD=changeme

export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)

docker compose -f docker-compose.traefik.yml up -d
# docker compose -f docker-compose.yml up -d