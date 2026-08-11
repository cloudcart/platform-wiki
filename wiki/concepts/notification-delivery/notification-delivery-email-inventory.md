---
type: concept
aliases: ["Transactional email inventory", "Customer-facing email types", "SendCustomerNotification labels", "Email template catalogue", "Notification mail labels"]
tags: [notifications, email, templates, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[notification-delivery]]. See the hub for the other aspects (event spine, retry semantics, admin alerts, customer suppression).

# Notification delivery — transactional email inventory

## Definition

The catalogue of **customer-facing transactional emails** CloudCart can send. The platform sends roughly **30 distinct email types** through a shared customer-notification helper — each one fired by its own in-store event, each with its own merchant-customisable template and its own allowed-variable list. These are **transactional** emails (triggered by something the customer or merchant did to a specific order / account), not marketing broadcasts. The merchant edits the templates on [[marketing-omnichannel-mails-list]] and can preview-send each via the **Send example email** button (gated by the `test_mail` plan feature).

This page is the **taxonomy** — the list of what exists and how it is gated. The trigger / queue mechanics are on [[notification-delivery-event-spine]]; the per-template allowed-variable tables live on [[marketing-omnichannel-mails-list]].

## Scope

What this covers:

- The full list of ~30 transactional email labels, grouped by purpose.
- The three labels that bypass the per-mail Active toggle.
- The global `customer_email_notifications` master switch and how it gates the bypass labels.

What it does NOT cover:

- The full allowed-variable table per label — see [[marketing-omnichannel-mails-list]].
- How each email is triggered / queued — see [[notification-delivery-event-spine]].
- Per-order suppression of status-change emails — see [[notification-delivery-suppression]].
- Marketing-campaign (broadcast) emails — those are a different system under Marketing → Campaigns.

## Contrasts

- **Transactional email vs. marketing campaign email**: transactional emails are one-per-event, no segmentation; campaign emails are broadcast to a chosen audience. Different systems, different queues.
- **Per-template Active toggle vs. global master switch**: most labels can be turned off individually; three labels ignore the individual toggle but are still subject to the global `customer_email_notifications` switch.
- **Customer-facing transactional email vs. admin alert email**: the labels here go to the *customer*; `alert_notification` (an admin escalation) goes to the *merchant* — see [[notification-delivery-admin-alerts]].

## Where it applies

- [[marketing-omnichannel-mails-list]] — where the merchant edits each template + sees the allowed variables.
- [[settings-statuses]] — `order_status_change` template fires per status transition.
- [[notification-delivery-suppression]] — per-order `notify_customer` flag that suppresses these at dispatch.
- [[subscriber-vs-customer]] — newsletter subscribe / unsubscribe labels touch the subscriber system.

## The full taxonomy (~30 labels)

**Account / authentication** — `welcome` (new account created), `email_confirmation` (verify your email), `email_confirmed` (confirmation success), `send_password_reset_link`, `password_change`, `remove_account_request` (GDPR deletion request), `account_banned` / `account_ban_lifted`, `cc2fa_email` (two-factor code).

**Order lifecycle** — `order_add` (new order placed), `order_status_change` (status transition), `order_product_add` / `order_product_remove` (line-item edits), `order_product_fulfil` (shipping dispatched), `manual_order` (admin-created order intro), `send_invoice` (invoice attached), `send_credit_notify` (credit note attached).

**Payment-flow** — `order_payment_add` (pay-link request), `order_payment_error` (payment failed), `order_payment_status_change`, `order_payment_via_bwt` (bank-wire instructions), `order_payment_via_cod` (cash-on-delivery), `order_payment_via_voucher`, `order_leasing` (financed-order info).

**Digital fulfilment** — `send_order_files_download_link` (download access for digital products), `send_order_page_access` (private-page access on purchase).

**Marketing-flavoured transactional** — `abandoned_restore_link` (abandoned-cart recovery), `rate_orders_products` (post-purchase review request), `customer_newsletter_subscribe` / `customer_newsletter_unsubscribe`.

**Stock / catalogue** — `product_out_of_stock` (favourited product went OOS), `product_quantity_low`.

**Other** — `contact` (contact-form submission echoed back), `product_review_added`.

## Gating: the master switch and the three bypass labels

Most labels carry a per-mail **Active** toggle on [[marketing-omnichannel-mails-list]] — turn one off and that email stops sending.

Three labels **bypass** the per-mail Active toggle, because they are operationally critical:

- `email_confirmation` (verify your email)
- `two_factor_action` / `cc2fa_email` (two-factor code)
- `alert_notification` (admin escalation — see [[notification-delivery-admin-alerts]])

Even these three are STILL gated by the global `customer_email_notifications` master switch. So:

- Turning off an individual non-critical template → that one email stops.
- The three critical labels ignore the individual toggle → they keep sending.
- Flipping the global `customer_email_notifications` switch off → even the critical labels stop.

See [[marketing-omnichannel-mails-list]] for the full table of allowed variables per label, and [[notification-delivery-suppression]] for the separate per-order `notify_customer` flag that suppresses status-change emails for one specific order.

## Related

- [[notification-delivery]] — hub.
- [[marketing-omnichannel-mails-list]] — template editor + allowed-variable tables + Send example email.
- [[notification-delivery-event-spine]] — the event → job mechanism that fires each email.
- [[notification-delivery-suppression]] — per-order suppression of status-change emails.
- [[notification-delivery-admin-alerts]] — the `alert_notification` label (merchant-facing).
- [[settings-statuses]] — status transitions firing `order_status_change`.
- [[subscriber-vs-customer]] — newsletter subscribe / unsubscribe labels.

## Open Questions

None.
