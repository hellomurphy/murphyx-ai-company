#!/usr/bin/env bash
# Dev tool — local Redis via docker. No business logic.
set -e
docker run -d --name murphyx-redis -p 6379:6379 redis:7-alpine 2>/dev/null || docker start murphyx-redis
echo "Redis on localhost:6379"
