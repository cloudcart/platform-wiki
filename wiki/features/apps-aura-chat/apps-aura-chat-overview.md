---
type: feature
nav_path: "Apps → Aura Chat → Overview"
route_name: apps.aura_chat.overview
route_path: /admin/apps/aura_chat
aliases: ["Aura Chat dashboard", "Aura Chat overview", "Aura Chat analytics", "Orders assisted", "Assisted revenue", "Encouraged orders", "Customers helped", "Conversion after a chat", "revenue from chat", "chat attribution", "табло на чата", "приходи от чата", "поръчки след чат", "асистирани поръчки"]
tags: [apps, ai, chat, analytics, attribution]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — the Overview dashboard and how orders are credited

> Part of [[apps-aura-chat]]. See the hub for the other aspects (conversations, topics and feedback, usage).

## Purpose

The **Overview** tab answers three questions: how much the assistant is used, what it brings in, and what shoppers ask and think. Its sales figures rest on one rule: an order is credited to a chat when **the same browser, or the same signed-in customer, placed it after chatting**. This page lists every figure and that rule.

## Where to find it

**Apps → Aura Chat → Overview** (`/admin/apps/aura_chat`), the first tab. The header has a date range and a comparison selector (**No comparison**, the previous period, the previous year). "Pick a comparison period to see the change" until one is chosen.

## What the merchant can do here

- Pick a period and compare it with the previous period or the previous year.
- Jump into the inbox already filtered: **See the conversations behind them**, **Read the complaints**, **See all conversations** ([[apps-aura-chat-conversations]]).
- See how much allowance is left and **Top up now** ([[apps-aura-chat-usage]]).

## Settings & fields

### Headline figures (each with a daily sparkline)

| Figure | Meaning |
|---|---|
| **Conversations** | Conversations that **started** in the period, by the store's time zone. Beneath it: conversations included / left in the allowance, **Total capacity**, **See usage in detail**. |
| **Customers helped** | Different browsers that chatted in the period. |
| **Orders assisted** | Orders placed in the period that followed a conversation (rule below). |
| **Assisted revenue** | The total of those orders. |

### Sales impact

"Revenue from orders placed after a chat."

| Row | Meaning |
|---|---|
| **Conversion after a chat** | Orders assisted ÷ conversations, as a percentage. Shoppers who never chatted are not counted. |
| **Average order value** | Assisted revenue ÷ orders assisted. |
| **Revenue per conversation** | Assisted revenue ÷ conversations. |

### Encouraged orders

"From orders containing a product the assistant showed." The orders assisted that contain at least one product the assistant **put on a card** in that conversation, with their revenue and their share **Of orders assisted**. The product counts even if a different colour or size was bought. A product only mentioned in a sentence does not count.

### What customers ask about

Conversations by topic, as **% of conversations**, with the smaller ones grouped under **The rest**. Unfiled conversations have their own bar. *Nothing filed yet.* until the first ones are filed ([[apps-aura-chat-topics-feedback]]).

### What shoppers thought

Thumbs up and down for the period, reported as **complaints per 100 conversations** alongside how many were rated. **Why they were not happy** breaks down the reasons picked.

### Customer service

| Row | Meaning |
|---|---|
| **Average time to reply** | From a shopper's message to the start of the reply. A conversation left open and resumed later does not count as slow. |
| **Average conversation length** | From the first to the last message. A single question and answer is near zero. |
| **Median time to an order** | For orders assisted, the typical time from the chat to the order. |

## Business rules

### How an order is credited to a conversation

- The platform records every completed checkout with the browser that placed it. The chat records the same browser on each conversation. An order is linked to a conversation when the **browser matches**, or the **signed-in customer** matches.
- The conversation must have **started before** the order. A chat opened after paying is support, not selling.
- If the shopper chatted more than once, the order goes to the **most recent** such conversation. When both a browser and a customer match, the browser wins.
- There is no fixed cut-off after the chat: the link lasts as long as the browser keeps the store's visitor id, or the customer signs in again.
- Each order is credited **once**. Its total and currency are frozen as they were when it was placed.

### Timing and gaps

- Orders are matched **hourly**, so one placed in the last hour may not show yet.
- The purchase record the matching reads is kept only about **7 days**. Matching resumes where it stopped after a break, but an order missed for longer than that is lost to the dashboard.
- Conversations are counted on the day they started and orders on the day they were placed. A chat on the 31st that sells on the 1st lands in next month's revenue, as in the store's own reports.

### "Assisted" is association, "Encouraged" is closer to cause

**Orders assisted** says the shopper chatted and then bought; the two may be unrelated. **Encouraged orders** says the order contains something the assistant showed on a card. Neither is proof of cause. The two are shown side by side so a merchant can tell them apart.

### Ratings are not a satisfaction score

Nothing prompts a rating, and most shoppers never give one. That is why the dashboard reports complaints per 100 conversations and how many were rated, not a percentage of happy shoppers.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-conversations]] — the conversations behind each figure.
- [[apps-aura-chat-topics-feedback]] — topics and ratings.
- [[apps-aura-chat-usage]] — the allowance shown under Conversations.
- [[apps-advanced-search-orders]] — Aura Search's comparable crediting of orders to a search.

## Open questions

- Whether an order that is later cancelled or refunded drops out of **Orders assisted**. The figure is taken when the order is placed, and nothing seen so far updates it (verify).
