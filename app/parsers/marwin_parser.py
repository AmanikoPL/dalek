import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any
from app.parsers.parsers_orm.marwin_parser_orm import save_games_to_db

class MarwinParser:
    """Класс для парсинга списка игр с сайта Marwin."""

    BASE_URLS = {
        "PlayStation 5": "https://www.marwin.kz/videogames/playstation/igry-dliya-playstation-5/",
        "PlayStation 4": "https://www.marwin.kz/videogames/playstation/igry-dliya-playstation-4/",
        "Xbox One": "https://www.marwin.kz/videogames/xbox/igry-dlya-microsoft-xbox-one/",
        "Nintendo Switch": "https://www.marwin.kz/videogames/nintendo/igry-dlya-nintendo-switch/"
    }

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self) -> List[Dict[str, Any]]:
        """Парсит список игр и возвращает их в виде списка словарей."""
        games = []

        for platform, base_url in self.BASE_URLS.items():
            for page in range(1, 3):
                url = f"{base_url}?p={page}" if page > 1 else base_url
                self.driver.get(url)

                try:
                    product_elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, '//*[@id="amasty-shopby-product-list"]/div[3]/ol/li')
                        )
                    )

                    for index in range(1, len(product_elements) + 1):
                        try:
                            base_xpath = f'//*[@id="amasty-shopby-product-list"]/div[3]/ol/li[{index}]'
                            title_xpath = f'{base_xpath}/div/div/strong/h3/a'
                            price_xpath = f'{base_xpath}//span[@class="price"]'
                            image_xpath = f'{base_xpath}/div/a/span/span/img'

                            title_element = self.driver.find_element(By.XPATH, title_xpath)
                            title = title_element.text.strip()

                            try:
                                price_element = self.driver.find_element(By.XPATH, price_xpath)
                                price_text = price_element.text.strip()
                                price = int("".join(filter(str.isdigit, price_text)))
                            except Exception:
                                price = None

                            try:
                                image_element = self.driver.find_element(By.XPATH, image_xpath)
                                image_url = image_element.get_attribute("src")
                            except Exception:
                                image_url = None

                            game_data = {
                                "title": title,
                                "platform": platform,
                                "price": price,
                                "availability": True,
                                "image_url": image_url
                            }
                            games.append(game_data)

                        except Exception:
                            pass

                except TimeoutException:
                    break

        return games

    def close(self):
        """Закрывает драйвер."""
        self.driver.quit()

if __name__ == "__main__":
    scraper = MarwinParser()
    try:
        games = scraper.parse()
        save_games_to_db(games)
        print("Парсинг завершён и данные сохранены в БД.")
    finally:
        scraper.close()
