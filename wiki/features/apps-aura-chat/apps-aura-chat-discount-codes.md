---
type: feature
nav_path: "Apps → Aura Chat → Knowledge & Skills → Promo codes"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["Aura Chat discount codes", "chat discount code", "personal discount code", "Offer discount codes", "When a discount may be offered", "When to consider a discount", "Before the same customer may get another", "AURA code", "Aura chat — персонални кодове", "чатът дава отстъпки", "персонален код за отстъпка", "код от чата"]
tags: [apps, ai, chat, discounts, settings]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — personal discount codes

> Part of [[apps-aura-chat]]. See the hub for the other aspects (skills, catalog rules, behaviour).

## Purpose

With the **Promo codes** skill on and a policy written, the assistant may issue **one single-use discount code to one shopper**. It is meant to tip a shopper who already wants a particular product, on occasions the merchant describes. The figures the merchant sets are **ceilings**. The occasions are the merchant's own words, and the assistant reads them as the only authority it has.

## Where to find it

**Apps → Aura Chat → Knowledge & Skills**, in the **Promo codes** section (`/admin/apps/aura_chat/knowledge`). The skill switch is at the top of the section, and the policy fields are below it, greyed until both the skill and **Offer discount codes** are on.

A status line says where things stand: *Codes are being offered when the occasions below are met.* or *Nothing is offered yet — describe the occasions below.*

## What the merchant can do here

- Allow or stop codes; set the kind, the ceiling and what a code hangs on.
- Cap a code's life and how often one shopper can get one.
- Describe in words when a code may be offered.

## Settings & fields

| Field | Values | Help text / behaviour |
|---|---|---|
| **Offer discount codes** | switch | "The assistant may issue a single-use code, on the occasions you describe below and nowhere else." |
| **Discount type** | **Percentage** · **Fixed amount** · **Free shipping** | Same names as the store's discounts screen. |
| **Discount value** (Percentage) | 1 up to the platform ceiling (50% at the time of writing) | "The most the assistant may take off. It is told to offer less where less will do, and never more than this." Higher values are reduced to the ceiling on save. |
| **Discount value** (Fixed amount) | a sum in the store's currency | No more than 50% of the **Order is over** threshold; the help line shows the current maximum. Against products it may not exceed 50% of the cheapest product named, checked when the code is issued. |
| **What the code applies to** | **Either — the assistant chooses (recommended)** · **An order over a set amount** · **The products the assistant showed** | "Either" lets the assistant use a threshold when the aim is a bigger basket, and named products when the talk is about one item. |
| **Order is over** | sum > 0 | "Codes apply only above this amount. Zero is refused — an unconditional code is a discount on everything, for anyone who repeats it." Shown for *order* and *either*. |
| **Valid for** | days, 1–90 | "The longest a code may last. The assistant gives shorter where shorter will do, and no code outlives this." |
| **Before the same customer may get another** | days, 1–3650 | Counted from when a code was issued. A signed-in customer is recognised across conversations; a guest by their browser. There is no "off": for "once only", set the maximum. |
| **When to consider a discount** | text, up to 600 characters, with a counter | Optional. The assistant already watches for hesitation, price objections, a basket gone quiet and a shopper about to leave. Text here is **added** to those moments and only decides when the policy is read, not what is given. Placeholder: *e.g. When a trade customer asks about volume, or during the winter sale*. |
| **When a discount may be offered** | text, up to 600 characters, with a counter | Anything past 600 characters is cut when saved; the counter turns red near the limit. "Read as policy: the assistant will not go beyond it. An occasion you have not described has no policy behind it, and the answer is then no." Placeholder: *e.g. When delivery is more than two days late, or when a shopper hesitates over a large basket and has asked about the price twice.* |

## Business rules

### No occasions written = nothing offered

Codes are offered only when **all** of these hold: the skill is on, **Offer discount codes** is on, **When a discount may be offered** has text, and the figures are valid (a threshold above zero where codes may hang on an order). Otherwise the assistant is told the store has no discount policy. It then says plainly that a discount is not something it can do, without hinting at a maybe.

### Being asked is not an occasion

"Do you have a discount?" gets an answer from the policy. If the situation is not one the merchant described, the answer is no, even with codes switched on. The assistant never negotiates: the figure does not rise under pressure, and a refusal is not reopened.

### The figures are ceilings, and the assistant starts below them

The assistant picks the amount itself, from the situation. A shopper who **asked** gets the smallest figure the policy honours; one the shop is trying to **keep** may get more, up to the ceiling. Shorter validity is treated as the stronger offer. It never tells the shopper how the figure was chosen. The tool refuses anything over the ceiling. It also reads the policy afresh at the moment of issuing, so lowering a figure or switching codes off takes effect at once.

### Every code is conditional and personal

- A minimum basket **or** named products (at most 10). There is no unconditional code.
- **Single use**, by one customer.
- Starts today and runs for the chosen number of days.
- Kept on the order even if the order is later edited so the condition no longer holds.
- Its code looks like `AURA` followed by random characters.

### One code per shopper, across conversations

A second request, even in a new conversation, gets the **same code repeated**, never a new one. That holds until **Before the same customer may get another** has passed. A guest in a cleared browser or a private window counts as a new shopper.

### The basket comes first

The assistant has the product added first, then gives the code together with a link that applies it to that basket, plus the condition and end date, with no added urgency.

### Products already advertised as reduced get no code

If the shop shows a "was" price on a product, no code is issued for it, at any size. The assistant tells the shopper the price is already the reduced one.

### Where the codes live

Every code sits under one discount in the store, created on first use: **Aura chat — персонални кодове**, a Code PRO discount ([[marketing-discounts-code-pro]]). Every code the chat issued is listed there with the assistant's reason for it. Switching that discount off stops all chat codes at once.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-skills]] — the Promo codes skill.
- [[apps-aura-chat-prompts]] — `aura-chat-skill-promo-codes.txt` and `aura-chat-promo-policy.txt`, word for word.
- [[marketing-discounts-code-pro]] — the parent discount and its codes.
- [[marketing-discounts]] — the store's other discounts.

## Open questions

- None known.
