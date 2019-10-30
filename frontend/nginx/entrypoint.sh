#!/bin/sh

if [ "$1" = 'nginx' ]; then
    exec nginx -g 'daemon off;';
fi

exec "$@"