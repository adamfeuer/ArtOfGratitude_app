#!/bin/bash -x
# for development
GRATITUDE_ENV=/opt/gratitude
GRATITUDE_HOME=$GRATITUDE_ENV/gratitude

source $GRATITUDE_ENV/bin/activate
python $GRATITUDE_HOME/bin/manage.py run_gunicorn --settings=conf.prod.settings --bind 127.0.0.1:8080

