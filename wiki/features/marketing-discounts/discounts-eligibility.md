---
type: feature
nav_path: "Marketing → Discounts → Eligibility & stacking"
route_name: ""
route_path: ""
aliases: ["Discount eligibility", "Discount stacking", "Customer-group discount restriction", "Geo zone discount", "Per-customer discount cap", "Discount max uses per customer", "Discount only for registered users", "code_apply", "apply_regular_price", "force_save discount", "Allow stacking on discounted products", "Ограничение по клиентска група", "Ограничение по регион", "Стак на промо кодове"]
tags: [marketing, discounts, promotions, eligibility, stacking, customer-groups, geo-zone]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Discount eligibility, stacking & per-customer caps

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (lifecycle, tax/VAT, storefront display, audit trail, known issues) plus per-type details.

## Purpose

This aspect covers **who** a discount applies to and **how it composes** with other discounts: customer-group / geo-zone restrictions, the only-registered-users gate, per-customer caps (`maxused_user`), stacking semantics (`code_apply`, `apply_regular_price`), and the save-on-edit flag (`force_save`). These rules apply across every discount type; the cart engine resolves them in a fixed order — see "Resolution order" below.

## Where to find it

**Sidebar → Marketing → Discounts → Edit form.** Five field-blocks: **Customer groups**, **Regions** (geo zone), **Registered users only**, **Discount limits** (`max_uses` + `maxused_user`), and **Generate a discount code** (which holds `code_apply` + `apply_regular_price` for code-types).

## What the merchant can do here

- Restrict a discount to customer groups (loyalty tiers, VIPs, wholesale) and/or a geo zone.
- Block **guests** entirely — only logged-in customers can use it.
- Cap total uses (`max_uses`) and per-customer uses (`maxused_user`).
- Decide whether a promo code can **stack** on already-discounted products (`code_apply`) and whether it re-evaluates against the original catalog price (`apply_regular_price`).
- Pin a discount to a saved order so admin edits don't detach it (`force_save`).

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|---|---|---|---|
| **All groups** → **Customer groups** | `customer_groups_target` / `customer_groups[]` | An **"All groups"** switch (`customer_groups_target`, default ON); turning it OFF reveals the `customer_groups[]` multi-select to restrict to specific [[customers-custom-groups]]. | Group-list is **not** force-validated: turning "All groups" off and leaving the list empty saves without error (and behaves as no group filter). |
| **Make it Global** → **Region (Geo zone)** | `all_regions` / `geo_zone_id` | A **"Make it Global"** switch (`all_regions`, default ON); turning it OFF reveals the `geo_zone_id` select to restrict to carts shipping inside one [[geo-zone]]. | Nullable; must exist. |
| **Only registered users** | `only_customer` | Hides the discount from guest carts. | 1 / 0. |
| **Discount limits** | `max_uses` | Total cap across all customers. NULL = unlimited. | Integer 1–100 000. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap. NULL = unlimited. | Integer 1–100 000. |
| **Apply discount even if the cart contains products with a discount** | `code_apply` | Allows code to stack on existing per-product discounts. OFF (default) REJECTS code if any cart line is discounted. | 1 / 0. "Discount" + "Fixed Discount" only. |
| **Apply to the regular price if this discount is higher** | `apply_regular_price` | Re-evaluates against original catalog price if that yields a bigger discount. | 1 / 0. Only visible when `code_apply = 1`. |
| **Save the discount on your order** | `force_save` | Preserves discount on saved order despite admin edits. Rendered inside the **Discount target** block, shown only when target = "Orders over" (`order_over`) or for a Free-shipping discount targeting the whole cart. | 1 / 0. Required for `type=shipping` OR `type=flat/percent` with `settings=order_over`. |

## Business rules

### Customer-group / region matching

The cart engine evaluates against the cart's customer (or the guest group if no customer). `customer_groups[]` requires membership in one of those groups; `geo_zone_id` requires the shipping address to be inside the [[geo-zone]]; `only_customer = 1` blocks guests entirely regardless of the other settings. Customer groups and regions compose with **AND** semantics — a discount restricted to "VIP + Bulgaria" requires both.

### Per-customer cap — auto-clear when hit

