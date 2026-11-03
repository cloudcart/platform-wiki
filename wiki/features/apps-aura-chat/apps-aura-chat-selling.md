---
type: feature
nav_path: "Apps → Aura Chat → Knowledge & Skills → Finding / Advising on products"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["how Aura Chat recommends products", "chat asks questions", "chat recommends", "product recommendation", "chat closes the sale", "best seller", "chat did not find product", "we don't sell that", "chat photo search", "pinned products", "как чатът препоръчва", "чатът задава въпроси", "препоръка на продукт", "търсене по снимка"]
tags: [apps, ai, chat, products, sales, behaviour]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 3
---

# Aura Chat — how it finds, recommends and closes

> Part of [[apps-aura-chat]]. See the hub for the other aspects (skills, behaviour, catalog rules, discount codes).

## Purpose

This page sums up the playbooks of the two product skills, **Finding products** and **Advising on products**: how the assistant turns a vague request into a recommendation, and a recommendation into a sale. The full text is in `aura-chat-skill-product-discovery.txt` and `aura-chat-skill-product-advice.txt` ([[apps-aura-chat-prompts]]).

## Where to find it

Switched on at **Apps → Aura Chat → Knowledge & Skills** ([[apps-aura-chat-skills]]). The results show in the transcripts ([[apps-aura-chat-conversations]]) and as **Encouraged orders** on the Overview ([[apps-aura-chat-overview]]).

## What the merchant can do here

- Switch either skill on or off.
- Narrow what can be shown ([[apps-aura-chat-catalog-rules]]).
- Add priorities in their own instructions, such as what to ask first or what to recommend.
- Let **Product research** fill catalog gaps ([[apps-aura-chat-agents]]).

## Settings & fields

None beyond the skill switches, the catalog rules and the instructions.

## Business rules

### Finding products: four steps, in order

1. **Learn the shop.** It reads the store's departments, brands, price spread and product properties, narrowing to the department in question, before any search.
2. **Ask, all at once.** It sends every useful question in one turn as cards. A question earns a card only if it divides the products actually in stock there and the shopper can answer it from memory. Price bands are drawn from the real spread of that department.
3. **Search** using the answers. Structured answers become filters, and the rest go into the search wording.
4. **Recommend and close.** It names its pick and says why, says who the runner-up suits better, and ends by asking which one appeals, as a card with the products as options.

On a **broad** request nothing is shown before the questions are answered. A request that is already specific (a named product, model or size) goes straight to search.

### What it shows

- Usually **4–5 cards**, up to 9 when the answers narrowed less.
- **Buyable products first.** It searches in-stock items when the aim is to buy, and says in a clause if the best fit is sold out.
- The **same product in several colours or sizes is shown once**, with the other options named.
- **Badges** (free delivery, installation, "from the TV advert") are stated as plain facts.
- A **real reduction** is said early. It knows a reduction only when the shop shows a "was" price.
- A **rating** is given with its count, e.g. *5/5 от 3 отзива*.
- Order of results: by default what the shop's customers buy most. It **never says** it recommends on sales, unless asked what is popular.

### When the search comes back empty or wrong

- **Nothing found**: it widens by dropping the least important condition, and says what it relaxed. It says "I could not find one", **never "we don't sell that"**, since the catalog rules may hide things it cannot see ([[apps-aura-chat-catalog-rules]]).
- **Wrong results or rejected**: it asks what is wrong, as a card, before searching again, then tries another angle and offers neighbours (another brand, size or model).
- **Three rounds at most.** After that it gives the link to the closest department listing so the shopper can browse. It does not hand them off to the shop's contacts.

### A photo is a request

It says in a clause what it sees, then searches for it. A photo of something already bought and broken is after-sale, not a product search.

### Advising on products: a verdict every time

When the shopper is holding something (a named product, a pinned card, "the second one"), the assistant answers the question in a sentence and then gives a verdict built from three parts:

1. **Why this one** over the others, in terms of what the shopper said it is for.
2. **The risk removed**: the return window (looked up from the shop's pages, never from memory), the rating with its count, and that it is in stock.
3. **The ask**: it says it would take it and names the real next step, **Избери действие → Добави в количката** on a card on screen.

It states consequences, not bare specs ("fits in the overhead locker as hand luggage").

### Pinned products and the page they are on

Products pinned with **Допълнителен въпрос** (up to three) are the subject until unpinned; with two or more, the question is taken as a comparison. On a product or category page, a question with no subject ("is there a cheaper one?") is answered within what they are looking at.

### Stock in physical shops

A question naming a town or shop is answered by checking per-shop stock and showing the shop on a map. It does not first ask which product, and it reports a level, not a count ([[apps-aura-chat-catalog-rules]]).

### Hesitation and leaving

- **Hesitation**: it names the concern, answers it concretely (what the price buys, a cheaper option that does the job, the return policy) and brings the rating. **Twice at most**, then it offers the department listing and lets go.
- **Leaving** ("thanks, I'll think about it") after liking a product: it addresses the last unanswered obstacle. Where the shop authorised a code for this moment it opens the discount policy ([[apps-aura-chat-discount-codes]]). **One attempt**, then it closes warmly.
- Never allowed: urgency or scarcity nobody stated, a discount nobody authorised, a promise the shop has not published.

### After an add to basket

It does not repeat what was bought. It may mention one relevant companion product, never a list.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-behaviour]] — the rules that apply to every reply.
- [[apps-aura-chat-catalog-rules]] — what can be shown.
- [[apps-aura-chat-agents]] — Store pages (return window) and Product research (catalog gaps).
- [[apps-aura-chat-discount-codes]] — codes at the moment of leaving.
- [[apps-aura-chat-overview]] — how orders from shown products are counted.

## Open questions

- None known.
