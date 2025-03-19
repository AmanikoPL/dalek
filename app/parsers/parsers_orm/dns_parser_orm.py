from sqlalchemy.orm import Session
from database import SessionLocal
from models import Game, Store, Platform
from typing import List, Dict, Any

def save_games_to_db(games: List[Dict[str, Any]]):
    """Сохраняет список игр в базу данных."""
    db: Session = SessionLocal()
    
    try:
        # Проверяем, существует ли магазин DNS
        store = db.query(Store).filter(Store.name == "DNS").first()
        if not store:
            store = Store(name="DNS")  # Исправлено с "Technodom" на "DNS"
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

            # Проверяем цену и конвертируем в int, если нужно
            try:
                price = str(game["price"]) if game["price"] else None
            except ValueError:
                price = None  # Если вдруг в price попало не число

            db_game = Game(
                title=game["title"],
                platform_id=platform.id,  # Используем ID платформы
                price=price,  # Исправлено преобразование цены
                availability=game["availability"],
                store_id=store.id
            )
            print(f"Processing game: {game}")
            print(f"DB Game Object: {db_game.__dict__}")

            db.add(db_game)
        
        db.commit()
    finally:
        db.close()
