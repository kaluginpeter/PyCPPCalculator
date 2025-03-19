# backend/celery_app.py
from celery import Celery

app = Celery('computation_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.update(
    result_expires=3600,
)

# Import the task
from backend.tasks import make_computation