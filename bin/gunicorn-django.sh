#! /bin/bash
APP=gratitude
VIRTUALENV=/opt/$APP
PORT=8080
LOGDIR=/var/log/gunicorn/
SETTINGS=conf.prod.settings
PATH=/bin:/usr/bin
USER=www-data
GROUP=www-data
IP=127.0.0.1
WORKERS=5
NAME=`basename $0`
DESC=$NAME
LOGFILE="$LOGDIR$NAME.log"
PIDFILE="$VIRTUALENV/run/$NAME.pid"
COMMAND="$VIRTUALENV/$APP/bin/manage.py run_gunicorn --user=$USER --group=$GROUP --workers=$WORKERS --bind=$IP:$PORT --pid=$PIDFILE --name=$NAME --log-file=$LOGFILE --log-level=info --settings=$SETTINGS"

source $VIRTUALENV/bin/activate
exec $COMMAND
