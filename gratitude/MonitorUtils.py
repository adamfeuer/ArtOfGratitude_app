import logging, subprocess
from django.conf import settings

logger = logging.getLogger(__name__)

class MonitorUtils:
   def __init__(self):
      pass

   def isWebserverRunning(self):
      p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
      out, err = p.communicate()
      djangoFound = False
      apacheFound = False
      for line in out.splitlines():
         if settings.DJANGO_PROCESS_NAME in line:
            djangoFound = True
         elif settings.APACHE_PROCESS_NAME in line:
            apacheFound = True
         if djangoFound and apacheFound:
            break
      return djangoFound and apacheFound
