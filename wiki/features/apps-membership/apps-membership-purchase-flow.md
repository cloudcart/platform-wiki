---
type: feature
nav_path: "Apps → Membership → Purchase flow"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership purchase flow", "How membership is granted", "Membership digital product", "Membership days", "Expiry stacking", "add_days"]
tags: [apps, administration, membership, orders, digital-products]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Membership — purchase / grant flow

> Part of [[apps-membership]]. See the hub for the other aspects (data model, renewal/revocation, records admin, API).

## Purpose

This aspect documents **how a membership is actually granted**: by buying a digital product linked to one or more Pages. There is no separate "membership tier" entity — tiers are built from differently-priced digital products. Understanding this flow explains expiry stacking, quantity multipliers, and the audit trail.

## Where to find it

The grant is configured in the catalog (Products) and triggered by an order reaching a paid status — not from a dedicated screen. The resulting records appear in the Settings tab (see [[apps-membership-records-admin]]).

## What the merchant can do here

- Build a "membership tier" as a `digital` product linked to Pages with validity days.
- Grant access to multiple pages from one product (one record per page).
- Use cart quantity as a days multiplier (buy 3× a 30-day membership → 90 days).
- Let customers renew early without losing remaining time (expiry stacks forward).

### What the merchant CANNOT do here

- Grant membership without an order reaching `paid` / `completed` — the grant is order-status-driven (see [[apps-membership-renewal-revocation]]).
- Avoid the per-page fan-out — linking a product to N pages always creates N records.

## Settings & fields

The grant reads three values:

- The product's `digital = yes` flag.
- The product-pages mapping rows, each carrying `product_id`, `page_id`, and `days`.
- The order line `quantity` (used as a days multiplier).

It writes the membership record's `expired` field and stores `add_days` on the order meta (the audit value).

## Business rules

### Membership is granted by purchasing a "digital" product linked to Pages

The merchant configures membership by:

1. Marking a Product as `digital = yes`.
2. Linking that product to one or more Pages via the product-pages mapping (carries `product_id`, `page_id`, and `days`).
3. When a customer's order with that product reaches status `paid` or `completed`, the platform automatically creates / extends a membership record for each `(customer_id, product_id, page_id)` combo with `expired = now + (days × quantity)`.

**This is the actual purchase flow** — there is no separate "membership tier" entity; tiers are differently-priced digital products with different page links and validity periods.

### Multi-product memberships — multiple records per customer

When a customer buys a digital product linked to MULTIPLE pages, one membership record is created PER linked page. So a "Gold Member" product could grant access to a Forum Page + a Members-Only Catalog Page + a Tutorials Page — three records, three independent expiry timers (all set to the same date initially). See [[apps-membership-data-model]] for the per-record shape.

### Quantity in cart MULTIPLIES the days granted

The platform computes membership days as `days × quantity` — so buying quantity 3 of a 30-day membership grants 90 days (or extends an existing membership by 90 days). Useful for gift / multi-pack purchases where the customer wants to top up.

### Expiry stacking: re-purchase extends from CURRENT expiry, not from today

When a customer re-purchases a digital membership product while their existing membership is still ACTIVE, the new days are added to the CURRENT expiry (not to "now"). So early renewal extends the expiry forward without losing time.

If the membership has ALREADY expired when the customer re-purchases, the new expiry is calculated from "now" — they lose the gap days but the membership reactivates.

### `add_days` order meta is the audit trail

Each order that grants membership stores `add_days` on its meta — the total days granted by that single order. This is used to:

- Prevent double-grants (the order only grants days once, even if the status flips between `paid` / `completed` repeatedly).
- Calculate exactly how many days to subtract back on refund / cancellation — see [[apps-membership-renewal-revocation]].

### Lifetime grant via `days = 0`

When the linked Page is configured with `days = 0` (or empty), the membership record is created with `expired = null` (lifetime). The quantity multiplier is irrelevant in that case. See [[apps-membership-data-model]].

## Related

- [[apps-membership]] — hub.
- [[products-products]] — the digital product that backs the grant.
- [[order]] — the order whose status drives the grant.
- [[apps-membership-renewal-revocation]] — the status transitions that grant and revoke.

## Open questions

None.
