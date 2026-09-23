---
type: feature
nav_path: "Apps → Aura Chat"
route_name: apps.aura_chat.overview
route_path: /admin/apps/aura_chat
aliases: ["Aura Chat", "AI chat", "AI assistant", "AI sales assistant", "storefront assistant", "shopping assistant", "chat assistant", "chatbot", "AI chatbot", "enable disable button", "app active toggle", "Аура чат", "AI чат", "AI асистент", "чат асистент", "виртуален асистент", "чатбот", "асистент в магазина"]
tags: [apps, others, ai, chat, storefront, sales, support]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 12
---

# Aura Chat

> **The assistant answers only while it has an allowance.** A new install starts with a small starter allowance so the chat can be tried. When it is used up, the chat tells shoppers it is temporarily unavailable until credit is added (**Buy more credits**). See [[apps-aura-chat-usage]].

## Purpose

**Aura Chat** puts an AI assistant in a chat window on the storefront. It speaks **as the shop** ("we", "our") and answers from the store's own data: the catalog, the shop's published pages, its orders and its physical shops. It does not answer from general knowledge. Depending on what the merchant switches on, it can:

- **Find and recommend products.** It asks a few questions as tappable cards and shows product cards the shopper can add to the basket without leaving the chat.
- **Advise on one product** — specifications, fit, comparisons, doubts before buying — and close the sale.
- **Answer from the shop's published pages** — delivery, returns, warranty, terms, FAQ — with a link to the page. This works even with every skill off.
- **Look up an order** from its number and the checkout email.
- **Lodge a return request** (needs the Aftercare app).
- **Issue a personal, single-use discount code**, only on the occasions and within the limits the merchant sets.
- **Speak first** on chosen pages, with the merchant's own wording (Proactive Sales).

The merchant can read every conversation, see which orders followed a chat, and see what shoppers ask about.

Aura Chat belongs to the **Aura** family of CloudCart apps, with [[apps-advanced-search]] (Aura Search). It is not the same as [[apps-live-chat]], which embeds the third-party LiveChat service for human agents.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so it can be switched off without uninstalling it. A disabled app stops working while keeping its settings ([[apps-aura-chat-setup]]).

## Where to find it

Sidebar → **Apps → Aura Chat** (`/admin/apps/aura_chat`). The header carries **Buy more credits**. Six tabs:

| Tab | Address | What it answers | Aspect |
|---|---|---|---|
| **Overview** | `/admin/apps/aura_chat` | How is the assistant doing, and what does it bring in? | [[apps-aura-chat-overview]] |
| **Settings** | `/admin/apps/aura_chat/settings` | How does the chat look, and what does it offer before a question? | [[apps-aura-chat-appearance]] |
| **Knowledge & Skills** | `/admin/apps/aura_chat/knowledge` | What may it do, what may it show, and how should it speak? | [[apps-aura-chat-skills]] |
| **Proactive Sales** | `/admin/apps/aura_chat/proactive` | When does the chat speak first? | [[apps-aura-chat-proactive]] |
| **Usage** | `/admin/apps/aura_chat/usage` | How much allowance is left? | [[apps-aura-chat-usage]] |
| **Conversations** | `/admin/apps/aura_chat/inbox` | What exactly was said? (opens full-screen) | [[apps-aura-chat-conversations]] |

## Sub-pages (in this cluster)

- [[apps-aura-chat-setup]] — installing, what a new store starts with, the two helper apps, switching off, uninstalling and reinstalling.
- [[apps-aura-chat-widget]] — what the shopper sees and can do in the chat.
- [[apps-aura-chat-appearance]] — the Settings tab: look, opening questions, the rating row, the disclaimer.
- [[apps-aura-chat-skills]] — the five skills, what each one does, and the merchant's own instructions.
- [[apps-aura-chat-catalog-rules]] — keeping products out of the assistant's reach (stock, price, categories, brands, tags) and exact stock counts.
- [[apps-aura-chat-discount-codes]] — personal discount codes: the policy, the ceilings, one code per shopper.
- [[apps-aura-chat-agents]] — the two agents behind the skills: the published-pages lookup and product research.
- [[apps-aura-chat-behaviour]] — how the assistant talks and what it will never do, drawn from its instructions.
- [[apps-aura-chat-selling]] — how it finds products, recommends, handles hesitation and closes.
- [[apps-aura-chat-orders-returns]] — order lookups and return requests, step by step.
- [[apps-aura-chat-prompts]] — the assistant's instructions word for word, and how they are put together.
- [[apps-aura-chat-proactive]] — Proactive Sales: rules for speaking first, conditions, variables, pages where it never speaks.
- [[apps-aura-chat-conversations]] — the inbox: filters, transcripts, orders after a chat, keeping a conversation.
- [[apps-aura-chat-overview]] — the Overview dashboard and how an order is credited to a conversation.
- [[apps-aura-chat-topics-feedback]] — conversation topics and the shopper's thumbs up / down.
- [[apps-aura-chat-usage]] — credits, the allowance, and what happens when it runs out.

