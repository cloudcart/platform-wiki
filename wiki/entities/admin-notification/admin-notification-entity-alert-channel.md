---
type: entity
nav_path: "Entity → Admin Notification → Alert channel"
aliases: ["alert_notification type", "Catch-all alert channel", "New notification type", "System alerts to admins", "Webhook auto-disable alert", "SSL expiry alert", "Plan limit alert", "Системно известие към администратор"]
tags: [entity, notifications, alerts, system-events, mandatory]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[admin-notification]]. See the hub for the other aspects (types, master switch, recipient, delivery, low-stock).

# Admin Notification — Alert channel (`alert_notification`)

## Identity

The **`alert_notification`** type is one of the 3 mandatory Admin Notification types (alongside `email_confirmation` and `two_factor_action` — see [[admin-notification-entity-types]]). Unlike the other 16 types, it is **open-ended**: any platform component can raise an `alert_notification` for a system-level event that the merchant must know about. There is no fixed list of triggers maintained on [[settings-admin-notifications]] — the catalogue below is the **documented set**, but new triggers can be added by any subsystem.

Because the channel is the platform's catch-all for operations-critical messaging, it cannot be silenced — neither the master switch nor a per-type toggle can suppress it (see [[admin-notification-entity-master-switch]] for the enforcement layers).

## Aliases

- **`alert_notification`** — the type identifier.
- **System alert** / **Системно известие** — informal phrasing for the channel.
- **"New notification"** — the type's user-facing label on [[settings-admin-notifications]].
- **Catch-all alert** / **Платформено известие** — informal phrasing for the open-ended nature of the channel.

## Key Attributes

### Documented trigger catalogue

The platform-shipped triggers that raise an `alert_notification`:

| Trigger | Source feature | What the alert says |
|---------|----------------|---------------------|
| **SSL certificate expiry** | [[settings-domains]] | When a custom domain's SSL cert expires, the platform sends an alert about the deactivation / fallback to the main host. |
| **Webhook auto-disable** | [[settings-hooks]] | When a [[webhook|Webhook]] receiver returns a permanent-failure HTTP code (400 / 401 / 403 / 404 / 405 / 406 / 410 / 411) or DNS resolution fails, the platform raises an alert via the `hooks.error.disable` template. The alert **contains the receiver's response body verbatim** so the merchant reads the actual error without leaving the screen — see [[notifications]] for the rendered message format. The merchant must fix the receiver and manually re-enable. **No "Webhook re-enabled" Admin Notification fires** when the merchant manually re-enables — the toggle is a silent DB flip. |
| **Webhook final give-up** | [[settings-hooks]] | After the 6-attempt / 20-minute retry sequence exhausts, the platform raises an alert via the SAME `hooks.error.disable` template — the alert text includes the last attempt's receiver error body. See [[settings-hooks-retry]] "Final give-up" + [[notifications]] for the exact rendered text. |
| **Plan-feature limit reached** | [[plan-gates]] | When the merchant exceeds a paid plan-feature limit (e.g., notification quota, storage), an alert explains the next steps. |
| **App uninstall on unpaid plans** | (apps subsystem) | When an app subscription lapses, an alert notifies the merchant about the auto-uninstall. |
| **Export complete** | (file-aggregation subsystem) | When a long-running export / aggregation file is ready, an alert includes the download URL. Note: this overlaps with the dedicated `file_download` toggleable type — `alert_notification` is the mandatory fallback when the aggregation subsystem cannot route via `file_download`. (verify) |
| **IP blocked / banned-IP enforcement** | [[settings-banned-ip]] | Surfaced in some flows when banned-IP enforcement takes a notable action. |
| **CloudCart-platform-staff messages** | Platform / CloudCart staff | Billing notices, security advisories, planned maintenance announcements — anything the CloudCart team sends merchants directly. |

The list is open-ended — any platform component can raise an alert via this channel. The set above is what is currently documented; new triggers can be added by subsystems without updating this entity page (drift risk — see Open Questions).

### Why the channel can't be silenced

