---
type: feature
nav_path: "Marketing → Discounts → Container codes → Redemption"
route_name: discounts-codes_list
route_path: /admin/marketing/discounts/codes
aliases: ["Container code redemption", "Cart-link auto-apply", "Container code reuse", "Container code stacking", "Прилагане на промо код", "Линк за автоматично прилагане"]
tags: [marketing, discounts, coupons, container, redemption, cart]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

# Container codes — distribution & redemption

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, parent-term inheritance, and the JSON-API.

## Purpose

This aspect covers what happens **after** codes are generated: how the merchant distributes them, how a customer applies one, and the cart-level rules that decide which codes can coexist. The key facts are that a code stays reusable until turned off or deleted, codes can be auto-applied via a shareable URL, and Container codes are mutually exclusive with stand-alone codes inside a cart.

## Where to find it

Redemption happens on the storefront cart / checkout, not in the admin panel. The merchant's touch-point is the Container codes list (`/admin/marketing/discounts/codes`), where each row exposes the click-to-copy cart link.

## What the merchant can do here

- **Distribute a code as a plain string** — the customer types it at checkout.
- **Distribute a code as an auto-apply URL** — copy the row's `<store-domain>/cart/discount:<CODE>` link and embed it in a newsletter / SMS so the code applies on click, with no typing.
- **Stop a code being typed** — toggling it inactive (see [[discounts-codes-list-view]]) makes typing it at checkout fail. To retire a leaked code fully, delete it.

## Settings & fields

This aspect has no admin settings of its own. The redemption behaviour is driven by the terms of the Container discount that wins at checkout (see [[discounts-codes-parent-terms]]) and the per-row `active` flag (see [[discounts-codes-list-view]]).

## Business rules

### Reusable until turned off or deleted

A Container code is not used up by an order. It keeps working, for any customer, until the merchant turns it off or deletes it. The list's Active flag shows only the merchant's own toggle, not whether the code was used. For a usage limit per code or per customer, use [[marketing-discounts-code-pro]] instead, where each code has its own `max_uses` and `maxused_user` — see [[discounts-codes-vs-code-pro]].

### Cart-link integration (auto-apply via URL)

Each row exposes a click-to-copy link in the format `<store-domain>/cart/discount:<CODE>`. When a customer opens that URL, the storefront **auto-applies the code to their cart** without requiring them to type it at checkout. This is the recommended mechanism for newsletter / SMS coupon campaigns where the merchant wants a click-through experience rather than an "enter this code" instruction. The auto-apply route is shared with all code-based discounts.

### Code lookup is case-insensitive

The checkout lookup matches case-insensitively — a customer typing `mycode` matches an upper-stored `MYCODE`. The generator only emits uppercase, but matching is case-flexible for customer-friendly input.

### Active scope at checkout lookup

Typing a code at checkout accepts only active codes; an inactive one gets *"Invalid discount code"*. To retire a leaked code fully, delete it.

### Cart can hold many Container codes — but only ONE stand-alone code

The customer's cart stores Container codes in an **array** (`discount_container_code`), and each typed Container code is appended to it. All active Containers for the customer's region try the entered codes; the highest total wins, and a code applies only if it fits what remains of that Container's value. Entering a stand-alone code (regular Promo / Code PRO) **clears the entire Container array**, and vice-versa: setting a stand-alone code wipes the Container codes, and adding a Container code clears the stand-alone code. **The two modes are mutually exclusive at the cart level.**

For merchants, this means one customer can use several Container codes in the same cart (e.g., a customer who collected multiple newsletter codes), with their percents adding up while they fit within the Container's value.

### Discounted products never block a Container code

A Container code is not refused because the cart holds discounted products. A Container's `code_apply` default is on and its form has no such switch, so its codes apply on discounted products too.

## Related

- [[marketing-discounts-codes]] — hub.
- [[marketing-discounts-code-pro]] — multi-use / per-customer-limit alternative.
- [[discount-code]] — entity page for individual codes.

## Open questions

No outstanding questions.
