#!/bin/bash -x
# for development
GRATITUDE_HOME=$HOME/personal/proj/gratitude/gratitude
python $GRATITUDE_HOME/bin/manage.py runserver --settings=gratitude.conf.dev.settings 127.0.0.1:8080

