from sqlalchemy.orm import Session
from app.orm.database import SessionLocal
from app.models.models import Game, Store
from typing import List, Dict, Any

def save_games_to_db(games: List[Dict[str, Any]]):
    """Сохраняет список игр в базу данных."""
    db: Session = SessionLocal()
    
    try:
        # Проверяем, существует ли магазин Technodom
        store = db.query(Store).filter(Store.name == "Technodom").first()
        if not store:
            store = Store(name="Technodom")
            db.add(store)
            db.commit()
            db.refresh(store)

        for game in games:
            db_game = Game(
                title=game["title"],
                platform=game["platform"],
                price=game["price"],
                availability=game["availability"],
                store_id=store.id
            )
            db.add(db_game)
        
        db.commit()
    finally:
        db.close()
