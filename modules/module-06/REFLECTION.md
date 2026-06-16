# Module 6 — Reflection

**Team name**: _______________
**Branch**: `module-06/<tristan>`
**Submitted**: before Module 7 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The auth-service issues JWT tokens that game-service validates locally — game-service never calls auth-service to check if a token is valid.

**Why can game-service verify the token without calling auth-service?**

Think about what a signature actually proves, and what the shared secret key does.

> The token is signed with a secret key, and game-service has the same key. That's it. If the signature is valid, the token came from auth-service and nobody touched it in transit. Game-service doesn't need to phone home to confirm any of that — it can do the math locally. The only thing you lose by not calling auth-service is the ability to revoke a token mid-life, but for most read/write APIs that's an acceptable tradeoff for not adding a network hop to every single protected request.

---

## 2. Your choice

The `require_admin` dependency in game-service checks `role == "admin"` inside the token payload.

**What does this trust model assume about the token?** And what happens if the secret key leaks?

> It assumes auth-service actually checked who the user is before handing out the token. The role claim is just a string in a JSON blob — game-service only trusts it because the signature proves auth-service wrote it. If the secret key leaks, none of that holds anymore. Anyone who has the key can sign their own token with whatever role they want. There's no second check, no database lookup, nothing. One leaked key and the whole authorization layer is gone.

---

## 3. The tradeoff

JWTs can't be invalidated before they expire. If an admin account is compromised, the attacker's token is valid until the `exp` claim runs out.

**What are your options for handling this, and what does each one cost?**

Is there a scenario where short expiry times alone are enough?

> Short expiry is the simplest fix — if tokens only live 5 minutes, the window for damage is small. The problem is it makes users log in constantly. A token blocklist lets you revoke specific tokens immediately, but now you're doing a database lookup on every request, which is basically adding back the thing stateless auth was supposed to avoid. Refresh tokens split the difference: short-lived access tokens do the actual work, and a longer-lived refresh token can be revoked when you need to cut someone off. Short expiry alone is probably fine for internal tools where the users are trusted and re-auth isn't a big deal. For anything where a compromised admin account could delete data or expose users, you need actual revocation.

---

*Keep this file. You will refer back to it during the oral presentation.*
