---
type: entity
nav_path: "Entity → Admin Notification"
aliases: ["Admin Notification", "Admin alert", "Admin email", "Administrator notification", "Notification to administrators", "Email to admins", "Bell-icon alert", "Известие към администратор", "Известие към администраторите", "Имейл известие", "Камбанка"]
tags: [entity, settings, notifications, email, alerts]
created: 2026-05-24
updated: 2026-06-10
source_count: 0
---

# Admin Notification

## Identity

An **Admin Notification** is a system-generated alert addressed to the merchant — delivered as an email to the store's primary email address AND surfaced in the admin panel's bell icon at the top of every page. It is the platform's "things you need to know about your store" channel: a new order was placed, a customer just registered, a product fell below the low-stock threshold, a webhook receiver returned a permanent failure and was auto-disabled, an export file is ready to download, the store SSL certificate is about to expire, a 2FA code is required to confirm an action.

Each Admin Notification ties together a **type** (one of 17 predefined event categories), a **title** + **body** (human-readable description, translated into the admin panel's selected language), an optional **link** (deep-link into the relevant admin screen), a **severity** (informational / warning / critical), a **grouping key** (so identical alerts don't pile up), and timestamps for when it was sent and when the merchant read it.

Admin Notifications are configured on [[settings-admin-notifications]] (Sidebar → Settings → Notifications to administrators). The merchant controls a master switch that mutes ALL toggleable notifications in one click, plus per-type toggles for 14 of the 17 categories. Three notification types — **email confirmation codes**, **two-factor authentication codes**, and **system alerts** — are **mandatory** and cannot be disabled at any layer. This is intentional: security-critical events MUST reach administrators regardless of their notification preferences.

An Admin Notification is distinct from a **customer-facing notification** (order-confirmation email, password-reset email, shipping update SMS) — those go to the buyer's inbox, not the merchant's. It is also distinct from a [[webhook|Webhook]] (an HTTP POST to a third-party URL) and from an in-app banner / toast (a transient UI message tied to a specific page action). See [[notification-delivery]] for how Admin Notifications fit alongside email, SMS, and webhooks as parallel consumers of the same platform event stream.

This page is the **hub** for the Admin Notification entity. The substantive content lives in 6 aspect pages — drill into the one that matches the question.

## Sub-pages (in this cluster)

- [[admin-notification-entity-types]] — the 17 notification types catalogue (14 toggleable + 3 mandatory), per-type `mail_<label>` setting keys, and which platform event triggers each one.
- [[admin-notification-entity-master-switch]] — the `administrator_email_notifications` master switch, per-type toggles, the three enforcement layers for mandatory notifications (UI / API / dispatch bypass), and settings-cache invalidation.
- [[admin-notification-entity-recipient]] — single recipient routing via `site_email`, no per-administrator copies, the two routing exceptions (email confirmation, 2FA code), CloudCart system sender vs store sender, and the late-binding recipient resolution.
- [[admin-notification-entity-delivery]] — async `admin_notify` queue vs sync 2FA dispatch, the bell-icon half (synchronous write), grouping by `mapping` key, the 1-day email + 5-minute push rate-limits, locale-filtered notification table, and the absent in-app failure surface.
- [[admin-notification-entity-alert-channel]] — the open-ended `alert_notification` mandatory type and its documented triggers (SSL expiry, webhook auto-disable, plan-feature limits, export complete, app uninstall on unpaid plans, banned-IP enforcement, CloudCart staff messages).
- [[admin-notification-entity-low-stock]] — the `product_quantity_low` + `product_out_of_stock` types, store-wide `product_threshold` vs per-product override, per-variant triggering granularity, and how the alert ties into [[inventory-tracking]].

## Aliases

