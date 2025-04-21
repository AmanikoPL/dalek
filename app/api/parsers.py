from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.parsers.models import Game, Platform
from selenium import webdriver
from typing import Dict, List, Any
from fastapi.responses import JSONResponse
from app.parsers.technodom_parser import TechnodomParser
from app.parsers.dns_parser import DNSScraper
from app.parsers.marwin_parser import MarwinParser
from app.parsers.parsers_orm.marwin_parser_orm import save_games_to_db
from app.tasks.celery import app
from sqlalchemy import func
from app.service.security import get_current_user
from typing import Optional
from app.parsers.models import User

router = APIRouter()

@router.get("/technodom", response_model=List[Dict[str, Any]])
def parse_technodom():
    scraper = TechnodomParser()
    try:
        return scraper.parse()
    finally:
        scraper.close()

@router.get("/dns")
def parse_dns() -> List[str]:
    scraper = DNSScraper()
    try:
        return scraper.parse()
    finally:
        scraper.close()

@router.get("/marwin")
def parse_marwin():
    parser = MarwinParser()
    try:
        games = parser.parse()
        save_games_to_db(games)
        return JSONResponse(content=games)
    finally:
        parser.close()

@router.get("/all")
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

@router.get("/games/{platform_name}")
def get_games_by_platform(platform_name: str, db: Session = Depends(get_db)):
    platform = db.query(Platform).filter(func.lower(Platform.name) == platform_name.lower()).first()
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")

    games = db.query(Game).filter(Game.platform_id == platform.id).all()
    return [
        {
            "id": game.id,
            "title": game.title,
            "price": game.price,
            "availability": game.availability,
            "store": game.store.name if game.store else None,
            "image_url": game.image_url,
        }
        for game in games
    ]

@router.get("/search")
def search_games(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    games = db.query(Game).filter(Game.title.ilike(f"%{q}%")).all()

    return [
        {
            "id": game.id,
            "title": game.title,
            "price": game.price,
            "platform": game.platform.name,
            "store": game.store.name if game.store else "Unknown",
            "image_url": game.image_url,
            "availability": game.availability,
            "url": game.url,
            "is_booked_by_me": current_user is not None and game.reserved_by_id == current_user.id
        }
        for game in games
    ]