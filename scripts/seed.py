#!/usr/bin/env python3
"""Seed Postgres with mock data from frontend/src/api/mock-data.json."""
import json
import pathlib
import sys
import urllib.request
import urllib.error

USER_URL = "http://localhost:8001/v1/users/"
GAME_URL = "http://localhost:8002/v1/games/"

mock = json.loads(
    (pathlib.Path(__file__).parent.parent / "frontend/src/api/mock-data.json").read_text()
)


def post(url, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


errors = 0

print("Seeding users...")
for u in mock["users"]["items"]:
    status, body = post(USER_URL, {
        "username": u["username"],
        "email": u["email"],
        "password": "password123",
    })
    if status == 201:
        print(f"  ✓ {u['username']}")
    elif status == 400 and "already" in str(body).lower():
        print(f"  - {u['username']} (already exists)")
    else:
        print(f"  ✗ {u['username']} — {status} {body}")
        errors += 1

print("\nSeeding games...")
for g in mock["games"]["items"]:
    status, body = post(GAME_URL, {
        "title": g["title"],
        "genre": g["genre"],
        "platform": g["platform"],
        "release_year": g.get("release_year"),
        "cover_url": g.get("cover_url"),
    })
    if status == 201:
        print(f"  ✓ {g['title']}")
    elif status == 400 and "already" in str(body).lower():
        print(f"  - {g['title']} (already exists)")
    else:
        print(f"  ✗ {g['title']} — {status} {body}")
        errors += 1

print(f"\nDone. {'No errors.' if not errors else f'{errors} error(s) above.'}")
sys.exit(1 if errors else 0)
