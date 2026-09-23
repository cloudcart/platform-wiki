---
type: feature
nav_path: "Apps → Aura Chat → Proactive Sales"
route_name: apps.aura_chat.proactive
route_path: /admin/apps/aura_chat/proactive
aliases: ["Proactive Sales", "chat speaks first", "proactive message", "When the chat speaks first", "Never speak here", "chat greeting popup", "chat bubble message", "proactive chat rules", "Kind of page", "Address contains", "проактивни продажби", "чатът пише пръв", "проактивно съобщение", "никога не говори тук"]
tags: [apps, ai, chat, proactive, marketing, settings]
plan_gates: ["aura-chat-credit"]
created: 2026-09-23
updated: 2026-09-23
source_count: 4
---

# Aura Chat — Proactive Sales: when the chat speaks first

> Part of [[apps-aura-chat]]. See the hub for the other aspects (widget, appearance, conversations).

## Purpose

**Proactive Sales** lets the chat open the conversation. After conditions the merchant sets (time on the site or page, pages seen, the kind of page, the address), a bubble with the merchant's own line appears above the launcher. Clicking it opens the chat with that line already said. The line is the merchant's text, so showing it costs nothing; a conversation starts only if the shopper answers.

## Where to find it

**Apps → Aura Chat → Proactive Sales** (`/admin/apps/aura_chat/proactive`). Two cards: **When the chat speaks first** (the rules) and **Never speak here** (the pages to leave alone).

## What the merchant can do here

- Write up to **5 rules**, each with conditions and a message.
- Put them in priority order by dragging (**Drag to reorder**).
- Switch a rule off without deleting it.
- List up to **20** places where the chat never speaks first.
- Install Datalayer in place when a rule needs it.

## Settings & fields

### A rule

| Part | Values |
|---|---|
| Name | For the merchant only (placeholder *e.g. Undecided on a product page*); never shown to shoppers. |
| **Show it when all of these are true** | 1–5 conditions, all must hold. For "either/or", write a second rule. |
| **What the shop says** | 1–300 characters (placeholder *e.g. Can I help you choose between these?*). |

### Conditions

| Condition | Meaning | Range |
|---|---|---|
| **Seconds on the site** | since the visit began | 1–3600 s |
| **Seconds on this page** | on the current page | 1–3600 s |
| **Pages seen** | pages opened in this visit | 1–100 |
| **Products seen** | how many times **this** product page has been opened in the visit. "2" means the shopper came back to it; false on any product seen once and on non-product pages. | 1–100 |
| **Kind of page** | Product, Category, Smart collection, Product list, Tag, Brand, Search, Home, Page, Blog, Article, Contacts, Discount, Cart, Checkout, Tax, Other | needs Datalayer |
| **Address contains** | "Matched anywhere in the address. A star makes the whole address have to fit: /gumi/* is everything under it." | text |

Time, pages seen and products seen **build up over the visit** and stay true once reached. Time on page, kind of page and address describe **where the shopper is now**. A **visit** ends after 30 minutes without a page view.

### Variables in the message

`{store}` (the Store name from Settings), `{h1}` (the page heading), `{title}` (the page title), `{product}` and `{category}` (need Datalayer). "A rule whose variable has no value on the page stays silent, because half a sentence is worse than nothing."

### Never speak here

"Pages where the chat never speaks first. Rules are not even looked at here, so this wins over all of them." Each entry is one of:

- an **address piece without a star**, matched anywhere: `/checkout` also stops `/checkout/payment` and `/en/checkout`;
- an **address with a star**, where the whole address must fit from its start: `/account/*` is everything under account but not `/account` itself; `/account*` is account and everything under it, but not `/my-account`; `/*-aeg` is any address ending in `-aeg`, such as `/pralnya-aeg`;
- a **kind of page**: any entry that does not start with `/` is read as a page kind (`checkout`, `cart`…), which needs Datalayer like the rule condition.

A new store starts with `/checkout`, `/cart*`, `/account*` ([[apps-aura-chat-setup]]).

## Business rules

### First match wins

"Rules are tried from the top. The first one that matches speaks and the rest are skipped, so drag the most specific to the top." A broad rule above a narrow one silences the narrow one.

### At most one opener per visit

Once a rule has fired, no other fires in that visit. Closing the bubble with × also ends it for the visit. Leaving the page parks the bubble, and it comes back if the shopper returns. A second product page does not produce a second greeting. While a bubble waits, the launcher shows a red count like an unread message, and the launcher icon ([[apps-aura-chat-appearance]]) is the bubble's avatar.

### The assistant knows why it spoke

When the shopper opens the chat from the bubble, the assistant is told which rule fired and its conditions ("browsed three products for ninety seconds"), and continues from there.

### The never-speak list is the only guard

The assistant has no built-in exception for checkout or payment pages. Emptying **Never speak here** lets a rule interrupt a payment.

### Datalayer for page kinds and product/category names

**Kind of page** and the `{product}` / `{category}` variables read page data the Datalayer app publishes. Without it the tab warns *These rules cannot fire yet*: those conditions never match, silently, on exactly the pages they target. **Install Datalayer** fixes it in place ([[apps-datalayer]]).

### The starter rule speaks the store's language

A new store gets one rule, "Proactive message", which fires after 10 seconds on any page. Its sentence is in the store's default language:

- Bulgarian: *Мога ли да ви помогна с нещо в {store}?*
- English: *Can I help you with something at {store}?*
- any other language: the Bulgarian sentence.

Stores that installed Aura Chat before this change keep the English sentence until the merchant rewrites it. A reinstall does not replace it ([[apps-aura-chat-setup]]).

### Rules are checked in the shopper's browser

The page checks the conditions every few seconds. There is no delay from the server, and nothing is spent until the shopper replies ([[apps-aura-chat-usage]]).

## Related

- [[apps-aura-chat]] — hub.
- [[apps-aura-chat-widget]] — the launcher and bubble on the storefront.
- [[apps-aura-chat-appearance]] — Store name (`{store}`) and launcher icon.
- [[apps-datalayer]] — required for page kinds and product/category variables.
- [[apps-aura-chat-setup]] — the starting rule and list.

## Open questions

- None known.
