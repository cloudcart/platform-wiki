---
type: concept
nav_path: "Concept → Abandoned cart recovery → Channels (email vs Messenger)"
aliases: ["Abandoned cart channels", "Email channel recovery", "Messenger channel recovery", "Facebook Messenger Bot recovery", "restore_source email", "restore_source messenger", "Facebook 24-hour window"]
tags: [orders, cart, abandoned, recovery, channels, email, messenger, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, eligibility, restore link, bulk send, attribution, plan quota).

# Abandoned cart — channels (Email vs Messenger)

## Definition

Cart recovery is a **two-channel pipeline** — **Email** (the default, sent through the platform's notification mailer; for a guest cart gated on the subscriber's [[marketing-channels-email|Email channel]] consent flags, for a registered customer's cart not consent-checked) and **Facebook Messenger** (via the Facebook Messenger Bot app integration). SMS, push, and other channels are NOT supported for cart recovery. Both channels share the same eligibility rules (see [[abandoned-cart-eligibility]]) and the same restore-link URL format (see [[abandoned-cart-restore-link]]) — what differs is the **delivery medium** and the value stored as **`restore_source`** on the recovered order (`email` or `messenger`).

In the **current production code**, only the **email** source is actively defined as a recovery source; the Messenger picker in [[settings-cart]] is hidden in the current UI. The Messenger pipeline is **paused** (source present but commented out) — likely a roadmap question, not a current-behaviour question. Recovered orders carrying `restore_source = messenger` would be historical records from a previous integration period.

## Scope

Covered:

- The two delivery channels (Email, Messenger) and what differs between them.
- The shared restore-link URL format and the per-channel `restore_source` value on the recovered order.
- The Email channel's consent + deliverability flags (guest carts only).
- The Messenger channel's consent model (customer must have engaged the bot).
- Facebook's 24-hour window — a third-party platform policy that blocks business-initiated messages outside it.
- Current paused-Messenger state in code + UI.

Not covered here:

- Email channel installation, DKIM / SPF / DMARC, sender reputation — see [[marketing-channels-email]].
- The Messenger app installation — see the Apps section.
- The two-layer consent gate generic semantics — see [[subscriber-vs-customer]] and [[abandoned-cart-eligibility]].

## Contrasts

- **Email vs Messenger** — same restore-link URL, same eligibility filter, different delivery medium, different `restore_source` tag on the recovered order. Email is the production-active path today; Messenger is paused in current code.
- **Recovery email vs marketing-campaign email** — recovery email is **one specific cart's restore link**, not a broadcast, and it goes out as promotional mail. Campaigns target a segment of [[subscriber|Subscribers]]; recovery targets the cart's specific customer or subscriber. For a guest cart it still checks the Email channel's marketing consent; a registered customer's cart is not consent-checked.
- **Platform consent (CloudCart) vs Facebook consent (Messenger Platform)** — even when CloudCart's checks all pass for Messenger, Facebook's Messenger Platform policy independently enforces the 24-hour business-message window. If the customer hasn't engaged the bot in over 24 hours, Facebook blocks the send at the API level.

## Where it applies

### Email channel (the default, production-active)

- **Sent through** the platform's notification mailer, like every other [[marketing-omnichannel-mails-list|Email notification]]: the store's own SMTP app when it is active and fully set up, otherwise CloudCart's shared sending account. It does **not** go through the store's Email marketing channel or its sub-account, so a broken or unconfigured Email channel does not stop it. The Email channel's subscriber flags still decide who receives it (next bullet).
- **Subject + body** are merchant-customisable via the [[marketing-omnichannel-mails-list|Email notifications]] template editor.
- **Consent / deliverability** — a registered customer's cart: none checked. A guest cart: the subscriber's Email-channel address needs `marketing = yes`, `unsubscribed = no`, `bounced = no`, and `verified = yes` (unless the channel's `unconfirmed_send` is ON). See [[abandoned-cart-eligibility]].
- **Promotional at the sending service** — mail sent through the platform's Elastic Email transport is transactional unless marked promotional, and restore links (`abandoned_restore_link`) are marked, as are bulk customer e-mails from the Admin GraphQL `sendCustomerEmail` mutation, whichever `type` the request names. Elastic Email adds its own unsubscribe link and does not send to contacts who unsubscribed through it. Order, invoice, billing and security e-mails still reach them. That unsubscribe stays with the sending service and does not change the marketing flags in the admin. A store sending by its own SMTP is outside this.
- **`restore_source` on the recovered order** — `email`.
- **Banner on [[orders-history]]** — *"Order was recovered through email"*.

### Messenger channel (Facebook Messenger Bot — currently paused)

- **Requires** the Facebook Messenger Bot app to be installed and connected to the store's Facebook Page.
- **Customer prerequisite** — the customer must have **previously engaged the bot**. Without prior engagement, Messenger's platform policy blocks the send.
- **`restore_source` on the recovered order** — `messenger`.
- **Banner on [[orders-history]]** — *"Order was recovered through messenger"*.
- **Current UI state** — the channel picker in [[settings-cart]] hides Messenger from the dropdown; only `email` is selectable. Messenger options are present in source but commented out. (verify) Whether the channel returns is a roadmap question, not a current-behaviour question.

### Facebook 24-hour window (third-party policy)

When Messenger IS active, **Facebook's Messenger Platform policy** restricts business-initiated messages to customers who have interacted with the page bot within the previous 24 hours.

- **Trigger** — the customer must have sent a message to the bot (or clicked an in-bot button) within the last 24 hours.
- **Behaviour outside the window** — Facebook blocks the send at the API level. The cart stays in the abandoned list, no recovery message reaches the customer, and the merchant sees **no per-cart error**.
- **Enforced by Facebook, not by CloudCart**. CloudCart doesn't pre-check the 24-hour window — it dispatches the message and absorbs the Facebook-side failure silently.
- **Customer bot-unsubscribe** — if the customer has unsubscribed from the bot, Facebook also blocks the send. Same silent-failure behaviour.

This means Messenger recovery, even when re-enabled, has a much narrower delivery window than Email and a much higher silent-failure rate.

### Picking the channel (when Messenger is active)

When the merchant has both channels available, the channel picker on [[settings-cart]] decides which is used for the automated sweep. Manual bulk send on [[orders-abandoned]] (see [[abandoned-cart-bulk-send]]) uses the same configured channel.

In the current paused state, the picker offers only Email, so the question is moot.

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-eligibility]] — shared eligibility filter and consent gate for both channels.
- [[abandoned-cart-restore-link]] — the shared URL format; only the `{source}` segment differs between channels.
- [[abandoned-cart-attribution]] — how `restore_source` surfaces on the recovered order and on [[orders-history]].
- [[abandoned-cart-bulk-send]] — bulk send uses whichever channel is configured.
- [[marketing-channels-email]] — the Email channel whose subscriber consent flags gate Email recovery (it does not carry the send).
- [[marketing-omnichannel-mails-list]] — Email notifications template editor (where merchants customise the recovery email body).
- [[settings-cart]] — channel picker and master switch live here.
- [[subscriber-vs-customer]] — the consent layers; the Email path reads only the Email-channel layer, for guest carts.
- [[notification-delivery]] — the platform's event → queued-job pattern that drives the actual email dispatch.

## Open Questions

- When (if ever) is the Messenger channel scheduled to come back into production? — current code path is commented out; treat as roadmap, not current behaviour. (verify against product roadmap)
