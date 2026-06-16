from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, service
from app.database import get_db

router = APIRouter(prefix="/v1/games", tags=["games"])


@router.post("/", response_model=schemas.GameOut, status_code=201)
def post_game(data: schemas.GameCreate, db: Session = Depends(get_db)):
    return service.register_game(db, data)


@router.get("/search", response_model=schemas.GameList)
def get_search(q: str, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return service.search_by_title(db, q, limit=limit, offset=offset)


@router.get("/", response_model=schemas.GameList)
def get_all(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return service.list_all_games(db, limit=limit, offset=offset)


@router.get("/{game_id}/summary")
def get_summary(game_id: str):
    from app.infrastructure.cache import get_game_summary
    summary = get_game_summary(game_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Not in cache")
    return summary


@router.get("/{game_id}", response_model=schemas.GameOut)
def get_one(game_id: str, db: Session = Depends(get_db)):
    try:
        return service.get_game_by_id(db, game_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
