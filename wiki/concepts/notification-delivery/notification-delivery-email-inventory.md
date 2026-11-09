---
type: concept
aliases: ["Transactional email inventory", "Customer-facing email types", "SendCustomerNotification labels", "Email template catalogue", "Notification mail labels"]
tags: [notifications, email, templates, concepts]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[notification-delivery]]. See the hub for the other aspects (event spine, retry semantics, admin alerts, customer suppression).

# Notification delivery — transactional email inventory

## Definition

The catalogue of **customer-facing transactional emails** CloudCart can send. The platform sends roughly **30 distinct email types** through a shared customer-notification helper — each one fired by its own in-store event, each with its own merchant-customisable template and its own allowed-variable list. These are **transactional** emails (triggered by something the customer or merchant did to a specific order / account), not marketing broadcasts. The merchant edits the templates on [[marketing-omnichannel-mails-list]] and can preview-send each via the **Send example email** button (gated by the `test_mail` plan feature).

This page is the **taxonomy** — the list of what exists and how it is gated. The trigger / queue mechanics are on [[notification-delivery-event-spine]]; the per-template allowed-variable tables live on [[marketing-omnichannel-mails-list]].

## Scope

What this covers:

- The full list of ~30 transactional email labels, grouped by purpose.
- The per-mail Active switch, the locked mails and the global `customer_email_notifications` switch.

What it does NOT cover:

- The full allowed-variable table per label — see [[marketing-omnichannel-mails-list]].
- How each email is triggered / queued — see [[notification-delivery-event-spine]].
- Per-order suppression of status-change emails — see [[notification-delivery-suppression]].
- Marketing-campaign (broadcast) emails — those are a different system under Marketing → Campaigns.

## Contrasts

- **Transactional email vs. marketing campaign email**: transactional emails are one-per-event, no segmentation; campaign emails are broadcast to a chosen audience. Different systems, different queues.
- **Per-template Active switch vs. global master switch**: each label can be turned off individually unless it is locked; the global switch reaches fewer sends than its name suggests.
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

**Marketing-flavoured transactional** — `abandoned_restore_link` (abandoned-cart recovery), `rate_orders_products` (post-purchase review request, defined but never sent), `customer_newsletter_subscribe` / `customer_newsletter_unsubscribe`.

**Stock / catalogue** — `product_out_of_stock` (favourited product went OOS), `product_quantity_low`.

**Other** — `contact` (contact-form submission echoed back). (`product_review_added` is an admin alert of the Product Reviews app, not a customer email.)

## Gating: the Active switch, locked mails and the master switch

Every label has its own **Active** switch on [[marketing-omnichannel-mails-list]] — turn one off and that email stops.

A **locked** mail (its switch disabled, forced on) always sends, ignoring its Active switch and the global switch; the Aftercare acknowledgement is one. `two_factor_action`, `email_confirmation` and `alert_notification` are locked on the merchant-alert side ([[notification-delivery-admin-alerts]]). The customer two-factor code email (`cc2fa_email`) is **not** locked: switched off, the withdrawal form and the checkout login code get no code.

The global `customer_email_notifications` switch applies only to a send that asks for it; the two-factor code email does not — see [[omnichannel-mails-toggles-gating]] (verify for other labels).

See [[marketing-omnichannel-mails-list]] for the full table of allowed variables per label, and [[notification-delivery-suppression]] for the separate per-order `notify_customer` flag that suppresses status-change emails for one specific order.

## Unsubscribe links in notifications

No notification template carries an unsubscribe link. `{$unsubscribe_url}` is a campaign variable: the notification templates neither offer nor fill it in, so typed into one it stays as literal text. A link such as "Unsubscribe" or "Manage notifications" at the foot of a notification comes from Elastic Email, the service behind CloudCart's shared sending account, which adds its own unsubscribe link to mail sent as promotional; its exact wording is Elastic Email's (verify).

- **Since 06.10.2026** only the abandoned-cart reminder (`abandoned_restore_link`) and bulk e-mails to customers go out as promotional; every other notification is sent as transactional, without that link, and still reaches people who unsubscribed through it.
- **Before that date** no mail was marked transactional, so any notification, and a campaign's **Send example email**, could carry the link.
- A store sending through its own [[apps-smtp|SMTP app]] gets no such link.

The page a campaign's own unsubscribe link opens is described on [[storefront-notifications]].

## Related

- [[notification-delivery]] — hub.
- [[marketing-omnichannel-mails-list]] — template editor + allowed-variable tables + Send example email.
- [[notification-delivery-event-spine]] — the event → job mechanism that fires each email.
- [[notification-delivery-suppression]] — per-order suppression of status-change emails.
- [[notification-delivery-admin-alerts]] — the `alert_notification` label (merchant-facing).
- [[settings-statuses]] — status transitions firing `order_status_change`.
- [[subscriber-vs-customer]] — newsletter subscribe / unsubscribe labels.
- [[storefront-notifications]] — the subscription page behind a campaign's unsubscribe link.

## Open Questions

None.
