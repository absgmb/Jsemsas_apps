import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
app=Celery("jsemsas")
app.config_from_object("django.conf:settings",namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule={"sync-nhia-tariffs-every-6-hours":{"task":"etc_claims.tasks.sync_nhia_tariffs","schedule":21600}}
