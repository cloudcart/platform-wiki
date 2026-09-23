---
type: feature
nav_path: "Apps → Aura Chat → Knowledge & Skills → Orders / Returns"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["chat order status", "where is my order chat", "chat return request", "return through chat", "chat withdrawal", "return verification code", "chat did not find my order", "return reference", "статус на поръчка в чата", "връщане през чата", "код за връщане", "къде е поръчката ми"]
tags: [apps, ai, chat, orders, returns, support]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 3
---

# Aura Chat — order lookups and return requests

> Part of [[apps-aura-chat]]. See the hub for the other aspects (skills, behaviour, selling).

## Purpose

This page sums up the playbooks of the two after-sale skills. **Orders** tells a shopper where an order stands. **Returns** takes a return request and lodges it with the store; it needs Aftercare. The full text is in `aura-chat-skill-order-status.txt` and `aura-chat-skill-order-returns.txt` ([[apps-aura-chat-prompts]]).

## Where to find it

Switched on at **Apps → Aura Chat → Knowledge & Skills** ([[apps-aura-chat-skills]]). Lodged returns land in the Aftercare inbox ([[apps-aftercare]]).

## What the merchant can do here

- Switch **Orders** and **Returns** on or off separately. Switching on one never switches on the other.
- Install Aftercare from the Returns section if it is missing.
- Decide in Aftercare what a return may contain and how refunds are made. The assistant asks only what the store's return settings allow.

## Settings & fields

None in Aura Chat beyond the two switches. Return options come from Aftercare.

## Business rules

### Orders: two keys, never a hint which one was wrong

- The lookup needs **both** the order's identifier and the **email used at checkout**. The assistant asks only for whichever is missing.
- It asks for "what is on your confirmation", because stores show a number (`93`) or a reference code (`KxaxH5R`), and both work.
- On no match it asks the shopper to check **both**, and **never says which one was wrong**, because that pair is what keeps a stranger out of someone's order.
- It reports status, payment, contents and the courier's own tracking progress. When courier events are unavailable, it hands over the tracking link.
- It never promises a delivery date, refund or exception the lookup did not confirm. When it cannot resolve something, it says what happens next and who follows up.
- It does not sell during a support conversation.

### Returns: four steps, and the store decides

1. **Who and which order.** Three free-text cards in one turn: name, the order's identifier and the order's email. It skips any the shopper already gave.
2. **The code.** A **6-digit code** is emailed to the order's email address and to no other. The assistant never knows or guesses it. It does not say the order was found, only that a code is on its way if the details match. Nothing arrived? It suggests the spam folder, then **resend**, telling the shopper the wait before a resend is allowed. Lost access to that mailbox means this cannot be done in the chat, and it points to the store's contacts.
3. **Choices.** It asks only what this store's return settings offer:
   - **which items and how many**, only if the store allows partial returns (bundle lines go back together; lines marked whole go back whole);
   - **why** — always asked once, optional, never to talk them out of it;
   - **how the money comes back**, only if the store records refund methods for that scope, with bank transfer adding **IBAN** and **account holder** (never card details);
   - **agreement to the store's legal pages**, by name and link, before anything is lodged.
   An order that never shipped is recorded as a **cancellation**, and the assistant says there is nothing to send back.
4. **Lodge it.** The request is created as `PENDING`, and the shopper gets the **reference** as a separate line.

### Only the store refuses

The assistant never refuses a return itself. The return window, if the store has one, is used only to answer "how long do I have". It is never turned into a refusal or a warning, and a shopper past it may still lodge the request. If the store's system refuses at the last step, the assistant relays that and stops.

### Amounts: what it cost vs what comes back

It may say what the order and each line **cost**. It never states what will be **refunded** until the store has worked that out and returned it, and then it quotes the store's own labels and figures exactly. It never promises that the return is approved, that money is on its way, or when.

### Checking a return already lodged

Needs **only the reference** (there is no search by order number or email). It reports:

- `PENDING` — lodged and waiting on the store (no guess how long);
- `RETURNED` — closed, the store has the goods;
- `CANCELLED` — will not go ahead.

It keeps apart three figures: what the order cost, what the store worked out to refund, and what was actually paid out. Money counts as sent only when a payment date is recorded.

### The store's internal note

A note the store wrote on a return is **relayed as written** when it explains the decision in terms the shopper can use. It is **withheld entirely** when it is not fit for a customer (an insult, internal shorthand, a colleague's name, a remark about someone else). In that case the assistant says the store has not given a reason it can share, and never hints that a note exists. When unsure, it withholds.

### Tone

One plain sentence acknowledging that something went wrong, then the steps. It gives no verdict on whose fault it was and does not upsell to someone returning goods.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-skills]] — the switches.
- [[apps-aftercare]] — where return requests land and where their options are set.
- [[orders]] — the order records the lookup reads.
- [[apps-aura-chat-behaviour]] — the rules that apply to every reply.

## Open questions

- None known.
