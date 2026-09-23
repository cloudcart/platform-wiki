---
type: feature
nav_path: "Apps → Aura Chat → Conversations"
route_name: apps.aura_chat.conversations
route_path: /admin/apps/aura_chat/inbox
aliases: ["Aura Chat conversations", "chat transcripts", "chat history admin", "read chat conversations", "Keep this conversation for later", "Kept for later", "Show tool calls", "Order after this chat", "Bought from what the assistant showed", "разговори в чата", "история на чата", "запази разговора", "прочети разговорите"]
tags: [apps, ai, chat, conversations, inbox]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — the Conversations inbox

> Part of [[apps-aura-chat]]. See the hub for the other aspects (overview, topics and feedback, usage).

## Purpose

The **Conversations** inbox is the merchant's record of every chat: what the shopper wrote, what the assistant answered, the cards it showed and the questions it asked. It also shows who the shopper was, whether they ordered afterwards, what they thought of the chat and what the conversation was about. It is read-only. The merchant cannot reply from here.

## Where to find it

**Apps → Aura Chat → Conversations** (`/admin/apps/aura_chat/inbox`). It opens **full-screen**, without the app's tabs; **Back** returns to the Overview. The Overview's links ("See the conversations behind them", "Read the complaints", "See all conversations") open it with a filter already set.

## What the merchant can do here

- Browse conversations, newest first, and open one.
- Filter by channel, outcome, feedback, topic, and "kept".
- Read the full transcript, optionally with the assistant's working steps (**Show tool calls**).
- See the order(s) that followed a conversation, and which shown products were bought.
- Mark a conversation **Keep this conversation for later** (and **Remove the mark**).

## Settings & fields

### Filters (top bar)

| Filter | Options |
|---|---|
| **Channel** | **Storefront chat** |
| **Outcome** | **With an order** · **Without an order** · **Bought from what the assistant showed** |
| **Feedback** | **Liked** · **Complaints** |
| **Topic** | the store's topics ([[apps-aura-chat-topics-feedback]]) |
| **Kept for later** | "Only the conversations somebody kept" |

**Clear filters** resets them. Empty states: *No conversations yet* and *Nothing matches these filters*.

### The list

Each row shows who it was, a preview of the last message, the time, a **Kept for later** mark and a badge when *This shopper ordered afterwards*.

**Who** is shown as:

- a signed-in **customer's name** when the store knows it;
- **Customer #id** when the customer has since been deleted;
- a generated nickname, or **Anonymous visitor**, for a guest;
- under it, a short **Visitor** handle: the browser the conversation is filed under.

### The transcript

Messages from the shopper and the **Assistant** in order, with product cards, shop cards, question cards (and the answer chosen) exactly as shown. The rating and any complaint text appear with it. **Show tool calls** adds the steps the assistant took, by name (searching the catalog, looking up an order); it does not show the raw search results the shopper never saw.

### Details panel

| Field | Meaning |
|---|---|
| **Channel** | Storefront chat |
| **Topic** | the topic it was filed under, or **Not filed yet** |
| **Feedback** | **Happy** / **Not happy**, with the reason |
| **Started** / **Last message** | timestamps |
| **Replies** | the assistant's replies |
| **Tokens**, **Cost** | how much work the conversation took, and what it used from the allowance ([[apps-aura-chat-usage]]) |
| **Order(s) after this chat** | each order with its number of products and when it came: *{n} min / h / days after the chat*. The shown products that ended up in it are listed as **Bought from what the assistant showed**. |

## Business rules

### Transcripts are kept six months

Messages are deleted **six months** after they were written. The conversation's figures (dates, replies, usage, orders credited to it) are kept for 24 months. **Keep this conversation for later** is a bookmark for finding it again; it does **not** protect a transcript from the six-month deletion. To keep a transcript longer, copy it out.

### What the transcript records

Text from both sides, including the short lines the assistant writes while it works, plus everything drawn on screen: product cards, shop cards, question cards and the answer picked. Search results that were never shown are not recorded; the search itself appears only as a named step. Uninstalling the app keeps the conversations ([[apps-aura-chat-setup]]).

### Orders are matched to a conversation afterwards

An order appears under a conversation once the hourly matching has run, so a fresh order can take up to about an hour to show. The matching rules are on [[apps-aura-chat-overview]].

### Topics and ratings arrive later

A conversation is filed under a topic after it has been quiet for 30 minutes, in a run every 20 minutes. Until then it shows **Not filed yet**. A rating appears as soon as the shopper presses a thumb; the shopper may change it, and the last press counts ([[apps-aura-chat-topics-feedback]]).

### The shopper's copy is separate

What the merchant sees here is independent of the shopper's own history in their browser ([[apps-aura-chat-widget]]). Clearing one does not affect the other.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-overview]] — the figures that link into this inbox.
- [[apps-aura-chat-topics-feedback]] — topics and ratings.
- [[apps-aura-chat-usage]] — what Tokens and Cost draw on.
- [[orders]] — the orders listed here.

## Open questions

- Whether a conversation whose transcript has been deleted after six months still shows in the list with its figures only (verify).
