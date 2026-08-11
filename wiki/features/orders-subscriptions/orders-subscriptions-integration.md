---
type: feature
nav_path: "Orders → Subscriptions → System integration"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership permissions", "Apps permission gate", "Membership failure logging", "Membership segment hook", "Membership condition manager", "Renewal campaigns", "Membership expiration segment"]
tags: [administration, membership, orders, subscriptions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Subscriptions — permissions, logging & segment hooks

## Purpose

This page covers how the Membership app plugs into the rest of the platform: who is allowed to manage subscriptions, what happens when the auto-create / auto-remove engine fails, and the customer-segment conditions the app contributes — which are how merchants drive renewal campaigns despite there being no built-in expiry email.

> Part of [[orders-subscriptions]]. See the hub for the other aspects (overview list, auto-lifecycle, manual admin, status model).

## Where to find it

- **Permissions**: staff roles in the admin settings; the membership routes are gated on the Apps permission scope.
- **Failure logs**: the system logs — see [[settings-files]].
- **Segment conditions**: surface inside [[customers-custom-groups]] when building a customer segment.

## What the merchant can do here

- Restrict which staff can manage subscriptions (via the Apps permission scope).
- Audit subscription-engine failures in the system logs.
- Build customer segments on membership state and feed them into [[marketing-campaigns]] for renewal outreach.

## Settings & fields

| Integration point | Where | Effect |
|-------------------|-------|--------|
| `hasApiPermission:apps` gate | staff role permissions | Staff without the Apps permission cannot access subscription management. |
| Failure log entries | [[settings-files]] | Search `Membership: failed to create subscription` / `Membership: failed to remove subscription`. |
| `MembershipConditionManager` | [[customers-custom-groups]] | Segment condition "has active membership on Page X". |
| `MembershipExpirationConditionManager` | [[customers-custom-groups]] | Segment condition "membership expires in N days". |

## Business rules

### Permissions — gated on the Apps permission scope

The membership routes are middleware-gated on `hasApiPermission:apps`. Staff users without the Apps permission can't access subscription management — so locking down the Apps scope also locks down memberships.

### Failure logging — silent to the merchant

If the auto-create / auto-remove logic throws (e.g. a database lock or foreign-key issue), the exception is caught and logged — the order's status change DOES NOT FAIL. So a broken membership-creation won't block paying for the order, but a customer might end up without their subscription. The merchant audits failures via the system logs ([[settings-files]]) by searching for `Membership: failed to create subscription` or `Membership: failed to remove subscription`. The engine itself is documented on [[orders-subscriptions-auto-lifecycle]].

### Membership has its own customer-segment hooks

The Membership app registers segment-condition managers that integrate with the [[customers-custom-groups]] system. Merchants can build customer segments like "has active membership on Page X" or "membership expires in N days" — driving renewal campaigns via [[marketing-campaigns]]. The segment query exists-joins against the membership data.

### Why the segment hooks matter

Because there is no built-in expiry email and no renewal billing (see [[orders-subscriptions-status-model]] and [[orders-subscriptions-settings]]), the "membership expires in N days" segment is the ONLY mechanism for proactive renewal outreach. The merchant builds the segment in [[customers-custom-groups]] and targets it with a campaign in [[marketing-campaigns]]; the customer renews by re-purchasing the membership product on the storefront.

## Related

- [[orders-subscriptions]] — hub.
- [[orders-subscriptions-auto-lifecycle]] — the engine whose failures land in the logs.
- [[customers-custom-groups]] — where the membership segment conditions are used.
- [[marketing-campaigns]] — renewal outreach driven by those segments.
- [[settings-files]] — system logs for auditing engine failures.

## Open questions

(none.)
