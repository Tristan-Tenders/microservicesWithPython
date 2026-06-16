# Module 5 — Reflection

**Team name**: _______________
**Branch**: `module-05/<tristan>`
**Submitted**: before Module 6 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The game-service now has two models for the same data: SQLite for writes, Redis for reads. They store the same games in two different shapes.

**Why go through the trouble of maintaining two representations of the same data?**

Think about what kind of queries each model is optimised for, and what would happen if you tried to use the write model for high-traffic read operations.

> SQLite is built for writes — constraints, consistency, safe concurrent access. Redis is built for reads — you give it a key and it gives you a value, no scanning, no joins. If you try to run heavy read traffic through SQLite when things get busy, you get lock contention and slow queries. Two representations is more overhead, but you're letting each tool do the one thing it's actually fast at instead of asking one of them to do both.

---

## 2. Your choice

The logging-service checks GDPR consent before recording any activity. If a user has not opted in, the log is silently dropped.

**What does this consent check force you to accept about your data?** It is incomplete by design — some activities will never be recorded.

From a system design perspective: where is the right place to enforce this rule — in the logging-service, in the activity-service, or at the gateway? Why?

> You have to accept that your data will always have gaps. Anything that happened before a user opted in is just gone — not delayed, not backfillable, gone. That's the design. As for where the check belongs: the logging-service. It owns both the consent records and the activity logs, so it's the only one with enough context to make that call. Putting the check in the gateway means the gateway now has to understand what logging is, which it shouldn't. Putting it in the activity-service means activity tracking suddenly has to care about GDPR consent, which are two separate concerns that have no business being tangled together.

---

## 3. The tradeoff

With CQRS, your write model and read model can drift out of sync — a game is updated in SQLite but the Redis projection still shows the old data.

**In what scenario does this inconsistency matter to the user? In what scenario is it completely acceptable?**

Is there a class of applications where eventual consistency is never acceptable? What are they?

> It matters when the user is the one who made the change. You update a game's title, hit the summary endpoint immediately, and see the old name — that feels broken even though the write worked fine. The closer the action and the read are in time, the more the inconsistency sticks out. It's totally fine for something like a trending games list, where nobody expects the numbers to update in real time anyway. Financial systems are where this gets genuinely dangerous — if your bank balance is a few seconds stale while you're making a payment, that's not a minor UX annoyance, that's a correctness problem. Same with anything that controls whether a purchase goes through or whether a medical decision gets made on current data.

---

*Keep this file. You will refer back to it during the oral presentation.*
