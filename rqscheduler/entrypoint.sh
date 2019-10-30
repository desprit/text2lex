#!/bin/sh

sleep 5
rqscheduler --host $REDIS_HOST --port $REDIS_PORT --password $REDIS_PASS --interval 30
