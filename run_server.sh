#!/bin/bash

set -e

LOGFILE=/webapp/default/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
test -d $LOGDIR || mkdir -p $LOGDIR

export DJANGO_SETTINGS_MODULE=insopesca.settings_prod
./manage.py migrate 
./manage.py collectstatic --noinput

gunicorn --worker-class gevent -w 1 \
--log-level=info -b 0.0.0.0 insopesca.asgi:application \
-k uvicorn.workers.UvicornWorker 

