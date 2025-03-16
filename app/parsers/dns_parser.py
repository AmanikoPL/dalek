from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any
from app.parsers.parsers_orm.dns_parser_orm import save_games_to_db

class DNSScraper:
    """Парсер игр с сайта DNS."""

    BASE_URLS = {
        "PlayStation": "https://www.dns-shop.kz/catalog/17a897ed16404e77/igry-dlya-playstation/?order=6&p={page}",
        "Xbox": "https://www.dns-shop.kz/catalog/17a9f99116404e77/igry-dlya-microsoft-xbox/?order=6&p={page}",
        "Nintendo": "https://www.dns-shop.kz/catalog/17a8b09516404e77/igry-dlya-nintendo/?order=6&p={page}"
    }

    def __init__(self, driver=None):
        self.driver = driver if driver else webdriver.Chrome()
        self.driver.maximize_window()

    def parse(self) -> List[Dict[str, Any]]:
        """Парсит список игр."""
        games = []

        for platform, base_url in self.BASE_URLS.items():
            page = 1

            while True:
                self.driver.get(base_url.format(page=page))
                found = False

                for i in range(1, 19):
                    try:
                        title_xpath = f'/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/div[{i}]/div[2]/a/span'
                        price_xpath = f'/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/div[{i}]/div[5]/div/div[1]'
                        availability_xpath = f'/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/div[{i}]/div[5]/div/div/button'

                        title_element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, title_xpath))
                        )
                        title = title_element.text.strip()

                        try:
                            availability_element = self.driver.find_element(By.XPATH, availability_xpath)
                            availability_text = availability_element.text.strip()
                            is_available = "В корзину" in availability_text
                        except Exception:
                            is_available = False

                        try:
                            price_element = self.driver.find_element(By.XPATH, price_xpath)
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
                        found = True
                    except TimeoutException:
                        break

                if not found:
                    break
                page += 1

        return games
    
    def close(self):
        """Закрывает браузер."""
        self.driver.quit()

if __name__ == "__main__":
    scraper = DNSScraper()
    try:
        games = scraper.parse()
        save_games_to_db(games)  # Сохранение в БД через отдельный модуль
    finally:
        scraper.close()
