---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → UpSell offer editor"
route_name: up-sell.diagram
route_path: /admin/marketing-new/up-sell/diagram/:id
aliases: ["UpSell Diagram", "UpSell offer editor", "Edit UpSell offer", "UpSell offer detail", "Диаграма на UpSell офертата", "UpSell редактор на оферта"]
tags: [marketing, upsell, cross-sell, offer, editor]
plan_gates: ["upsells"]
created: 2026-05-23
updated: 2026-07-13
source_count: 5
---

# UpSell offer editor (diagram)

## Purpose

The UpSell **diagram** page is where the merchant views and edits a **single UpSell offer**. An UpSell offer pairs a **trigger product** (what the customer already has in the cart) with an **offer product** (the premium replacement to suggest) — e.g. *"customer added the 128 GB phone → offer the 256 GB version."* The page shows the offer as a **summary card** (trigger → offer); all configuration happens in an **edit modal**.

> This replaced the older multi-step "decision-tree" builder. The current UpSell is a **single trigger → offer pairing per record** — there is **no** branching accept/decline tree, no node chaining, and no visual flow canvas. Each offer stands on its own.

## Where to find it

- Sidebar → Marketing → **UpSell** → click an offer row in the list ([[marketing-up-sell-list]]) to open its diagram page; or **+ Add UpSell** to create a new one.
- Route: `/admin/marketing-new/up-sell/diagram/:id`.
- The Cross-Sell equivalent is the analogous editor at `/admin/marketing-new/cross-sell/diagram/:id` — same page shape, but a Cross-Sell offer is defined by **target-condition groups + action groups** rather than a single trigger/offer product pair (see [[marketing-cross-sell]]).

## What the merchant can do here

- See the offer **summary card**: the **trigger** ("On {event}" + the trigger product and its variant) and the **offer** ("Offer by {display type}" + the offer product and its variant), with an Active / Inactive badge.
- **Edit** the offer (opens the modal — fields below).
- **Preview** it on the storefront (opens the preview URL in a new browser tab; does not change live state).
- **Delete** the offer (with a confirmation prompt).

## Settings & fields — the Edit modal

Editing opens a modal titled *"Edit Up Sell"* / *"Create new Up Sell"* with **two tabs**.

### General settings tab

- **Sandbox** — test-mode toggle; the offer runs only for the merchant / testers, not for real customers.
- **Texts** — **System title** (internal name), **Offer title** and **Description** shown to the customer. The description accepts variables: `{$only}` (price difference only), `{$trigger_product_name}`, `{$trigger_product_price}`, `{$offer_product_name}`, `{$offer_product_price}`. Plus **Button text** and **Cancel button text** (default *"No, thanks"*).
- **Design** — Background color, Text color, Button background color, Button text color, and a **Display effect** (None / **Confetti** / **Fireworks** / **School pride**) with a Test button. A live **Preview** of the popup updates as the fields change.

### Products tab

- **Selected product from customer** — the **trigger product** the customer must have in the cart (optionally narrowed to a specific variant).
- **Offer as replacement** — the **offer product** to propose (optionally a specific variant).
- **Trigger event** — when the offer fires.
- **Product settings** — *"Only display the additional cost of the replacement product"*, *"Match quantity of products"*, and *"Show the offer only if the selected product from customer is out of stock"*.

## Business rules

- **One trigger → one offer per record.** Building a follow-up chain (propose a further product after this one is accepted) is **not** supported in the current editor.
- **App-gated.** The UpSell pages require the **Up/Cross-Sell app** to be installed — see [[apps-up-cross-sell]].
- **Plan cap.** The number of UpSell offers is capped by the plan's `upsells` feature; the **Add UpSell** button shows the remaining budget and creates are blocked at the cap — see [[marketing-up-sell-list]] for the counter and [[plan-features]].

## Related

- [[marketing-up-sell-list]] — the offer list these rows come from (table, bulk actions, plan budget, storefront firing).
- [[marketing-cross-sell]] — the Cross-Sell engine + its analogous diagram editor (condition-group based).
- [[marketing-cross-sell-list]] — the Cross-Sell offer list.
- [[apps-up-cross-sell]] — gateway app that gates these routes.
- [[products-products]] — products picked as the trigger / offer.
- [[apps-cart-rules]] — sister conditional engine (discounts vs recommendations).

## Open questions

- The legacy `parent` field persists on the offer record but is not editable in the current UI; whether any pre-existing multi-step chains still render on the storefront is out of scope here. (verify)
