# celery.py
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

# create a Celery instance and configure it using the settings from Django.
app = Celery("webapp")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

if(os.environ.get("REDISCLOUD_URL")):   
    app.conf.update(
        BROKER_URL=os.environ["REDISCLOUD_URL"], CELERY_RESULT_BACKEND=os.environ["REDISCLOUD_URL"]
    )
else:
    app.conf.update(
        BROKER_URL="redis://localhost:6379/0", CELERY_RESULT_BACKEND="redis://localhost:6379/0"
    )