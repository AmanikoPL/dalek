
from celery import Celery
import logging
from app.parsers.dns_parser import DNSScraper
from app.parsers.marwin_parser import MarwinParser
from app.parsers.technodom_parser import TechnodomParser
from app.parsers.parsers_orm.dns_parser_orm import save_games_to_db as save_dns_games
from app.parsers.parsers_orm.marwin_parser_orm import save_games_to_db as save_marwin_games
from app.parsers.parsers_orm.technodom_parser_orm import save_games_to_db as save_technodom_games

app = Celery("tasks")

app.config_from_object("app.tasks.celery_config")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.task
def run_parser():
    """Запускает все парсеры и сохраняет данные в БД"""
    logger.info("Запуск парсеров...")
    
    dns_scraper = DNSScraper()
    marwin_scraper = MarwinParser()
    technodom_scraper = TechnodomParser()
    
    try:
        games_dns = dns_scraper.parse()
        games_marwin = marwin_scraper.parse()
        games_technodom = technodom_scraper.parse()
        
        logger.info(f"DNS: {len(games_dns)} игр найдено")
        logger.info(f"Marwin: {len(games_marwin)} игр найдено")
        logger.info(f"Technodom: {len(games_technodom)} игр найдено")
        
        if games_dns:
            save_dns_games(games_dns)
            logger.info("Данные из DNS сохранены в БД.")
        
        if games_marwin:
            save_marwin_games(games_marwin)
            logger.info("Данные из Marwin сохранены в БД.")
        
        if games_technodom:
            save_technodom_games(games_technodom)
            logger.info("Данные из Technodom сохранены в БД.")
        
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}", exc_info=True)
    
    finally:
        dns_scraper.close()
        marwin_scraper.close()
        technodom_scraper.close()
        
    return "Парсинг завершен!"