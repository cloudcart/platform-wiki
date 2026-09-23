---
type: feature
nav_path: "Apps → Aura Chat → Knowledge & Skills → Finding products"
route_name: apps.aura_chat.knowledge
route_path: /admin/apps/aura_chat/knowledge
aliases: ["hide products from chat", "Minimum stock", "Minimum price", "Never show these categories", "Never show these brands", "Never show these tags", "Exact stock quantities", "chat recommends out of stock", "chat shows cheap products", "only 2 left", "скриване на продукти от чата", "минимална наличност", "минимална цена", "точни наличности"]
tags: [apps, ai, chat, catalog, settings]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 3
---

# Aura Chat — catalog rules: what the assistant may show

> Part of [[apps-aura-chat]]. See the hub for the other aspects (skills, discount codes, behaviour).

## Purpose

Catalog rules keep chosen products out of the assistant's reach, for example low-stock items, very cheap accessories, a brand the shop would rather not push, or a department that should not be sold through chat. One more switch decides whether the assistant knows exact stock numbers. The rules are **filters on the search itself**, not requests in the instructions. An excluded product never reaches the assistant, and nothing a shopper says can bring it back.

## Where to find it

**Apps → Aura Chat → Knowledge & Skills**, inside the **Finding products** section (`/admin/apps/aura_chat/knowledge`). The fields are greyed while the skill is off, but they govern **Advising on products** too: both skills use the same search ([[apps-aura-chat-skills]]).

## What the merchant can do here

- Hide products with too little stock.
- Hide products below a price.
- Hide whole categories, brands or tags.
- Let the assistant see, and quote when asked, exact stock quantities.

## Settings & fields

| Field | Values | Help text / behaviour |
|---|---|---|
| **Minimum stock** | number 0–10000, placeholder *No limit* | "Hide anything with fewer left than this. Zero or empty hides nothing. A product the shop keeps no count for is never hidden — untracked means always available." Applied per variant. |
| **Minimum price** | number ≥ 0, in the store's currency, placeholder *No limit* | "Hide anything cheaper than this, in your own currency." Compared with the price the catalog sorts by (whether a reduced price counts: verify). |
| **Never show these categories** | categories picked from the store's tree, up to 100 | Products in any of them never appear. |
| **Never show these brands** | brands picked from the store's list, up to 100 | Matched on the brand name as the catalog spells it. |
| **Never show these tags** | free text, **Type a tag and press enter**, up to 100 | Matched as a phrase inside the product's tags. Excluding `sale` also hides a product tagged `summer sale`. |
| **Exact stock quantities** | switch, off by default | "What the assistant is told about how many of a product you have left. Off — only whether it is in stock or not. On — the exact number from your inventory, which it may pass on to the shopper: 'only 2 left'." |

## Business rules

### Hidden means never found, for search and cards alike

The same filter applies when the assistant searches and when it draws a product card. A hidden product cannot be shown even by asking for its exact name or id.

### The assistant is told that rules exist, not what they hide

With any rule set, the assistant is told its search is narrowed ("an empty result means you did not find it — never that we do not sell it"). It gets the minimum stock and price figures, the hidden brand and tag names, and **only the number** of hidden categories. It is told never to mention the rules or explain why something is missing. So a shopper asking for a hidden item hears "I could not find one" and a nearby alternative, never "we do not sell that". The exact wording is in `aura-chat-02-store-profile.txt` ([[apps-aura-chat-prompts]]).

### Untracked stock is always available

A product whose stock the shop does not track is never hidden by **Minimum stock**. The assistant treats it as available, not as sold out.

### Exact quantities are quoted only when asked

With **Exact stock quantities** on, the assistant gives a number only when the shopper asked for one. It is never added as urgency. With it off, the assistant knows only in stock / out of stock, and its per-shop check reports a level ("limited" and the like), never a count.

### Out-of-stock products are handled by the skill, not by a rule

Without any rule, sold-out products are still in the catalog, and the assistant normally searches for what can be bought. It includes sold-out items only when the question is about the range (what the shop carries, what a model is called). Set **Minimum stock** to 1 to remove sold-out tracked products entirely. Leaving it at 0 or empty hides nothing.

### Rules apply to new searches at once

The rules are part of every search, so a change applies to the next search in any conversation. The line in the assistant's brief that describes them is set when a conversation starts.

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-skills]] — the skills the rules narrow.
- [[apps-aura-chat-behaviour]] — how the assistant words an empty result.
- [[products-categories]], [[products-vendors]] — where categories and brands are managed.
- [[inventory-tracking]] — what "tracked" stock means.

## Open questions

- Whether hiding a parent category also hides products filed only in its subcategories (verify).
