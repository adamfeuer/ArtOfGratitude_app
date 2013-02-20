#!/bin/bash -x
GRATITUDE_ENV=/opt/gratitude
source $GRATITUDE_ENV/bin/activate
cd $GRATITUDE_ENV/gratitude
python bin/manage.py cron sendActivationReminders --settings=conf.prod.settings

