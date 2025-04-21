from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any
from app.parsers.parsers_orm.technodom_parser_orm import save_games_to_db

class TechnodomParser:
    """Парсер игр с сайта Technodom без перехода по страницам."""

    BASE_URLS = {
        "PlayStation": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejmerov/igry-dlja-pristavok/igry-playstation-5",  # единая страница PlayStation
        "Xbox": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejмеров/игры-xbox",
        "Nintendo": "https://www.technodom.kz/karaganda/catalog/vsjo-dlja-gejмеров/игры-nintendo",
    }

    def __init__(self, driver: webdriver.Chrome = None):
        self.driver = driver or webdriver.Chrome()
        self.driver.maximize_window()

    def parse(self) -> List[Dict[str, Any]]:
        games: List[Dict[str, Any]] = []

        for platform, url in self.BASE_URLS.items():
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((
                        By.XPATH,
                        '//*[@id="__next"]/section/main/section/div/div[2]/article/ul/li'
                    ))
                )
            except TimeoutException:
                continue

            items = self.driver.find_elements(
                By.XPATH,
                '//*[@id="__next"]/section/main/section/div/div[2]/article/ul/li'
            )

            for prod in items:
                try:
                    title = prod.find_element(
                        By.XPATH,
                        './/div/div[2]/div[1]/p'
                    ).text.strip()
                except Exception:
                    continue

                # всегда помечаем как доступное
                is_available = True

                try:
                    price_text = prod.find_element(
                        By.XPATH,
                        './/div/div[2]/div[3]/p'
                    ).text
                    price = int("".join(filter(str.isdigit, price_text)))
                except Exception:
                    price = None

                # поиск URL картинки
                img_url = None
                for img_xpath in [
                    './/div/div[1]/div[2]/div/picture/img',
                    './/div/div[1]/div[2]/div/div[1]/div/div[1]/div/div/picture/img'
                ]:
                    try:
                        img_el = prod.find_element(By.XPATH, img_xpath)
                        img_url = img_el.get_attribute("src")
                        if img_url:
                            break
                    except Exception:
                        continue

                games.append({
                    "title": title,
                    "platform": platform,
                    "price": price,
                    "availability": is_available,
                    "image_url": img_url,
                })

        save_games_to_db(games)
        return games

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = TechnodomParser()
    try:
        games = scraper.parse()
        print("Парсинг Technodom завершён и данные сохранены в БД.")
    finally:
        scraper.close()