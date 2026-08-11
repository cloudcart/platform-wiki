---
type: concept
nav_path: "Concept → Abandoned cart recovery → Channels (email vs Messenger)"
aliases: ["Abandoned cart channels", "Email channel recovery", "Messenger channel recovery", "Facebook Messenger Bot recovery", "restore_source email", "restore_source messenger", "Facebook 24-hour window"]
tags: [orders, cart, abandoned, recovery, channels, email, messenger, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, eligibility, restore link, bulk send, attribution, plan quota).

# Abandoned cart — channels (Email vs Messenger)

## Definition

Cart recovery is a **two-channel pipeline** — **Email** (the default, powered by the merchant's [[marketing-channels-email|Email channel]]) and **Facebook Messenger** (via the Facebook Messenger Bot app integration). SMS, push, and other channels are NOT supported for cart recovery. Both channels share the same eligibility rules (see [[abandoned-cart-eligibility]]) and the same restore-link URL format (see [[abandoned-cart-restore-link]]) — what differs is the **delivery medium** and the value stored as **`restore_source`** on the recovered order (`email` or `messenger`).

In the **current production code**, only the **email** source is actively defined as a recovery source; the Messenger picker in [[settings-cart]] is hidden in the current UI. The Messenger pipeline is **paused** (source present but commented out) — likely a roadmap question, not a current-behaviour question. Recovered orders carrying `restore_source = messenger` would be historical records from a previous integration period.

## Scope

Covered:

- The two delivery channels (Email, Messenger) and what differs between them.
- The shared restore-link URL format and the per-channel `restore_source` value on the recovered order.
- The Email channel's two-layer marketing consent + deliverability flags.
- The Messenger channel's consent model (customer must have engaged the bot).
- Facebook's 24-hour window — a third-party platform policy that blocks business-initiated messages outside it.
- Current paused-Messenger state in code + UI.

Not covered here:

- Email channel installation, DKIM / SPF / DMARC, sender reputation — see [[marketing-channels-email]].
- The Messenger app installation — see the Apps section.
- The two-layer consent gate generic semantics — see [[subscriber-vs-customer]] and [[abandoned-cart-eligibility]].

## Contrasts

- **Email vs Messenger** — same restore-link URL, same eligibility filter, different delivery medium, different `restore_source` tag on the recovered order. Email is the production-active path today; Messenger is paused in current code.
- **Recovery email vs marketing-campaign email** — recovery email is **transactional-flavoured marketing** — one specific cart's restore link, not a broadcast. Campaigns target a segment of [[subscriber|Subscribers]]; recovery targets the cart's specific customer or subscriber. Recovery still respects the two-layer marketing consent.
- **Platform consent (CloudCart) vs Facebook consent (Messenger Platform)** — even when CloudCart's checks all pass for Messenger, Facebook's Messenger Platform policy independently enforces the 24-hour business-message window. If the customer hasn't engaged the bot in over 24 hours, Facebook blocks the send at the API level.

## Where it applies

### Email channel (the default, production-active)

- **Powered by** the merchant's [[marketing-channels-email|Email channel]] (Elastic Email sub-account).
- **Subject + body** are merchant-customisable via the [[marketing-omnichannel-mails-list|Email notifications]] template editor.
- **Consent / deliverability** — respects the two-layer marketing consent (Customer + Email-channel) per [[subscriber-vs-customer]], plus `unsubscribed = no`, `bounced = no`, and `verified = yes` (unless the channel's `unconfirmed_send` is ON).
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
- [[marketing-channels-email]] — the Email channel powering Email recovery.
- [[marketing-omnichannel-mails-list]] — Email notifications template editor (where merchants customise the recovery email body).
- [[settings-cart]] — channel picker and master switch live here.
- [[subscriber-vs-customer]] — two-layer marketing consent referenced by the Email path.
- [[notification-delivery]] — the platform's event → queued-job pattern that drives the actual email dispatch.

## Open Questions

- When (if ever) is the Messenger channel scheduled to come back into production? — current code path is commented out; treat as roadmap, not current behaviour. (verify against product roadmap)
