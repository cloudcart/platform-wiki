---
type: concept
nav_path: "Concept → Abandoned cart recovery"
route_name: (none)
route_path: (none)
aliases: ["Abandoned cart recovery", "Cart recovery", "Cart recovery flow", "Abandoned cart pipeline", "Restore link", "Restore link flow", "Send restore link", "Cart restoration", "Recovery email", "Abandoned cart email", "Възстановяване на изоставена количка", "Изоставена количка", "Имейл за изоставена количка", "Линк за възстановяване"]
tags: [orders, cart, abandoned, recovery, marketing, concepts]
plan_gates: ["abandoned_notification"]
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Abandoned cart recovery

## Definition

**Abandoned cart recovery** is the end-to-end flow CloudCart uses to bring back customers who added products to their cart, sat idle past a configurable timer, but never placed an order. The merchant has two trigger paths — an **automated reminder** that fires after the timer expires (driven by an every-3-minute platform sweep), and a **manual bulk Send restore link** action on [[orders-abandoned]] to nudge specific carts on demand. Both paths produce the same outcome: a recovery message containing a unique restore-link URL goes to the customer's email (or Facebook Messenger inbox), the customer clicks the link, the cart contents are restored into a fresh checkout session, and the customer either completes the purchase (producing an order tagged `abandoned = 1` + `restore_source`) or drops off (the cart eventually ages out).

Recovery is a **two-channel** pipeline — **email** (the default, powered by the merchant's [[marketing-channels-email|Email channel]]) and **Facebook Messenger** (currently paused in code; see [[abandoned-cart-channels]]). SMS, push, and other channels are NOT supported. Both channels share the same eligibility filter, the same per-period `abandoned_notification` plan-feature quota, and the same restore-link URL format — what differs is the delivery medium and the value stored as `restore_source` on the recovered order (`email` / `messenger`).

The single most-misunderstood detail: **the "abandoned" state is inferred, not stored.** `AbandonedCart` is an alias model extending `Cart`; the same cart row alternates between Active and Abandoned by virtue of `updated_at`'s age against the `abandoned_remainder_interval` threshold. See [[abandoned-cart-threshold]].

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[abandoned-cart-threshold]] — the `abandoned_remainder` master switch + `abandoned_remainder_interval` timer (default 60 min, options 30 / 45 / 60 / 90 / 180); the every-3-minute platform sweep; what resets `updated_at`; the up-to-3-min latency.
- [[abandoned-cart-eligibility]] — the seven-check eligibility filter applied per cart; the two-layer marketing consent (Customer + Email-channel); the subscriber-`identified_at`-before-cart-`updated_at` cross-leak guard; silent-failure semantics.
- [[abandoned-cart-restore-link]] — the `/restore-abandoned/{code}/{source}/{discount_code?}` URL anatomy; the click handler's merge-into-active-session-cart behaviour; guest vs logged-in address carryover; the "original cart not deleted on restore" detail.
- [[abandoned-cart-channels]] — Email vs Messenger; same URL, different `restore_source`; the Facebook 24-hour window; current paused-Messenger state in code.
- [[abandoned-cart-bulk-send]] — the manual bulk Send action on [[orders-abandoned]]; per-path failure UX (silent-delete on bulk vs hard paywall on single-cart vs silent-skip on auto-sweep); the commented-out re-send guard.
- [[abandoned-cart-attribution]] — `abandoned = 1`, `restore_source`, `cart_id`, `campaign_id` on the recovered order; banner on [[orders-history]]; Recovered source filter on [[orders]]; direct-resubmit edge case (not tagged).
- [[abandoned-cart-plan-quota]] — `abandoned_notification` plan feature; `plan.count.email.abandoned_notification` Setting-row counter; period rollover behaviour; shared meter with third-party recovery integrations.

## Scope

What this concept covers (across the 7 sub-pages):

- The threshold + sweep cadence that detects abandonments.
- The per-cart eligibility filter + two-layer marketing consent gate.
- The restore-link URL format and click-handler behaviour.
- The Email vs Messenger channel split (Messenger currently paused).
- The merchant's three send paths (auto-sweep, manual bulk, manual single-cart) and their failure UX.
- The recovered order's attribution fields and merchant-visible surfaces.
- The `abandoned_notification` plan-feature quota.

What it does NOT cover:

