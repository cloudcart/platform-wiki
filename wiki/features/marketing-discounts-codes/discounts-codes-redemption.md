---
type: feature
nav_path: "Marketing → Discounts → Container codes → Redemption"
route_name: discounts-codes_list
route_path: /admin/marketing-new/discounts/codes
aliases: ["Container code redemption", "Cart-link auto-apply", "Single-use coupon redemption", "Container code stacking", "Прилагане на промо код", "Линк за автоматично прилагане"]
tags: [marketing, discounts, coupons, container, redemption, cart]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Container codes — distribution & redemption

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, parent-term inheritance, and the JSON-API.

## Purpose

This aspect covers what happens **after** codes are generated: how the merchant distributes them, how a customer applies one, and the cart-level rules that decide which codes can coexist. The key facts are that each code is single-use, codes can be auto-applied via a shareable URL, and Container codes are mutually exclusive with stand-alone codes inside a cart.

## Where to find it

Redemption happens on the storefront cart / checkout, not in the admin panel. The merchant's touch-point is the Container codes list (`/admin/marketing-new/discounts/codes`), where each row exposes the click-to-copy cart link.

## What the merchant can do here

- **Distribute a code as a plain string** — the customer types it at checkout.
- **Distribute a code as an auto-apply URL** — copy the row's `<store-domain>/cart/discount:<CODE>` link and embed it in a newsletter / SMS so the code applies on click, with no typing.
- **Retire a leaked code** — toggling it inactive (see [[discounts-codes-list-view]]) makes the checkout reject it immediately.

## Settings & fields

This aspect has no admin settings of its own. The redemption behaviour is driven by the parent Container discount's terms (see [[discounts-codes-parent-terms]]) and the per-row `active` flag (see [[discounts-codes-list-view]]).

## Business rules

### Single-use redemption — one code, one order

Container codes are designed for **one-and-done campaigns**: each code may be redeemed exactly once. After a successful redemption the code's row is consumed. The merchant doesn't see a per-code "uses" counter in the listing — only the active flag (active = available; inactive = consumed or manually disabled). For codes redeemable multiple times by the same or many customers, use [[marketing-discounts-code-pro]] instead, where each code has its own `max_uses` and `maxused_user` — see [[discounts-codes-vs-code-pro]].

### Cart-link integration (auto-apply via URL)

Each row exposes a click-to-copy link in the format `<store-domain>/cart/discount:<CODE>`. When a customer opens that URL, the storefront **auto-applies the code to their cart** without requiring them to type it at checkout. This is the recommended mechanism for newsletter / SMS coupon campaigns where the merchant wants a click-through experience rather than an "enter this code" instruction. The auto-apply route is shared with all code-based discounts; it is just particularly load-bearing for Container codes since the merchant is mass-distributing many codes at once.

### Code lookup is case-insensitive

The checkout lookup matches case-insensitively — a customer typing `mycode` matches an upper-stored `MYCODE`. The generator only emits uppercase, but matching is case-flexible for customer-friendly input.

### Active scope at checkout lookup

The checkout discount-lookup filters codes by `active = 1`. Inactive codes are skipped before the cart even attempts to validate them.

### Cart can hold many Container codes — but only ONE stand-alone code

The customer's cart stores Container codes in an **array** (`discount_container_code`), so a customer can stack multiple Container coupons against the same parent campaign — each redeemed sequentially up to the parent's `total_value` cap, if set. Each typed Container code is appended to the array. Entering a stand-alone code (regular Promo / Code PRO) **clears the entire Container array**, and vice-versa: setting a stand-alone code wipes the Container codes, and adding a Container code clears the stand-alone code. **The two modes are mutually exclusive at the cart level.**

For merchants, this means a campaign mailout shipping 1,000 unique Container codes can have one customer redeem several of them in the same cart (e.g., a customer who collected multiple newsletter codes), with successive codes adding to the discount value until the parent's cap is reached.

### The parent's `code_apply` controls reject-on-conflict — not the child's

A Container code's own row has no `code_apply` field. When the customer enters a Container code, the checkout validator reads **the parent Container discount's** `code_apply` setting. If the parent has `code_apply = 0` and the cart already carries a per-product discount, the Container code is rejected — even though the row being redeemed is a leaf-level code row. The parent's `apply_regular_price` similarly applies to all of its Container children. See [[discounts-codes-parent-terms]] for the full list of inherited terms.

## Related

- [[marketing-discounts-codes]] — hub.
- [[marketing-discounts-code-pro]] — multi-use / per-customer-limit alternative.
- [[discount-code]] — entity page for individual codes.

## Open questions

No outstanding questions.
