---
type: feature
nav_path: "Marketing → Discounts → Known issues"
route_name: ""
route_path: ""
aliases: ["Discount gotchas", "Discount edge cases", "Discount validation messages", "Discount target combinatorial cap", "10,000 combinations", "Countdown single-instance", "Container codes stacking carve-out", "Order_over strict greater", "Free shipping insertion order", "MSRP display gotcha", "discount.created HTTP 403", "Грешки при отстъпки"]
tags: [marketing, discounts, promotions, known-issues, edge-cases, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Discount known issues & merchant gotchas

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (lifecycle, eligibility, storefront display, audit trail) plus per-type details.

## Purpose

This aspect catalogues the **by-design surprises** and **historical wiki corrections** the support agent should look up first when a merchant reports unexpected behaviour. Each item is either: (a) a validation rule that rejects something the merchant thought should work, (b) a cart-engine resolution rule that picks a different winner, or (c) an older wiki claim corrected against the backend. The **first page to read** for "the discount doesn't apply / the wrong discount applied / I got an error I don't understand" tickets.

## Where to find it

These surface at three points: **save-time validation errors** (conflicting fields), **checkout-time messages** (code can't apply), and **silent cart-engine choices** (no error, but a different total than expected).

## What the merchant can do here

- Re-architect a target list that hits the 10 000-combination cap into multiple smaller discounts.
- Set `order_over` thresholds 0.01 below the intended minimum to dodge the strict-greater rule.
- Avoid two overlapping no-code Free Shipping discounts (their tie-break is undefined).
- Decide whether to use MSRP mode given the "Save X" merchant-trap.
- Subscribe to webhooks for audit (no internal log exists — see [[discounts-audit-trail]]).

## Settings & fields

This page introduces no new fields; it documents corner-case behaviour of fields on the other aspects.

## Business rules

### Countdown — single-instance limit per store

Only ONE Countdown discount may exist per store. A second save returns `"Countdown discount already exists"`. To run back-to-back flash sales the merchant either edits the existing one or deactivates and creates a new one (subject to the 10-minute activation cooldown — see [[discounts-lifecycle]]).

### Quantity — one Quantity discount per product

A product can be tied to ONE Quantity discount at a time. Second save on the same `product_id` returns `"A volume discount with this product already exists"`. For different tiers per customer group, use [[apps-cart-rules]] instead.

### Fixed — no parent + child category overlap

A Fixed discount cannot target both a parent category and any of its children. Rejects with `"Parent and Child product categories, can not be included"`. Either target the parent (accept all children inherit the fixed price) or target specific children (exclude the parent).

### Promo code uniqueness

A promo code is unique across `discounts.code` per store. Code PRO codes live in a separate table (`discounts_code_pro.code`) and don't collide with regular codes — see [[marketing-discounts-code-pro]]. Container child codes have their own scope — see [[marketing-discounts-codes]].

### Target combinatorial cap — 10 000 combinations

When targeting the intersection of many dimensions (products × categories × customer_groups × selections), the platform multiplies the array sizes and **rejects** if the product > **10 000**: `"The maximum combinations allowed is 10,000, current: :count"`. Triggered by `category_vendor` or selection-based discounts with many entries × many customer groups. Protects the per-product-attachment regen job (see [[discounts-storefront-display]]). **Workaround**: narrow the target, or split into multiple smaller discounts.

### Strict-greater rules — `order_over` and `max_uses`

`order_over`: for a **code / Flat / Percent** discount the cart subtotal must be **strictly greater than** the threshold; equal does NOT qualify. A 50 EUR threshold rejects 50 EUR with `"The cart sum is not over the discount minimum"`. Workaround: set threshold slightly below (e.g., 49.99). (Note: no-code **Free shipping** `order_over` uses an **inclusive** check — a cart exactly at the threshold DOES qualify — see [[marketing-discounts-shipping]].)

`max_uses > uses`: a discount with `max_uses = 100` is still active at `uses = 99` and becomes inactive at `uses = 100`. The 100th order consumes the last slot when its status hits a counted status — see [[discounts-lifecycle]].

### `order_over` resolution + shipping tie-break

Multiple **non-code `order_over`** Flat / Percent discounts: engine picks ONE winner by **largest absolute saving**, NOT highest threshold. Cannot stack two over-amount discounts on the same cart. See [[discounts-eligibility]] for the resolution order.

**Shipping discounts use a SEPARATE path** (not the `order_over` pool). The engine returns the **first match** in database-insertion order — **undefined if two shipping discounts both match**. Don't run two overlapping no-code Free Shipping discounts simultaneously; if two are needed, use narrow customer-group / geo-zone scopes so they cannot both match.

### Container child codes bypass code-stacking validation

Container discount child codes (bulk-generated single-use coupons) follow a different stacking path than regular promo codes: the code-input validator rejects ONLY if the cart already has `price_saved > 0` AND the container's parent has `code_apply = 0`. The discount-validation engine's code-stacking check (which rejects regular codes on discounted carts) is **skipped** for Container codes — once accepted at input, the applicator doesn't re-check. Container discounts therefore behave subtly differently when stacking with per-product Fixed discounts. See [[marketing-discounts-codes]].

### Code lookup order — first hit wins

The code lookup tries: (1) exact `discounts.code`, (2) barcode match (EAN-13 / EAN-8 + optional store prefix), (3) Code PRO `discounts_code_pro.code`, (4) Container `discount_codes.code`. A regular numeric code can accidentally pre-empt an EAN match because exact-code is checked first.

### MSRP-mode "Save X" label can mislead customers

When a Fixed discount has `msrp = 1`, the strikethrough + "Save X EUR" reflects the saving **against MSRP**, not the catalog price. Example: catalog 800, MSRP 1 000, fixed 700 → storefront shows "Save 300" (1 000 − 700); actual saving vs the previously-shown catalog is only 100. **By design** — MSRP mode anchors against manufacturer's RRP — but merchants migrating to MSRP should expect "why 300 when it dropped by 100?" tickets. See [[marketing-discounts-fixed]] + [[discounts-storefront-display]].

### Per-customer cap auto-clears the code

When a logged-in customer hits `maxused_user`, the platform **clears the code from the cart entirely** (not just blocks redemption) and returns *"You have already used this discount the maximum number of times"*. UX surprise for repeat customers expecting the code to stack across orders — the cap is total uses per customer, not per order. See [[discounts-eligibility]].

### Bulk-toggle silently skips in-cooldown rows

The bulk activate / deactivate action **silently skips** rows still inside their 10-minute activation cooldown (see [[discounts-lifecycle]]). The merchant gets a success toast but some discounts may be untouched. Workaround: wait 10 minutes and re-run.

### JSON-API v2 corrections

- **HTTP 403**, not 402, on plan-cap exceeded (older wiki said 402). Returns an **upgrade-required plan message** (built from the plan-feature mapping), not a literal "Not supported by plan" string. Unlike the admin Discounts panel — where the create-time gate only actually fires for Code PRO (see the hub's Plan-gates note) — the JSON-API path enforces the per-type plan quotas server-side.
- **Quantity and Countdown not creatable via API.** The JSON-API v2 allowlist is 5 types: `percent`, `flat`, `fixed`, `shipping`, `code-pro` (note this differs from the admin form, which accepts `quantity` but not `code-pro`). See [[api-discounts]].
- **"API writes audit log with api2 tag" is INCORRECT.** No internal audit log exists for discount CRUD — only webhooks; payload does not distinguish API vs admin. See [[discounts-audit-trail]].

## Related

- [[marketing-discounts]] — hub.
- [[apps-cart-rules]] — workaround engine when a single Quantity discount isn't flexible enough.
- [[json-api-v2]] / [[api-discounts]] — programmatic CRUD with the 5-type allowlist + HTTP 403 on plan cap.

## Open questions

None.
