

from celery.schedules import crontab
from dotenv import load_dotenv
import os

load_dotenv()

# CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

CELERY_BEAT_SCHEDULE = {
    "run_parser_every_hour": {
        "task": "tasks.task.run_parser",
        "schedule": crontab(minute=0, hour="*/1"),
    },
}

CELERY_BROKER_URL = "redis://localhost:6379/0"
