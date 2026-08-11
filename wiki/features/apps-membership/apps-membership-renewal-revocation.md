---
type: feature
nav_path: "Apps → Membership → Renewal & revocation"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership renewal", "Membership revocation", "Membership auto-renew", "Membership grace period", "Membership expiry reminders", "Membership refund revoke"]
tags: [apps, administration, membership, orders, lifecycle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Membership — renewal & revocation

> Part of [[apps-membership]]. See the hub for the other aspects (data model, purchase flow, records admin, API).

## Purpose

This aspect documents the **lifecycle** of a membership after the initial grant: how it renews, when it is automatically revoked, and the several things that do NOT happen automatically (no card-on-file billing, no grace period, no expiry-reminder emails). The whole lifecycle is driven by **order-status transitions**, not by a scheduled job.

## Where to find it

There is no lifecycle screen. Renewal and revocation are side-effects of changing an order's status from [[orders-details]]. Expiry-reminder segments are built in [[marketing-subscribers]].

## What the merchant can do here

- Renew a membership by having the customer place a new order for the same digital product (extends the existing record — see [[apps-membership-purchase-flow]]).
- Rely on automatic revocation when a membership order is refunded / cancelled.
- Build expiry-reminder emails via a subscriber segment using the membership-expiration condition.

### What the merchant CANNOT do here

- Get a card-on-file recurring charge — there is no scheduled billing inside the module.
- Get a built-in grace period after expiry — expiry is a hard timestamp.
- Get a built-in "your membership expires soon" email — the module ships no reminder template.

## Settings & fields

The lifecycle reads:

- The order's status (built-in vs custom `order-*` statuses).
- The order-meta `add_days` value (how many days to subtract back on revocation — see [[apps-membership-purchase-flow]]).
- The membership record's `expired` timestamp.

## Business rules

### Order-status-driven renewal AND auto-cancellation

Order-status transitions drive renewal and revocation:

- Order reaches `paid` or `completed` → expiry is extended by `days × quantity`.
- Order leaves those statuses (refund, cancellation, etc.) AND `add_days` was previously set on the order's meta → those days are SUBTRACTED back. If the resulting expiry is in the past, the membership row is DELETED.

**So if a customer disputes / refunds their membership purchase, the platform automatically revokes the membership.** The order-meta `add_days` field ensures the platform knows exactly how much to subtract (preventing double-subtraction or under-subtraction when the order is later restored).

### Custom merchant-defined order statuses do NOT revoke memberships

The revocation flow only fires when the order leaves the `paid` / `completed` statuses AND the new status is NOT one that begins with `order-` (i.e., a merchant-defined custom status). So orders moved into custom-named statuses (e.g., `order-shipped`, `order-on-hold`) **preserve** the customer's membership.

This is intentional: if the merchant moves an order from "Paid" to a custom workflow status like "Order shipped", the membership stays valid. Only built-in statuses such as `cancelled`, `refunded`, `pending` trigger automatic revocation.

### Auto-renew via online payment is order-driven, not card-on-file

There is no scheduled-charge mechanism inside the Membership module. "Renewal" means the customer comes back, places a new order for the same digital product, and the platform extends the existing membership row. **There is no automatic recurring charge** to the customer's saved card unless the merchant uses a separate recurring-billing app + an order-creation automation. The "auto-renew" UX described elsewhere is essentially "remind the customer to re-purchase," not card-on-file billing.

### No grace period for failed renewals

The `expired` field is a hard timestamp; once it passes, the membership flips to inactive and lapses immediately. There is no built-in grace period (e.g., "still active for 7 days after expiry while we retry payment"). The merchant can simulate one by extending expiry timestamps manually (the Extra Days action — see [[apps-membership-records-admin]]).

### No built-in expiry-reminder emails

The module ships exactly ONE email template (page-access-test). There is NO "your membership expires in 7 days" reminder template and no scheduled job that emails members before expiry. The merchant must build expiry reminders via:

- A subscriber segment using a membership-expiration condition (which exposes the membership expiry as a date-interval condition) — see [[marketing-subscribers]].
- An email automation targeting that segment.

The membership-expiration condition lets the merchant create segments like "members whose membership expires in the next 7 days" — which a marketing email can then target.

### Membership-expiration subscriber segment

The integration ships a condition manager that registers a segment condition for [[marketing-subscribers]]: the merchant can build a segment like "Members whose membership expires in the next N days". This is the recommended way to send expiry-reminder emails (since no built-in reminder email exists).

### Page visibility is gated by Membership, not by Private Store

Private Store gates the WHOLE storefront behind login; Membership gates SPECIFIC Pages (via `page_id` on the membership record). **The page-level visibility check is enforced by the Page rendering code reading the customer's active membership rows** (matches `customer_id` and checks `expired > now`). So a non-member sees a "not available" placeholder on member-only pages while still browsing the public catalog. There is no public-vs-member catalog switcher UI — it's implicit in which pages render content vs the unauthorised fallback. See [[apps-private-store]] for the alternative full-store-gating model.

### Failure logging is silent to the merchant

Failures during membership create / remove are logged to the platform's internal log table — the merchant does NOT see a notification. If membership creation fails (e.g., the customer has been deleted but the order still gets paid), the order proceeds normally and the membership simply doesn't materialise.

## Related

- [[apps-membership]] — hub.
- [[orders-details]] — where order-status transitions are made.
- [[orders-status-change]] — the status-transition mechanics that drive grant / revoke.
- [[marketing-subscribers]] — the membership-expiration segment condition.
- [[apps-private-store]] — alternative full-store gating.

## Open questions

None.
