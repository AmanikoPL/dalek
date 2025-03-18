from sqlalchemy.orm import Session
from app.models.models import User
from app.service.security import hash_password
from app.schemas.user import UserCreate

def create_user(db: Session, user_data: UserCreate, password: str):
    hashed_password = hash_password(password)  # предполагаемая функция хеширования
    db_user = User(email=user_data.email, hashed_password=hashed_password, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
