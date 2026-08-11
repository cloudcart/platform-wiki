---
type: entity
nav_path: "Entity → Admin Notification → Types catalogue"
aliases: ["Admin notification types", "Notification categories", "17 notification types", "Toggleable notification types", "Mandatory notification types", "mail_<label> settings", "Категории известия"]
tags: [entity, settings, notifications, email, alerts, types]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[admin-notification]]. See the hub for the other aspects (master switch, recipient, delivery, alert channel, low-stock).

# Admin Notification — Types catalogue

## Identity

The Admin Notification entity carries one **type** (one of 17 predefined event categories). The type drives two things: which platform event triggers the notification, and which per-type toggle on [[settings-admin-notifications]] gates it. The 17 types split into **14 toggleable** (the merchant can disable them individually via `mail_<label>` settings) and **3 mandatory** (security-critical / operations-critical — cannot be disabled at any layer).

## Aliases

- **Notification type** / **Notification category** — used interchangeably in the [[settings-admin-notifications]] table.
- **`mail_<label>` setting** — the persistence key on the underlying settings row for each toggleable type (e.g., `mail_order_add`).
- **Mandatory notification** — informal phrasing for the 3 protected types.

## Key Attributes

### The 14 toggleable types

Each has a `mail_<label>` setting on [[settings-admin-notifications]]. Default is ON when missing.

| Type | `mail_<label>` key | Triggered when |
|------|--------------------|----------------|
| **Contact request** | `mail_contact` | A visitor submits the storefront contact form. |
| **Order Payment Status Change** | `mail_order_payment_status_change` | An [[order|Order]]'s payment status changes (e.g., pending → paid). |
| **Order Status Change** | `mail_order_status_change` | An Order's general status changes (e.g., pending → shipped). |
| **New Customer Registration** | `mail_new_customer_register` | A new [[customer|Customer]] account is created on the storefront. |
| **New Order Add** | `mail_order_add` | A new Order is placed. |
| **Customer Newsletter Subscribe** | `mail_customer_newsletter_subscribe` | A customer subscribes to the store's newsletter. |
| **Customer Newsletter Unsubscribe** | `mail_customer_newsletter_unsubscribe` | A customer unsubscribes from the newsletter. |
| **New Admin Account Created** | `mail_new_admin_account` | A new Administrator or Moderator account is created (see [[settings-staff]]). |
| **Admin Account Info Changes** | `mail_admin_account_changes` | An existing Admin/Moderator account is edited. |
| **Admin Account Password Changed** | `mail_admin_account_password_change` | An Admin/Moderator changes their password. |
| **Admin Account Password Reset** | `mail_admin_account_password_reset` | An Admin/Moderator requests a password reset. |
| **Products Out Of Stock** | `mail_product_out_of_stock` | A [[product|Product]]'s stock falls to zero. |
| **Products Quantity Low** | `mail_product_quantity_low` | A product crosses the low-stock threshold (see [[admin-notification-entity-low-stock]]). |
| **Large aggregation file download** | `mail_file_download` | A long-running export (orders CSV, product feed, analytics report) is ready for download. |

### The 3 mandatory types

These cannot be disabled at any layer — the UI toggle is rendered disabled, the settings API returns HTTP 422 *"This notification cannot be disabled"* on disable attempts, and the dispatch path bypasses the master-switch gate. See [[admin-notification-entity-master-switch]] for the full enforcement model.

| Type | Triggered when | Why it can't be disabled |
|------|----------------|--------------------------|
| **Email confirmation** (`email_confirmation`) | The merchant changes the store email in [[settings-general]] — two codes go out, one to the OLD address and one to the NEW. | Security-critical: prevents account hijack via email change. |
| **Two factor code verify** (`two_factor_action`) | An Admin/Moderator performs a 2FA-protected action and a verification code is required. | Security-critical: the code IS the auth factor. Bypasses the queue and sends synchronously (see [[admin-notification-entity-delivery]]). |
| **New notification** (`alert_notification`) | A system-level alert is raised that administrators must see — see [[admin-notification-entity-alert-channel]] for the open-ended trigger list. | Catch-all "things you need to know" channel that CloudCart cannot let the merchant silence. |

### Type counts

- **17 total** types currently shipped.
- **14 toggleable** — each gated by master switch AND per-type toggle.
- **3 mandatory** — bypass the master switch entirely.

### Type-to-entity coverage

Each type ties to a domain entity:

- **Order-driven** (3 types): `order_add`, `order_status_change`, `order_payment_status_change`.
- **Customer-driven** (3 types): `new_customer_register`, `customer_newsletter_subscribe`, `customer_newsletter_unsubscribe`.
- **Staff-driven** (4 types): `new_admin_account`, `admin_account_changes`, `admin_account_password_change`, `admin_account_password_reset`.
- **Product-driven** (2 types): `product_out_of_stock`, `product_quantity_low`.
- **Storefront-driven** (1 type): `contact`.
- **Operational** (1 toggleable type): `file_download`.
- **Security-critical mandatory** (2 types): `email_confirmation`, `two_factor_action`.
- **Catch-all mandatory** (1 type): `alert_notification`.

## Where it appears

- [[settings-admin-notifications]] — the master configuration screen renders the 17 types as rows in the toggle table; for toggleable types the row is interactive, for mandatory types it is rendered disabled.
- [[orders]] / [[orders-details]] — origin of the 3 order-driven types.
- [[customers]] — origin of `new_customer_register`.
- [[products-products]] — origin of the 2 product-driven types (stock-decrement at order time).
- [[settings-staff]] — origin of the 4 staff-driven types.
- [[settings-hooks]] — webhook auto-disable raises an `alert_notification` (see [[admin-notification-entity-alert-channel]]).
- [[settings-general]] — store-email-change raises an `email_confirmation`.

## Related

- [[admin-notification]] — hub.
- [[settings-admin-notifications]] — master configuration where types are exposed.
- [[admin-notification-entity-master-switch]] — how the toggleable / mandatory distinction is enforced.
- [[admin-notification-entity-alert-channel]] — the open-ended `alert_notification` trigger catalogue.
- [[admin-notification-entity-low-stock]] — the two product-driven types in full.
- [[notification-delivery]] — platform-wide event spine.
- [[order]] / [[customer]] / [[product]] / [[staff-member]] — domain entities that drive most notification types.

## Open Questions

- Whether additional `mail_<label>` settings can be introduced by apps (the 17 listed are the platform-shipped set; app-added types are not documented here) (verify).
