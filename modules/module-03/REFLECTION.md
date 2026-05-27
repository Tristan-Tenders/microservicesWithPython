# Module 3 — Reflection

**Team name**: Tristan
**Branch**: `module-03-Tristan`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> Without the gateway, you'd have to hardcode every service address into every client. 8001 for users, 8002 for games, 8003 for activities. The second something moves or scales, you're chasing down broken URLs everywhere. One address is just way less to manage.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> If you skip user validation and let the request through anyway, you end up with activities tied to users that don't exist. That's messy data and a pain to clean up. The game fetch is different though — it's just extra info on the response. If game-service is down, the activity still happened and returning null is totally fine. Holding up the whole request over that would be worse than just moving on.

---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> Every service in the chain adds its own response time on top. If one takes 3 seconds, everyone waits 3 seconds minimum. And if any service goes down completely the whole request fails, not just that piece of it. The longer the chain, the more single points of failure you're introducing.

---

*Keep this file. You will refer back to it during the oral presentation.*
