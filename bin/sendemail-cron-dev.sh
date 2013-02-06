#!/bin/bash -x
# for development
GRATITUDE_ENV=$HOME/personal/proj/gratitude
cd $GRATITUDE_ENV/gratitude
python bin/manage.py cron sendMessages --settings=conf.dev.settings

