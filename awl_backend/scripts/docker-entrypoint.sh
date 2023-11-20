#!/bin/sh
set -e

/wait-for-it.sh -t 300 $POSTGRES_HOST:$POSTGRES_PORT

exec "$@"
