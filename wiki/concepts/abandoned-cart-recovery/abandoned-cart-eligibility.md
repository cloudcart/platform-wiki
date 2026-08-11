---
type: concept
nav_path: "Concept → Abandoned cart recovery → Eligibility & consent"
aliases: ["Abandoned cart eligibility", "Seven-check filter", "Recovery eligibility", "Two-layer marketing consent", "whereAbandoned scope", "Identified subscriber check"]
tags: [orders, cart, abandoned, recovery, eligibility, consent, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, restore link, channels, bulk send, attribution, plan quota).

# Abandoned cart — eligibility & consent gate

## Definition

Even when a cart has crossed the abandonment threshold (see [[abandoned-cart-threshold]]), the platform applies a **seven-check eligibility filter** plus a **two-layer marketing consent gate** before any restore link is actually dispatched. Both the automated sweep AND the manual bulk **Send restore link** action on [[orders-abandoned]] run through the same filter. A cart that fails any check is skipped (auto-sweep) or silently deleted from the list (bulk action — see [[abandoned-cart-bulk-send]] for the per-path failure handling).

## Scope

Covered:

- The seven runtime eligibility checks the platform applies to every cart pre-send.
- The two-layer marketing consent gate (Customer-level + Email-channel — same as [[subscriber-vs-customer]]).
- The identified-subscriber-before-cart-update rule (cross-customer-leak guard).
- The `unconfirmed_send` interaction for subscriber-only recipients.
- Silent-failure semantics — why merchants don't see per-cart error messages.

Not covered here:

- The threshold and sweep cadence — see [[abandoned-cart-threshold]].
- The restore-link URL and click handler — see [[abandoned-cart-restore-link]].
- Bulk-send vs auto-sweep failure paths — see [[abandoned-cart-bulk-send]].

## Contrasts

- **Eligibility filter vs marketing consent** — the seven-check filter is a *plumbing* check (does this cart have an identifiable recipient with a non-expired token?). The two-layer consent is a *permission* check (did the customer agree to marketing on the Customer record AND on the Email channel?). Failing either suppresses the send.
- **Anonymous guest vs identified subscriber** — only carts with a logged-in customer (`user_id`) OR an identified email subscriber (`subscriber_id`) ever qualify. Fully anonymous carts (no captured email anywhere) are excluded from the list entirely.
- **Customer-owned cart vs Subscriber-owned cart** — customer-owned carts only need the Customer-level `marketing` flag + standard Email-channel deliverability flags. Subscriber-owned carts additionally need email verification IF the Email channel's `unconfirmed_send` setting is OFF (the default).

## Where it applies

### The seven-check eligibility filter

Before any restore link is sent (auto-sweep or manual bulk action), the cart must pass **ALL** of these:

1. **Has line items** — the cart contains at least one product.
2. **Identifiable recipient** — the cart has either a logged-in customer (`user_id`) OR an identified email subscriber (`subscriber_id`). Fully anonymous guests with no captured email are excluded.
3. **Non-empty email** — the customer's / subscriber's email is set.
4. **Valid cart token (`key`)** — the cart still has its session-token; expired tokens disqualify.
5. **No order placed against this cart yet** — `order.cart_id` doesn't reference this cart.
6. **No prior order's metadata references this cart** — guards against duplicate recovery on already-recovered carts.
7. **Cart is not soft-deleted** — the merchant hasn't already deleted it from the list.

A cart that fails any check is excluded from the abandoned list AND from auto-sweep sends AND from manual bulk sends. See [[abandoned-cart-bulk-send]] for the silent-delete behaviour on the bulk path.

### Two-layer marketing consent (per [[subscriber-vs-customer]])

For the recovery EMAIL specifically (Messenger has its own consent model — see [[abandoned-cart-channels]]), the platform additionally checks:

1. **Customer-level `marketing` flag** — if the cart's customer has `marketing = no`, the recovery email is suppressed.
2. **Email-channel `marketing` flag** — the linked subscriber's Email channel must have `marketing = yes`.

Plus the standard Email-channel deliverability flags:

- `unsubscribed = no`
- `bounced = no`
- `verified = yes` *if the Email channel's `unconfirmed_send` setting is OFF (the default — see [[marketing-channels-email]]).*

Any one of these failing skips the send silently. The cart remains in [[orders-abandoned]] with `date_sent = NULL`.

### Subscriber-owned carts — identification timing

For carts owned by a subscriber (not a logged-in customer), the platform checks that the subscriber's email-channel record was **identified BEFORE the cart's last update** — i.e., the subscriber-channel `identified_at` must be earlier than the cart's `updated_at` (or NULL). This blocks the cross-customer-leak scenario where two visitors share a browser cookie / UUID and end up associated to the same subscriber row at different times: the cart that was last updated BEFORE the current subscriber was identified is excluded from recovery, so the wrong person doesn't receive someone else's cart restore link. (verify)

### Why merchants don't see per-cart error messages

The eligibility and consent gates fail **silently**:

- **Auto-sweep** — the cart simply isn't processed this tick. No log surface to the merchant.
- **Manual bulk send** — carts that fail are deleted from the list; merchant sees only the aggregate "X emails sent" toast.
- **Manual single-cart Send** — this path explicitly throws the platform code ONLY on plan-quota exhaustion. Eligibility failures still happen silently.

So a merchant investigating "why didn't this cart get a recovery email?" has to manually verify each check against the cart's details before clicking Send. See [[abandoned-cart-bulk-send]] for the per-path failure UX.

### Example: Customer didn't tick marketing consent

1. Customer adds items, fills email on the shipping address step (creating a Subscriber with `subscriber_from = order_creating`), then leaves without checking out.
2. Subscriber row was auto-created. Email channel `marketing = no` (customer didn't tick the consent box).
3. Cart goes abandoned. The seven-check eligibility filter passes (has items, has identifiable subscriber, has email, valid token, no order, not soft-deleted).
4. **But the two-layer consent check fails** — Email-channel `marketing = no` blocks the send.
5. The recovery email is suppressed silently. The cart remains in [[orders-abandoned]] but `date_sent` stays NULL.
6. The merchant clicks Send restore link in bulk on this cart — but the same two-layer check applies, and the cart is deleted from the list without a clear reason (see [[abandoned-cart-bulk-send]]).

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-threshold]] — what brings the cart to eligibility-check time in the first place.
- [[abandoned-cart-restore-link]] — what happens on the send path after eligibility passes.
- [[abandoned-cart-channels]] — Messenger channel has its own consent model.
- [[abandoned-cart-bulk-send]] — silent-delete behaviour on eligibility failure during bulk send.
- [[subscriber-vs-customer]] — the canonical reference for the two-layer marketing consent model.
- [[marketing-channels-email]] — the Email channel deliverability flags (`marketing`, `unsubscribed`, `bounced`, `verified`, `unconfirmed_send`).
- [[cart]] — the cart entity carrying `key`, `user_id`, `subscriber_id`, `updated_at`.
- [[customer]] — recipient when the cart belongs to a registered customer.
- [[subscriber]] — recipient when the cart belongs to an identified email subscriber.
- [[orders-abandoned]] — the list driven by `whereAbandoned` (threshold + eligibility filter applied at query time).

## Open Questions

None.
