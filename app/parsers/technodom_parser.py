import json
from sqlalchemy.orm import Session
from app.orm.database import SessionLocal
from app.models.models import Game, Store, Platform
# from app.models.store import Store
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any

class TechnodomParser:
    """Парсер игр с сайта Technodom, сохраняющий данные в PostgreSQL."""
    
    BASE_URLS = {
        "PlayStation": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-playstation-4",
        "PlayStation": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-playstation-5",
        "Xbox": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-xbox",
        "Nintendo": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-nintendo"
    }

    def __init__(self, driver=None):
        self.driver = driver if driver else webdriver.Chrome()
        self.db: Session = SessionLocal()

    
    def save_to_db(self, games: List[Dict[str, Any]]):
        """Сохраняет игры в PostgreSQL."""
        store = self.db.query(Store).filter(Store.name == "Technodom").first()
        if not store:
            store = Store(name="Technodom")
            self.db.add(store)
            self.db.commit()
            self.db.refresh(store)

        for game in games:
            db_game = Game(
                title=game["title"],
                platform=game["platform"],
                price=game["price"],
                availability=game["availability"],
                store_id=store.id
            )
            self.db.add(db_game)
        
        self.db.commit()
    
    def parse(self) -> List[Dict[str, Any]]:
        """Парсит список игр и сохраняет в БД."""
        games = []

        for platform, base_url in self.BASE_URLS.items():
            self.driver.get(base_url)

            for i in range(1, 25):
                try:
                    title_xpath = (
                        f'//*[@id="__next"]/section/main/section/div/div[2]/article/ul/li[{i}]/a/div/div[2]/div[1]/p'
                    )
                    availability_xpath = (
                        f'//*[@id="__next"]/section/main/section/div/div[2]/article/ul/li[{i}]/a/div/div[3]/div/button/p'
                    )
                    price_xpath = (
                        f'//*[@id="__next"]/section/main/section/div/div[2]/article/ul/li[{i}]/a/div/div[2]/div[3]/p'
                    )

                    title_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, title_xpath))
                    )
                    title = title_element.text.strip()

                    availability_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, availability_xpath))
                    )
                    availability_text = availability_element.text.strip()
                    is_available = availability_text == "В корзину"

                    try:
                        price_element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, price_xpath))
                        )
                        price_text = price_element.text.replace("\xa0", "").replace("₸", "").strip()
                        price = int("".join(filter(str.isdigit, price_text)))
                    except Exception:
                        price = None

                    game_data = {
                        "title": title,
                        "platform": platform,
                        "price": price,
                        "availability": is_available,
                    }
                    games.append(game_data)
                except Exception:
                    break
        
        self.save_to_db(games)
        return games
    
    def close(self):
        """Закрывает браузер и БД."""
        self.driver.quit()
        self.db.close()

if __name__ == "__main__":
    scraper = TechnodomParser()
    try:
        scraper.parse()
    finally:
        scraper.close()
