---
type: feature
nav_path: "Settings → Notifications to administrators"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["Admin notifications", "Email notifications to admins", "Известия към администраторите", "Имейл известия"]
tags: [settings, notifications, email]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---
# Notifications to administrators

## Purpose

Controls which platform events send an email to the store's administrative recipient. The screen has a single master switch ("Send notifications to administrators") that turns everything off in one click, plus a table of 17 individual notification types — each can be toggled on or off independently, except for three that are mandatory and cannot be disabled (email confirmation codes, two-factor codes, and system alerts). All notifications go to a single recipient address: the store's primary email, configured in [[settings-general]].

This hub page is slim — each operational aspect (master switch, per-type toggles, mandatory three, recipient routing, delivery queue, alert triggers, permissions / locale) is documented on its own sub-page. Drill into the aspect that matches the question rather than reading every page.

## Where to find it

Direct URL: `/admin/settings/admin-notifications`. The page's breadcrumb reads "Settings → Notifications to administrators". The header icon is a bell.

> **Note (verified against the sidebar navigation tree):** the "Notifications to administrators" entry is **currently NOT shown in the Settings sidebar sub-menu** — its navigation link is commented out in the Settings menu builder. The page itself is live and fully functional at its direct URL and route; it's just not linked from the sidebar today. Merchants who need it must navigate to the URL directly (or be deep-linked there).

## What the merchant can do here

- Turn ALL admin email notifications on or off in one click via the master switch in the page header — see [[admin-notifications-master-switch]].
- Enable or disable each of the 14 toggleable notification types individually (e.g., suppress order-creation notifications during a high-volume campaign while keeping low-stock alerts on) — see [[admin-notifications-per-type-toggles]].
- See the three mandatory notifications (email confirmation, two-factor authentication, system alerts) listed with their toggles disabled — visual confirmation that these always go out. See [[admin-notifications-mandatory-three]].
- See the human-readable names of each notification in the admin panel's currently selected language.

The merchant cannot:

- Change the recipient address from this page. That lives in [[settings-general]] (Store Details → Email). For routing rules + the two exceptions to `site_email`, see [[admin-notifications-recipient-routing]].
- Edit the template / wording of each email. (Those are CloudCart-provided multilingual templates.)
- Add new notification types or remove existing ones from the list.
- See a delivery history of past emails on this page. There is no in-app failure surface either — see [[admin-notifications-delivery-queue]] for the queue + visibility gaps.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. Each is small enough that the Assistant can read just the relevant one to answer a question.

- [[admin-notifications-master-switch]] — the master toggle, its two different defaults (display vs dispatch), and the "flip-once" guidance for new merchants.
- [[admin-notifications-per-type-toggles]] — the 14 toggleable rows, the `mail_<label>` setting keys, per-type defaults, and the hidden 18th notification (`product_review_added`).
- [[admin-notifications-mandatory-three]] — `email_confirmation`, `two_factor_action`, `alert_notification` and the three enforcement layers (UI / API / helper bypass) that keep them always-on.
- [[admin-notifications-recipient-routing]] — `site_email` as default recipient for 15 of 17 types; the two exceptions; sender = CloudCart-branded From; single-recipient model with no per-administrator copies.
- [[admin-notifications-delivery-queue]] — `admin_notify` SiteQueue task → `system7` worker queue; 2FA synchronous bypass; failure visibility; settings cache invalidation.
- [[admin-notifications-alert-triggers]] — what raises the always-on `alert_notification` channel (SSL expiry, webhook auto-disable, plan-feature limits, app uninstall, banned-IP, CloudCart staff messages).
- [[admin-notifications-permissions-locale]] — the `settings.general` permission gate (bundled with General settings) and the locale-filtered notifications table.

## Settings & fields

The page has two interactive elements: a master switch in the action area of the page header, and a table of notification types in the main body. Field-level details (setting keys, defaults, validation) are on the relevant sub-pages — this hub gives the at-a-glance map.

| Field / Control | Sub-page | Notes |
|-----------------|----------|-------|
| **Send notifications to administrators** (`administrator_email_notifications`) | [[admin-notifications-master-switch]] | Master toggle. Saves immediately on flip. Mandatory notifications bypass it. |
| **Per-type "Active" toggle** (one per row; setting keys `mail_<label>`) | [[admin-notifications-per-type-toggles]] | 14 toggleable rows. Each saves immediately. Mandatory rows render with the toggle disabled. |
| Recipient address (read-only, not on this page) | [[admin-notifications-recipient-routing]] | The `site_email` setting from [[settings-general]] — changing it from here is not possible. |

## Modals and sub-flows

**This page has no modals, no wizards, no side-panels.** The entire surface is:

- The master switch in the page header — see [[admin-notifications-master-switch]] for the save flow + error handling.
- The notifications table — see [[admin-notifications-per-type-toggles]] for the per-row save flow.

No confirm dialogs. No bulk-action wizard. No batch-edit. No test-send flow. No template editor. No recipient picker. There is nothing more to discover on this screen — what you see is the entire feature.

## Business rules

The detailed business rules are distributed across the sub-pages; this list maps each rule to its home.

- Master switch suppresses ALL toggleable notifications — see [[admin-notifications-master-switch]].
- Per-type toggles suppress at dispatch time via `mail_<label>` — see [[admin-notifications-per-type-toggles]].
- Three notifications are mandatory and bypass both toggles — see [[admin-notifications-mandatory-three]].
- Recipient is the store's primary email (with two exceptions) — see [[admin-notifications-recipient-routing]].
- Sender is CloudCart, not the store — see [[admin-notifications-recipient-routing]].
- Notifications are queued (asynchronous delivery; 2FA is synchronous) — see [[admin-notifications-delivery-queue]].
- Notification list is locale-filtered — see [[admin-notifications-permissions-locale]].
- Saves are immediate; no draft / cancel — see [[admin-notifications-master-switch]] + [[admin-notifications-per-type-toggles]].
- Settings cache invalidation is immediate on save — see [[admin-notifications-delivery-queue]].
- Permission gate uses `settings.general`, not a dedicated permission — see [[admin-notifications-permissions-locale]].
- Master toggle has two different defaults in code (display path vs dispatch path) — see [[admin-notifications-master-switch]].

## Related

- [[settings-general]] — where `site_email` is configured (the recipient for 15 of 17 notification types) and where the email-confirmation flow originates.
- [[settings]] — parent hub.
- [[settings-staff]] — Administrator and Moderator accounts; `new_admin_account`, `admin_account_changes`, `admin_account_password_change`, `admin_account_password_reset` are triggered from there.
- [[customer]] — `new_customer_register` and the customer newsletter subscribe/unsubscribe notifications.
- [[order]] — `order_add`, `order_status_change`, `order_payment_status_change` are triggered by order lifecycle events.
- [[product]] — `product_out_of_stock` and `product_quantity_low` trigger from inventory state changes.
- [[subscriber]] — `customer_newsletter_subscribe` / `customer_newsletter_unsubscribe`.
- [[notification-delivery]] — cross-feature concept page about how email/SMS/webhook delivery works platform-wide.
- [[merchant-roles]] — Administrator vs Moderator distinction.
- [[background-queue-inventory]] — catalogue of all background processes; covers the `admin_notify` queue that fans out these alerts and how to spot a stuck notification.
- [[order-processing-pipeline]] — the admin-email queue dispatch points across the pipeline (new order, out of stock, low stock).

## Open questions

None.
