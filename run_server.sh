#!/bin/bash

set -e

LOGFILE=/webapp/default/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
test -d $LOGDIR || mkdir -p $LOGDIR

./manage.py migrate --noinput
./manage.py collectstatic --noinput

gunicorn --worker-class gevent -w $NUM_WORKERS \
--log-level=info -b 0.0.0.0 insopesca.wsgi
