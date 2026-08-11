---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber → Message format"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber message format", "Viber Business Message structure", "Viber 1000 chars", "Viber image button", "Viber send request shape", "omni/1/advanced", "Verified business badge"]
tags: [marketing, channels, viber, message-format, infobip]
plan_gates: ["viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-viber]]. See the hub for the other aspects (settings, self-credentials, send pipeline, DLR, system messages, plan cap).

# Viber channel — Message format & customer-side rules

## Purpose

Documents the shape of a Viber Business Message — what fields the merchant fills in, what the customer sees, and what customer-side requirements must hold for delivery. Covers the InfoBip omni-channel send-request payload (so support can debug "why isn't the image showing?" tickets), the verified-business-badge rules, and the per-subscriber pre-flight check that decides whether the send even leaves the queue.

## Where to find it

The merchant authors message content via:

- The campaign editor's **"Viber message"** action — see [[marketing-campaigns]].
- The Viber system-messages editor — see [[viber-channel-system-messages]].

Validation happens at save time (template / campaign step) and again at send time (queue worker) — see [[viber-channel-send-pipeline]] for the runtime length check.

## What the merchant can do here

- Compose a Viber body up to 1000 characters.
- Optionally attach an image (URL).
- Optionally attach an action button (text + tappable URL).
- Optionally choose a sender name (default `"CloudCart"` for the shared sender; merchant's own brand for Self-credentials).

## Settings & fields

### Message validation rules

| Field | Validation |
|-------|------------|
| `internal_title` | `required\|string\|max:191` — merchant's reference label, not shown to the recipient. |
| `viber_message` | `required\|string\|max:1000` — the message body. |
| `imageURL` | Optional, must be a valid URL. |
| `buttonText` | Optional, sent only alongside `buttonURL`. |
| `buttonURL` | Optional, must be a valid URL. |

A Viber Business message looks materially different from an SMS in the customer's inbox:

- The sender shows as a **verified business** with a green checkmark badge — recipient trust is higher than for an SMS short code.
- The message can include an **image**, **a text body up to 1000 characters**, and **an action button** (text + tappable URL) — closer to an in-app push card than an SMS.
- If the recipient doesn't have Viber installed or has it switched off, the message **fails silently** (Viber is opt-in by definition; there is no SMS fallback unless the merchant builds one into the campaign).

### Send-request shape (InfoBip omni/1/advanced)

Each Viber send goes out as a POST to `{host}/omni/1/advanced` (InfoBip's omni-channel endpoint) with JSON body:

```
{
  "scenarioKey": "<service or promo key>",
  "bulkId": "<site_id>_<microtime>",
  "destinations": {
    "to": { "phoneNumber": "<E.164>" }
  },
  "viber": {
    "text": "<message body>",
    "imageURL": "<optional>",
    "buttonText": "<optional>",
    "buttonURL": "<optional>"
  }
}
```

Authentication is HTTP Basic Auth with the appropriate (service or promo) credentials — the choice is automatic per message based on the presence of `imageURL` / `buttonURL` (see [[viber-channel-send-pipeline]]).

The recipient's phone number is normalised to international format (E.164) before being placed in `destinations.to.phoneNumber`. The `bulkId` is per-send (`{site_id}_{microtime(true)}`) for per-store DLR reconciliation.

### Per-subscriber pre-flight check

For each Viber send, the platform checks the recipient's Phone channel row:

| Field | Required value |
|-------|----------------|
| `channel_identifier` | non-empty (phone number must exist on the subscriber). |
| `unsubscribed` | `0` |
| `marketing` | `1` |
| `verified` | `1` |
| `bounced` | `0` |

Plus: the **rendered** message text after placeholder substitution must be ≤ 1000 chars. Failure short-circuits the send with the failure recorded on the log row.

See [[marketing-subscribers]] for how Phone channel rows are managed, and [[viber-channel-send-pipeline]] for the runtime length check.

## Business rules

### Verified-business badge

InfoBip-routed Viber Business messages display a verified-business indicator on the recipient's Viber app. The badge appears next to the sender name and reassures the customer the message is from a real registered business. This requires:

- The Viber Business sender to be **pre-registered** with Viber (done by InfoBip on CloudCart's behalf for the shared `"CloudCart"` sender, or by the merchant directly for Self-credentials accounts).
- The business name to match the registered entity.

CloudCart's shared sender is `"CloudCart"`. Merchants on Self-credentials register their own brand directly with InfoBip / Viber Business — see [[viber-channel-self-credentials]].

### Customer-side requirement

The recipient must:

1. Have **Viber installed** on their phone.
2. Have **internet connectivity** when the message is sent (Viber is OTT — over-the-top — not carrier-routed).
3. Not have **blocked** the sender or business category.

If any of these fails, the message lands as `UNDELIVERED` / `UNDELIVERABLE` / `EXPIRED` on the log — see [[viber-channel-dlr-status]] for the status table.

**There is no automatic SMS fallback within the same Viber campaign step.** The merchant must explicitly chain a Viber step → conditional check (`message_read` / `message_not_read`) → SMS fallback step if they want a multi-channel cascade. The Viber channel's condition options include both `link_clicked` / `link_not_clicked` and `message_read` / `message_not_read` for exactly this branching — see [[viber-channel-dlr-status]].

### Sender override gating

The `regular.from` field is freely editable in the UI, but actually using a non-default sender requires the platform's `different_sender` flow + an active `viber_messages_subscription` plan-feature value. See [[viber-channel-settings]] for the toggle and [[viber-channel-plan-cap]] for the subscription gate.

### Promo vs Service routing decided by content

The send is flagged `promo = true` if `imageURL` OR `buttonText`/`buttonURL` is set. This routes the request through CloudCart's promo InfoBip account credentials (or stays on Self-credentials if the merchant is on that path). See [[viber-channel-send-pipeline]] for the runtime decision and [[viber-channel-plan-cap]] for the billing implications.

## Related

- [[marketing-channels-viber]] — hub.
- [[viber-channel-send-pipeline]] — the runtime that builds and sends the payload above.
- [[viber-channel-dlr-status]] — what happens after send; the status table merchants see.
- [[viber-channel-system-messages]] — the system-messages editor exposes image / button only when `allow_promo_messages = true`.
- [[viber-channel-settings]] — `regular.from` / `self_credentials.from` (the sender names shown to recipients).
- [[viber-channel-plan-cap]] — `prices.viber = 50` internal pricing unit; service-vs-promo billing.
- [[marketing-subscribers]] — Phone channel row that gates per-subscriber sends.

## Open questions

- Confirm the exact E.164 normalisation rules — what happens to a phone number that fails normalisation? `(verify)`
- Are there per-locale character-encoding constraints (e.g., Cyrillic counts the same as Latin for the 1000-char cap)? `(verify)`
