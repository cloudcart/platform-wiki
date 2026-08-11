---
type: feature
nav_path: "Settings → Notifications to administrators → Per-type toggles"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["Admin notification rows", "mail_label settings", "Per-notification toggle", "Notifications table", "mail_order_add", "mail_product_quantity_low"]
tags: [settings, notifications, email]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-admin-notifications]]. See the hub for the other aspects (master switch, mandatory three, recipient routing, delivery queue, alert triggers, permissions / locale).

# Admin notifications — per-type toggles

## Purpose

The notifications table on [[settings-admin-notifications]] lets the merchant enable or disable each platform event independently. There are 14 toggleable rows; each maps to a per-type setting key `mail_<label>` (e.g., `mail_order_add`, `mail_new_customer_register`). Flipping a row's switch sends the new value to the API, which persists it and flushes the settings cache; the next time that event fires anywhere in the platform, the helper checks the per-type setting and skips dispatch if it's `no`.

The three mandatory rows (`email_confirmation`, `two_factor_action`, `alert_notification`) appear in the same table but with their toggle disabled — see [[admin-notifications-mandatory-three]].

## Where to find it

The notifications table is the main body of [[settings-admin-notifications]]. Columns are "Notification" (the human-readable name in the admin panel's currently selected language) and "Active" (the switch).

## What the merchant can do here

- Independently enable or disable each of the 14 toggleable notification types — e.g., keep low-stock alerts on while silencing per-order new-order emails during a campaign spike.
- See at a glance which notifications are currently active.

The merchant cannot:

- Reorder the rows. Sort is deterministic: toggleable rows first, mandatory rows pinned at the bottom.
- Add a new row or remove an existing one. The set of rows is platform-defined (with the locale + per-store install filtering described below).
- Edit the email template / wording per row.

## Settings & fields

Each toggleable row has its own setting key `mail_<label>`. Default value is `yes` (send) — when missing, the dispatch helper treats it as enabled. Flipping the toggle persists `yes` / `no` explicitly.

| Display name | Internal label | Setting key | Triggered when |
|--------------|----------------|-------------|----------------|
| Contact request | `contact` | `mail_contact` | A visitor submits the storefront contact form. |
| Order Payment Status Change Notification | `order_payment_status_change` | `mail_order_payment_status_change` | An order's payment status changes (e.g., pending → paid). |
| Order Status Change Notification | `order_status_change` | `mail_order_status_change` | An order's general status changes (e.g., pending → shipped). |
| New Customer Registration | `new_customer_register` | `mail_new_customer_register` | A new customer account is created on the storefront. |
| New Order Add Notification | `order_add` | `mail_order_add` | A new order is placed. |
| Customer Newsletter Subscribe | `customer_newsletter_subscribe` | `mail_customer_newsletter_subscribe` | A customer subscribes to the store's newsletter. |
| Customer Newsletter Unsubscribe | `customer_newsletter_unsubscribe` | `mail_customer_newsletter_unsubscribe` | A customer unsubscribes from the newsletter. |
| New Admin Account Created | `new_admin_account` | `mail_new_admin_account` | A new Administrator or Moderator account is created. |
| Admin Account Info Changes | `admin_account_changes` | `mail_admin_account_changes` | An existing Admin/Moderator account details are edited. |
| Admin Account Password Changed | `admin_account_password_change` | `mail_admin_account_password_change` | An Admin/Moderator changes their password. |
| Admin Account Password Reset | `admin_account_password_reset` | `mail_admin_account_password_reset` | An Admin/Moderator requests a password reset. |
| Products Out Of Stock | `product_out_of_stock` | `mail_product_out_of_stock` | A product's stock falls to zero. |
| Products Quantity Low | `product_quantity_low` | `mail_product_quantity_low` | A product crosses the merchant-configured low-stock threshold. See [[inventory-in-stock-badge]] for the threshold + alert gating. |
| Large aggregation file download | `file_download` | `mail_file_download` | A long-running export / aggregation file (orders CSV, product feed) is ready for download. |

### Per-row save flow

When the merchant flips any row's switch:

- Mandatory rows — the switch is disabled at the UI level; click does nothing.
- Toggleable rows — `PATCH /admin/api/core/settings/admin-notifications/` is fired with `{label, active}`. On success: toast *"Saved successfully."* and the table refetches. On error: toast *"An error occurred."*.

### Sort order is deterministic

The table renders all non-readonly (toggleable) rows first, then all `readonly` (mandatory) rows pinned at the bottom. The mandatory rows are forced to display `active=true` regardless of any stale local state.

## Modals and sub-flows

None. Each row is a single click. No confirm dialog.

## Business rules

### Per-type toggles suppress at dispatch time

When the merchant flips a row's toggle off, the setting becomes `mail_<label>=no`, and the admin notification helper skips dispatch for that specific notification. The check fires inline — no queue task is created when the toggle is off. Defaults to `yes` (sent) if the setting is missing.

### Default for new notification types is "ON"

When CloudCart ships a new event type later, its `mail_<label>` setting doesn't exist yet for existing stores. The default-`yes` rule means the new notification is automatically delivered to every existing store until the merchant explicitly turns it off. This is unlike the master switch, which has a more complex two-defaults situation (see [[admin-notifications-master-switch]]).

### Master switch overrides per-type toggles

If the master switch (`administrator_email_notifications`) is OFF, no per-type row matters — every toggleable notification is suppressed regardless. See [[admin-notifications-master-switch]].

### The hidden 18th notification — `product_review_added` (verify)

The admin-helper's internal label map includes ONE notification (`mail_product_review_added`) that is NOT in the page's standard 17-row table. It's used by the Product Reviews app to alert admins when a customer posts a review. Whether it appears as an 18th row depends on whether the per-store install has a translation row for the `product_review_added` label — most stores have it via the Product Reviews module install. So depending on which apps the merchant has installed, the table might show 18 rows instead of 17.

### Locale filtering can hide rows

Rows without a translation in the admin panel's currently selected language are not shown — see [[admin-notifications-permissions-locale]] for the locale rule.

### Third-party apps can plug into the same suppression machinery (verify)

When a CloudCart developer or app passes a `notification_label` parameter, the admin-notification helper looks up the corresponding `mail_<label>` setting — so third-party apps that register an admin notification under a known label automatically participate in the merchant's per-type toggle. There is no public list of registered notification labels exposed in the admin panel; merchants only see labels that have at least one translation row for their store.

## Related

- [[settings-admin-notifications]] — hub.
- [[admin-notifications-master-switch]] — the master gate that overrides every row.
- [[admin-notifications-mandatory-three]] — the three notifications that cannot be toggled.
- [[admin-notifications-recipient-routing]] — who receives each row's email.
- [[admin-notifications-delivery-queue]] — how each toggled-on row reaches the recipient.
- [[inventory-in-stock-badge]] — low-stock + out-of-stock alert gating (`mail_product_quantity_low`, `mail_product_out_of_stock`).
- [[order-processing-pipeline]] — where `mail_order_add`, `mail_order_status_change`, `mail_order_payment_status_change` are dispatched.
- [[settings-staff]] — origin of `mail_new_admin_account`, `mail_admin_account_changes`, `mail_admin_account_password_change`, `mail_admin_account_password_reset`.

## Open questions

- The "third-party apps can pass `notification_label`" extension hook should be confirmed against the current helper code — useful for an app-developer doc but doesn't affect merchants directly. `(verify)`
- Whether the `product_review_added` row appears for stores without the Product Reviews app installed is anecdotally "no" but not exhaustively verified. `(verify)`
