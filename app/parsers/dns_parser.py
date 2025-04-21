from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any
from app.parsers.parsers_orm.dns_parser_orm import save_games_to_db

class DNSScraper:
    BASE_URLS = {
        "PlayStation": "https://www.dns-shop.kz/catalog/17a897ed16404e77/igry-dlya-playstation/?order=6&p={page}",
        "Xbox": "https://www.dns-shop.kz/catalog/17a9f99116404e77/igry-dlya-microsoft-xbox/?order=6&p={page}",
        "Nintendo": "https://www.dns-shop.kz/catalog/17a8b09516404e77/igry-dlya-nintendo/?order=6&p={page}"
    }

    def __init__(self, driver=None):
        self.driver = driver or webdriver.Chrome()
        self.driver.maximize_window()

    def parse(self) -> List[Dict[str, Any]]:
        games = []

        for platform, base_url in self.BASE_URLS.items():
            page = 1

            while True:
                self.driver.get(base_url.format(page=page))

                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "catalog-product"))
                    )
                except TimeoutException:
                    break

                product_elements = self.driver.find_elements(By.CLASS_NAME, "catalog-product")
                if not product_elements:
                    break

                for product in product_elements:
                    try:
                        title = product.find_element(By.CLASS_NAME, "catalog-product__name").text.strip()
                    except Exception:
                        continue

                    try:
                        price_text = product.find_element(By.CLASS_NAME, "product-buy__price").text
                        price = int("".join(filter(str.isdigit, price_text)))
                    except Exception:
                        price = None

                    # availability всегда True
                    is_available = True

                    try:
                        img_element = product.find_element(By.CSS_SELECTOR, "img")
                        img_url = img_element.get_attribute("src") or img_element.get_attribute("data-src")
                    except Exception:
                        img_url = None
                        
                    try:
                        link_element = product.find_element(By.XPATH, ".//a[@class='catalog-product__name ui-link ui-link_black']")
                        url = link_element.get_attribute("href")
                    except Exception:
                        url = None


                    game_data = {
                        "title": title,
                        "platform": platform,
                        "price": price,
                        "availability": is_available,
                        "image_url": img_url,
                        "url": url
                    }

                    games.append(game_data)

                page += 1

        save_games_to_db(games)
        return games

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = DNSScraper()
    try:
        scraper.parse()
    finally:
        scraper.close()
