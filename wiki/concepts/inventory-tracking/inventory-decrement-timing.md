---
type: concept
nav_path: "Concept → Inventory tracking → Decrement timing"
aliases: ["Inventory decrement timing", "Stock decrement timing", "order_status_for_quantity_decrease", "Paid vs pending decrement", "When does stock drop", "Decrement matrix"]
tags: [catalog, inventory, stock, orders, decrement, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (variant model, restock, oversell, bundle stock, multi-warehouse, in-stock badge, debugging playbook).

# Inventory — decrement timing

## Definition

The single most consequential inventory setting in the platform is **`order_status_for_quantity_decrease`** on [[settings-cart]] (the "I want to decrease product quantity when the status is" dropdown). It picks **when** stock comes off the Variant's `quantity` count along the order lifecycle:

- **`paid`** (default) — stock decrements ONLY when the order reaches `status = paid` AND `status_fulfillment = fulfilled`. Orders sitting in `pending` (awaiting payment) do NOT touch stock. Two customers can place pending orders against the same last unit; whichever pays first wins the inventory.
- **`pending`** — stock decrements at order submission, when the order first hits `status = pending` AND `status_fulfillment = fulfilled`. Order placement immediately reserves stock; even unpaid orders block the inventory until the order is cancelled.

The setting applies to **all** orders on the store — it is not per-product or per-customer.

## Scope

Covered:

- The `order_status_for_quantity_decrease` setting and its two values.
- Merchant guidance per payment-method mix (mostly-paid checkouts vs cash-on-delivery dominant).
- The deterministic decrement matrix per (status × fulfillment × setting).
- The `fulfilled` requirement that gates decrement even at `paid` / `pending`.

Not covered here:

- How stock returns on cancellation / refund — see [[inventory-restock]].
- Oversell semantics (decrement clamping at 0) — see [[inventory-oversell]].
- The full per-line decrement-tracking flag mechanics — see [[inventory-restock]].
- How to investigate "stock changed unexpectedly" tickets — see [[inventory-debugging-playbook]].

## Contrasts

- **`paid` decrement vs `pending` decrement** — `paid` (default) reserves stock only after the customer's payment clears; `pending` reserves at submission. Stores with mostly-paid checkouts (Stripe / card-on-file) typically pick `paid`; cash-on-delivery-dominant stores typically pick `pending` to avoid the "second customer races to the same last unit" problem during the delivery cycle.
- **Decrement on transition IN vs re-credit on transition OUT** — decrement happens on status transitions INTO `paid` / `pending` (per setting); the symmetric re-credit happens on transitions OUT (cancelled / refunded / voided / failed). See [[inventory-restock]] for the symmetric flow.

## Where it applies

The setting drives every order-status transition the platform handles:

- **Storefront submission** — order goes `pending`. Decrements stock immediately if the setting is `pending` (no fulfillment needed); on the `paid` setting it waits for `paid`.
- **Manual / gateway payment success** — order transitions `pending → paid` (or `pending → completed`). On the default `paid` setting this decrements stock **right then, whether or not the order is fulfilled**.
- **Manual fulfillment marking** ([[orders-details]]) — marking an order fulfilled is an **early** decrement trigger: if the order hadn't yet reached the setting's status threshold (e.g. still `pending` on a `paid`-setting store), fulfilling it decrements stock immediately. (If it had already reached the threshold, stock was already taken.)
- **Cancellation / refund / chargeback** — transitions OUT of `paid`/`pending`. Re-credits stock per [[inventory-restock]].
- **Order edit on [[orders-details]]** — quantity changes on an order whose stock has already been decremented trigger delta-adjustment (decrement if quantity increased, re-credit if decreased); a new / edited line on a not-yet-decremented order follows the same status-threshold rule above.

### Merchant choice — payment-method mix drives the right setting

- **Mostly-paid checkouts** (Stripe / Adyen / card-on-file dominant) → `paid` works well. Pending orders are short-lived; chargebacks and timeouts are rare; reserving stock pre-payment offers little benefit and risks shipping out before the bank settles.
- **Cash-on-delivery dominant** (typical for some Bulgarian / Eastern-European markets) → `pending` works better. The customer commits at submit; reserving stock at `pending` avoids the second-customer race during the multi-day delivery cycle. The trade-off: abandoned `pending` orders block stock until the merchant cancels them.

The decision is store-wide. Merchants with mixed payment mixes pick whichever majority case is more painful to break (oversell vs lost-sale) and live with the minority trade-off.

### The decrement-allowed matrix (verified against backend)

For `order_status_for_quantity_decrease = paid` (default):

| Order status | Fulfillment | Decrement on transition IN | Re-credit on transition OUT |
|---|---|---|---|
| `pending` | not fulfilled | No | No (was never decremented) |
| `pending` | `fulfilled` | **Yes** — fulfillment is an early trigger | Yes |
| `paid` / `authorized` / `completed` | any | **Yes** | Yes (on transition OUT to a terminal status) |
| `cancelled` / `refunded` / `voided` / `failed` / `chargebacked` | any | No (terminal) | Yes (returns the decrement, if one was taken) |

For `order_status_for_quantity_decrease = pending`, the threshold drops one step: decrement fires as soon as the order is `pending` (or any later non-terminal status), or when it's fulfilled.

**Fulfillment is an _additional, earlier_ decrement trigger — NOT a requirement** (corrected 2026-06-13, verified against `allowIncrementDecrementProducts`). With the default `paid` setting, reaching `paid` decrements stock **immediately, whether or not the order is fulfilled**; separately, marking an order **fulfilled while it is still `pending`** also decrements it early. So the decrement fires at the **earlier** of: the order reaching the setting's status threshold, or being marked fulfilled — so a "paid but not yet shipped" order on the default setting **has already taken stock**. Cancelling / refunding re-credits per [[inventory-restock]].

## Related

- [[inventory-tracking]] — hub.
- [[inventory-restock]] — symmetric stock-return flow on cancel / refund.
- [[inventory-oversell]] — clamping at 0 when `continue_selling = yes`.
- [[inventory-debugging-playbook]] — investigating unexpected stock changes; this setting is one of the suspects.
- [[settings-cart]] — where `order_status_for_quantity_decrease` lives.
- [[settings-statuses]] — the order-status taxonomy that transitions reference.
- [[orders-details]] — per-order edit + fulfillment marking trigger decrements.
- [[order-processing-pipeline]] — the full status-transition pipeline that drives decrement / re-credit.
- [[cart-vs-order-lifecycle]] — cart-stage vs order-stage stock semantics.

## Open Questions

None.
