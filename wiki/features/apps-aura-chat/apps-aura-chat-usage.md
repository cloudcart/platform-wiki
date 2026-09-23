---
type: feature
nav_path: "Apps → Aura Chat → Usage"
route_name: apps.aura_chat.usage
route_path: /admin/apps/aura_chat/usage
aliases: ["Aura Chat usage", "Aura Chat credits", "Buy more credits", "Top up now", "Aura Chat allowance", "Conversations left", "Total capacity", "chat stopped answering", "allowance is used up", "Aura Chat price", "кредити за чата", "лимит на чата", "чатът спря да отговаря", "оставащи разговори"]
tags: [apps, ai, chat, billing, usage]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — credits, the allowance, and running out

> Part of [[apps-aura-chat]]. See the hub for the other aspects (overview, setup, conversations).

## Purpose

Aura Chat runs on **prepaid credit**. Every answer the assistant gives uses up some of the store's **allowance**. When the allowance is used up, the assistant stops answering until more credit is bought. This page covers where to see the allowance, how credit is added, and how "conversations left" is estimated. Actual prices and per-conversation amounts are shown in the admin and depend on the AI processing each conversation takes, so they are not recorded here.

## Where to find it

- **Apps → Aura Chat → Usage** (`/admin/apps/aura_chat/usage`): the detail.
- **Overview**: a summary under **Conversations**, with **Top up now** and **See usage in detail** ([[apps-aura-chat-overview]]).
- **Buy more credits**, in the app header on every tab, opens the purchase dialog **Aura Chat credits**.

## What the merchant can do here

- See the allowance, how much is used, and roughly how many conversations are left.
- See this month's activity: conversations, replies, length, and what one conversation takes.
- Buy credit.

## Settings & fields

### The allowance ("Counted since the assistant was installed")

| Field | Meaning |
|---|---|
| **Allowance** | The ceiling the assistant may spend in total. |
| **Loaded** | Credit bought and paid for. |
| **Used** | What the assistant has used since installation. |
| **Conversations left** | An estimate of how many more conversations the rest will cover. |
| **Total capacity** | The same estimate for the whole allowance. |

"Credits are added to the balance and do not expire."

### This month

**Started this month**, **Conversations**, **Replies** ("Answers the assistant gave"), **Replies per conversation**, **Average length** ("From the first message to the last"), **Per conversation** ("How much it takes to answer one") and **Conversations day by day**.

## Business rules

### Credit accumulates; it is not a monthly quota

The allowance is a running total. It is **not reset each month** and credit **does not expire**. Each paid credit pack adds its value; buying the same pack three times adds it three times, and a pack that renews adds it again with each paid renewal. Only a **paid** invoice counts: a declined card or failed renewal adds nothing.

### The starter allowance

A new install gets a small starter allowance so the chat works from its first minute. At the first credit purchase, the allowance is recalculated as **the total of all paid packs**; the starter amount is not added on top. The starter allowance goes only to a store installing Aura Chat for the first time; uninstalling and reinstalling leaves the allowance as it was ([[apps-aura-chat-setup]]).

### What uses the allowance

Each reply uses an amount that depends on the AI processing behind it: a longer conversation, or one that needs more looking up, uses more. Nothing is used by a proactive bubble until the shopper replies ([[apps-aura-chat-proactive]]), or by a visitor who never opens the chat. Each conversation's use appears as **Cost** in the inbox's details ([[apps-aura-chat-conversations]]).

### "Conversations left" is an estimate, and ignores the date picker

Conversations left = what remains ÷ the average conversation over the **last 30 days**. With no conversations in that window, it uses the store's whole history and says so: *Estimated from this store's history, as this month has no conversations yet.* It does not change when the merchant changes the Overview's period, because the remaining balance does not change either. A longer average conversation lowers the estimate within days.

### When it runs out

- The admin shows *The allowance is used up. The assistant stops answering until it is raised.* (or *No allowance is loaded, so the assistant cannot answer.*).
- Shoppers see only *Чатът временно не е достъпен. Моля, опитайте по-късно или се свържете с магазина по друг начин.* There is no mention of billing or credit ([[apps-aura-chat-widget]]).
- Buying credit raises the allowance as soon as the payment is confirmed, and the assistant answers again.

### Credit is a separate purchase from the Aura Search plan

Aura Chat credit (`aura-chat-credit`) is bought on its own and covers only the chat. It is separate from any Aura Search plan ([[apps-advanced-search-plans]]).

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-overview]] — the summary under Conversations.
- [[apps-aura-chat-setup]] — the starter allowance and reinstalling.
- [[apps-aura-chat-conversations]] — per-conversation Cost.
- [[plan-gates]] — how feature packs are bought and billed.

## Open questions

- Whether a conversation already under way is cut off mid-conversation when the allowance runs out, or only new messages are refused (verify).