- **Admin Notification** / **Administrator notification** — the canonical merchant-facing term in the [[settings-admin-notifications]] page header and in support documentation.
- **Admin alert** / **Bell-icon alert** — informal phrasing for the in-panel half of the delivery (the bell icon at the top right of every admin page).
- **Admin email** / **Email to admins** — informal phrasing for the email half of the delivery.
- **Notification to administrators** — the exact wording of the master-switch label on [[settings-admin-notifications]].
- **Известие към администратор** / **Известие към администраторите** / **Имейл известие** / **Камбанка** — Bulgarian labels used interchangeably in the BG admin (Камбанка = "bell" — the icon).

## Key Attributes

Six aspect pages own the substantive attribute detail. This hub gives the top-level shape — drill in.

| Aspect of the Admin Notification | Lives on |
|----------------------------------|----------|
| What categories exist + when each fires | [[admin-notification-entity-types]] |
| How the merchant turns them on / off | [[admin-notification-entity-master-switch]] |
| Who receives the email | [[admin-notification-entity-recipient]] |
| How / when it lands (email + bell) | [[admin-notification-entity-delivery]] |
| The catch-all `alert_notification` channel | [[admin-notification-entity-alert-channel]] |
| Low-stock / out-of-stock specifics | [[admin-notification-entity-low-stock]] |

Each Admin Notification carries: a **type** (which gates it against the master switch + per-type toggle), a **title** + **body** (translated into the admin's selected language), an optional **link** (deep-link to the relevant admin screen), a **severity** (one of `alert` / `warning` / `error` / `important` / `success` / `info` — visually undifferentiated in the current UI), a **grouping key** (collapses repeated alerts for the same root cause), and **read state** + **sent timestamp** + **created timestamp**.

## Where it appears

- [[settings-admin-notifications]] — the master configuration screen. Master switch + 17-row toggle table.
- [[settings-general]] — the source of the `site_email` recipient address.
- The bell icon at the top right of every admin page — the in-panel half of delivery.
- Any feature page that triggers an Admin Notification — examples: [[orders]] (new-order alert), [[customers]] (new-registration alert), [[products-products]] (low-stock alert), [[settings-hooks]] (webhook auto-disable alert), [[settings-staff]] (new-admin alert), [[settings-domains]] (SSL expiry alert).

## Related

### Related entities

- [[webhook]] — webhook auto-disable + final-give-up failures raise an Admin Notification via the `alert_notification` channel.
- [[order]] — order-create, order-status-change, and payment-status-change drive three of the 14 toggleable notification types.
- [[customer]] — new-customer-registration + newsletter-subscribe / -unsubscribe drive three notification types.
- [[product]] — out-of-stock + low-stock events drive two notification types.
- [[subscriber]] — newsletter subscribe / unsubscribe events.
- [[staff-member]] — admin-account create / edit / password-change / password-reset drive four notification types; staff members are the *intended* readers but the *actual* recipient is the single store email.

### Cross-cutting concepts

- [[notification-delivery]] — the platform-wide event spine. Admin Notifications are one of four parallel consumers (alongside customer-facing emails / SMS, webhooks, and analytics aggregation).
- [[merchant-roles]] — Administrator vs Moderator distinction. The recipient address does NOT depend on the role — every admin shares the single store email.
- [[plan-gates]] — plan-feature-limit-reached events are surfaced as Admin Notifications.
- [[inventory-tracking]] — the source of the low-stock + out-of-stock triggers (see [[admin-notification-entity-low-stock]]).

### Settings & feature pages

- [[settings-admin-notifications]] — master configuration.
- [[settings-general]] — `site_email` recipient address.
- [[settings-hooks]] — webhook auto-disable alerts (one of the `alert_notification` triggers).
- [[settings-staff]] — staff-account events.
- [[settings-cart]] — store-wide low-stock threshold.
- [[settings-domains]] — SSL-expiry alerts.
- [[settings-banned-ip]] — banned-IP enforcement events.

## Open Questions

No outstanding questions on the hub — all items resolved or distributed to aspect pages.
