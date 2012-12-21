#!/bin/bash -x
# for development
GRATITUDE_ENV=$WORKON_HOME/gratitude
GRATITUDE_HOME=$GRATITUDE_ENV/gratitude

source $GRATITUDE_ENV/bin/activate
python $GRATITUDE_HOME/bin/manage.py run_gunicorn --settings=conf.dev.settings --bind 127.0.0.1:8080

