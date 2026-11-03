---
type: feature
nav_path: "Payment Providers → ePay One Touch"
route_name: apps.epay_one_touch.settings
route_path: /admin/payment-providers/epay_one_touch
aliases: ["ePay One Touch", "EpayOneTouch", "ePay 1-click", "ePay one-click", "ePay token", "ePay saved card", "ePay one-touch"]
tags: [paymentproviders, payment-providers, epay-one-touch, epay, wallet, bulgaria, save-card]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# ePay One Touch

## Purpose

A configuration screen for **ePay One Touch** — the one-click variant of the ePay.bg gateway that lets returning customers pay without re-entering credentials. On the first checkout the customer authorizes their ePay account once; CloudCart stores an ePay token tied to the customer record; subsequent checkouts charge that token automatically, skipping the ePay redirect entirely.

This is a separate provider (provider key `epay_one_touch`) from the base [[payment-providers-epay]] gateway — different routes, different credentials, different flows. The base ePay always redirects to the ePay site; ePay One Touch redirects on FIRST purchase and then becomes silent (one-click) for the same returning customer.

## Where to find it

Payment Providers → **ePay One Touch**. Provider key: `epay_one_touch`. Route name `apps.epay_one_touch.settings`, path `/admin/payment-providers/epay_one_touch/settings`.

## What the merchant can do here

- **Toggle Test / Live mode** (separate Mode switch, same Mode field as base ePay).
- **Enter the ePay One Touch credentials**: APP ID, Secret, KIN. All three required.
- **See the read-only Return URL** that must be entered in the ePay One Touch merchant application configuration.
- **Customer-facing title** override.
- **Logo override**.
- **Per-provider discount / fee** ([[discount]]).
- **From / To availability window**.
- **Active toggle**.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** switch | Test → ePay One Touch demo endpoint. Live → production. | `mode=test` after install | Stored as `configuration.mode`. Shares the help text "Use test mode to test your connection. Live mode is for the actual payment processing. Use live mode when you have verified your credentials." |
| **APP ID** | ePay One Touch application identifier — issued by ePay when the merchant registers their one-touch application. | required | Stored as `configuration.app_id`. Source label: *"APP ID"*. Validation error: "APP ID is required". |
| **Secret** | Shared secret for signing one-touch payment requests. | required | Stored as `configuration.secret`. Source label: *"SECRET"*. Validation error: "Secret is required". |
| **KIN** | ePay customer number (same as base ePay's KIN — the merchant's identifier in ePay). | required | Stored as `configuration.kin`. Validation error: "KIN is required". |
| **Return URL** (read-only) | The URL the merchant must register with ePay so ePay knows where to redirect the customer back after the first-time authorization. | `<cc_payments-domain>/return/provider/epay_one_touch` | Auto-generated. |

## Business rules

### Two distinct flows — first purchase vs. returning customer

On purchase, the integration first checks if the current customer already has a stored ePay One Touch card (via the platform's save-card mechanism):

- **Customer has a saved card** → an auto-purchase runs. The platform charges the stored token directly with no redirect. The customer sees the order-success page immediately. The platform then polls ePay's status up to 5 times (every 2 seconds) until the payment moves out of `pending` into `completed` / `failed` / `cancelled`.

- **Customer does NOT have a saved card** → CloudCart asks ePay for a payment request URL and redirects the customer to ePay. The customer authorizes (logs in, picks a card, agrees to save it). ePay redirects back to the Return URL. If the customer ticked "save card", a card token is stored against their customer record for next time.

### Saved card is bound to the customer record (not the order)

The ePay token (plus device and payment instrument) is stored on the customer record under `epay_one_touch`. The token is reused across orders — the customer doesn't see the ePay redirect again as long as the token remains valid on ePay's side. **Guest customers cannot save a card** — the save flow only runs for logged-in customers, so guest orders always redirect through ePay even on repeat purchases.

### Polling instead of webhook for confirmation

Unlike base ePay (which is IPN-driven), ePay One Touch confirms payment by **polling** ePay, not from an asynchronous notification. After the customer returns from ePay (or after the auto-purchase), the platform checks the payment status up to 5 times, every 2 seconds — a maximum of 10 seconds while the customer waits on the order-success page. If the payment is still `pending` after 10 seconds, polling gives up: the merchant sees the order in `pending`, and the platform re-syncs only when the next operation (e.g., a manual sync trigger) runs.

### ePay status code mapping

ePay One Touch's response includes a `payment.STATE` integer code:

| ePay STATE | CloudCart status |
|------------|------------------|
| 2 | `pending` |
| 3 | `completed` |
| 4 | `cancelled` |
| (anything else) | `requested` |

Special handling:
- `response.status == 'ERR'` → `failed`
- `response.msg == 'EXPIRED'` → `timeouted`
- `response.msg == 'NOT PAID'` → `cancelled`

### Currency: BGN only

Like base ePay, ePay One Touch processes in **BGN**. The integration passes the cart amount as-is, with no currency conversion. Non-BGN stores cannot effectively use this provider.

### Order ID in the ePay description

The payment description sent to ePay is `Order #<order_id> / <site_url>`, where `<order_id>` is either the order's increment hash (if the store's Order ID display setting is `increment_hash`) or the raw order ID. This is what the customer sees in their ePay receipt / account history.

### Return URL configuration

The merchant must configure the Return URL — shown read-only on this settings page as `<cc_payments-domain>/return/provider/epay_one_touch` — in their ePay One Touch application registration. Without this, the customer returns to a 404 on the ePay side after their first authorization.

### Refund

Refunds are not supported through CloudCart for ePay One Touch. As with base ePay, refunds are handled in the merchant's ePay dashboard, then marked Refunded in CloudCart manually.

### Cancel an in-flight payment

If the customer abandons before ePay returns, the platform transitions the payment from `initiated/requested/pending` → `cancelled` on the next platform call (e.g., when the merchant manually cancels the order).

### Permission

Requires `store.payment_providers`.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-epay]] — the base ePay gateway (different flow, separate provider, full redirect every time).
- [[payment-providers-epay-worldwide]] — ePay's international card processor (separate).
- [[settings-payment-providers]] — install/uninstall.
- [[customer]] — the saved ePay token lives on the customer record (`epay_one_touch` attribute).
- [[orders-payment-refund]] — manual Refund.
- [[discount]] — per-provider fee/discount.
- [[checkout-flow]] — first-purchase redirect vs. returning-customer one-click branching.

## Open questions

- ⏸️ One-touch token TTL — ePay may reject an expired token at payment time. The exact token lifetime is set by ePay (not encoded in CloudCart); merchants should ask ePay support if customers report repeated failures on saved one-touch tokens.
