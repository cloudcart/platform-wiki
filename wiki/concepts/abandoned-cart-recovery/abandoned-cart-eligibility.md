---
type: concept
nav_path: "Concept → Abandoned cart recovery → Eligibility & consent"
aliases: ["Abandoned cart eligibility", "Seven-check filter", "Recovery eligibility", "Two-layer marketing consent", "whereAbandoned scope", "Identified subscriber check"]
tags: [orders, cart, abandoned, recovery, eligibility, consent, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, restore link, channels, bulk send, attribution, plan quota).

# Abandoned cart — eligibility & consent gate

## Definition

Even when a cart has crossed the abandonment threshold (see [[abandoned-cart-threshold]]), the platform applies a **seven-check eligibility filter**, plus a **consent check on guest carts only**, before any restore link is actually dispatched. Both the automated sweep AND the manual bulk **Send restore link** action on [[orders-abandoned]] run through the same filter. A cart that fails any check is skipped (auto-sweep) or silently deleted from the list (bulk action — see [[abandoned-cart-bulk-send]] for the per-path failure handling).

## Scope

Covered:

- The seven runtime eligibility checks the platform applies to every cart pre-send.
- The consent check, made only for guest (subscriber) carts, never for a registered customer's cart.
- The identified-subscriber-before-cart-update rule (cross-customer-leak guard).
- The `unconfirmed_send` interaction for subscriber-only recipients.
- Silent-failure semantics — why merchants don't see per-cart error messages.

Not covered here:

- The threshold and sweep cadence — see [[abandoned-cart-threshold]].
- The restore-link URL and click handler — see [[abandoned-cart-restore-link]].
- Bulk-send vs auto-sweep failure paths — see [[abandoned-cart-bulk-send]].

## Contrasts

- **Eligibility filter vs marketing consent** — the seven-check filter is a *plumbing* check (does this cart have an identifiable recipient with a non-expired token?). The consent check is a *permission* check, made only for a guest cart: does the subscriber's Email channel accept marketing?
- **Anonymous guest vs identified subscriber** — only carts with a logged-in customer (`user_id`) OR an identified email subscriber (`subscriber_id`) ever qualify. Fully anonymous carts (no captured email anywhere) are excluded from the list entirely.
- **Customer-owned cart vs Subscriber-owned cart** — a registered customer's cart goes to the account's email with no consent or Email-channel check. A guest cart needs an Email-channel address that accepts marketing, is not unsubscribed or bounced, and is verified unless the Email channel's `unconfirmed_send` setting is ON (default OFF).

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

Wallet top-up and gift card carts are never tracked ([[wallet-gift-instrument-checkout]]). A cart that fails any check is excluded from the abandoned list AND from auto-sweep sends AND from manual bulk sends. See [[abandoned-cart-bulk-send]] for the silent-delete behaviour on the bulk path.

### Consent check — guest carts only

For the recovery EMAIL (Messenger has its own model — see [[abandoned-cart-channels]]):

- **Registered customer's cart** — **no consent check**. The reminder goes to the account's email whatever the customer's marketing flag or Email-channel flags say.
- **Guest (subscriber) cart** — the subscriber needs an Email-channel address with `marketing = yes`, `unsubscribed = no`, `bounced = no`, and `verified = yes` unless the Email channel's `unconfirmed_send` is ON ([[email-channel-settings-pane]]). Without such an address no reminder is sent, and a cart whose address lacks marketing consent is dropped from the list when the send runs.

At the sending service the reminder goes out as promotional: Elastic Email adds its own unsubscribe link and skips addresses that unsubscribed through it ([[abandoned-cart-channels]]).

### Subscriber-owned carts — identification timing

For carts owned by a subscriber (not a logged-in customer), the platform checks that the subscriber's email-channel record was **identified BEFORE the cart's last update** — i.e., the subscriber-channel `identified_at` must be earlier than the cart's `updated_at` (or NULL). This blocks the cross-customer-leak scenario where two visitors share a browser cookie / UUID and end up associated to the same subscriber row at different times: the cart that was last updated BEFORE the current subscriber was identified is excluded from recovery, so the wrong person doesn't receive someone else's cart restore link. (verify)

### Why merchants don't see per-cart error messages

The eligibility and consent gates fail **silently**:

- **Auto-sweep** — the cart simply isn't processed this tick. No log surface to the merchant.
- **Manual bulk send** — carts that fail are deleted from the list; merchant sees only the aggregate "X emails sent" toast.
- **Manual single-cart Send** — this path explicitly throws a a plan-restriction error ONLY on plan-quota exhaustion. Eligibility failures still happen silently.

So a merchant investigating "why didn't this cart get a recovery email?" has to manually verify each check against the cart's details before clicking Send. See [[abandoned-cart-bulk-send]] for the per-path failure UX.

### Example: Customer didn't tick marketing consent

1. Customer adds items, fills email on the shipping address step (creating a Subscriber with `subscriber_from = order_creating`), then leaves without checking out.
2. Subscriber row was auto-created. Email channel `marketing = no` (customer didn't tick the consent box).
3. Cart goes abandoned. The seven-check eligibility filter passes (has items, has identifiable subscriber, has email, valid token, no order, not soft-deleted).
4. **But the consent check fails** — the guest's Email channel has `marketing = no`.
5. When the send runs (sweep or **Send restore link**), the cart gets no email and is dropped from [[orders-abandoned]].
6. Had the visitor been signed in as a registered customer, the reminder would have gone out: a registered customer's cart is not consent-checked.

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-threshold]] — what brings the cart to eligibility-check time in the first place.
- [[abandoned-cart-restore-link]] — what happens on the send path after eligibility passes.
- [[abandoned-cart-channels]] — Messenger channel has its own consent model.
- [[abandoned-cart-bulk-send]] — silent-delete behaviour on eligibility failure during bulk send.
- [[subscriber-vs-customer]] — the two consent layers; only the Email-channel layer is read here, and only for guest carts.
- [[marketing-channels-email]] — the Email channel deliverability flags (`marketing`, `unsubscribed`, `bounced`, `verified`, `unconfirmed_send`).
- [[email-channel-settings-pane]] — the `unconfirmed_send` switch.
- [[cart]] — the cart entity carrying `key`, `user_id`, `subscriber_id`, `updated_at`.
- [[customer]] — recipient when the cart belongs to a registered customer.
- [[subscriber]] — recipient when the cart belongs to an identified email subscriber.
- [[orders-abandoned]] — the list driven by `whereAbandoned` (threshold + eligibility filter applied at query time).

## Open Questions

None.
