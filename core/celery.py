# core/celery.py
import os
from celery import Celery

# Add this line to set the worker pool to 'solo' on Windows.
if os.name == 'nt':  # 'nt' is the name for Windows
    os.environ['CELERY_WORKER_POOL'] = 'solo'

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Create a Celery app instance.
app = Celery('core')

# ... (the rest of your celery.py file)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debuf_task(self):
    print(f"Request: {self.request!r}")