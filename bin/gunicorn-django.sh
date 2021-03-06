#! /bin/bash -x
APP=gratitude
VIRTUALENV=/opt/$APP
PORT=8080
LOGDIR=/var/log/gunicorn
SETTINGS=conf.prod.settings
PATH=/bin:/usr/bin
USER=www-data
GROUP=www-data
IP=127.0.0.1
WORKERS=5
NAME=django-gunicorn
DESC=$NAME
LOGFILE="$LOGDIR/$NAME.log"
PIDFILE="$VIRTUALENV/run/$NAME.pid"
UMASK="0660"
COMMAND="$VIRTUALENV/$APP/bin/manage.py run_gunicorn --user=$USER --group=$GROUP --workers=$WORKERS --bind=$IP:$PORT --pid=$PIDFILE --name=$NAME --log-file=$LOGFILE --umask $UMASK --log-level=info --settings=$SETTINGS"
#COMMAND="$VIRTUALENV/$APP/bin/manage.py run_gunicorn --bind=$IP:$PORT --pid=$PIDFILE --name=$NAME --log-file=$LOGFILE --log-level=info --settings=$SETTINGS"

source $VIRTUALENV/bin/activate
exec $COMMAND
