from sqlalchemy.orm import Session

from app import repository
from app.infrastructure.cache import set_game_summary
from app.schemas import GameCreate, GameList, GameOut


def search_by_title(db: Session, q: str, limit: int = 20, offset: int = 0) -> GameList:
    rows, total = repository.find_games_by_title(db, q, limit=limit, offset=offset)
    return GameList(
        items=[GameOut.model_validate(r) for r in rows],
        total=total,
        limit=limit,
        offset=offset,
    )


def list_all_games(db: Session, limit: int = 20, offset: int = 0) -> GameList:
    rows, total = repository.fetch_games(db, limit=limit, offset=offset)
    return GameList(
        items=[GameOut.model_validate(r) for r in rows],
        total=total,
        limit=limit,
        offset=offset,
    )


def get_game_by_id(db: Session, game_id: str) -> GameOut:
    record = repository.find_game(db, game_id)
    if record is None:
        raise ValueError(f"Game {game_id} not found")
    return GameOut.model_validate(record)


def remove_game(db: Session, game_id: str) -> None:
    deleted = repository.delete_game(db, game_id)
    if not deleted:
        raise ValueError(f"Game {game_id} not found")


def register_game(db: Session, data: GameCreate) -> GameOut:
    record = repository.insert_game(db, data)
    set_game_summary(record.id, {
        "id": record.id,
        "title": record.title,
        "genre": record.genre,
        "platform": record.platform,
    })
    return GameOut.model_validate(record)
