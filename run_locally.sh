#!/bin/bash
eval $(ssh-agent)
ssh-add 
DOCKER_BUILDKIT=1 docker build --ssh default -t paint-api:dev .
docker run --network="host" -it --rm --env-file dev.env -p 8124:8124 -v ~/.cache:/root/.cache/ paint-api:dev
