# Module 1 — Service Decomposition

**Duration**: 2h in class
**Branch to submit**: `module-01/<team-name>`

---

## Objective

Before writing a single line of code, you need to design the system on paper. Every decision you make here: where to draw service boundaries, who owns what data, how services talk to each other, is hard to reverse once you start coding.

This module is about slowing down and thinking like an architect, not a developer.

Read these two documents before doing anything else:

- `docs/domain.md` — what GameHub is and who uses it
- `docs/specs.md` — the tech stack and key architectural decisions

> The CTO has already laid out the `services/` folder structure. Use it as a starting point, but your job is to **justify** why each folder deserves to be its own service — not just accept it.

---

## Task 1 — Identify bounded contexts _(~40 min)_

A bounded context is a part of the system that has a clear responsibility and owns its data exclusively. No other service should reach into its database.

For each bounded context you identify, fill in the table:

| Bounded Context | Responsibilities                                         | Owned Entities      | Team       |
| --------------- | -------------------------------------------------------- | ------------------- | ---------- | --- |
| Identity        | Manages who users are, handles registration and profiles | User, Session       | Platform   |
| Game Library    | Manages the games metadata and genres                    | Game,Genre,Platform | Content    |
| Activity        | Tracks what players play                                 | Activity , sessions | Engagement |
| Social          | Friends connections                                      | Friends             | Engagement |
|                 |                                                          |                     |            |     

There is no single correct answer: what matters is that you can justify each row.

---

## Task 2 — Define service contracts _(~30 min)_

For each pair of services that need to communicate, define:

- **Direction**: A → B
- **Trigger**: what causes the call
- **Protocol**: REST or event (async)
- **Payload**: key fields exchanged

Example:

```
activity-service → logging-service
Trigger: an activity is logged
Protocol: RabbitMQ message (async — why not REST here?)
Payload: { activity_id, user_id, action, game_id, timestamp }
```

Focus on the flows that feel non-obvious. You do not need to document every possible pair.

```
game-service -> activity-service
Trigger: load game detail page, "friends playing now" and popularity is needed
Protocol: REST
Payload: request{game_id , user_id}, reponse {active_players,friend_playing{user_id,game_id}}
```
```
logging-service → activity-service
Trigger: user decline GDPR via logging-service
Protocol: RabbitMQ event (async — fan-out, multi consumer)
Payload: { user_id, consent: false, revoked_at }
```

---

## Task 3 — Draw the service map _(~20 min)_

Draw the full GameHub service map:

- One box per service
- Arrows between services (solid line = synchronous REST, dashed line = async event)
- Label each arrow with its protocol
- One box at the top labelled **gateway** — all client requests enter here, no client ever calls a service directly

This can be a sketch on paper, a whiteboard photo, or ASCII art committed to your branch.

```
gameHub map


              [ gateway 8000 ]   
                    |
       -------------------------------
       |     |     |     |     |     |
       v     v     v     v     v     v
     auth  user  game  activity notif logging
     8005  8001  8002   8003   8004   8006


service -> service calls:

  gateway  -> auth      GET /v1/auth/me              (REST, per request, jwt check)
  activity -> game      GET /v1/games/{id}           (REST, enrich w/ title+cover)
  activity -> logging   GET /v1/consent/{uid}        (REST, opt-in check b4 publish)

  activity -> logging       activity.logged           (event, write audit row if opted in)
  activity -> notification  activity.created          (event, fan-out to friends)
  logging  -> activity      consent.revoked           (event, stop emitting for user)
```

---

## Discussion _(~15 min)_

Three questions to discuss as a team before you leave:

1. Why does `notification-service` use Node.js instead of Python like the rest? What does that tell you about microservices and technology choices?
2. What is the risk of `activity-service` calling `logging-service` synchronously — why might you prefer an async event instead?
3. Why does `logging-service` need a GDPR consent check before recording any activity?

You do not need to write these answers down — they are warm-up for your REFLECTION.md.

---

## Minimum to submit this branch

- [ X] Bounded context table filled in (at least 4 services justified)
- [ x] At least 3 service contracts defined
- [X ] Service map committed (sketch, photo, or ASCII)
- [X ] `REFLECTION.md` completed and committed

The map does not need to be perfect. It needs to be yours.
