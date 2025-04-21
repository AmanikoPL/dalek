# app/parsers/parsers_orm/technodom_parser_orm.py
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.parsers.models import Game, Store, Platform
from typing import List, Dict, Any

def save_games_to_db(games: List[Dict[str, Any]]):
    db: Session = SessionLocal()
    try:
        # 1) Store
        store = db.query(Store).filter_by(name="Technodom").first()
        if not store:
            store = Store(name="Technodom")
            db.add(store); db.commit(); db.refresh(store)

        for g in games:
            # 2) Platform
            plat = db.query(Platform).filter_by(name=g["platform"]).first()
            if not plat:
                plat = Platform(name=g["platform"])
                db.add(plat); db.commit(); db.refresh(plat)

            # 3) Обновляем или создаём игру
            existing = (
                db.query(Game)
                  .filter_by(title=g["title"],
                             platform_id=plat.id,
                             store_id=store.id)
                  .first()
            )
            if existing:
                existing.price        = g["price"]
                existing.availability = g["availability"]
                existing.image_url    = g["image_url"]
            else:
                new_game = Game(
                    title        = g["title"],
                    platform_id  = plat.id,
                    store_id     = store.id,
                    price        = g["price"],
                    availability = g["availability"],
                    image_url    = g["image_url"]
                )
                db.add(new_game)

        db.commit()
    finally:
        db.close()
