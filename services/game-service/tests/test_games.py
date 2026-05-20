import pytest
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DB_URL = "sqlite:///./test.db"

test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def db_lifecycle():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def http():
    def _override():
        session = TestSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


SAMPLE = {
    "title": "Hollow Knight",
    "genre": "Metroidvania",
    "platform": "Switch",
    "release_year": 2017,
    "cover_url": "https://example.com/hk.jpg",
}


def test_search_is_case_insensitive(http):
    http.post("/v1/games/", json=SAMPLE)
    r = http.get("/v1/games/search?q=HOLLOW")
    assert r.status_code == 200
    assert r.json()["total"] == 1


def test_search_filters_by_title(http):
    http.post("/v1/games/", json=SAMPLE)
    http.post("/v1/games/", json={**SAMPLE, "title": "Celeste"})
    r = http.get("/v1/games/search?q=hollow")
    body = r.json()
    assert r.status_code == 200
    assert body["total"] == 1
    assert body["items"][0]["title"] == "Hollow Knight"


def test_list_returns_envelope(http):
    http.post("/v1/games/", json=SAMPLE)
    r = http.get("/v1/games/")
    body = r.json()
    assert r.status_code == 200
    assert body["total"] == 1
    assert len(body["items"]) == 1


def test_missing_game_is_404(http):
    r = http.get("/v1/games/does-not-exist")
    assert r.status_code == 404


def test_fetch_game_by_id(http):
    created = http.post("/v1/games/", json=SAMPLE).json()
    r = http.get(f"/v1/games/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_post_game_returns_201(http):
    r = http.post("/v1/games/", json=SAMPLE)
    body = r.json()
    assert r.status_code == 201
    assert body["title"] == "Hollow Knight"
    assert "id" in body
