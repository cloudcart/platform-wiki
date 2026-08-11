---
type: feature
nav_path: "Orders → Details → Payment"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order payment row", "Payment action row", "Change payment provider", "Mark paid", "Capture authorization", "Cancel authorization", "Payment refund", "Mokka confirm", "Klear confirm", "Payment details", "Payment View more", "Payment log", "Full LOG", "Лог на плащанията", "Истор на плащанията"]
tags: [orders, order-details, payment, refund, capture, mark-paid, payment-log]
plan_gates: ["authorize_payment"]
created: 2026-06-10
updated: 2026-08-06
source_count: 5
---

> Part of [[orders-details]]. See the hub for the other aspects (header, products, addresses, shipping, history, actions, known issues).

# Order details — Payment

## Purpose

The **Payment action row** in the main column of the order details page surfaces the payment provider, the current payment status, primary action buttons (mark paid, sync, capture / cancel authorisation, refund, manual confirm, lease), a cog dropdown with secondary actions, and an inline **View more** panel with the full payment record. A separate sub-row appears for BNPL providers (Mokka, Klear) awaiting platform-side confirmation. Each action has its own detail page, linked inline.

## Where to find it

Main column of `/admin/orders/details/<order_id>`, below the products table, alongside the **Shipping** + **Fulfillment** rows. Rendered whenever the order has a payment record.

## What the merchant can do here

- Provider icon + name.
- **Change provider** dropdown (when status allows) — gating under "Business rules".
- Primary action button(s) — depend on payment status (table below).
- Cog icon → secondary actions dropdown (table below).
- **View more** link → inline expansion of the full payment record.
- **Authorized amount row** (capture-style payments only): formatted authorised amount + the primary capture action.
- **Mokka / Klear confirm row**: appears for BNPL orders with status `paid` or `completed` and a missing provider confirmation flag. Surfaces a **Confirm** button opening the manual-confirmation modal.

### Primary action button — by payment status

| Payment status | Primary action(s) |
|---|---|
| `authorized` (authorisation hold) | **Capture authorization** (formatted amount in label) + **Cancel authorization** — both only if the gateway supports `captureAuthorization`. Capture is hidden if `allow_capture_authorization` is not strictly `true`. Full flow: [[orders-payment-capture]]. |
| `completed` (paid) | **Refund** (only if admin has `orders.refund` permission AND provider supports refund). On a **returnable** order this opens the return modal, not a plain refund — see Business rules and [[orders-details-returns]]; otherwise [[orders-payment-refund]]. |
| `requested` / `pending` (offline) | **Mark as paid** (opens the offline-payment modal below). Full flow: [[orders-payment-mark-paid]]. |
| Other statuses | No primary action. |

### Cog dropdown — secondary actions by status

| Payment status | Secondary actions surfaced |
|---|---|
| `authorized` | **Capture** + **Cancel authorization**. |
| `completed` | **Refund** + **Sync** (only if provider supports `sync` — re-queries the gateway for the latest status). |
| `requested` / `pending` | **Mark as paid** + **Lease** (only when payment is type=credit and provider is NOT `fusion_pay` / `klear` / `dsk_bnpl` / `fibank_bnpl` — re-sends the leasing email). |
| `cancelled` | **Sync** (only if provider supports sync). |
| Other statuses | No secondary actions. |

### Mark-as-paid modal (offline payments)

Triggered by **Mark as paid**. POSTs to `admin.orders.payment.mark_paid`. One field: **Provider reference ID** (`provider_reference_id`, text input, prefilled with the existing value) — the bank-transfer reference, cheque number, or any provider-side ID for cross-referencing. Full flow: [[orders-payment-mark-paid]].

### Mokka / Klear manual-confirmation modal

Triggered by **Confirm** in the Mokka / Klear sub-row. POSTs to `admin.orders.payment.manual`. One field: **Document number** (`document_number`, text input, autofocused, prefilled with the next invoice number when available). Full flow: [[orders-payment-manual]].

### Payment details inline panel (View more)

An inline expansion (not a modal) showing a read-only payment table: payment number (`site_reference_id`), `provider_reference_id`, last-update date / time, payment status badge, and formatted amount. The payment-actions cog (same secondary-action list as above) is nested inside this panel. For pending payments (`is_not_paid`), the panel auto-opens on load.

When the gateway has rich `provider_data` (transactions, auth codes), a **Full LOG** link is surfaced top-right of the panel — opens the per-payment request/response log (route `admin.orders.payment.log`) in a new tab.

### Payment Log (Full LOG link)

The single place to read the **full request/response history** the platform exchanged with the provider for one order — covers both **card-gateway exchanges** (authorize / capture / refund / sync / 3DS callbacks to the bank) and **BNPL request exchanges** (loan-application / status-poll / confirm / refund calls to the lender), in one unified timeline. To reach it: open the order, scroll to the **Payment** row, click **View more**, then **Full LOG**. Each entry shows **Date**, **Action**, **Sender**, **Receiver**, **REQUEST** body, **RESPONSE** body, separated by `=========================`.

