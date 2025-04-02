import re
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.parsers.models import Game, Store, Platform
from typing import List, Dict, Any

def clean_game_title(title: str, platform: str) -> str:
    """Очищает название игры, оставляя только имя и платформу."""

    title = re.sub(r"\(.*?\)|\[.*?\]", "", title).strip()

    title = re.sub(r"\s+", " ", title)

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
        store = db.query(Store).filter(Store.name == "DNS").first()
        if not store:
            store = Store(name="DNS")
            db.add(store)
            db.commit()
            db.refresh(store)

        for game in games:
            platform = db.query(Platform).filter(Platform.name == game["platform"]).first()
            if not platform:
                platform = Platform(name=game["platform"])
                db.add(platform)
                db.commit()
                db.refresh(platform)

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
