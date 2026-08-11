---
type: concept
nav_path: "Concept → Checkout flow → Abandoned detection"
aliases: ["Abandoned cart detection", "abandoned_remainder_interval", "Cart recovery", "Restore link", "Recovered cart", "Restore source"]
tags: [orders, checkout, cart, abandoned, concepts]
plan_gates: [abandoned_notification]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[checkout-flow]]. See the hub for the other aspects (cart entity, submit-to-order, guest vs registered, lifecycle overview, discounts & rules, events & webhooks).

# Checkout flow — Abandoned-cart detection

## Definition

A cart is **abandoned** the moment its `updated_at` falls behind the configured `abandoned_remainder_interval` window. At that point the platform makes the cart eligible for a customer-facing **recovery email** + optional **Messenger bot** message, surfaces it on the [[orders-abandoned]] admin list, and exposes it to the *Begin order* segment condition. If the customer clicks the restore link, the cart is restored into the session and the recovery source is recorded; if they instead return directly and submit, the resulting order is NOT flagged as recovered.

## Scope

Covered:

- The `abandoned_remainder_interval` setting + its allowed values.
- What "abandoned" enables — recovery email, Messenger message, admin list, segment condition.
- Restore-link mechanics + `restore_source` capture (`email` / `messenger-bot`).
- The direct-resubmit edge case where `abandoned = 1` is NOT set.

Not covered here:

- Cart row lifecycle outside the abandoned window — see [[checkout-flow-cart-entity]].
- What runs on submit (the cart → order snapshot) — see [[checkout-flow-submit-order-creation]].
- The dedicated abandoned-cart admin screen — see [[orders-abandoned]].

## Contrasts

- **Eligible vs sent** — eligibility is triggered by `updated_at` age; whether the email actually goes out depends on the `abandoned_notification` plan-feature ([[plan-gates]]) AND the customer's marketing-consent state.
- **Recovered via restore link vs direct resubmit** — only the **restore-link handler** sets `abandoned = 1` on the cart (then copied to the order at submit) and records `restore_source`. A customer who returns directly to the site and submits the same cart produces a NORMAL order with `abandoned = 0` and no Recovered banner.

## Where it applies

The abandoned threshold is checked by a background sweep (verify queue name) plus on every cart write:

- The cart is eligible for the customer-facing **recovery email** (when the `abandoned_notification` plan-feature is enabled — see [[plan-gates]]) and / or **Messenger bot** message (when the Messenger app is connected).
- The cart appears on the [[orders-abandoned]] admin screen and in the [[analytics-abandoned-carts]] / [[analytics-abandoned-checkout]] dashboards.
- A *Begin order* segment condition fires on this same threshold — see [[marketing-segments]].

### The `abandoned_remainder_interval` setting

| Setting | Location | Allowed values | Default |
|---|---|---|---|
| `abandoned_remainder_interval` | [[settings-cart]] | 30 / 45 / 60 / 90 / 180 minutes | 60 minutes |

The interval is a single store-wide value — not per-customer, not per-product, not per-payment-method.

### Restore-link flow

1. Recovery email contains the restore link (a signed URL pointing at the cart row).
2. Customer clicks → the restore handler loads the cart into the visitor's session, sets `abandoned = 1` on the cart row, and writes `restore_source = email` (or `messenger-bot` for the bot variant).
3. Customer continues from where they left off — items + selected shipping/payment intact.
4. On submit, the cart's `abandoned` flag + `restore_source` are copied to the new Order row, which is what surfaces the "Recovered" banner + analytics attribution.

### Direct-resubmit edge case

When the customer leaves an abandoned cart, the recovery email is sent (or never fires due to consent), then the customer eventually returns and submits the cart directly — without clicking the restore link — the resulting order is **NOT** flagged `abandoned = 1`. The flag is set on the cart ONLY by the restore-link handler. So a direct submission produces a normal order with `abandoned = 0`, no `restore_source` metadata, and no Recovered banner. This is the most common source of "we sent the email but the recovery isn't attributed" support tickets.

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-cart-entity]] — the `updated_at` field that drives the threshold + auto-touch behaviour.
- [[checkout-flow-events-and-webhooks]] — `cart.created` / `cart.updated` webhooks that fire during the abandoned window.
- [[orders-abandoned]] — admin list of abandoned carts + recovery configuration.
- [[settings-cart]] — `abandoned_remainder_interval` setting.
- [[plan-gates]] — `abandoned_notification` plan-feature gate.
- [[marketing-segments]] — *Begin order* segment condition.
- [[analytics-abandoned-carts]] / [[analytics-abandoned-checkout]] — dashboards.
- [[storefront-known-issues]] — the merchant-perspective version of the direct-resubmit gotcha.

## Open Questions

- Confirm the queue / cron name used to dispatch the abandoned-cart sweep (verify).
- Confirm whether `restore_source` accepts values beyond `email` and `messenger-bot` (e.g. SMS variants) (verify).
