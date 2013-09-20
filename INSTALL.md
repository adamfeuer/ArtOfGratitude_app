Ubuntu Linux installation instructions
======================================

Note that this may work for other Linux distributions, but I have not tested them.

1. Install Apache 2.6 web server.
2. Install Python 2.7.x.
3. Install PIP (Python package manager). On Ubuntu, this can be done with "apt-get install python-pip"
4. Install Python packages virtualenv and optionally virtualenvwrapper
5. Make a new Python virtualenv. 
6. Clone the repo (or link it) to YOUR_NEW_VIRTUALENV/gratitude
7. Install the Python packages needed: "pip install -r YOUR_NEW_VIRTUALENV/gratitude/requirements.pip"
8. Run gunicorn with YOUR_NEW_VIRTUALENV/gratitude/bin/gunicorn-django.sh 

This will run gunicorn on port 8080. You may want to set up apache or nginx to accept requests on port 443 and forward them to port 80. 

This application assumes there is an apache webserver running on port 80 and 443. It redirects all port 80 to port 443. There is a 
Wordpress installation doing content management, and this app is made to look as if it is part of that Wordpress website.


