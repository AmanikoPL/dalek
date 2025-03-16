import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.baseclass import Base  # Импортируем базовый класс моделей


# Загружаем переменные из .env
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для отладки

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Создаёт сессию для взаимодействия с БД и закрывает её после работы"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def init_db():
#     """Создание таблиц в базе данных"""
#     from app.models import game, store, user, platforms  # Импортируем модели, чтобы SQLAlchemy их увидел
#     Base.metadata.create_all(bind=engine)

# from app.orm.database import init_db

# if __name__ == "__main__":
#     init_db()
#     print("✅ Таблицы успешно созданы!")