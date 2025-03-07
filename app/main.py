from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.technodom_parser import TechnodomParser
from app.api.dns_parser import DNSScraper
from app.api.marwin_parser import MarwinParser
from app.orm.database import init_db, get_db
from app.models import user
from app.schemas.user import UserCreate
from app.service.auth import create_user
from app.database import Base, engine
from selenium import webdriver
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
from app.service.user import create_user
from app.models.user import User
from app.api.auth import router as auth_router
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.service.jwt import create_access_token
from app.service.hashing import verify_password
from app.schemas.user import UserLogin

app = FastAPI()
router = APIRouter()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")

Base.metadata.create_all(bind=engine)
print("🚀 Создаём таблицы в базе данных...")
init_db()
print("✅ Таблицы успешно созданы!")
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    print("Таблицы успешно созданы!")

@app.get("/parse/technodom")
def parse_technodom() -> Dict[str, List]:
    driver = webdriver.Chrome()
    try:
        parser = TechnodomParser(driver)
        return parser.parse()
    finally:
        driver.quit()

@app.get("/parse/dns")
def parse_dns() -> List[str]:
    scraper = DNSScraper()
    try:
        return scraper.parse()
    finally:
        scraper.close()

@app.get("/parse/marwin")
def parse_marwin() -> List[str]:
    scraper = MarwinParser()
    try:
        return scraper.parse()
    finally:
        scraper.close()

@app.get("/parse/all")
def parse_all() -> Dict[str, List]:
    technodom_games, dns_games, marwin_games = [], [], []

    driver = webdriver.Chrome()
    try:
        technodom_parser = TechnodomParser(driver)
        technodom_games = technodom_parser.parse()
    finally:
        driver.quit()

    dns_scraper = DNSScraper()
    try:
        dns_games = dns_scraper.parse()
    finally:
        dns_scraper.close()

    marwin_scraper = MarwinParser()
    try:
        marwin_games = marwin_scraper.parse()
    finally:
        marwin_scraper.close()

    return {
        "technodom": technodom_games,
        "dns": dns_games,
        "marwin": marwin_games
    }

@app.post("/register/")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user_data)
    return {"email": new_user.email, "is_active": new_user.is_active}


@router.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
