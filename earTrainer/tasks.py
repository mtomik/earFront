from __future__ import absolute_import, unicode_literals
from celery import shared_task
from functools import wraps
from earDetectionWebApp.celery import app


@shared_task
def add(x,y):
    return x+y


@app.task
def create_samples():
    return "hello"
