from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.parsers.models import Game
from fastapi.responses import RedirectResponse
from app.parsers.models import Game, User
from app.service.security import get_current_user


router = APIRouter()

@router.post("/games/{game_id}/click")
def reserve_game(game_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.reserved_by_id and game.reserved_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Game already reserved")

    game.availability = False
    game.reserved_by_id = current_user.id
    db.commit()
    return {"redirect_url": game.url}

@router.get("/user/reserved")
def get_reserved_games(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    games = db.query(Game).filter(Game.reserved_by_id == current_user.id).all()

    return [
        {
            "id": g.id,
            "title": g.title,
            "price": g.price,
            "platform": g.platform.name if g.platform else "Unknown",
            "image_url": g.image_url,
            "store": g.store.name if g.store else "Unknown",
            "url": g.url,
        }
        for g in games
    ]
