from tasks.celery import app
from parsers.dns_parser import DNSScraper
from parsers.marwin_parser import MarwinParser
from parsers.technodom_parser import TechnodomParser

from parsers.parsers_orm.dns_parser_orm import save_games_to_db as save_dns_games
from parsers.parsers_orm.marwin_parser_orm import save_games_to_db as save_marwin_games
from parsers.parsers_orm.technodom_parser_orm import save_games_to_db as save_technodom_games

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.config_from_object('app.tasks.celery_config', namespace='CELERY')

app.autodiscover_tasks(['tasks'])

@app.task
def run_parser():
    """Запускает все парсеры и сохраняет данные в БД"""
    print("Запуск парсеров...")

    dns_scraper = DNSScraper()
    marwin_scraper = MarwinParser()
    technodom_scraper = TechnodomParser()

    try:
        games_dns = dns_scraper.parse()
        games_marwin = marwin_scraper.parse()
        games_technodom = technodom_scraper.parse()

        print(f"DNS: {len(games_dns)} игр найдено")
        print(f"Marwin: {len(games_marwin)} игр найдено")
        print(f"Technodom: {len(games_technodom)} игр найдено")

        if games_dns:
            save_dns_games(games_dns)
            print("Данные из DNS сохранены в БД.")

        if games_marwin:
            save_marwin_games(games_marwin)
            print("Данные из Marwin сохранены в БД.")

        if games_technodom:
            save_technodom_games(games_technodom)
            print("Данные из Technodom сохранены в БД.")

    finally:
        dns_scraper.close()
        marwin_scraper.close()
        technodom_scraper.close()

    return "Парсинг завершен!"

# PYTHONPATH=$(pwd)/app celery -A tasks.celery worker --loglevel=info