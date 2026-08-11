---
type: concept
nav_path: "Concept → Cart vs Order lifecycle → Cart abandonment"
aliases: ["Cart abandonment", "Abandoned cart eligibility", "Abandoned remainder interval", "Abandoned threshold", "abandoned_remainder_interval", "Abandoned-cart sweep", "Abandoned notification quota", "Изоставена количка", "Праг за изоставена количка"]
tags: [cart, order, lifecycle, abandonment, concepts]
plan_gates: ["abandoned_notification"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[cart-vs-order-lifecycle]]. See the hub for the other aspects (cart state machine, order state machine, handoff, restore).

# Cart abandonment

## Definition

A cart is **abandoned** when it crossed the configured **abandoned threshold** (`abandoned_remainder_interval` on [[settings-cart]]; default 60 min; options 30 / 45 / 60 / 90 / 180), still has at least one line item, has an identifiable customer or subscriber, and no order has been placed against it yet. Abandoned carts show up in [[orders-abandoned]] and become eligible for the recovery email (which the merchant sends manually — see [[cart-restore]] for the restore-link mechanics).

The platform sweeps for newly-abandoned carts every **3 minutes** (180 seconds) on the system queue. The actual recovery email therefore fires after threshold + up to 3 min of sweep-delay. Abandonment is gated by a per-period plan quota (`abandoned_notification`) and by 7 distinct eligibility rules — when any fails, no abandoned-cart record is produced, which is the most-common reason a merchant complains "my abandoned cart email didn't fire".

## Scope

Covered:

- The 7-rule abandoned-cart eligibility check.
- The 3-minute sweep cadence + threshold + per-period plan quota.
- The `abandoned_remainder_interval` configuration on [[settings-cart]] (defaults + options).
- Why anonymous and UUID-tracked guests are excluded.
- What happens to a cart after the recovery email is sent (stays in [[orders-abandoned]] until merchant deletes; `date_sent` set; quota decrements).
- The Lost end-state for abandoned carts whose customers never return.
- Why draft orders ([[orders-add]] with `is_draft = 1`) never appear in [[orders-abandoned]] (no cart row).

Not covered here:

- The Cart entity data shape + the six cart states (Active / Abandoned / Recovered / Converted / Lost / Soft-deleted) — see [[cart-state-machine]].
- The restore-link click handler + `abandoned = 1` flag on the resulting order — see [[cart-restore]].
- Currency / locale freeze on the order produced from a recovered cart — see [[cart-to-order-handoff]].
- The full recovery-attribution analytics (Recovered source filter, conversion-rate reporting) — see [[orders-abandoned]] + [[analytics-abandoned-carts]].

## Contrasts

- **Abandoned vs Lost**: an Abandoned cart crossed the threshold AND has identifiable customer / subscriber — eligible for recovery. A Lost cart has been abandoned, recovery was attempted (or never qualified), and the cart aged out without conversion — eventually deleted.
- **Abandoned vs anonymous**: anonymous (guest, no email) carts NEVER become Abandoned — they have no contact channel. They sit in Active until aged out (Lost) without ever appearing in [[orders-abandoned]].
- **Abandoned cart vs analytics abandoned-cart**: the cart shows in [[orders-abandoned]] for the recovery workflow only when eligibility passes. The [[analytics-abandoned-carts]] / [[analytics-abandoned-checkout]] dashboards count broader funnel drop-off (including anonymous traffic), so the two numbers will not match.
- **Sweep vs threshold**: the threshold is when the cart QUALIFIES; the sweep is when the platform DETECTS it. Sweep runs every 3 min, so detection lags qualification by up to 3 min.
- **Per-period quota vs per-cart limit**: `abandoned_notification` is a **per-period plan-feature quota** (decrements on email send). There is no per-cart limit on how many recovery emails can be sent — the merchant chooses when to nudge, manually, per cart or bulk.

## Where it applies

**The 7 eligibility rules.** A cart qualifies for abandoned-cart recovery when ALL of these are true:

