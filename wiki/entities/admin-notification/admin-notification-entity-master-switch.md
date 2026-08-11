---
type: entity
nav_path: "Entity → Admin Notification → Master switch & toggles"
aliases: ["Admin notification master switch", "administrator_email_notifications setting", "Per-type notification toggle", "Mandatory notification enforcement", "Notification opt-out", "Главен ключ за известия"]
tags: [entity, settings, notifications, toggles, configuration]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[admin-notification]]. See the hub for the other aspects (types, recipient, delivery, alert channel, low-stock).

# Admin Notification — Master switch & per-type toggles

## Identity

The merchant configures Admin Notifications through **two layers of opt-out**: a single global **master switch** (mutes ALL 14 toggleable notifications in one click) and **14 per-type toggles** (mute a single category independently). Both layers are surfaced on [[settings-admin-notifications]] (Sidebar → Settings → Notifications to administrators) — there is no separate global setting page, no per-administrator opt-out, and no batch-toggle workflow.

The **3 mandatory notification types** (`email_confirmation`, `two_factor_action`, `alert_notification` — see [[admin-notification-entity-types]]) bypass BOTH layers. They cannot be disabled at any layer, and the platform enforces that protection at three independent guards (UI, API, dispatch path).

## Aliases

- **Master switch** — informal name for `administrator_email_notifications`.
- **Notification to administrators** — the exact wording of the master-switch label on [[settings-admin-notifications]].
- **Per-type toggle** — the 14 row-level on/off switches in the notification table.
- **`mail_<label>` setting** — the persistence key for each per-type toggle (e.g., `mail_order_add`, `mail_new_customer_register`).

## Key Attributes

### The master switch — `administrator_email_notifications`

| Property | Value |
|----------|-------|
| Setting key | `administrator_email_notifications` |
| Label on UI | "Notification to administrators" |
| Default | ON (default ON when missing) |
| Effect when OFF | All 14 toggleable notifications are suppressed at dispatch time — the queue job is never created. |
| Effect on mandatory types | None — they bypass this gate entirely. |
| Save UX | Immediate (no Save button); next dispatched notification respects the new state. |

When the master switch is OFF the dispatch helper short-circuits before any of the 14 toggleable notification paths run — no email enqueued, no bell-icon alert created.

### The 14 per-type toggles — `mail_<label>`

Each toggleable notification type has its own setting key on the same row. The toggle persists `yes` (ON) or `no` (OFF). Default is ON when the row is missing. The dispatch helper checks this AFTER the master switch — meaning a toggleable notification is delivered only when **master switch ON AND per-type toggle ON**. Either OFF suppresses it.

| Gate combination | Result |
|------------------|--------|
| Master ON, per-type ON | Notification delivered. |
| Master ON, per-type OFF | Notification suppressed (specific type only). |
| Master OFF, per-type ON | Notification suppressed (all 14 types). |
| Master OFF, per-type OFF | Notification suppressed. |
| Any gate state + type is mandatory | Notification delivered (bypass). |

Saves are immediate — there is no "Save" button and no batch-toggle workflow. Each click writes one row and flushes the settings cache.

### Mandatory enforcement — three independent guards

The 3 mandatory types are protected at three layers so a UI bug or hand-crafted API call cannot silence them:

1. **UI guard** — on [[settings-admin-notifications]] the toggle for each mandatory type is rendered disabled. The merchant cannot interact with it.
2. **API guard** — the settings-update endpoint rejects disable attempts with HTTP 422 *"This notification cannot be disabled"*. A hand-crafted PATCH that tries to set `mail_alert_notification = no` (etc.) is rejected before it persists.
3. **Dispatch bypass** — the dispatch paths for mandatory types don't go through the master-switch gate or the per-type toggle gate at all. They enqueue (or send synchronously, for 2FA) directly.

So even if a bug in the toggle UI somehow flipped the master switch off, these specific notifications would still go out.

### Settings cache invalidates immediately on save

Each toggle save persists the change and flushes the settings cache. The next dispatched notification (anywhere in the platform) immediately respects the new toggle state. There is no propagation delay between save and effect — a merchant who turns OFF `mail_order_add` mid-day will receive no order notifications for orders placed after that save.

### No history / no audit log on the settings page

[[settings-admin-notifications]] does not show a history of past notifications — there is no "alerts sent in the last 30 days" view. The bell icon shows current unread alerts only; once read, they're cleared. To verify a notification was sent, the merchant must check the receiving inbox.

### No per-administrator preferences

The master switch and per-type toggles are **store-wide settings**, not per-administrator. There is no UI for "Administrator John wants to receive order alerts but Moderator Jane does not" — every admin and moderator shares the same single inbox (see [[admin-notification-entity-recipient]]) and the same single toggle state.

### Notification table is locale-filtered

The [[settings-admin-notifications]] table only shows notification types that have a translation in the admin panel's currently selected language. For less-common admin languages, some rows may be missing from the table — the underlying toggles still exist and still gate dispatch, but the merchant has no UI to flip them. CloudCart ships translations for the major languages so this is uncommon; see [[admin-notification-entity-delivery]] for more on locale handling.

## Where it appears

- [[settings-admin-notifications]] — both the master switch and the 14 per-type toggles are configured here. The 3 mandatory types appear in the same table but with their toggles disabled.
- [[settings-general]] — `site_email` is the recipient address that the master switch ultimately gates delivery TO (see [[admin-notification-entity-recipient]]).
- Per-administrator settings — **none**. There is no equivalent screen in the admin profile for per-user preferences.

## Related

- [[admin-notification]] — hub.
- [[admin-notification-entity-types]] — the 17 categories that the toggles gate.
- [[admin-notification-entity-recipient]] — what address the (non-suppressed) notification reaches.
- [[admin-notification-entity-delivery]] — how a non-suppressed notification then propagates.
- [[settings-admin-notifications]] — the configuration screen.
- [[settings-general]] — recipient address.
- [[notification-delivery]] — cross-cutting concept; admin notifications are one of four parallel consumers.

## Open Questions

- The exact verbatim Bulgarian translation of *"This notification cannot be disabled"* on the settings API guard (verify).
