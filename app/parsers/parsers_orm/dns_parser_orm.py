import re
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.parsers.models import Game, Store, Platform
from typing import List, Dict, Any

def clean_game_title(title: str, platform: str) -> str:
    title = re.sub(r"\(.*?\)|\[.*?\]", "", title).strip()
    title = re.sub(r"\s+", " ", title)
    platform_map = {
        "PlayStation": "PS",
        "Xbox": "XB",
        "Nintendo": "NS"
    }

    short_platform = platform_map.get(platform, platform)
    return f"{title} {short_platform}"

def save_games_to_db(games: List[Dict[str, Any]]) -> None:
    db: Session = SessionLocal()
    store = db.query(Store).filter_by(name="DNS").first()
    if not store:
        store = Store(name="DNS")
        db.add(store)
        db.commit()
        db.refresh(store)

    for game in games:
        platform = db.query(Platform).filter_by(name=game["platform"]).first()
        if not platform:
            platform = Platform(name=game["platform"])
            db.add(platform)
            db.commit()
            db.refresh(platform)

        clean_title = clean_game_title(game["title"], game["platform"])

        existing_game = db.query(Game).filter_by(
            title=clean_title,
            platform_id=platform.id,
            store_id=store.id
        ).first()

        if existing_game:
            existing_game.price = game["price"]
            existing_game.availability = game["availability"]
            existing_game.image_url = game["image_url"]
            existing_game.url = game.get("url")  # 🆕 добавлено обновление URL
        else:
            new_game = Game(
                title=clean_title,
                platform_id=platform.id,
                store_id=store.id,
                price=game["price"],
                availability=game["availability"],
                image_url=game["image_url"],
                url=game.get("url")  # 🆕 добавлено при создании
            )
            db.add(new_game)

    db.commit()
    db.close()
