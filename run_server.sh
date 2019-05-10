#!/bin/bash

set -e

LOGFILE=/webapp/default/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=4
test -d $LOGDIR || mkdir -p $LOGDIR

./manage.py migrate 
./manage.py collectstatic --noinput

# gunicorn --worker-class gevent -w $NUM_WORKERS \
# --log-level=info -b 0.0.0.0 insopesca.wsgi

# uvicorn insopesca.asgi:application --log-level critical --workers 4


# uvicorn --host 0.0.0.0 --port 8003 --loop asyncio --http h11 insopesca.asgi:application
# uvicorn insopesca:asgi --port 8001

gunicorn --worker-class gevent -w $NUM_WORKERS \
--log-level=info -b 0.0.0.0 insopesca.asgi:application \
-k uvicorn.workers.UvicornWorker 

