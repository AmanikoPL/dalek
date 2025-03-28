import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any
from parsers_orm.technodom_parser_orm import save_games_to_db

class TechnodomParser:
    """Парсер игр с сайта Technodom."""

    BASE_URLS = {
        "PlayStation 4": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-playstation-4",
        "PlayStation 5": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-playstation-5",
        "Xbox": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-xbox",
        "Nintendo": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-nintendo"
    }

    def __init__(self, driver: webdriver.Chrome = None):
        """Инициализация парсера с возможностью передачи драйвера."""
        self.driver = driver or webdriver.Chrome()

    def parse(self) -> List[Dict[str, Any]]:
        """Парсит список игр и возвращает их в виде списка словарей."""
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

        return games

    def close(self):
        """Закрывает браузер."""
        self.driver.quit()

if __name__ == "__main__":
    scraper = TechnodomParser()
    try:
        games = scraper.parse()
        save_games_to_db(games)  # Сохраняем в БД
        print("Парсинг завершён и данные сохранены в БД.")
    finally:
        scraper.close()