## What the merchant can do here

- **Style the chat** to the brand: name, colour, position, launcher shape, product-card layout ([[apps-aura-chat-appearance]]).
- **Choose what the assistant may do** by switching skills on and off ([[apps-aura-chat-skills]]).
- **Hide products** from its recommendations ([[apps-aura-chat-catalog-rules]]).
- **Authorise discount codes** and set when and how much ([[apps-aura-chat-discount-codes]]).
- **Write the shop's own instructions**: tone, what to recommend, what to avoid ([[apps-aura-chat-skills]]).
- **Make the chat speak first** on chosen pages ([[apps-aura-chat-proactive]]).
- **Read conversations** and keep the useful ones ([[apps-aura-chat-conversations]]).
- **Track results**: conversations, orders after a chat, topics, complaints ([[apps-aura-chat-overview]]).
- **Top up credit** ([[apps-aura-chat-usage]]).

### What the merchant CANNOT do here

- **Edit the assistant's core rules.** The merchant's instructions sit on top of them and cannot switch them off ([[apps-aura-chat-behaviour]]).
- **Chat with shoppers themselves.** There is no human takeover; the inbox is read-only apart from keeping a conversation.
- **Make the assistant answer from general knowledge** or from other sites. Only the product research agent reads outside the shop, and only for product facts ([[apps-aura-chat-agents]]).
- **Pick the language model** — that is set by the platform.

## Settings & fields

The settings are spread over the tabs: look and feel on [[apps-aura-chat-appearance]]; skills and instructions on [[apps-aura-chat-skills]]; catalog rules on [[apps-aura-chat-catalog-rules]]; the discount policy on [[apps-aura-chat-discount-codes]]; agent switches on [[apps-aura-chat-agents]]; topics on [[apps-aura-chat-topics-feedback]]; proactive rules on [[apps-aura-chat-proactive]].

## Business rules

### A new store starts with no skills on

On install the chat is live, but every skill is off. It can greet, answer from the shop's published pages and show shops. It cannot search the catalog, look up orders or give codes until the merchant switches those skills on. See [[apps-aura-chat-setup]].

### Everything it states must come from the shop

Products, prices, stock, policies and orders come only from the store's own data. The assistant never makes a fact up ([[apps-aura-chat-behaviour]]).

### Checkout, cart and account are left alone

A new store's proactive settings keep the chat from speaking first on `/checkout`, `/cart*` and `/account*`. This list is the only protection, so clearing it lets a rule interrupt a payment ([[apps-aura-chat-proactive]]).

### Two features lean on other apps

Returns need **Aftercare** ([[apps-aftercare]]). Proactive conditions on the kind of page, and the `{product}` / `{category}` variables, need **Datalayer** ([[apps-datalayer]]). The admin warns and offers an in-place **Install** button for each.

### Conversations are kept for six months

Transcripts are deleted six months after each message. Marking a conversation **Keep this conversation for later** is a bookmark, not an exemption ([[apps-aura-chat-conversations]]).

## Related

- [[apps]] — the App Store.
- [[apps-advanced-search]] — Aura Search, the other Aura app.
- [[apps-aftercare]] — returns and withdrawals, used by the Returns skill.
- [[apps-datalayer]] — page data used by Proactive Sales.
- [[apps-stores]] — the physical shops the assistant shows on a map.
- [[marketing-discounts-code-pro]] — where the assistant's discount codes live.
- [[page]], [[page-faq]] — the published pages the assistant reads.
- [[plan-gates]] — how paid features and credit packs work.

## Open questions

- None at the hub level; each aspect lists its own.
