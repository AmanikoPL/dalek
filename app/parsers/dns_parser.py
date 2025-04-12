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
        self.driver = driver if driver else webdriver.Chrome()
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
                        try:
                            price_text = product.find_element(By.CLASS_NAME, "product-buy__price").text
                            price = int("".join(filter(str.isdigit, price_text)))
                        except Exception:
                            price = None
                        try:
                            availability_text = product.find_element(By.CLASS_NAME, "button-ui").text.strip()
                            is_available = "В корзину" in availability_text
                        except Exception:
                            is_available = False
                        try:
                            img_element = product.find_element(By.CSS_SELECTOR, "img")
                            img_url = img_element.get_attribute("src") or img_element.get_attribute("data-src")
                        except Exception:
                            img_url = None

                        game_data = {
                            "title": title,
                            "platform": platform,
                            "price": price,
                            "availability": is_available,
                            "image_url": img_url
                        }
                        
                        games.append(game_data)
                    except Exception:
                        continue

                page += 1
        save_games_to_db(games)
        return games

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = DNSScraper()
    print('Name vizvalsya')
    try:
        games = scraper.parse()
        save_games_to_db(games)
    finally:
        scraper.close()
