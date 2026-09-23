---
type: feature
nav_path: "Apps → Aura Chat → Knowledge & Skills → Agents"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["Aura Chat agents", "Store pages agent", "Product research agent", "policy lookup", "chat reads my pages", "chat answers delivery questions", "chat searches the internet", "manufacturer specifications", "агенти на чата", "проучване на продукт", "страници на магазина", "чатът чете условията"]
tags: [apps, ai, chat, agents, settings]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — the agents behind the skills

> Part of [[apps-aura-chat]]. See the hub for the other aspects (skills, behaviour, prompts).

## Purpose

An **agent** is a separate assistant with its own instructions and tools, which the chat assistant hands one question to and gets a short report back from. The admin puts it this way: "A skill is a playbook the assistant follows. An agent is a separate one with its own tools." There are two. **Store pages** reads the shop's own published pages. **Product research** looks up product facts outside the shop. Neither talks to the shopper; the chat assistant decides what to say with what they return.

## Where to find it

**Apps → Aura Chat → Knowledge & Skills → Agents** (box title *Agents behind the skills*), below the skill sections (`/admin/apps/aura_chat/knowledge`).

## What the merchant can do here

- Nothing to set for **Store pages**. It is marked **Always on**.
- Switch **Product research** on or off. The switch works only while **Advising on products** is on; the row says *Requires the "Advising on products" skill.*

## Settings & fields

| Agent | Switch | What it reads | What it never does |
|---|---|---|---|
| **Store pages** | **Always on** | The shop's published pages: delivery, returns, warranty, terms, privacy, payment, the FAQ, and pages the shop builds for things like a service network or a brochure. | Answer from what shops usually do; quote a page it did not open. |
| **Product research** | off by default; needs **Advising on products** | The manufacturer's own site, product pages, manuals and datasheets for facts; reviews and owner comments for how living with the product is. | Name, link or quote another shop; fetch a price, stock, delivery, returns or warranty terms; say whether the shop sells something. |

Each agent's instructions are in `wiki/resources/aura-chat-prompts/` (`aura-chat-agent-policy-lookup.txt`, `aura-chat-agent-product-research.txt`); see [[apps-aura-chat-prompts]].

## Business rules

### Store pages: the only way the assistant reads the shop's pages

The chat assistant cannot open the shop's pages itself. Whenever an answer would otherwise rest on "what shops usually do", it asks **Store pages** with the shopper's full question: delivery times and prices, the return window, warranty, payment methods, instalments, privacy. What comes back is quoted exactly (fourteen days stays fourteen days; "unused, in its original packaging" stays word for word), with a link to each page used. The assistant offers one of those links to the shopper.

- **What it reads**: the store's active pages of the ordinary and FAQ kinds ([[page]], [[page-faq]]). A policy that exists only in an image, a PDF or a banner is not read.
- **How it looks**: it searches page **titles** for the topic, tries other word forms and the word a shop would use (a repair filed under "сервиз"), and if needed reads the full list of titles before opening the pages that could hold the answer. It says "not published" only after every title has been seen.
- **Dated pages**: it is given today's date and treats a campaign or condition whose period has ended as not in force. It mentions it as history, never as the terms.
- **When nothing is published**: the assistant says so and offers the shop's own contacts. It does not fill the gap.

### Pages are found by their titles

The agent picks pages by title before it reads them. A policy on its own plainly titled page ("Доставка", "Връщане на стока", "Гаранция") is found in one step. A clause inside a long general-terms page is found only once the agent decides to open that page. Every answer on delivery, returns and warranty comes from these pages and nowhere else.

### Product research: only for gaps in the catalog

The assistant calls **Product research** only when three things hold: it searched the catalog with full details, the answer was not there, and the shopper's decision turns on it. It is for two kinds of question:

- **what the product is**: a dimension, capacity, material, what is in the box, compatibility (from the manufacturer only);
- **what owning it is like**: noise, what wears out, ease of cleaning (from owners, reported as what people say, with how many agree).

The report marks each finding as **fact** or **experience**, with its source, what could not be found, and how sure it is. A finding from the internet that disagrees with the shop's catalog is treated as wrong: the shop's record binds. Without this agent, a catalog gap is answered from what the catalog does hold, and the shopper is offered the shop's contacts for an exact figure.

### An agent runs only when both switches allow it

**Product research** needs its own switch **and** the **Advising on products** skill. Switching on the skill alone does not switch on the agent. Store pages needs no skill: it works even with every skill off ([[apps-aura-chat-skills]]).

### What the agents read is treated as data

Text inside a page, PDF or review that reads like an instruction is never followed. Only the question the assistant asked is answered.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-skills]] — the skills the agents work behind.
- [[apps-aura-chat-behaviour]] — how the assistant passes their answers on.
- [[apps-aura-chat-prompts]] — both agents' instructions, word for word.
- [[page]], [[page-faq]] — the published pages Store pages reads.

## Open questions

- Whether pages set as hidden from the storefront menu, but still active, are read (they are listed if active — verify).
