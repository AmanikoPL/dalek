from sqlalchemy.orm import Session
from app.parsers.database import SessionLocal
from app.parsers.models import Game, Store, Platform
from typing import List, Dict, Any

def save_games_to_db(games: List[Dict[str, Any]]):
    """Сохраняет список игр в базу данных."""
    db: Session = SessionLocal()
    
    try:
        store = db.query(Store).filter(Store.name == "Marwin").first()
        if not store:
            store = Store(name="Technodom")
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
            print(db_game)
            db.add(db_game)
        
        db.commit()
    finally:
        db.close()
