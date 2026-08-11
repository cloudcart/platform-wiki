---
type: feature
nav_path: "Orders → Order details → Notify customer → Manual re-send"
route_name: admin.orders.notify-customer
route_path: /admin/orders/action/other/:order_id/notify-customer
aliases: ["Re-send customer email", "Manual resend", "Resend invoice", "Resend confirmation", "Resend download link", "Изпрати отново имейл"]
tags: [orders, notification, customer, email]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-notify-customer]]. See the hub for the other aspects (the toggle, suppression scope, send-URL flow).

# Notify customer — manual re-send by email type

## Purpose

The [[orders-notify-customer-toggle]] only suppresses FUTURE automated emails — it never re-sends. To MANUALLY re-fire a transactional email that was already sent (or was suppressed while the toggle was OFF), the merchant uses a different per-email-type path. This page is the lookup table mapping each customer email to the action that re-sends it, plus the rule for how the toggle gates each path.

## Where to find it

There is no single "re-send" button on [[orders-details]]. Each email type re-sends from its own screen / action (invoice from [[orders-invoice]], credit note from [[orders-credit]], abandoned-cart link from [[orders-abandoned]], etc.) — see the table below.

## What the merchant can do here

Re-fire a specific transactional email by taking the matching action below. The merchant CANNOT trigger customer-account emails (welcome / password reset / 2FA / email confirmation) from the admin — those are customer-initiated from the storefront account area only.

## Settings & fields

### Re-send paths by email type

| Email type | How to re-send | Mail label |
|------------|---------------|------------|
| Order confirmation | Re-apply the same status via [[orders-status-change]] (with the toggle ON) | `order_add` / `order_status_change` |
| Payment-request / checkout-resume link | Click **Send as email** on the draft alert ([[orders-notify-customer-send-url]]) OR re-trigger via [[orders-payment-manual]] | `manual_order` / `order_payment_add` |
| Invoice | Re-issue from [[orders-invoice]] → **Send to customer** | `send_invoice` |
| Receipt | Re-issue from [[orders-receipt]] | `send_invoice` (receipt variant) |
| Credit note | Re-issue from [[orders-credit]] | `send_credit_notify` |
| Shipping / fulfillment notification | Set fulfillment status to `not_fulfilled` and back to `fulfilled` (or click a related shipping-provider action) | `order_product_fulfil` |
| Digital-product download link | Re-trigger via order status → `paid` / `completed` | `send_order_files_download_link` |
| Abandoned-cart restore link | Use [[orders-abandoned]] → **Send restore link** (per-cart or bulk) | `abandoned_restore_link` |
| Welcome / password reset / 2FA / email confirmation | Customer-initiated only (from storefront account area); merchant CANNOT trigger from admin | `welcome` / `send_password_reset_link` / `cc2fa_email` / `email_confirmation` |

## Business rules

### Toggle gates the status-driven re-sends

For any order-scoped re-send that runs through a status transition or an automated dispatch (confirmation, payment link, fulfilment, digital link), the [[orders-notify-customer-toggle]] must be ON or the path suppresses — see [[orders-notify-customer-suppression-scope]] for the full suppressible set. So if a re-send "does nothing", the first thing to check is whether `notify_customer = no`.

### Explicit sends bypass the toggle

The explicit document sends — **Send invoice** ([[orders-invoice]]), **Send receipt** ([[orders-receipt]]), **Send credit note** ([[orders-credit]]) — are direct merchant actions, NOT status-driven dispatches, so they fire regardless of the per-order `notify_customer` flag. The store-wide `customer_email_notifications` kill switch on [[settings-cart]] still applies to them, however.

### Re-applying a status re-sends the status email

Re-applying the same status (e.g. Paid → Paid via [[orders-status-change]]) re-fires that status's notification email, provided the three gates pass. This is the canonical way to re-send an order-confirmation / status email — there is no dedicated "re-send confirmation" button.

### Fulfilment re-send needs a status round-trip

There is no direct "re-send shipping notification" button. The merchant toggles fulfilment to `not_fulfilled` and back to `fulfilled` to re-fire the `order_product_fulfil` email (toggle ON required).

## Related

- [[orders-notify-customer]] — hub.
- [[orders-notify-customer-toggle]] — the flag that gates the status-driven re-sends.
- [[orders-notify-customer-suppression-scope]] — which emails the flag suppresses vs bypasses.
- [[orders-notify-customer-send-url]] — the payment-link / checkout-resume re-send.
- [[orders-status-change]] — re-applying a status re-fires its email.
- [[orders-invoice]] — invoice re-send.
- [[orders-receipt]] — receipt re-send.
- [[orders-credit]] — credit-note re-send.
- [[orders-payment-manual]] — payment-request re-trigger.
- [[orders-abandoned]] — abandoned-cart restore-link re-send.
- [[settings-cart]] — kill switch still applies to explicit sends.

## Open questions

None.
