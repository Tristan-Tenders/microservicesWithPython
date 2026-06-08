# Module 4 — Reflection

**Team name**: Tristan
**Branch**: `module-04/Tristan`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> activity-service doesn't wait on notification-service. The activity saves, the request returns, done. If notification-service is slow or down, the message just waits in the queue until it recovers.

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> For user validation we need the answer before we can continue — can't log an activity for a nonexistent user. Notifications are different, nobody's waiting on them. If we called notification-service over HTTP and it crashed, the message is gone. The queue keeps it.

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> Users won't notice — they never see notification delivery status anyway. As a dev you lose the immediate feedback. An HTTP call throws on failure. A queued message that never gets consumed just sits there unless you're watching the queue or logging on the consumer side.

---

*Keep this file. You will refer back to it during the oral presentation.*
