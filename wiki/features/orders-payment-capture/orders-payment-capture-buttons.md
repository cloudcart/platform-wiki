---
type: feature
nav_path: "Orders → Order details → Payment → Capture / Cancel → Buttons & visibility"
route_name: admin.orders.payment.capture
route_path: /admin/orders/action/payment/capture-authorization/:payment_id
aliases: ["Capture button visibility", "Cancel authorization button", "allow_capture_authorization", "Capture cog dropdown", "Full-amount capture", "Sync payment cog item"]
tags: [orders, payment, capture, authorization, visibility, smarty]
plan_gates: ["authorize_payment"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[orders-payment-capture]]. See the hub for the other aspects (provider matrix, amount-exceeds rule, side effects, automatic triggers, API access).

# Payment capture — buttons & visibility

## Purpose

Documents **where the Capture / Cancel buttons appear, when they show, and what they can't do**. Two button surfaces render the same actions, and a 3-state per-payment property (`allow_capture_authorization`) decides whether Capture is offered, hidden, or replaced by an explanatory alert.

## Where to find it

From [[orders-details]] → **Payment action row**, when the payment status is **Authorized**. The same Capture / Cancel actions appear in **two places**:

1. **Primary action row** (large buttons under the payment row) — **Authorize `<amount>`** (gray button) + **Cancel authorization** (red button). These are the prominent CTAs the merchant sees first.
2. **Secondary settings dropdown** — a small cog/settings icon (`<i class="fal fa-cog">`) next to the payment status badge opens a menu with the same actions, each with its own icon: **Capture** (`fa fa-check-circle`, green) and **Cancel authorization** (`fa fa-undo`, red).

Both surfaces call the same routes and produce identical results. The cog dropdown is useful when the primary row is hidden behind another modal or when the merchant prefers a compact UI.

## What the merchant can do here

| Button | Visible when | Action |
|--------|--------------|--------|
| **Authorize `<amount>`** (Capture) | `allow_capture_authorization === true` (gateway-specific check) | Captures the order's **current total** (`<amount>`), which may be **less than** the authorized hold. |
| **Cancel authorization** | Always when payment status is Authorized | Releases the hold. |

The Capture amount in the button label (e.g. *"Authorize 100.00 BGN"*) is the order's **current total** — so after editing the order down, the label reflects the new, lower amount that will actually be charged.

### What the merchant CANNOT do here

- **Type an arbitrary capture amount** — there is no "enter amount to capture" field. The button captures the order's **current total** (the platform keeps the payment amount in sync with the order). **To capture _less_ than was authorized, the merchant edits the order down first** (remove items, reduce quantities / weight, add a discount), then captures — the gateway is charged the reduced total. This is the normal flow for **variable-weight goods** (see [[orders-payment-capture]]). The merchant **cannot capture _more_** than the authorized hold — that is blocked (see [[orders-payment-capture-amount-exceeds]]).
- **Capture an expired authorization** — gateway authorisations expire after a window. Once expired, the Capture button may still render (the platform doesn't always know), but clicking it returns an error from the gateway. The merchant must then ask the customer to re-pay.
- **Re-authorize a cancelled / expired authorization** — there is no merchant-facing button to ask the gateway to re-authorize using a saved card. The saved-card flow happens at the storefront only. The workaround is to ask the customer to re-place the order or pay again via a checkout link.
- **Bulk capture / cancel** — both actions are strictly per-order via the buttons on [[orders-details]]; there is no bulk action on [[orders]]. For dozens of pending authorisations, the merchant works through each order individually or scripts via the API (see [[orders-payment-capture-api-access]]).

## Settings & fields

### Capture-allowed gating

The Capture button shows ONLY when all three hold:

1. Payment status is **Authorized**.
2. The provider supports capture-authorization (platform-side check — see [[orders-payment-capture-provider-matrix]]).
3. The payment's `allow_capture_authorization` is exactly `true`.

### `allow_capture_authorization` — a 3-state property

A per-payment computed property that the gateway integration sets:

| Value | What it means |
|-------|---------------|
| **`true`** (boolean) | Capture is allowed — button visible. |
| **`false`** | Capture not allowed (e.g. gateway not reachable). Button hidden silently. |
| **String** | Capture not allowed AND there is a SPECIFIC reason to show the merchant. The string is rendered as a `danger` alert under the payment row (e.g. *"Authorization expired"*, *"Card on file unavailable"*). |

This 3-state design lets the gateway integration explain *why* capture isn't available, not just hide the button. The one concrete failure case the platform actively surfaces — order total exceeds authorized amount — is documented on [[orders-payment-capture-amount-exceeds]].

### Sync payment item (cog dropdown, Completed state)

For payments in **Completed** state on gateways supporting `sync`, the cog dropdown ALSO shows a **Sync payment** item (`fa fa-refresh notification-orange` icon). Clicking it asks the gateway to re-fetch the payment's current status — useful when a webhook may have been missed or the local status looks stale. Sync does NOT change money flow; it just refreshes CloudCart's record from the gateway. For **Authorized** payments the cog dropdown does NOT include Sync — only Capture + Cancel surface there.

## Business rules

- **Capture charges the order's current total, capped at the authorized hold** — the captured amount is the payment's current amount (kept in sync with the order total), **not** the frozen authorization. Editing the order **down** before capture charges less; the total may **not exceed** the hold (see [[orders-payment-capture-amount-exceeds]]). There is no field to type an arbitrary partial amount — the order total *is* the amount. (Cancel always releases the whole hold.)
- **No expiration tracking on the order page** — the platform does NOT display when the authorisation expires; the Capture button stays visible regardless of how long ago the auth was placed. The merchant should know their gateway's hold window and capture promptly.
- **Permission** — standard `orders` scope (see [[settings-staff]]); no special grant required, unlike `orders.refund`.

### Smarty / jQuery / AJAX

- Buttons use the `js-payment-action` class.
- Click handler issues an AJAX call to the capture / cancel route.
- The confirmation dialog is a browser-style `data-confirm` (keys `order.payment.confirm.authorize` / `order.payment.confirm.cancel_authorization`).
- Success / error feedback via `toastr`.

## Related

- [[orders-payment-capture]] — hub.
- [[orders-payment-capture-provider-matrix]] — which providers pass the platform-side capability check.
- [[orders-payment-capture-amount-exceeds]] — the string-state alert when the order total exceeds the authorized amount.
- [[orders-details]] — parent page (buttons live in the payment action row).
- [[orders]] — parent list (no bulk capture / cancel).
- [[settings-staff]] — orders permission grant.

## Open questions

None.
