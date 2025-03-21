import re
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Game, Store, Platform
from typing import List, Dict, Any

def clean_game_title(title: str, platform: str) -> str:
    """Очищает название игры, оставляя только имя и платформу."""
    # Убираем всё в скобках (обычные и квадратные)
    title = re.sub(r"\(.*?\)|\[.*?\]", "", title).strip()

    # Убираем лишние пробелы
    title = re.sub(r"\s+", " ", title)

    # Сокращаем платформу
    platform_map = {
        "PlayStation": "PS",
        "Xbox": "XB",
        "Nintendo": "NS"
    }
    short_platform = platform_map.get(platform, platform)

    return f"{title} {short_platform}"

def save_games_to_db(games: List[Dict[str, Any]]):
    """Сохраняет список игр в базу данных с очищенными названиями."""
    db: Session = SessionLocal()
    
    try:
        # Проверяем, существует ли магазин DNS
        store = db.query(Store).filter(Store.name == "DNS").first()
        if not store:
            store = Store(name="DNS")
            db.add(store)
            db.commit()
            db.refresh(store)

        for game in games:
            # Проверяем, существует ли платформа
            platform = db.query(Platform).filter(Platform.name == game["platform"]).first()
            if not platform:
                platform = Platform(name=game["platform"])
                db.add(platform)
                db.commit()
                db.refresh(platform)

            # Очищаем название игры
            clean_title = clean_game_title(game["title"], game["platform"])

            db_game = Game(
                title=clean_title,
                platform_id=platform.id,
                price=game["price"],
                availability=game["availability"],
                store_id=store.id
            )
            print(f"Processing game: {game}")
            print(f"Cleaned title: {clean_title}")

            db.add(db_game)
        
        db.commit()
    finally:
        db.close()
