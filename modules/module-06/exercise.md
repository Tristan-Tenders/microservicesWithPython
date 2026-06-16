# Module 6 — Authentication & Authorization

**Duration**: 2h in class
**Branch to submit**: `module-06/<team-name>`

---

## Objective

Right now any caller can hit any endpoint. This module adds a dedicated `auth-service` that issues signed JWT tokens, and wires token validation into `game-service` so that only admins can delete games.

You will implement two things: the JWT creation and verification logic in `auth-service`, and the admin-only `DELETE /v1/games/{id}` endpoint in `game-service`.

---

## Before you start

Your module-05 work must be in place: gateway on port 8000, all prior services running.

No new infrastructure is needed for this module — `auth-service` is a plain FastAPI app with no database.

Install dependencies:

```bash
cd services/auth-service && pip install -r requirements.txt
cd services/game-service && pip install -r requirements.txt
```

---

## What's provided

- `auth-service` skeleton with hardcoded users (testuser/gamer, admin/adminpass, activity-service/m2m-secret)
- `auth-service/app/security.py` — two stub functions to implement
- `game-service/app/security.py` — `require_admin` dependency, fully implemented, waiting to be wired in
- Both services share the same secret key (`dev-secret-change-in-production`) — that's how game-service can verify tokens without calling auth-service

---

## Part A — JWT implementation in auth-service *(~40 min)*

Open `services/auth-service/app/security.py`. Two functions raise `NotImplementedError`:

**`create_access_token(data: dict) -> str`**

1. Copy the `data` dict so you don't mutate the original
2. Add an `"exp"` claim: `datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)`
3. Encode with `jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)`
4. Return the token string

**`get_current_user(credentials) -> dict`**

1. Decode with `jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])`
2. Catch `JWTError` and raise `HTTPException(status_code=401, detail="Invalid or expired token")`
3. Return the decoded payload dict

Test with:

```bash
# Start auth-service
uvicorn app.main:app --port 8005

# Get a token
curl -X POST http://localhost:8005/v1/auth/token \
  -d "username=testuser&password=password"

# Verify /me returns your claims
curl http://localhost:8005/v1/auth/me \
  -H "Authorization: Bearer <token>"
```

Paste the token at https://jwt.io to inspect the claims directly.

---

## Part B — Admin-protected delete in game-service *(~40 min)*

1. Uncomment `auth_secret_key` in `game-service/app/config.py` — it must match `auth-service`'s secret key
2. Add `DELETE /v1/games/{game_id}` to `game-service/app/routes.py` using `require_admin` as a dependency:

```python
from app.security import require_admin

@router.delete("/{game_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_one(game_id: str, db: Session = Depends(get_db)):
    ...
```

Register `auth-service` in the gateway (`gateway/app/config.py` and `gateway/app/main.py`) — the lines are commented out with `# Added in Module 6`.

Test the three cases:

```bash
# No token → 403
curl -X DELETE http://localhost:8000/v1/games/<id>

# Gamer token → 403 (valid token, wrong role)
TOKEN=$(curl -s -X POST http://localhost:8005/v1/auth/token \
  -d "username=testuser&password=password" | jq -r .access_token)
curl -X DELETE http://localhost:8000/v1/games/<id> \
  -H "Authorization: Bearer $TOKEN"

# Admin token → 204
ADMIN=$(curl -s -X POST http://localhost:8005/v1/auth/token \
  -d "username=admin&password=adminpass" | jq -r .access_token)
curl -X DELETE http://localhost:8000/v1/games/<id> \
  -H "Authorization: Bearer $ADMIN"
```

---

## Discussion *(~15 min)*

- `game-service` never calls `auth-service` to validate a token. How does it know the token is genuine?
- The role claim inside the token is just a string. What's stopping a caller from forging it?
- JWT tokens can't be revoked before they expire. What are your options if an admin account is compromised?

---

## Minimum to submit this branch

- [ ] `POST /v1/auth/token` returns a signed JWT
- [ ] `GET /v1/auth/me` returns the token payload
- [ ] `DELETE /v1/games/{id}` returns 401 with no token, 403 with a gamer token, 204 with an admin token
- [ ] `auth-service` registered in the gateway under `auth`
- [ ] `REFLECTION.md` completed and committed
