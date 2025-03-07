import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any
from app.orm.database import SessionLocal
from app.models.store import Store  # Импортируем модель Store
from app.models.game import Game  # Импортируем модель Game

class MarwinParser:
    """Класс для парсинга списка игр с сайта Marwin и сохранения данных в БД."""
    
    BASE_URLS = {
        "PS5": "https://www.marwin.kz/videogames/playstation/igry-dliya-playstation-5/",
        "PS4": "https://www.marwin.kz/videogames/playstation/igry-dliya-playstation-4/",
        "Xbox One": "https://www.marwin.kz/videogames/xbox/igry-dlya-microsoft-xbox-one/",
        "Nintendo Switch": "https://www.marwin.kz/videogames/nintendo/igry-dlya-nintendo-switch/"
    }

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.db = SessionLocal()  # Создаём сессию для работы с БД
    
    def parse(self) -> List[Dict[str, Any]]:
        """Парсит список игр и сохраняет их в базу данных."""
        games = []

        for platform, base_url in self.BASE_URLS.items():
            for page in range(1, 3):
                if page > 1:
                    next_page_url = f"{base_url}?p={page}"
                    self.driver.get(next_page_url)
                else:
                    self.driver.get(base_url)

                try:
                    product_elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, '//*[@id="amasty-shopby-product-list"]/div[3]/ol/li')
                        )
                    )

                    for index in range(1, len(product_elements) + 1):
                        try:
                            title_xpath = (
                                f'//*[@id="amasty-shopby-product-list"]/div[3]/ol/li[{index}]'
                                '/div/div/strong/h3/a'
                            )
                            price_xpath = (
                                f'//*[@id="amasty-shopby-product-list"]/div[3]/ol/li[{index}]'
                                '//span[@class="price"]'
                            )

                            title_element = self.driver.find_element(By.XPATH, title_xpath)
                            title = title_element.text.strip()

                            try:
                                price_element = self.driver.find_element(By.XPATH, price_xpath)
                                price_text = price_element.text.strip()
                                price = int("".join(filter(str.isdigit, price_text)))
                            except Exception:
                                price = None

                            game_data = {
                                "title": title,
                                "platform": platform,
                                "price": price,
                                "availability": True,  # В коде не указаны товары "нет в наличии", считаем, что доступны
                                "store_id": 2  # Предполагаем, что store_id для Marwin фиксированный
                            }
                            
                            # Сохраняем данные в БД
                            self.save_to_db(game_data)

                        except Exception:
                            pass

                except TimeoutException:
                    break

        return games
    
    def save_to_db(self, game_data: Dict[str, Any]):
        """Сохраняет данные о игре в базе данных."""
        # Проверяем, существует ли магазин Technodom в базе данных
        store = self.db.query(Store).filter(Store.name == "Marwin").first()
        if not store:
            # Если магазина нет, создаём новый
            store = Store(name="Marwin")
            self.db.add(store)
            self.db.commit()
        
        # Создаём запись об игре
        game = Game(
            title=game_data['title'],
            platform=game_data['platform'],
            price=game_data['price'],
            availability=game_data['availability'],
            store_id=store.id
        )
        self.db.add(game)
        self.db.commit()
    
    def close(self):
        """Закрывает драйвер и сессию."""
        self.db.close()  # Закрываем сессию
        self.driver.quit()

if __name__ == "__main__":
    scraper = MarwinParser()
    try:
        scraper.parse()
        print("Парсинг завершён и данные сохранены в БД.")
    finally:
        scraper.close()