1. Cart has at least one line item.
2. Cart's `updated_at` is older than the configured `abandoned_remainder_interval` (default 60 min; configurable 30 / 45 / 60 / 90 / 180 min on [[settings-cart]]).
3. Either a logged-in customer is attached (`user_id`) OR an identified email subscriber exists (`subscriber_id`); guests with no email captured are excluded. See [[cart-state-machine]] for the identity-state table.
4. The customer / subscriber's email is non-empty.
5. No order has been placed against this cart yet.
6. The cart still has a valid `key` (restore token) — bot sentinel keys (see [[cart-state-machine]]) fail this check.
7. The cart is not soft-deleted.

When any rule fails, no abandoned-cart record is produced. This is the most-common reason a merchant complains "my abandoned cart email didn't fire" — they expected guest-cart recovery, or the customer's email subscription wasn't verified, or the cart was already converted, or the plan's per-period `abandoned_notification` quota is exhausted.

**The 3-minute sweep cadence.** The platform sweeps for newly-abandoned carts every **3 minutes** (180 seconds) on the system queue. The actual recovery email fires after the merchant's configured interval **plus up to 3 minutes** of sweep-delay. Note also that the cart's `updated_at` may have been refreshed by [[cart-state-machine|cart auto-touch]] — any page-view / AJAX cart load older than 10 minutes silently moves the timestamp forward, pushing the abandoned-cart trigger back by another full interval.

**When the email goes out.**

- The merchant's per-period `abandoned_notification` plan-feature quota decrements by 1.
- The cart's `date_sent` timestamp is set.
- The cart **remains** in [[orders-abandoned]] (not auto-removed) — the merchant uses bulk delete to clean.

The merchant manually triggers Send restore link from [[orders-abandoned]] per cart or bulk. The platform does NOT automatically re-send after time — the merchant decides when to nudge. See [[cart-restore]] for the customer-click handler.

**Lost — auto-cleanup end-state.** If the customer never returns, the cart eventually auto-cleans: the underlying cart-session expires and the cart row is removed by the [[cart-state-machine|7-day TTL cleanup]] (or by the post-Order soft-delete pass if a different cart eventually produced an order with this one's `cart_id` — n/a here since this cart never converted).

**Draft orders never appear in [[orders-abandoned]].** Admin-created orders with `is_draft = 1` ([[orders-add]]) bypass the cart entirely — no cart row is created for them, so they cannot appear in [[orders-abandoned]] (which scans cart rows). The `is_draft` order itself has a customer-facing checkout / payment URL; if the merchant shares that URL, the customer can complete payment from the storefront, and the normal post-creation pipeline runs (see [[cart-to-order-handoff]]) — but no abandoned-cart entry is ever produced.

**Worked example — abandons cart, recovers via email.**

1. Customer adds 2 items to cart on the storefront → cart row created. `updated_at = 10:00`.
2. Customer browses for 5 minutes, removes one item, adds another → `updated_at = 10:05`.
3. Customer closes the browser without checking out.
4. At 11:05 (60 min later), the platform's sweep job (running every 3 min) detects the cart as abandoned. Cart appears in [[orders-abandoned]].
5. Merchant goes to [[orders-abandoned]] → selects the cart → clicks **Send restore link**.
6. Restore-link email is queued and sent. Cart's `date_sent = 11:08`. `abandoned_notification` plan quota decrements by 1.
7. Customer clicks the link 30 minutes later — see [[cart-restore]] for what happens next.

## Related

- [[cart-vs-order-lifecycle]] — hub.
- [[cart-state-machine]] — the six cart states (Abandoned is one of them); identity-state eligibility; 10-minute auto-touch; 7-day TTL.
- [[cart-restore]] — what happens when the customer clicks the restore-link email.
- [[cart-to-order-handoff]] — `abandoned = 1` flag set only by restore-link handler.
- [[settings-cart]] — `abandoned_remainder_interval`, the entire pre-purchase configuration.
- [[orders-abandoned]] — abandoned-cart admin list + Send restore link / Delete bulk actions.
- [[analytics-abandoned-carts]] — abandoned-cart trends.
- [[analytics-abandoned-checkout]] — checkout funnel drop-off.
- [[plan-gates]] — `abandoned_notification` quota.
- [[subscriber-vs-customer]] — UUID-tracked anonymous visitors vs subscribers vs customers (why UUID-only carts are not eligible).
- [[abandoned-cart-recovery]] — the cross-cutting recovery concept page.
- [[orders-add]] — admin-side manual order creation (draft orders bypass abandonment).

## Open Questions

None.
