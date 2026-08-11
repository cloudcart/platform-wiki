---
type: feature
nav_path: "Orders → Order details → Payment → Mark as paid → Form"
route_name: admin.orders.payment.mark_paid
route_path: /admin/orders/action/payment/mark_paid/:payment_id
aliases: ["Mark as paid form", "Provider reference ID", "Complete order payment modal", "Mark-paid visibility", "Mark-paid surfaces"]
tags: [orders, payment, manual-payment, offline, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-payment-mark-paid]]. See the hub for the other aspects (post-paid pipeline, status-flip rules, adjacent actions, API position).

# Mark as paid — the form & visibility

## Purpose

This aspect covers the visible side of the action: **when** the *Mark as paid* button appears, **where** it appears on the order details page, the single-field modal it opens, and the rules around the one field it carries (`provider_reference_id`). The cascade that fires after Save is on [[orders-mark-paid-pipeline]].

## Where to find it

From [[orders-details]] → **Payment action row**, when the payment is:

1. **Offline type** (`isType('offline')` — bank transfer, COD, manual, voucher, etc.).
2. **Pending status** OR **Requested status** with a non-credit type.

The button label is *"Mark as paid"* (`order.action.mark_as_paid`). It opens as a **modal** (not inline AJAX).

Route: `/admin/orders/action/payment/mark_paid/{payment_id}`:
- GET → renders the form modal (`payment/complete-form.tpl`).
- POST → marks the payment as paid.

### Two surfaces — primary button + cog-dropdown secondary action

Like the other payment actions, **Mark as paid** appears in **two places** on the order details page:

1. **Primary action row** — the prominent gray "Mark as paid" button under the payment row (`payment/action.tpl`).
2. **Cog-dropdown secondary actions** — a small settings icon next to the payment status badge opens a menu containing **Mark as paid** with a green `fa fa-check-circle` icon (`payment/details_action.tpl`).

Both surfaces route through the same modal — pick whichever the merchant prefers.

## What the merchant can do here

### Open the Mark-as-paid form

Click **Mark as paid** → a modal slides in with title *"Complete order payment - `<Provider name>`"* (translated, e.g., *"Complete order payment - Bank transfer"*).

The form contains ONE field:

| Field | Required | Notes |
|-------|----------|-------|
| **Provider reference ID** (`provider_reference_id`) | Optional | The transaction reference for the offline payment — e.g., bank-transfer reference number, COD receipt code, voucher ID. Helps the merchant cross-reference with their bank statement / courier report. |

A help text under the field explains its purpose (`order.help.order_payment_provider_reference_id`).

### Save

Click Save → the form submits via AJAX:
1. The platform stores the `provider_reference_id` on the payment record.
2. Sets the payment's status to **completed**.
3. Syncs the payment (which may trigger gateway-side reconciliation if applicable).
4. Fires the order's post-paid hooks — the heavyweight cascade detailed on [[orders-mark-paid-pipeline]].
5. Toast confirms success.
6. The modal closes; the order details page refreshes.

### What the merchant CANNOT do here

- **Mark an online payment as paid** — the action is hidden for online providers (Stripe / PayPal / etc.). For those, the platform listens to webhook events and marks payment automatically; a manual override would conflict with reconciliation.
- **Specify a partial amount** — the action marks the FULL payment as paid. For partial payments, the merchant uses multiple payment records via the Change Provider workaround (see [[orders-mark-paid-adjacent-actions]]).
- **Skip the modal** — there's no one-click "Mark paid" that bypasses the reference input. The modal always opens.
- **Mark a payment that's already in a terminal state** (Completed / Refunded / Cancelled).

## Settings & fields

### Offline payment types

The platform's payment-type taxonomy includes (verify exact strings):
- `offline` — bank transfer, manual.
- `cod` — cash on delivery.
- `voucher` — pre-paid voucher / gift card.
- (Others depending on installed apps.)

The action is visible when the payment provider's `type` matches `offline`.

### Modal layout

The modal uses the platform's standard modal scaffolding (with built-in Save / Cancel buttons in the footer). Body is a single form with one field as above.

### Smarty + jQuery + AJAX modal

- Button uses `js-payment-action` with `modal: true` flag.
- Click handler: opens the modal via `data-modal-ajax`.
- Form submission: `ajaxForm` (no full-page reload).
- Success: toast + modal close + parent panel refresh.

## Business rules

### Reference ID is free-text — no format validation

The platform stores the typed `provider_reference_id` AS-IS — no length check, no format mask, no sanitisation. The merchant can type any string (bank reference, courier slip code, "received cash", or leave blank). The form has no client-side validation either.

### Reference ID IS searchable from the orders list

The platform's global search includes `provider_reference_id` in the matching clauses. So when the merchant types a bank reference / COD slip code in the orders search box, matching orders DO surface. This is the platform's built-in reconciliation path.

### Single form field — same for all offline providers

There is ONE generic field (`provider_reference_id`). No per-provider customisation — bank transfer, COD, voucher, and any other offline type all see the same single text input. Provider-specific labelling is achieved only via the modal title.

### Reference ID storage and visibility

The optional `provider_reference_id` is stored on the payment record. It's visible later in:
- [[orders-details]] payment row (when expanded via View more / details).
- Payment Details popup on [[customers-details-payments]].

It is NOT pushed to any gateway — there's no external system to push it to for offline payments. It's purely the merchant's internal cross-reference.

## Related

- [[orders-payment-mark-paid]] — hub.
- [[orders-mark-paid-pipeline]] — what Save triggers (post-paid cascade).
- [[orders-mark-paid-adjacent-actions]] — the Sync / Lease buttons that occupy the same payment row for non-offline / credit payments.
- [[orders-details]] — parent page (button in payment action row).
- [[customers-details-payments]] — where the reference ID surfaces later.
- [[settings-payment-providers]] — offline payment provider list.

## Open questions

None.
