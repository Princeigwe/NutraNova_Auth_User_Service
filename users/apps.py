from django.apps import AppConfig
import os
from django.conf import settings
from utils.run_celery_worker import start_worker


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # by default the django autoreloader runs twice. 
    # so any function called in the ready function is called twice.
    # this is the reason for adding the Django 'RUN_MAIN' env variable. Calls function once on auto reload.
    # Reference to: https://stackoverflow.com/questions/28489863/why-is-run-called-twice-in-the-django-dev-server/28504072#28504072
    # def ready(self) -> None:
    #     if os.environ.get('RUN_MAIN'):
    #         if settings.ENVIRONMENT == ("production" or "staging"):
    #             start_worker() # run celery worker
            