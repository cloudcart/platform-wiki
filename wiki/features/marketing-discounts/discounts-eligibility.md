---
type: feature
nav_path: "Marketing → Discounts → Eligibility & stacking"
route_name: ""
route_path: ""
aliases: ["Discount eligibility", "Discount stacking", "Customer-group discount restriction", "Geo zone discount", "Per-customer discount cap", "Discount max uses per customer", "Discount only for registered users", "code_apply", "apply_regular_price", "force_save discount", "Allow stacking on discounted products", "Ограничение по клиентска група", "Ограничение по регион", "Стак на промо кодове"]
tags: [marketing, discounts, promotions, eligibility, stacking, customer-groups, geo-zone]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

# Discount eligibility, stacking & per-customer caps

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (lifecycle, tax/VAT, storefront display, audit trail, known issues) plus per-type details.

## Purpose

This aspect covers **who** a discount applies to and **how it composes** with other discounts: customer-group / geo-zone restrictions, the only-registered-users gate, per-customer caps (`maxused_user`), stacking semantics (`code_apply`, `apply_regular_price`), and the save-on-edit flag (`force_save`). Which of these a form offers depends on the discount type.

## Where to find it

**Sidebar → Marketing → Discounts → Edit form.** Field-blocks, depending on the type: **Customer groups** (all types), **Regions** (geo zone; code, Container and Code PRO), **Registered users only** (Global, code, Code PRO, Countdown), **Discount limits** (`max_uses` + `maxused_user`), and **Generate a discount code** (which holds `code_apply` + `apply_regular_price` for code-types).

## What the merchant can do here

- Restrict a discount to customer groups (loyalty tiers, VIPs, wholesale) and/or a geo zone.
- Limit a discount to registered customers (`only_customer`).
- Cap total uses (`max_uses`) and per-customer uses (`maxused_user`).
- Decide whether a promo code also applies to lines that already hold a product discount (`code_apply`) and whether it is worked out on the regular price instead (`apply_regular_price`).
- Keep a discount deducting on a saved order after admin edits (`force_save`).

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|---|---|---|---|
| **All groups** → **Customer groups** | `customer_groups_target` / `customer_groups[]` | An **"All groups"** switch (`customer_groups_target`, default ON); turning it OFF reveals the `customer_groups[]` multi-select to restrict to specific [[customers-custom-groups]]. | Group-list is **not** force-validated: turning "All groups" off and leaving the list empty saves without error (and behaves as no group filter). |
| **Make it Global** → **Region (Geo zone)** | `all_regions` / `geo_zone_id` | A **"Make it Global"** switch (`all_regions`, default ON); turning it OFF reveals the `geo_zone_id` select to restrict to carts shipping inside one [[geo-zone]]. | Nullable; must exist. |
| **Only registered users** | `only_customer` | Limits the discount to logged-in customers, see below. | 1 / 0. |
| **Discount limits** | `max_uses` | Total cap across all customers. NULL = unlimited. | Integer 1–100 000. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap. NULL = unlimited. | Integer 1–100 000. |
| **The discount is applied even when the cart contains discounted products.** | `code_apply` | ON: the code also applies to lines holding a product discount. OFF (default): see "Stacking" below. | 1 / 0. "Discount" + "Fixed discount" only. |
| **Apply to the regular price of products, if this discount is greater** | `apply_regular_price` | Works the code out on the regular price and replaces the product discount on a line if that gives a lower price. | 1 / 0. Only visible when `code_apply = 1`. |
| **Save the discount on your order** | `force_save` | Preserves discount on saved order despite admin edits. Rendered inside the **Discount target** block, shown only when target = "Orders over" (`order_over`) or for a Free-shipping discount on all orders. | 1 / 0. The merchant's own switch; it can be off. |

## Business rules

### Customer-group / region matching

The cart engine evaluates against the cart's customer (or the guest group if no customer). `customer_groups[]` requires membership in one of those groups; `geo_zone_id` requires the shipping address to be inside the [[geo-zone]]. Customer groups and regions compose with **AND** semantics — a discount restricted to "VIP + Bulgaria" requires both.

`only_customer = 1` is enforced for codes at entry (*"The code is valid only for registered users"*) and for no-code Orders over and Countdown discounts in the totals. The customer list applies to no-code Orders over and no-code free shipping; codes use customer groups.

