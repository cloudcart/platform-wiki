---
type: entity
nav_path: "Entity → Admin Notification → Recipient routing"
aliases: ["Admin notification recipient", "site_email recipient", "Single store email", "Admin notification sender", "Notification routing", "No per-administrator copies", "Получател на известията"]
tags: [entity, settings, notifications, email, routing]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[admin-notification]]. See the hub for the other aspects (types, master switch, delivery, alert channel, low-stock).

# Admin Notification — Recipient routing

## Identity

For **15 of the 17 notification types**, the recipient of an Admin Notification is the **single store email** (`site_email`) configured on [[settings-general]]. There is no per-administrator opt-in, no per-administrator opt-out, and no "fan out to all staff" mode in the platform itself. Two notification types — **email confirmation** (`email_confirmation`) and **two-factor code** (`two_factor_action`) — route to dedicated addresses tied to the specific user action that triggered them.

Outbound mail uses a **CloudCart system sender** as the From header — NOT the store's own configured customer-facing sender. Merchants should expect admin notifications to arrive from a CloudCart-branded address.

## Aliases

- **Recipient address** — the resolved email address that receives the notification.
- **Store email** / **`site_email`** — the canonical setting on [[settings-general]].
- **Shared inbox** — common merchant workaround for fanning admin notifications out to multiple humans.
- **System sender** / **CloudCart sender** — informal phrasing for the CloudCart-branded From header used on admin notifications.

## Key Attributes

### Default routing — `site_email`

| Property | Value |
|----------|-------|
| Source setting | `site_email` on [[settings-general]] |
| Applies to | 15 of the 17 notification types (all except `email_confirmation` and `two_factor_action`) |
| Per-administrator copies | NONE — every admin and moderator shares the single store email |
| Per-administrator opt-out | NONE |
| Format | A single email address |
| If wrong / typo | Every admin notification is silently misdelivered until corrected |

The 15 types that route to `site_email` cover: contact requests, order events, customer events, newsletter events, staff-account events, low-stock / out-of-stock events, large-file-download events, and the catch-all `alert_notification` channel (see [[admin-notification-entity-alert-channel]]).

### Late-binding recipient resolution

The recipient address is resolved at the moment the queue worker picks up the job (NOT at the moment the job was enqueued). This means:

- If the merchant changes `site_email` after a notification is enqueued but before it ships, the notification is delivered to the **new** address.
- A typo in `site_email` doesn't poison the queue — fixing the setting unblocks the next dispatch immediately.
- Historical notifications that were already sent stay delivered to whatever address was current at send time.

### The two routing exceptions

**`email_confirmation`** — two codes go out during the [[settings-general|store-email change flow]]: one to the **OLD** address (to confirm the merchant controls the existing email), one to the **NEW** address (to confirm the merchant controls the destination). Neither code routes to `site_email` itself — `site_email` is precisely what's being changed in this flow.

**`two_factor_action`** — the verification code goes to the **user's own email** (the admin attempting the 2FA-protected action), NOT the store email. This is the only notification type whose recipient depends on **which admin** triggered it. The 2FA address is read from the admin's own profile / staff record.

### CloudCart sender, not store sender

| Mail channel | From header source |
|--------------|--------------------|
| Customer-facing transactional (order confirmation, password reset) | Store's configured sender on [[settings-general]] |
| Admin notifications | CloudCart system sender (platform-branded address) |

This is intentional: admin notifications travel between CloudCart and the merchant on a CloudCart-controlled channel; customer-facing mail travels between the store and the customer on the store's own brand.

### No per-administrator preferences anywhere

The recipient model is store-level, not user-level. Three consequences:

- A merchant who wants Administrator John to receive order alerts but NOT Moderator Jane has no platform mechanism to do this.
- Every staff member with access to the store inbox receives every admin notification.
- A merchant with multiple administrators ([[settings-staff]]) cannot distribute the notification load by category — the only fan-out path is the merchant's own email-provider rules on the shared inbox.

### Practical merchant guidance — use a distribution list

The standard workaround for fan-out: set `site_email` to a shared inbox / distribution list (e.g., `team@merchant.com`, `alerts@store.com`) that the merchant's own email provider forwards to multiple recipients. CloudCart sends one email to that single address; the merchant's mail provider handles the multi-recipient delivery.

Merchants who need per-category routing (orders → fulfillment team, low-stock → buying team, webhook auto-disable → tech team) typically configure their distribution-list rules at the email-provider level on top of the shared inbox.

## Where it appears

- [[settings-general]] — the source of `site_email`.
- [[settings-admin-notifications]] — does NOT show the recipient address; the merchant must check [[settings-general]] separately. (verify)
- [[settings-staff]] — staff member records carry their own emails, but only the 2FA path consults those addresses.
- Admin email inbox — actual delivery surface; nothing in the admin panel shows a "sent log".

## Related

- [[admin-notification]] — hub.
- [[admin-notification-entity-types]] — the 17 categories; 15 route to `site_email`, 2 are exceptions.
- [[admin-notification-entity-delivery]] — how the recipient is then dispatched (queue / synchronous).
- [[admin-notification-entity-master-switch]] — what gates suppression upstream of recipient resolution.
- [[settings-general]] — `site_email` configuration.
- [[settings-staff]] — staff records consulted by the 2FA route.
- [[merchant-roles]] — Administrator vs Moderator distinction does NOT affect recipient routing.
- [[notification-delivery]] — cross-cutting concept; recipient routing is the admin-notification half of the platform-wide event spine.

## Open Questions

- Whether `site_email` validation rejects multiple comma-separated addresses (the field is documented as a single address; some platforms accept comma-separated lists as a built-in fan-out) (verify).
- Whether there is a "reply-to" override on admin notifications separate from the From header (verify).
