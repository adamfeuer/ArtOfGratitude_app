#!/bin/bash -x
# for development
GRATITUDE_HOME=$WORKON_HOME/gratitude/gratitude
python $GRATITUDE_HOME/bin/manage.py run_gunicorn --settings=gratitude.conf.dev.settings --bind 127.0.0.1:8080

