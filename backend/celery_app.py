from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv()
host=os.getenv('MYSQL_HOST')
celery = Celery(
    "builder",
    broker=f"redis://{host}:6379/0",
    backend=f"redis://{host}:6379/1",
    include=["app.celery_tasks"]
)

celery.conf.update(
    task_track_started=True,
    result_expires=3000,
)

