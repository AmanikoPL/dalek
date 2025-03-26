# from dotenv import load_dotenv
# from celery import Celery
# from app.tasks.celery import celery_app
# from app.config import project_settings
# from app.parsers.technodom_parser import TechnodomParser

# load_dotenv()

# celery_app = Celery("tasks")
# celery_app.config_from_object('app.tasks.celery_config')
# celery_app.autodiscover_tasks()
# celery_app.conf.worker_pool = 'solo'

# celery_app.conf.timezone = "UTC"

# @celery_app.task
# def process_task(data):
#     go_parse_technodom = TechnodomParser(driver=driver)
#     print(f'Processing task with data: {data}')
#     return f'Processed: {data}'

from celery import Celery

app = Celery("tasks")

app.config_from_object("tasks.celery_config")

app.autodiscover_tasks(["tasks"])
