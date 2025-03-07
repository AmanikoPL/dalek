from sqlalchemy.orm import Session
from app.models.user import User
from app.service.hashing import hash_password

def create_user(db: Session, email: str, password: str):
    hashed_password = hash_password(password)
    user = User(email=email, hashed_password=hashed_password, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
