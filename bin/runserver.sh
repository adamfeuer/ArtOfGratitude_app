#!/bin/bash -x
# for development
GRATITUDE_HOME=$WORKON_HOME/gratitude/gratitude
python $GRATITUDE_HOME/bin/manage.py runserver --settings=gratitude.conf.dev.settings