When `maxused_user` is set, the platform counts how many orders from THIS customer (in counted statuses — see [[discounts-lifecycle]]) have used this discount. When the count reaches `maxused_user`, the cart engine **clears the code from the cart entirely** (not just blocks redemption) and returns *"You have already used this discount the maximum number of times"*. The customer enters a different code or finishes without one. Distinct from `max_uses` (global cap, deactivates for everyone): `maxused_user` only clears it for **this customer**.

### Stacking — by default, NO stacking on already-discounted items

**The most important merchant-facing rule.** When `code_apply = 0` (default), a promo code is **REJECTED** at checkout if ANY cart line already has a discount applied (typically a Fixed discount on one of the products) `(verify exact validation string)`.

To **allow** stacking, the merchant turns ON **"Apply discount even if the cart contains products with a discount"** (`code_apply = 1`). With it ON, the code applies on top of existing per-product discounts (additive). If `apply_regular_price = 1` is also ON, the code re-evaluates against the ORIGINAL catalog price (ignoring per-product Fixed discounts) if that would yield a larger total discount — the cart engine picks whichever gives the customer more savings.

For free-shipping codes with target `all`, the same `code_apply = 0` rule blocks stacking — but `order_over` Free Shipping discounts CAN apply regardless (target type matters).

### Cart engine picks ONE `order_over` discount — largest saving wins

When the cart qualifies for multiple **non-code `order_over`** Flat / Percent discounts, the engine deduplicates into ONE winner by **largest absolute saving**, NOT highest threshold. Example: "10 EUR off over 50" vs "5 EUR off over 100" on a 150 EUR cart → 10 EUR wins. "20 % off over 50" vs "10 EUR off over 100" on 150 EUR → 30 EUR > 10 EUR, percent wins. Cannot stack two over-amount Flat / Percent discounts on the same cart. Shipping discounts use a separate path (see [[discounts-known-issues]] for the insertion-order ambiguity).

### Discounts then Cart Rules — fixed ordering

[[apps-cart-rules]] run AFTER Discounts at checkout. Cart Rules see the per-line amount **POST-discount** — a "Cart total > 100 EUR" trigger evaluates against the discounted cart, not the pre-discount one. Merchants designing both should remember this when their Cart Rule thresholds seem to "not fire".

### Strictly-greater subtotal check on `order_over`

When a code requires `order_over`, the cart subtotal must be **strictly greater than** the threshold. A 50 EUR threshold rejects a cart at exactly 50 EUR with: *"The cart sum is not over the discount minimum"*. The merchant either sets the threshold slightly below the intended minimum (e.g., 49.99) or accepts the strict-greater semantic. See [[discounts-known-issues]].

### `force_save` — discount survives an order edit

When `force_save = 1` and an admin edits a saved order on [[orders-details]], the discount stays on the order even if the new cart contents no longer meet the conditions. Critical for shipping discounts (keep free shipping when the qualifying product is removed) and `order_over` discounts (when admin edits push the cart below threshold). Without it, editing detaches the discount. The flag is **required** by validation when `type = shipping` OR `type = flat/percent` with `settings = order_over`. Each [[marketing-discounts-code-pro]] child code has its OWN `force_save` flag.

### Resolution order at checkout

For each cart, the engine evaluates in this fixed order (failing any step skips the discount): **active scope** (see [[discounts-lifecycle]]) → **customer-group match** → **geo-zone match** → **guest gate** (`only_customer`) → **per-customer cap** (`maxused_user`) → **stacking check** (`code_apply`) → **target check** (`settings` + targets). Code-types return a customer-facing message; no-code types silently don't fire.

## Related

- [[marketing-discounts]] — hub.
- [[discounts-lifecycle]] — the active-scope check (status + date + `max_uses`) that runs FIRST.
- [[discounts-known-issues]] — the strict-greater `order_over` check + Container-codes stacking carve-out + free-shipping resolution ambiguity.
- [[customers-custom-groups]] — the customer-group entity used by `customer_groups[]`.
- [[geo-zone]] — the geo-zone entity used by `geo_zone_id`.
- [[apps-cart-rules]] — the more flexible composable engine that runs AFTER Discounts.
- [[orders-details]] — admin-side order edit; `force_save` controls whether the discount survives.

## Open questions

- Exact validation string when `code_apply = 0` rejects a code on a cart with discounted products `(verify)`.