- The Cart entity's full lifecycle (Active / Abandoned / Recovered / Converted / Lost) — see [[cart-vs-order-lifecycle]].
- The cross-entity Cart → Order journey — see [[checkout-flow]].
- Email channel installation, DKIM / SPF / DMARC, sender reputation — see [[marketing-channels-email]].
- The Messenger app installation flow — see the Apps section.
- Manual order creation that bypasses the cart entirely — see [[orders-add]].
- Marketing-campaign broadcasts (campaigns target Subscribers; recovery targets the cart's specific recipient) — see [[marketing-campaigns]].

## Contrasts

- **Recovery vs abandoned cart** — an abandoned cart is just a Cart whose `updated_at` crossed the threshold; recovery is the platform's attempt to bring the customer back. Carts can be abandoned without ever being recovered.
- **Automated reminder vs manual Send restore link** — the auto-sweep fires once per cart (filters `date_sent IS NULL`); the manual bulk action permits re-sends. See [[abandoned-cart-bulk-send]].
- **Email vs Messenger channel** — see [[abandoned-cart-channels]].
- **Recovered order vs normal order** — identical workflow; only the `abandoned = 1` + `restore_source` flags differ. See [[abandoned-cart-attribution]].
- **Recovery vs retargeting** — recovery is CloudCart's first-party mechanism via email / Messenger; retargeting (Facebook / Google Ads) is third-party advertising and doesn't use the restore-link infrastructure.
- **Recovery path vs full cart-vs-order lifecycle** — this concept covers the recovery PATH (timer, send, restore, attribution); [[cart-vs-order-lifecycle]] covers the full state machines with recovery as one transition.

## Where it applies

- **Merchant surfaces** — [[orders-abandoned]] (the list + bulk Send action), [[settings-cart]] (master switch + timer + channel picker), [[orders]] (Recovered source filter), [[orders-history]] (recovery banner).
- **Analytics** — [[analytics-abandoned-carts]] (trend dashboard), [[analytics-abandoned-checkout]] (checkout-funnel drop-off).
- **Marketing / consent** — [[marketing-channels-email]] (Email channel must be installed + verified), [[subscriber-vs-customer]] (two-layer consent gating the recovery email).
- **Plan gating** — [[plan-gates]] (`abandoned_notification` feature governs whether the flow runs at all).
- **Entities** — [[cart]] (transitions to abandoned, carries the recovery `key` token), [[order]] (created with `abandoned = 1` on recovery), [[customer]] / [[subscriber]] (the recipient is one of these).

## Related

- [[orders-abandoned]] — abandoned-cart list with the Send restore link bulk action.
- [[settings-cart]] — `abandoned_remainder`, `abandoned_remainder_interval`, channel picker.
- [[cart]] — the cart entity that gets recovered.
- [[order]] — the order entity created on successful recovery.
- [[customer]] — the recipient when the cart belongs to a registered customer.
- [[subscriber]] — the recipient when the cart belongs to an identified email subscriber.
- [[cart-vs-order-lifecycle]] — the full Cart and Order state machines, of which recovery is one transition.
- [[checkout-flow]] — the cross-entity journey the customer re-enters after restore.
- [[subscriber-vs-customer]] — the two-layer marketing consent that gates the recovery email.
- [[marketing-channels-email]] — the Email channel that delivers the recovery email.
- [[marketing-omnichannel-mails-list]] — Email notifications template editor (recovery email body).
- [[notification-delivery]] — the platform's event → queued-job pattern that drives the email dispatch.
- [[orders]] — placed-orders list with the Recovered source filter.
- [[orders-history]] — per-order audit log with the recovery banner.
- [[order-status-workflow]] — the normal order-status lifecycle the recovered order runs through.
- [[order-processing-pipeline]] — the full status-transition pipeline that handles the recovered order from `pending` onward.
- [[marketing-discounts]] — discount codes that can be attached to the restore link as a recovery incentive.
- [[plan-gates]] — `abandoned_notification` plan feature that gates the flow.
- [[plan-features]] — paywall screen for purchasing more `abandoned_notification` quota.
- [[analytics-abandoned-carts]] — abandoned-cart trend analytics.
- [[analytics-abandoned-checkout]] — checkout-funnel drop-off analytics.
- [[background-queue-inventory]] — catalogue of background processes including the every-3-min sweep.

## Open Questions

No outstanding questions at the hub level. Per-aspect open questions live on the relevant sub-pages.
