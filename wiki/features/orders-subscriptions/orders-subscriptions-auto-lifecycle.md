---
type: feature
nav_path: "Orders → Subscriptions → Auto create / remove"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Auto-create subscription on paid", "Auto-remove subscription on unpaid", "Membership order trigger", "createSubscription", "removeSubscription", "order-* status exemption", "Quantity multiplies days"]
tags: [administration, membership, orders, subscriptions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Subscriptions — automatic create / remove on order status

## Purpose

This is the **hidden engine** behind storefront memberships: the merchant almost never issues subscriptions by hand. When a customer's order turns paid/completed, the Membership app grants the matching subscriptions automatically; when that order later reverts to a non-paid status, the access is revoked proportionally. This page documents those triggers, the day-math, and the carve-outs.

> Part of [[orders-subscriptions]]. See the hub for the other aspects (overview list, manual admin, status model, integration).

## Where to find it

There is no dedicated screen — this logic runs server-side on every order status change. The merchant observes the result on the overview list ([[orders-subscriptions-overview]]) and on the storefront content-gate. Failures are surfaced only in the system logs — see [[orders-subscriptions-integration]].

## What the merchant can do here

Nothing to click — the value here is understanding *why* a customer's access appeared or vanished. The merchant indirectly controls it by:

- Marking an order `paid` or `completed` (grants access).
- Reverting an order to `pending` / `refunded` / `cancelled` (revokes access).
- Configuring which digital products link to which pages, with a per-page `days` value, on the product editor ([[products-products]]).

## Settings & fields

The behaviour is driven by order status and by the product→page `days` mapping, not by fields on this surface. The relevant inputs:

| Input | Where set | Effect |
|-------|-----------|--------|
| Order status → `paid` / `completed` | [[orders-details]] / [[orders-status-change]] | Triggers auto-create. |
| Order status → non-paid (`pending`, `refunded`, `cancelled`) | order status change | Triggers auto-remove (unless status starts with `order-`). |
| Product `digital = 'yes'` | [[products-products]] | Only digital products are scanned — non-digital grant nothing. |
| Page `days` (per linked page) | [[products-products]] | Days granted per unit; `days = 0` → unlimited. |
| Order quantity | the order | Multiplies `page.days`. |

## Business rules

### Subscriptions are auto-created on order status change — NOT at purchase

When an order's status changes to `paid` OR `completed`, the Membership app's event listener runs the auto-create flow for that order:

1. Looks at the order's products where `digital = 'yes'` (membership products MUST be digital).
2. For each digital product, finds linked pages via `ProductPages` (set up by the merchant in [[products-products]]).
3. For each (product × page) combination:
   - If the customer already has a membership for that page+product:
     - If existing membership has expired → starts fresh from today + (page.days × order.quantity).
     - If existing membership is still active → EXTENDS the expiry by (page.days × order.quantity).
     - If existing membership has `expired = NULL` (unlimited) → no change.
   - Otherwise → creates a new membership with expiry = today + (page.days × order.quantity).
4. Records on the order's meta: `add_days = total days granted`.

So the merchant doesn't issue subscriptions manually — they happen automatically when the order is paid/completed. The `add_days` meta is the idempotency guard: it's only created once per order's transition into a paid state.

### Subscriptions are auto-REMOVED on un-paid status

If an order that carries the `add_days` meta transitions back to a non-paid status (e.g. `pending`, `refunded`, `cancelled` — but NOT a custom status starting with `order-`), the auto-remove flow runs:

1. For each digital product on the order, finds linked pages.
2. Subtracts (page.days × order.quantity) from existing memberships.
3. If the subtracted expiry is in the past → DELETES the membership row entirely.
4. If the subtracted expiry is still in the future → updates the membership with the new earlier expiry.
5. Removes `add_days` meta from the order.

So refunding / cancelling a paid order REVOKES the customer's subscription access proportionally.

### Custom status prefix `order-*` is EXEMPT from removal

Status names starting with `order-` (e.g. `order-special-handling`, `order-on-hold`) do NOT trigger auto-remove. Only canonical non-paid statuses do. This protects merchants who use custom intermediate statuses from an unwanted membership revoke.

### Multi-page products grant multiple memberships per purchase

If a product is linked to MULTIPLE pages via [[products-products]], a single purchase creates ONE membership per page. Buying a "Premium Bundle" product linked to 3 pages = 3 membership records per customer.

### Quantity multiplies membership days

Order quantity acts as a multiplier on `page.days`. Buying 2 units of a 30-day subscription product → 60 days of access. Bulk orders extend access proportionally.

### `days = 0` on the product-page link → unlimited

If a linked page has `days = 0` (or NULL), the membership created on purchase has `expired = NULL` → lifetime access (see [[orders-subscriptions-status-model]] for what *Unlimited* means downstream).

## Related

- [[orders-subscriptions]] — hub.
- [[orders-subscriptions-manual-admin]] — the admin-initiated path (Create / Add Extra Days) that uses the same extend semantics.
- [[orders-status-change]] / [[orders-details]] — where order status transitions originate.
- [[products-products]] — product editor; the digital flag + page `days` mapping the engine consumes.

## Open questions

(none.)
