from .celery import app as celery_app

# a list of public objects of that module, as interpreted by import *
__all__ = ('celery_app',)
