---
type: feature
nav_path: "Apps → Aura Chat → Knowledge & Skills"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["Aura Chat skills", "Knowledge & Skills", "Finding products", "Advising on products", "Orders skill", "Returns skill", "Promo codes skill", "Instructions for the assistant", "How it should speak", "custom instructions", "chat cannot find products", "chat cannot check orders", "умения на чата", "инструкции за асистента", "как да говори", "чатът не търси продукти"]
tags: [apps, ai, chat, skills, settings]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-11-09
source_count: 6
---

# Aura Chat — skills and the merchant's own instructions

> Part of [[apps-aura-chat]]. See the hub for the other aspects (catalog rules, discount codes, agents, behaviour, prompts).

## Purpose

A **skill** is a job the assistant may do, with its own playbook and its own tools. The merchant switches each one on or off. A skill that is off is not just unused: the assistant is never told it exists and has none of its tools. This page covers the five skills and the free-text **Instructions for the assistant**.

## Where to find it

**Apps → Aura Chat → Knowledge & Skills** (`/admin/apps/aura_chat/knowledge`). One section per skill, each with its switch and the settings it governs (greyed while the skill is off). Below them come **Agents** ([[apps-aura-chat-agents]]), **How it should speak** and **Conversation topics** ([[apps-aura-chat-topics-feedback]]).

## What the merchant can do here

- Switch each of the five skills on or off.
- Set the catalog rules inside **Finding products** ([[apps-aura-chat-catalog-rules]]).
- Set the discount policy inside **Promo codes** ([[apps-aura-chat-discount-codes]]).
- Install **Aftercare** from the **Returns** section when it is missing.
- Write the shop's own instructions.

## Settings & fields

### The five skills

| Skill (admin label) | Admin help text | What the assistant does with it | Word-for-word playbook |
|---|---|---|---|
| **Finding products** | "For a shopper who has not named a product — a category, a need, or an idea too broad to answer with one item." | Looks at how the shop's range is organised, asks all its questions at once as cards, searches, then names a pick and asks which one appeals. See [[apps-aura-chat-behaviour]]. | `aura-chat-skill-product-discovery.txt` |
| **Advising on products** | "Deciding between products, or questions about one: specifications, compatibility, sizes, differences, doubts before buying." | Gives a verdict with three parts: why this one, what removes the risk (the return window from the shop's pages, the rating), and the ask. It handles hesitation and a shopper about to leave. It checks stock per shop. | `aura-chat-skill-product-advice.txt` |
| **Orders** | "Anything about an order already placed — where it is, when it arrives, what it contained." | Looks up an order from **both** its identifier (number or reference code) and the checkout email. It reports status, payment, contents and the courier's tracking. | `aura-chat-skill-order-status.txt` |
| **Returns** | "Sending something back: whether it can be, how long is left, and lodging the request." | Takes a return request in four steps (details → emailed 6-digit code → choices → lodge) and looks up an existing one by its reference. **Needs Aftercare.** | `aura-chat-skill-order-returns.txt` |
| **Promo codes** | "Whether a code applies, what it gives, and why one was refused." | Issues a single-use personal code only on the occasions the merchant describes ([[apps-aura-chat-discount-codes]]). | `aura-chat-skill-promo-codes.txt` |

The playbook files are in `wiki/resources/aura-chat-prompts/`. [[apps-aura-chat-prompts]] explains how they fit together.

### How it should speak

- **Instructions for the assistant** — free text, up to **8000** characters. Placeholder: *e.g. We are a tool shop. Ask what the customer is working on before recommending anything. Never promise next-day delivery.*
- The box description: "Anything particular to your shop: tone, what to recommend, what to avoid. These sit on top of the assistant's own rules — it will still never invent a product, a price or a policy."

## Business rules

### Without skills, the chat still answers from the shop's pages

With every skill off, the assistant has no catalog or order tools. It can still greet the shopper and answer delivery, returns, warranty, payment and privacy questions from the shop's published pages ([[apps-aura-chat-agents]]). It can also show the shop's physical shops on a map. Anything needing the store's records gets one short reply saying this chat cannot look it up, and where the shopper can.

### Which tools each skill unlocks

| Skill | Can |
|---|---|
| Finding products, Advising on products (shared) | search the catalog, show product cards, check stock per physical shop |
| Orders | look up one order |
| Returns | start a return, look up a return |
| Promo codes | issue a discount code (and nothing else: switching on Orders or Returns never switches on discounts) |
| *(always, no skill needed)* | read the shop's overview, know which page the shopper is on, list and show physical shops, ask the published-pages agent |

### A skill is loaded when the request calls for it

The assistant sees the list of switched-on skills with the descriptions above and loads one when the shopper asks for something it covers. It does not load one for small talk. When one message spans two skills, an existing problem is dealt with before a new sale. A request no switched-on skill covers gets a brief "not something this chat handles" instead of an improvised answer.

### Product search uses the Aura Search product index

Both product skills search the catalog by meaning only, over the [[apps-advanced-search]] product index; a product code (SKU, barcode) is matched exactly. Aura Search's searched fields, weights and **AI semantic search** switch do not apply. Without an Aura Search plan, searches left this month, or the app on, both skills are off with the reason and a fix button: see [[apps-aura-chat-setup]]. The chat's searches do not use the Aura Search quota.

### The merchant's instructions come after the platform's rules

The instructions are added after the assistant's own rules and the store profile, framed as guidance to follow "as long as it does not conflict with anything above". They can set tone, priorities and shop-specific facts. They cannot switch off the one-store rule, the rule against inventing facts, the skills' boundaries or customer privacy. A standing promotional line (free-delivery threshold, showroom invitation, slogan) is used **at most once per conversation**, even if written as "always say…". The exact framing is in `aura-chat-03-store-guidance.txt`.

### Returns without Aftercare

With **Returns** on but Aftercare missing, the section shows "Aftercare is not installed — Returns are handled by the Aftercare app. Without it the assistant can neither start a return nor look one up, however this is set." and an **Install Aftercare** button ([[apps-aftercare]]).

### A skill switched on mid-conversation

The instructions, and the list of skills the assistant is told about, are set when a conversation starts. A change applies fully to conversations opened after it; one already under way keeps its opening brief.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-catalog-rules]], [[apps-aura-chat-discount-codes]] — the settings inside two of the skills.
- [[apps-aura-chat-agents]] — the agents that work behind the skills.
- [[apps-aura-chat-behaviour]] — what the playbooks make the assistant do.
- [[apps-aura-chat-prompts]] — the playbooks word for word.
- [[apps-aftercare]] — required by Returns.

## Open questions

- None known.
