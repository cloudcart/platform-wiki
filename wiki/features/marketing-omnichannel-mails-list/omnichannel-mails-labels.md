---
type: feature
nav_path: "Marketing → Channels → Email notifications → Mail labels"
route_name: marketing-mails-list
route_path: /admin/marketing-new/omnichannel/mails/list
aliases: ["Customer mail labels", "Transactional email types", "Mail label catalogue", "Customer notification events", "Имейл етикети", "Видове клиентски имейли"]
tags: [marketing, omnichannel, email, notifications, transactional, labels]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 2
---

> Part of [[marketing-omnichannel-mails-list]]. See the hub for related aspects (editor modal, toggles & gating, variables, abandoned-cart, customisation limits).

# Email notifications — mail labels

## Purpose

This page catalogues the **fixed set of platform mail labels** that drive transactional / system emails to customers. Each `label` is hard-wired to a platform event (order placed, password reset, etc.) and identifies the row in the **Email notifications** list. The merchant **cannot add new labels** — they're CloudCart-defined; new platform mail types are a code change.

## Where to find it

Each label appears as one row in the list at `/admin/marketing-new/omnichannel/mails/list`. Sidebar → **Marketing** → **Channels** → **Email notifications**.

## What the merchant can do here

For every label below, the merchant can open its row to customise **Name**, **Subject**, **HTML body**, and (implicitly) the `template_json` shape — see [[omnichannel-mails-editor-modal]]. The label itself is read-only.

## Settings & fields

### Mail label catalogue (verbatim from `App\Helper\Mail\Config::$customer_mail_type_vars`) (verify)

| Label | Trigger event |
|-------|--------------|
| `welcome` | New customer account created |
| `email_confirmation` | Account created; ask the customer to verify their email |
| `email_confirmed` | Customer successfully confirmed their email |
| `password_change` | Customer changed their password |
| `send_password_reset_link` | Customer requested a password reset |
| `order_add` | Customer placed a new order |
| `order_product_add` | Product added to an order |
| `order_product_remove` | Product removed from an order |
| `order_product_fulfil` | Order product(s) fulfilled / shipped |
| `order_status_change` | Order status changed (e.g., processing → shipped) |
| `order_payment_add` | Manual payment request sent to the customer |
| `order_payment_error` | A payment failed for this order |
| `order_payment_via_bwt` | Bank wire transfer payment instructions |
| `order_payment_via_cod` | Cash-on-delivery payment confirmation |
| `order_payment_via_voucher` | Voucher payment confirmation |
| `order_payment_status_change` | Order's payment status changed |
| `send_order_files_download_link` | Digital-products download link |
| `send_invoice` | Invoice attached / sent |
| `send_credit_notify` | Credit notification |
| `order_leasing` | Leasing / financed order |
| `manual_order` | Order created from the admin panel |
| `abandoned_restore_link` | Abandoned-cart recovery — sends a "come back" link with cart contents (see [[omnichannel-mails-abandoned-cart]]) |
| `customer_newsletter_subscribe` | Customer subscribed to newsletter |
| `customer_newsletter_unsubscribe` | Customer unsubscribed |
| `product_out_of_stock` | Product the customer favourited went out of stock |
| `product_quantity_low` | Low-stock alert for a favourited product |
| `product_review_added` | Customer's review was approved |
| `rate_orders_products` | Post-purchase review-request |
| `remove_account_request` | Customer requested account deletion (GDPR) |
| `account_banned` | Customer account banned by merchant |
| `account_ban_lifted` | Ban lifted |
| `contact` | Contact-form submission (sent to merchant, not customer) |
| `file_download` | File download notification |

Three labels are forced-on regardless of per-mail Active flag (security/auth critical) — see [[omnichannel-mails-toggles-gating]]:

- `email_confirmation` — verification link for new accounts.
- `two_factor_action` — 2FA action notifications.
- `alert_notification` — critical platform alerts.

## Business rules

### Label is the dispatcher key

Every event firing a customer email passes its `label` (e.g., `order_add`) into the send pipeline. The platform looks up the merchant's `Mail` row by `(site_id, label)`, picks the `MailLanguage` for the recipient's locale, and renders. **Label collisions are impossible** — each label is unique per store.

### Recipient is fixed per label

- Order-prefixed labels (`order_*`, `send_invoice`, `send_credit_notify`, `manual_order`, `order_leasing`, `send_order_files_download_link`) → the order's customer.
- Account-prefixed labels (`welcome`, `email_confirmation`, `email_confirmed`, `password_change`, `send_password_reset_link`, `account_banned`, `account_ban_lifted`, `remove_account_request`) → the [[customer]] account.
- `abandoned_restore_link` → the cart's customer OR the email-channel [[subscriber]] linked to the cart.
- `customer_newsletter_*` → the subscriber.
- `product_out_of_stock` / `product_quantity_low` → customers who favourited the product (see [[products-favorite-products]] + [[products-missing-product]]).
- `rate_orders_products` / `product_review_added` → the order's customer.
- `contact` → the merchant (`site_email`), NOT the customer.

The merchant cannot override the recipient or add CC / BCC — see [[omnichannel-mails-customisation-limits]].

### Trigger sources per label group

- `order_*`, `send_invoice`, `send_credit_notify` → [[orders-details]] workflows + [[orders-status-change]]. Note `order_status_change` is a single mail shared by every status — there is no per-status variant.
- `manual_order` → admin-created order with online payment awaiting customer click — see [[orders-notify-customer]].
- `abandoned_restore_link` → the platform-level abandoned-cart job — see [[omnichannel-mails-abandoned-cart]].
- `welcome` / `email_confirmation` / `email_confirmed` / `password_change` / `send_password_reset_link` → customer-account flows on the storefront.
- `product_out_of_stock` / `product_quantity_low` → inventory transitions — see [[inventory-tracking]].

### Each label has its own allowed-variable list

The variable allow-list is per-label, served by `GET /admin/api/core/marketing/customer-mails/{id}/variables`. `welcome` allows account variables but not order variables; `order_*` labels allow order variables but not subscriber variables. See [[omnichannel-mails-variables]] for the full mechanics.

## Related

- [[marketing-omnichannel-mails-list]] — hub.
- [[customer]] — recipient entity for most labels.
- [[subscriber]] — recipient entity for `abandoned_restore_link` and `customer_newsletter_*`.
- [[order]] — data source for order-prefixed labels.
- [[cart]] — data source for `abandoned_restore_link`.
- [[orders-details]] / [[orders-status-change]] / [[orders-invoice]] / [[orders-credit]] / [[orders-payment-manual]] — the workflows that re-fire labelled mails.
- [[orders-notify-customer]] — the per-order `notify_customer` flag gating `order_status_change`.
- [[products-missing-product]] / [[products-favorite-products]] — sources for product-out-of-stock / low-stock labels.

## Open questions

- 📡 **`two_factor_action` and `alert_notification` label trigger surfaces.** Both are forced-on but the exact event-emitting code paths are not yet mapped on the wiki (verify).
