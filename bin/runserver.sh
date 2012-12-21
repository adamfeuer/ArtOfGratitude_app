#!/bin/bash -x
# for development
GRATITUDE_HOME=/opt/gratitude/gratitude
python $GRATITUDE_HOME/bin/manage.py runserver --settings=conf.prod.settings 127.0.0.1:8080

