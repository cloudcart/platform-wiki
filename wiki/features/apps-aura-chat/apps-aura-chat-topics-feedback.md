---
type: feature
nav_path: "Apps → Aura Chat → Knowledge & Skills → Conversation topics"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["Conversation topics", "chat topics", "What customers ask about", "Conversation feedback", "Ask what the shopper thought", "thumbs up down chat", "chat rating", "Restore the standard reasons", "Помогнах ли ти?", "Некласифицирани", "теми на разговорите", "оценка на разговора", "палец нагоре надолу"]
tags: [apps, ai, chat, topics, feedback, analytics]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — conversation topics and shopper feedback

> Part of [[apps-aura-chat]]. See the hub for the other aspects (overview, conversations, appearance).

## Purpose

Two settings let the merchant read conversations in bulk rather than one by one:

- **Conversation topics**: the store's own list of subjects. Every finished conversation is filed under exactly one, and the dashboard counts them.
- **Conversation feedback**: a thumbs-up / thumbs-down row the shopper can press, with reasons to choose from after a thumbs-down.

## Where to find it

- Topics: **Apps → Aura Chat → Knowledge & Skills → Conversation topics** (`/admin/apps/aura_chat/knowledge`).
- Feedback: **Apps → Aura Chat → Settings → Ask what the shopper thought** (`/admin/apps/aura_chat/settings`).
- Results: the Overview's *What customers ask about* and *What shoppers thought* ([[apps-aura-chat-overview]]), and the inbox filters ([[apps-aura-chat-conversations]]).

## What the merchant can do here

- Add, rename, describe and remove topics (up to 12).
- Switch the rating row on or off.
- Edit the reasons offered after a thumbs-down (up to 8), or **Restore the standard reasons**.

## Settings & fields

### Conversation topics

"What every conversation is filed under, and what the dashboard counts. Renaming one is free — it keeps its place in the chart. Removing one that has conversations behind it keeps the name for the months it existed, because a past chart of unreadable slugs helps nobody."

| Field | Limit |
|---|---|
| Topic name | up to 60 characters (placeholder *e.g. Warranty*) |
| Description | up to 200 characters, optional: "When the name alone would not say where the line falls" |
| Number of topics | up to 12 (**Add a topic**; *You can have at most 12 topics.*) |

**Друго (Other)** cannot be removed: "Kept always: without it a conversation that fits nothing is forced into whichever topic is nearest." Removed topics that were already used appear under **No longer offered**, kept only to label past months.

The standard topics a new store starts with:

| Topic | Covers |
|---|---|
| Препоръка на продукт | helping them choose what to buy |
| Информация за продукт | a question about a specific product: specifications, materials, what fits what |
| Наличност | whether something is in stock, or where it can be seen |
| Статус на поръчка | an order already placed: where it is, when it arrives |
| Доставка | how delivery works: prices, deadlines, couriers, areas |
| Връщания и рекламации | returning, exchanging, or complaining about something bought |
| Магазини и работно време | the shops themselves: addresses, opening hours, contacts |
| Друго | anything that fits none of the others |

### Conversation feedback

"A thumbs up or down on the conversation as a whole, not on one reply. Nothing nags: the row appears once, ten seconds after the assistant has finished, and goes away on the next message."

- **Ask the shopper to rate the conversation**: the switch. "One row under the newest reply. It disappears on the next message, or two seconds after they answer."
- **Reasons**: "What the shopper can point at when they are not happy. They may also write a sentence of their own." Up to 8, each up to 60 characters (placeholder *e.g. It did not find what I was looking for*, **Add a reason**). Removed reasons that shoppers already chose are kept under **No longer offered**.
- **Restore the standard reasons** puts back the four standard ones, in the store's language:

| Bulgarian | English |
|---|---|
| Не намери каквото търся | Could not find what I want |
| Даде ми грешна информация | Gave me wrong information |
| Не разбра въпроса ми | Did not understand my question |
| Не можа да помогне | Could not help |

A **new store starts with it on**, with the four standard reasons ([[apps-aura-chat-setup]]).

## Business rules

### Filing is automatic, after the conversation goes quiet

A conversation is filed once it has been quiet for **30 minutes**, in a run every **20 minutes**. The filing reads **only what the shopper wrote** (about the first 1,500 characters), never the assistant's replies, so the subject is what the shopper came for rather than what was recommended. It picks exactly one topic from the store's current list, using the descriptions to decide close cases. Until filed, a conversation shows **Not filed yet**; on the chart it counts under **Некласифицирани** (unfiled), which is different from **Друго**. The filing instruction is in `aura-chat-topic-filing.txt` ([[apps-aura-chat-prompts]]).

### Changing the list does not refile the past

New and renamed topics apply to conversations filed from then on. Conversations already filed keep their topic. A removed topic keeps its name on past months and is never offered again.

### What the shopper sees

*Помогнах ли ти?* with **Да** / **Не**. After **Не**: *Какво не беше наред?*, the reasons as buttons and a free-text field (*или напиши…*, up to 500 characters), then *Благодаря.* A shopper who presses **Да** is asked nothing.

### One rating per conversation, the last press counts

The rating belongs to the conversation, not a single reply. A shopper may change their mind; the last press is kept. A thumbs-up clears any reason given earlier.

### Read complaints, not a satisfaction rate

Most shoppers never rate, so silence is not approval. The dashboard shows **complaints per 100 conversations** and how many were rated, and lists **Why they were not happy** by reason ([[apps-aura-chat-overview]]). **Read the complaints** opens the inbox filtered to complaints.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-overview]] — the charts built from topics and ratings.
- [[apps-aura-chat-conversations]] — the Topic and Feedback filters.
- [[apps-aura-chat-appearance]] — the rest of the Settings tab.

## Open questions

- None known.
