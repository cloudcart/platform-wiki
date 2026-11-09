---
type: entity
nav_path: "Entity → Cart Rule → Actions"
aliases: ["Cart Rule actions", "Cart Rule action types", "Cart Rule messages", "Action value type"]
tags: [entity, marketing, automation, discounts, rules-engine, actions]
created: 2026-06-10
updated: 2026-11-09
source_count: 6
---

# Cart Rule — Actions

> Part of [[cart-rule]]. See the hub for related aspects (fields, rows-and-triggers, stacking, lifecycle, evaluation).

## Identity

When a row's triggers all match, its **action** fires. This page documents the fixed action shape, the three supported action value types, and the customer-facing message slot that ships alongside the action.

## Aliases

- "Cart Rule actions" — the canonical term.
- "Action value type" — the `percent` / `amount` / `free_shipping` choice.
- "Cart Rule messages" — the per-row customer-facing string slot.

## Key Attributes

Each row's action carries:

- **Action value type** — `percent` / `amount` / `free_shipping`.
- **`group`** — `cart` (whole-cart) vs `product` (per-line). Drives stacking — see [[cart-rule-stacking]].
- **Value** — numeric percent / amount; ignored for `free_shipping`.
- **Action-scoping filters** — `product_from_condition`, `product_not_from_condition`, `product_lowest_price`, `product_highest_price`. Narrow which lines receive the discount.
- **Message** — optional customer-facing nudge toward a row not yet reached.

## Action is fixed to "discount"

The current implementation supports only discount actions. The merchant CANNOT use Cart Rules to:

- Automatically add a free product to the cart.
- Upgrade the shipping tier (e.g., *"if cart > 500, auto-upgrade to express"*).
- Send a notification (campaign, SMS, push).
- Show a popup or modal.

Each row's action is a discount of one of the standard shapes — flat amount, percent, or free shipping.

## Action value types

Three action value types are supported in the discount calculation:

- **`percent`** — percentage off. Applies either to a specific product line (the line's price × percent / 100) or to the cart total (the cart-level apply), determined by the row's `group` field.
- **`amount`** — fixed amount off (the modification value). Same line-vs-cart choice via `group`. One defensive cap: a fixed-amount modification is silently dropped if it would push the per-unit price below zero (percent modifications are always allowed).
- **`free_shipping`** — zeros out the shipping line on the cart-level apply.

The `group` field on the action determines whether the discount targets a specific cart line (product-level) or the whole cart (cart-level). This split matters for stacking — see [[cart-rule-stacking]].

## Action-scoping filters

Inside an action's own narrowing filters (NOT the row's triggers), the merchant can use `product_from_condition`, `product_not_from_condition`, `product_lowest_price`, `product_highest_price` to choose which cart lines actually receive the discount. *"Buy 5, get the cheapest one free"* uses `product_lowest_price` on the action side. See [[cart-rules-actions]] for the editor UX.

## Custom message at checkout

Each row has an optional **message**. It shows while the shopper has **not** reached the row, never once the row applies, so it suits nudges (*"Add 6 EUR more for free shipping"*), not confirmations (*"10% applied"*). Exactly when it shows is on [[cart-rules-stacking]] § *Message-row precedence*.

The customer sees the message; the merchant sees the firing stats (see [[cart-rule-evaluation]] for matches-vs-notifications semantics).

## Notifications carried by the cart

The storefront shows each message as a dashed box in the cart drawer, the cart page and the checkout summary, joined by `Or` / `Или` when there are several. There is no other channel — no email or push.

## Where it appears

- [[cart-rules-actions]] — per-row action editor and the full action UX.
- [[apps-cart-rules]] — list + editor.
- [[checkout-flow]] — where messages surface to the customer.

## Related

- [[cart-rule]] — hub.
- [[cart-rule-fields]] — top-level rule attributes.
- [[cart-rule-rows-and-triggers]] — what gates whether an action fires.
- [[cart-rule-stacking]] — how cart-level vs product-level actions stack.
- [[cart-rule-evaluation]] — matches + notifications outputs.
- [[discount]] — the simpler single-condition counterpart.

## Open Questions

None.
