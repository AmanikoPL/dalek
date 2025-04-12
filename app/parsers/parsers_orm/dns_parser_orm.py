import re
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.parsers.models import Game, Store, Platform
from typing import List, Dict, Any

def clean_game_title(title: str, platform: str) -> str:
    title = re.sub(r"\(.*?\)|\[.*?\]", "", title).strip()
    title = re.sub(r"\s+", " ", title)
    print('3333333333333333333333333')
    platform_map = {
        "PlayStation": "PS",
        "Xbox": "XB",
        "Nintendo": "NS"
    }

    short_platform = platform_map.get(platform, platform)
    return f"{title} {short_platform}"

def save_games_to_db(games: List[Dict[str, Any]]) -> None:
    db: Session = SessionLocal()
    print('2222222222222222222222222222222')
    store = db.query(Store).filter_by(name="DNS").first()
    if not store:
        store = Store(name="DNS")
        db.add(store)
        db.commit()
        db.refresh(store)

    for game in games:
        print('111111111111111111111111')
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
        else:
            new_game = Game(
                title=clean_title,
                platform_id=platform.id,
                store_id=store.id,
                price=game["price"],
                availability=game["availability"],
                image_url=game["image_url"]
            )
            db.add(new_game)

    db.commit()
    db.close()
