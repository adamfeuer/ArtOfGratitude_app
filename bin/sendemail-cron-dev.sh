#!/bin/bash -x
# for development
GRATITUDE_ENV=$WORKON_HOME/gratitude
cd $GRATITUDE_ENV/gratitude
python bin/manage.py cron sendMessages --settings=conf.dev.settings