Three reasons the platform refuses to expose a disable switch for this type:

1. **Security-relevant events** route through it (banned-IP, webhook permanent failures, SSL expiry — all can mask attack signals).
2. **Operations-critical events** route through it (export complete with the only download URL, plan-feature limit blocking new operations, app uninstall — silencing them strands the merchant).
3. **CloudCart-staff messaging** routes through it (billing notices, planned maintenance) — the platform owner needs a guaranteed channel.

### Heavy user of grouping / rate-limiting

The `alert_notification` channel is the heaviest user of the `mapping`-based grouping and the 1-day email + 5-minute push rate limits (see [[admin-notification-entity-delivery]]). A webhook that fails 50 times an hour produces:

- One row (collapsed by mapping).
- One email per day (rate-limited per mapping).
- At most one bell push per 5 minutes (rate-limited per mapping).

This is intentional: without aggressive grouping, the catch-all channel would generate hundreds of alerts per day on a busy store.

### Auto-disable detection rules — webhook specifics

The webhook auto-disable case is the most common `alert_notification` trigger in practice. The detection rule (verify against current source):

- **Permanent HTTP codes** trigger immediate auto-disable: 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 405 (Method Not Allowed), 406 (Not Acceptable), 410 (Gone), 411 (Length Required).
- **DNS resolution failure** triggers immediate auto-disable.
- **Transient failures** (5xx, timeout) trigger the **6-attempt / 20-minute** retry sequence; auto-disable kicks in only if the final attempt fails. See [[settings-hooks-retry]] for the verified timeline.

See [[settings-hooks]] for the full webhook receiver state machine.

### Plan-feature limit triggers — sample list

The plan-feature-limit-reached case typically covers:

- Notification quota exceeded (the store has sent more storefront notifications than the plan allows).
- Storage quota reached (image / asset storage at the plan ceiling).
- API call quota reached (JSON-API v2 rate limit per plan tier).
- App-count quota reached (more apps installed than the plan allows).

The alert message includes the limit name, current usage, and the next-step (upgrade plan, archive content, etc.).

### Bell-icon severity is undifferentiated

Although the underlying Admin Notification entity carries a `severity` field with six values (`alert`, `warning`, `error`, `important`, `success`, `info` — see [[admin-notification]] hub), the bell-icon UI does **not** visually differentiate severity in the current build. An SSL-expiry critical alert and an export-complete success alert appear identical in the bell-icon list. (verify whether a future build adds severity styling)

## Where it appears

- [[settings-hooks]] — webhook auto-disable + webhook-final-give-up are the most common triggers.
- [[settings-domains]] — SSL-expiry alerts.
- [[plan-gates]] — plan-feature-limit-reached alerts.
- [[settings-banned-ip]] — banned-IP enforcement alerts.
- (apps subsystem) — app-uninstall-on-unpaid-plan alerts; export-complete alerts in some flows.
- Bell icon at the top right of every admin page — primary surfacing channel.
- Admin recipient's inbox — email half.

## Related

- [[admin-notification]] — hub.
- [[admin-notification-entity-types]] — `alert_notification` is one of the 3 mandatory types.
- [[admin-notification-entity-master-switch]] — why the mandatory bypass guards exist.
- [[admin-notification-entity-delivery]] — grouping + rate-limit mechanics this channel relies on heavily.
- [[settings-hooks]] — webhook auto-disable + final-give-up triggers.
- [[settings-domains]] — SSL-expiry trigger.
- [[plan-gates]] — plan-feature-limit trigger.
- [[settings-banned-ip]] — banned-IP enforcement trigger.
- [[webhook]] — entity whose lifecycle drives the most common alerts on this channel.

## Open Questions

- Whether app-installed components can register their own `alert_notification` triggers, or only the platform core (verify).
- The exact relationship between `alert_notification` and the dedicated `file_download` toggleable type when both could apply to an export-complete event (verify routing rules).
- Whether the bell-icon UI will gain severity-based styling in a future build (currently undifferentiated).
