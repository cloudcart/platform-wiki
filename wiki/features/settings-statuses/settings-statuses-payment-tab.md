---
type: feature
nav_path: "Settings → Statuses → Payment"
route_name: payment-statuses
route_path: /admin/settings/statuses/payment
aliases: ["Payment statuses tab", "Payment status taxonomy", "Status of payment", "Статуси на плащания"]
tags: [settings, statuses, payment]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-statuses]]. See the hub for the other taxonomies (orders, shipping) and the cross-cutting mechanics (rename, custom codes, delete protection, permissions).

# Statuses — Payment tab

## Purpose

The Payment tab of [[settings-statuses]] is the management surface for the **payment status taxonomy** — the low-level state of payment processing on an order (authorized, captured, refunded, voided, etc.). It is the largest of the three built-in lists (**13** statuses) but the most restricted in terms of merchant writes: **rename-only** (no Add, no Delete). The merchant uses this tab to make payment states read in business language ("Held for review" instead of `held`) rather than in the gateway's native terms.

## Where to find it

Sidebar → Settings → **Statuses** → **Payment** tab. Route: `/admin/settings/statuses/payment`.

## What the merchant can do here

- See all 13 built-in payment statuses listed with their current merchant-facing labels.
- **Rename** any one by typing inline in the "New status name" column. Per-row Save button appears when the value differs from saved; click to commit. No auto-save on blur or Enter — same inline-edit UX as the Orders tab; see [[settings-statuses-orders-tab]].

What the merchant **cannot** do on this tab:

- **No Add.** The `+ Add status` button is **hidden** on this tab. The payment taxonomy is platform-defined and cannot be extended — payment states are set automatically by CloudCart based on payment-gateway callbacks. A custom payment status would have no gateway to set it. (If the modal is invoked via a routing quirk, the client-side defensive check fires toast *"Only order statuses can be created"*; the backend route returns 404 for `POST /statuses/payment/create` due to the route-level `->where('type', 'order')` constraint on Create — see [[settings-statuses-permissions-validation]].)
- **No Delete.** The Actions column does not render trash icons on this tab — built-in payment statuses are non-deletable.
- **No reorder.** The platform's order is fixed.
- **Cannot manually change the payment status on an order from this tab — or from the order details page.** Payment statuses are driven by gateway callbacks and the order lifecycle; the merchant cannot flip them by hand. This tab only controls the *display label* of those gateway-set states.
- **Cannot change the underlying status code.** Only the display label.

## Settings & fields

| Column | Shows | Editable? | Notes |
|--------|-------|-----------|-------|
| **Current status name** (`translation`) | The original translated label (e.g., "Изчакваща" for `pending` via `payment.status_<code>`). | No | Read-only display of the platform's default for the active locale. |
| **New status name** (`new_name`) | The merchant's custom rename, or empty if unset. | Yes (inline) | Per-row Save button commits via `PATCH /statuses/payment/update`. No auto-save on blur. |
| **Actions** | _(empty on this tab)_ | n/a | Trash icons not rendered — built-in statuses cannot be deleted. |

No modal. No bulk save. Each rename is its own API call.

## Business rules

### The 13 built-in payment statuses (in display order)

`authorized`, `initiated`, `requested`, `pending`, `held`, `completed`, `failed`, `refunded`, `voided`, `cancelled`, `timeouted`, `chargebacked`, `disputed`.

Each one corresponds to a phase of the gateway-driven payment lifecycle:

- `authorized` — the gateway has reserved (but not captured) the funds.
- `initiated` / `requested` — the merchant or storefront has asked the gateway to start a transaction.
- `pending` — the gateway has not yet returned a definitive outcome.
- `held` — the gateway has flagged for manual review.
- `completed` — funds successfully captured.
- `failed` — the gateway returned a hard failure.
- `refunded` — funds returned to the customer post-capture.
- `voided` — an authorization was released without capture.
- `cancelled` / `timeouted` — the transaction was aborted before completion.
- `chargebacked` / `disputed` — the customer has reversed the charge through their bank.

Five of these (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`) are flagged as **gateway-driven** elsewhere in the platform — see [[orders-status-change-api]] for how the JSON-API v2 layer hides them from the writable surface.

### Renames are display-only

Webhooks, exports, JSON-API v2 reads, and any code referencing a payment status sees the unchanged code (e.g., `completed`, `refunded`). Only the human-facing label in the admin / customer emails / invoice templates changes. This means a merchant can rename `chargebacked` to "Disputed by customer" without breaking any external integration.

### Rename is a translation override

Same mechanic as Orders / Shipping: the platform stores `(type=payment, status=<code>, name=<custom>)` in the status-override table. Platform reads override first; falls back to `payment.status_<code>` otherwise. Clearing the field and saving deletes the override row. See [[settings-statuses-rename-mechanic]] for the full precedence story vs [[settings-translations]].

### Why no Add — payment is gateway-driven

Payment states change only in response to gateway callbacks (or admin actions like capture / refund on [[orders-payment-capture]]). The merchant can't define a "Waiting for bank wire" custom payment status that the platform would know how to set — there'd be no event source to drive transitions into or out of it. The merchant who wants finer payment-tracking should use **order status** custom statuses (e.g., a custom order status "Awaiting bank wire") and leave the payment taxonomy alone. See [[settings-statuses-orders-tab]].

### Backend write path

`PATCH /statuses/payment/update` is the only mutating endpoint exposed for this tab. The Form Request layer validates: `status` required (the status code being renamed), `type` must be `payment` (rejected as *"Invalid type"* otherwise). No name uniqueness, no length cap. Full validation on [[settings-statuses-permissions-validation]].

### Default Bulgarian label sample

- `payment.status_pending` → "Изчакваща"
- `payment.status_completed` → "Завършена" *(verify)*
- `payment.status_refunded` → "Възстановена" *(verify)*

Many English-locale defaults are empty strings — merchants on English-language stores typically rename here to get a readable label.

## Related

- [[settings-statuses]] — hub.
- [[settings-statuses-rename-mechanic]] — how renames are stored as overrides; precedence vs [[settings-translations]].
- [[settings-statuses-permissions-validation]] — server-side validation + the route-level `type` constraint that gates Create / Delete out of this tab.
- [[payment-status]] — entity page.
- [[orders-payment-capture]] — admin-driven payment actions (capture, void, refund) that change the payment status.
- [[orders-status-change-api]] — the five gateway-driven payment statuses that the JSON-API v2 layer hides.
- [[settings-invoicing]] — `credit_payment` rule references payment statuses on the credit-note tab.

## Open questions

- Exact English-locale defaults for several payment status keys. *(verify)*
- Whether the `cancelled` payment status is reachable in practice or is a legacy state. *(verify)*
