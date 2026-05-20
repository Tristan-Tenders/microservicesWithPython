# Module 2 — Reflection

**Team name**: _______________
**Branch**: `module-02/<team-name>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

 Layers matter when something has to change. Swapping SQLite for Postgres is a `database.py` edit, not a grep across every route. And a new dev knows where to look instead of reading one giant file.

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

 If notification-service wrote directly to my `games` table, it skips `GameCreate` validation, so junk rows show up that `GameOut` can't even serialize. Then I add a column next sprint and their old inserts break in prod. Coupled at the worst level: the table.

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

 The more files, more imports, more tests pasy off when a second dev shows up. The alternative is a 600-line file you can't find anything in.

---

*Keep this file. You will refer back to it during the oral presentation.*
