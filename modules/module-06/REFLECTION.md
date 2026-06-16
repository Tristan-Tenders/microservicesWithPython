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

> JWTs are self-contained. The auth-service signs the token with a secret key, and game-service has the same key, so it can verify the signature locally without asking anyone. If the signature checks out, the token is genuine — nobody tampered with it. The only thing a central auth check would add is the ability to revoke tokens before they expire, which we're not doing here. For most use cases, local verification is fast enough and removes a network call on every protected request.

---

## 2. Your choice

The `require_admin` dependency in game-service checks `role == "admin"` inside the token payload.

**What does this trust model assume about the token?** And what happens if the secret key leaks?

> It assumes the token was issued by a service that actually verified the user's identity and assigned them the right role. The role claim in the payload is just a string — game-service trusts it because the signature proves auth-service put it there. If the secret key leaks, that whole trust model collapses. Anyone with the key can mint a token with `"role": "admin"` and delete every game in the system. The key is the only thing standing between the system and a full privilege escalation.

---

## 3. The tradeoff

JWTs can't be invalidated before they expire. If an admin account is compromised, the attacker's token is valid until the `exp` claim runs out.

**What are your options for handling this, and what does each one cost?**

Is there a scenario where short expiry times alone are enough?

> The main options are: short expiry (tokens die fast, so the damage window is small), a token blocklist (you store revoked token IDs server-side, which adds a database lookup on every request and partially defeats the point of stateless auth), or rotating refresh tokens (short-lived access tokens paired with longer-lived refresh tokens that can be revoked). Short expiry alone is enough when the risk is low and the UX cost of re-authenticating frequently is acceptable — internal tooling, for example. For anything where a compromised admin account could cause serious damage, you need a blocklist or refresh token rotation so you can actually cut off access when you notice the breach.

---

*Keep this file. You will refer back to it during the oral presentation.*
