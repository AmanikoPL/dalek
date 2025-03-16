from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user import UserCreate
from app.service.hashing import hash_password

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
