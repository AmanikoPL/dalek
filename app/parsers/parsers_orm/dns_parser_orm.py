from sqlalchemy.orm import Session
from app.orm.database import SessionLocal
from app.models.models import Game, Store, Platform
from typing import List, Dict, Any

def save_games_to_db(games: List[Dict[str, Any]]):
    """Сохраняет список игр в базу данных."""
    db: Session = SessionLocal()

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

        db_game = Game(
            title=game["title"],
            platform_id=platform.id,
            price=game["price"],
            availability=game["availability"],
            store_id=store.id
        )
        db.add(db_game)

    db.commit()
    db.close()
