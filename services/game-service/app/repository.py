from sqlalchemy.orm import Session

from app.models import Game
from app.schemas import GameCreate


def find_games_by_title(
    db: Session, q: str, limit: int = 20, offset: int = 0
) -> tuple[list[Game], int]:
    query = db.query(Game).filter(Game.title.ilike(f"%{q}%"))
    total = query.count()
    rows = query.offset(offset).limit(limit).all()
    return rows, total


def fetch_games(db: Session, limit: int = 20, offset: int = 0) -> tuple[list[Game], int]:
    total = db.query(Game).count()
    rows = db.query(Game).offset(offset).limit(limit).all()
    return rows, total


def find_game(db: Session, game_id: str) -> Game | None:
    return db.query(Game).filter(Game.id == game_id).first()


def delete_game(db: Session, game_id: str) -> bool:
    record = db.query(Game).filter(Game.id == game_id).first()
    if record is None:
        return False
    db.delete(record)
    db.commit()
    return True


def insert_game(db: Session, data: GameCreate) -> Game:
    record = Game(
        title=data.title,
        genre=data.genre,
        platform=data.platform,
        release_year=data.release_year,
        cover_url=data.cover_url,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