### Per-customer cap

When `maxused_user` is set, the platform counts this customer's uses on orders in counted statuses (see [[discounts-lifecycle]]). On Code PRO it counts across the whole campaign. A cancelled order that was already fulfilled still counts here. The limit applies to logged-in customers, on codes at entry and on no-code Orders over and Countdown discounts. When the limit is reached, the cart engine **clears the code from the cart entirely** and returns *"You have used this discount code the maximum number of times"*. Distinct from `max_uses` (global cap, deactivates for everyone): `maxused_user` only clears it for **this customer**.

### Stacking — `code_apply` and lines with a product discount

**The most important merchant-facing rule.** Only product-level discounts count as "already discounted". With `code_apply = 0` (default), an Orders-over code or a free-shipping code with a threshold is **refused** at entry if any line holds a product discount, with *"This discount code can not be applied because you already have a discounted products at your cart"*. Free shipping for all orders and Code PRO are refused with *"Invalid discount code"*. A code for every product or a specific target is **accepted**: lines with a product discount are skipped, and if all are discounted nothing comes off and no message shows.

With the switch ON (`code_apply = 1`), the code also applies to those lines, on the already reduced amount. If `apply_regular_price = 1` is also ON, the code is worked out on the regular price and compared with the current discounted price: if the code's price is lower it replaces the product discount, otherwise the line keeps the product discount and no code. See [[discount-stacking-code-apply]].

No-code discounts have no such switch.

### One no-code `order_over` discount — highest threshold wins

When the cart qualifies for several **no-code `order_over`** Flat / Percent discounts, the highest threshold the subtotal passes wins, whatever it saves. Example: "10 EUR off over 50" vs "5 EUR off over 100" on a 150 EUR cart → 5 EUR off. "20 % off over 50" vs "10 EUR off over 100" on 150 EUR → 10 EUR off. If that one cannot apply, no other is tried. An Orders-over code can apply alongside it. Shipping discounts use a separate path (see [[discounts-known-issues]]).

### Cart Rules — after line-level discounts, before order-level discounts

[[apps-cart-rules]] are evaluated after product discounts and line-level codes, and before order-level discounts. A "Cart total > 100 EUR" condition sees the total after product discounts and line-level codes, not after an Orders-over discount, Countdown or payment discount. Those order-level discounts are calculated, and their thresholds checked, on the subtotal after product-level rule reductions. See [[discount-stacking-cart-rules-interaction]].

### Strictly-greater subtotal check on `order_over`

When a code requires `order_over`, the cart subtotal must be **strictly greater than** the threshold. A 50 EUR threshold rejects a cart at exactly 50 EUR with: *"The discount could not be applied because the minimum total price of the products has not been reached."* The merchant either sets the threshold slightly below the intended minimum (e.g., 49.99) or accepts the strict-greater semantic. See [[discounts-known-issues]].

### `force_save` — discount survives an order edit

When `force_save = 1` and an admin edits a saved order on [[orders-details]], the discount stays on the order even if the new cart contents no longer meet the conditions. Critical for shipping discounts (keep free shipping when the qualifying product is removed) and `order_over` discounts (when admin edits push the cart below threshold). Without it, the discount stays listed on the order, but stops being deducted while the conditions are not met. It is the merchant's own switch and can be off. Each [[marketing-discounts-code-pro]] child code has its OWN `force_save` flag.

### Resolution order at checkout

A code at entry is checked in this order, and failing any step refuses it: **active scope** (see [[discounts-lifecycle]]) with **customer group** and **region** → **registered-only** (`only_customer`) → **per-customer cap** (`maxused_user`) → **threshold** (`order_over`) → **stacking** (`code_apply`) and **target check**. Code-types return a customer-facing message; no-code types silently don't fire.

## Related

- [[marketing-discounts]] — hub.
- [[discounts-lifecycle]] — the active-scope check (status + date + `max_uses`) that runs FIRST.
- [[discounts-known-issues]] — the strict-greater `order_over` check + Container codes + free-shipping resolution.
- [[customers-custom-groups]] — the customer-group entity used by `customer_groups[]`.
- [[geo-zone]] — the geo-zone entity used by `geo_zone_id`.
- [[apps-cart-rules]] — the more flexible composable engine.
- [[orders-details]] — admin-side order edit; `force_save` controls whether the discount survives.

## Open questions

None.