**Supported provider allowlist** — the Full LOG link is only rendered for these 14 provider keys (verified 2026-06-10): card gateways `borica_way4`, `raiffeisen`, `dsk_bank`, `nestpay`, `euplatesc`, `cardlink`, `cib_bank`, `btepos`, `icard`; BNPL providers `iute`, `payapp`, `dsk_bnpl`, `fibank_bnpl`, `plati_posle`. Other providers (Stripe, Braintree, EveryPay, Mokka, FusionPay / Klear, TBI Bank, SmartUcf, Mollie, PayPal, etc.) write to the same log but the **Full LOG** link is NOT surfaced — only CloudCart staff can read those entries directly.

## Settings & fields

The payment row reads from the order's payment record. The visible action set is computed from the payment status, the provider's capability flags (`captureAuthorization`, `refund`, `sync`, `allow_capture_authorization`), and the merchant's permissions (`orders.refund` for Refund).

The selectable providers in **Change provider** are gated by:

- [[settings-payment-providers]] — installed + enabled providers for the store.
- `manual_order_payments` setting on [[settings-cart]] — for drafts, only providers whose codes are in this list are surfaced.

## Business rules

### Payment provider dropdown — gated by `manual_order_payments`

The provider select omits providers by order type:

- **Storefront-created orders** (`is_draft = null`): all installed providers (except `tbi`).
- **Manual-created draft orders** (`is_draft = 1`): only providers whose codes are in `manual_order_payments` (on [[settings-cart]]); if the setting is null, all are listed.

The dropdown is also auto-DISABLED when the order has no products yet, or no shipping configured (for non-digital orders).

### Payment provider dropdown — filtered by digital + shipping type

On top of the gating above, the offered providers are filtered by the order's **contents** and **shipping type** — so the merchant can't always switch to every installed method:

- **Digital-only order** → only **online** payment providers are listed; offline methods (Cash on delivery, bank transfer) are hidden, since a digital order has nothing to collect on delivery.
- **Local-pickup (marketplace) shipping** → **Cash on delivery is hidden**, and the pay-on-pickup provider (`pop`) appears **only** for marketplace shipping (it's hidden for normal courier shipping).

This is why a method that exists on the store can still be missing from a specific order's Change-provider dropdown — the order's digital-ness and shipping type narrow the list.

### Payment provider dropdown — locked after certain statuses

The dropdown is HIDDEN once the order reaches any of `authorized`, `completed`, `paid`, `refunded` — or once fulfillment is done. The provider is then locked.

### Refund permission

**Refund** requires the `orders.refund` permission on the admin's role AND a gateway that supports refund. Without either, the button is hidden even on a `completed` payment. See [[settings-staff]].

### The Refund button does TWO different things

Same red **Refund** label, two behaviours, decided by whether the order is **returnable** (invoiced or ready to be, not already fully returned, not in a negative status):

- **Returnable** → clicking **Refund** opens the **full return modal**, pre-set to the *By card* refund method. The merchant ends up creating a return record — which is what drives the restock and the credit note. See [[orders-details-returns]].
- **Not returnable** → clicking **Refund** fires the direct gateway refund behind a plain confirmation dialog. See [[orders-payment-refund]].

Merchants who expect "one click = money back at the gateway" are surprised by the modal. It is the intended path: refunding an invoiced order without a return would leave the fiscal documents inconsistent.

### Authorization auto-cancel on negative status

When the merchant moves an order to ANY negative status (cancelled / refunded / voided / failed / chargebacked / disputed / timeouted) AND there's an outstanding authorisation hold, the platform automatically cancels the authorisation with the provider. No need to click **Cancel authorization** first.

### Capture authorization is plan-gated

The capture flow requires the `authorize_payment` plan-feature — see [[orders-payment-capture]].

### Mokka / Klear confirmation is a separate flow

Mokka and Klear BNPL providers route through a manual-confirmation modal distinct from **Mark as paid**. It asks for a document number (typically the invoice number) and POSTs to `payment.manual`. Used only after the lender approves the customer's BNPL application. See [[orders-payment-manual]].

### Lease action is one-click

The **Lease** action (cog dropdown, credit-type providers) re-sends the leasing-application email to the customer. No modal — just a toast *"Leasing request sent successfully"*. Used for consumer-credit providers.

### `order.updated` webhook fires on every payment action

Every action that changes the payment status (mark-paid, refund, capture, cancel-authorisation, manual-confirm) fires the `order.updated` webhook via [[settings-hooks]]. Receivers must be idempotent.

## Related

- [[orders-details]] — hub.
- [[orders-payment-mark-paid]] — canonical Mark-as-paid detail page.
- [[orders-payment-refund]] — canonical Refund detail page (the non-returnable path).
- [[orders-details-returns]] — the return modal the Refund button opens on a returnable order.
- [[orders-payment-capture]] — canonical Capture-authorisation detail page (plan-gated by `authorize_payment`).
- [[orders-payment-manual]] — canonical Mokka / Klear manual-confirmation page.
- [[orders-sync-cod]] — COD-sync sub-action that pairs with the payment row.
- [[orders-status-change]] — status-change side effects (auth auto-cancel etc.).
- [[settings-payment-providers]] — provider catalogue + capability flags.
- [[settings-cart]] — `manual_order_payments` (draft-order provider whitelist).
- [[settings-staff]] — `orders.refund` permission.
- [[settings-hooks]] — `order.updated` webhook.

## Open questions

None.
