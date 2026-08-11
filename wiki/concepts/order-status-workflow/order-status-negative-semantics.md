---
type: concept
nav_path: "Concept → Order status workflow → Negative-status semantics"
aliases: ["Negative order statuses", "Revenue exclusion", "Fulfillment reset on negative", "Reversal lock", "Order locked after cancellation", "Payment authorisation release", "Stock restore on negative", "Auto-created return"]
tags: [orders, statuses, negative, revenue, fulfillment, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status-workflow]]. See the hub for the other aspects (taxonomy, custom statuses, transitions, auto-transitions, side-effects, action gates).

# Order status — negative-status semantics

## Definition

Seven of the 11 built-in order statuses are classified as **negative**: `voided`, `timeouted`, `cancelled`, `failed`, `refunded`, `chargebacked`, `disputed`. The grouping is fixed. When an order transitions INTO any of the 7, several **shared rules** apply on top of the standard side-effect cascade ([[order-status-side-effects]]): revenue exclusion, fulfillment reset, stock restore, a lower discount-uses recount, and payment-authorisation release. Two of the seven — `cancelled` and `refunded` — go further: on a committed sale they auto-record a **system return** and then **lock the order's status**.

This page documents what makes "negative" different — the shared semantics that custom statuses ([[order-status-custom]]) do NOT inherit even when the merchant intends them as negative-equivalents.

## Scope

Covered:

- The 7 negative statuses and their shared rules.
- Revenue / income / segment exclusion.
- Fulfillment reset on the same save.
- Stock restore + the lower discount-uses recount.
- The auto-created system return on `cancelled` / `refunded`.
- The reversal lock that follows it.
- Payment-authorisation release at the gateway.

Not covered here:

- The full cascade that ALL transitions fire — see [[order-status-side-effects]].
- What each negative status means individually — see [[order-status-taxonomy]].
- The credit-note issuance flow itself — see [[orders-credit]].
- Gateway-driven negative transitions (`failed`, `timeouted`, `chargebacked`, `disputed`, `voided`) — see [[order-status-auto-transitions]].

## Contrasts

- **Negative vs positive flow** — the 4 positive statuses are counted in revenue / fulfillment; the 7 negative are excluded. The "negative" classification drives every shared rule on this page.
- **Negative status vs custom "negative-like" status** — a custom status named "Lost in shipping" looks negative to the merchant but the platform does not treat it as negative. It does NOT trigger revenue exclusion, fulfillment reset, stock restore, or auth release. See [[order-status-custom]].
- **Merchant-pickable negative (`cancelled` / `refunded`) vs gateway-driven (`failed`, `timeouted`, `chargebacked`, `disputed`, `voided`)** — same shared rules apply, different entry points.
- **Credit-eligible (`cancelled` / `refunded`) vs other negatives** — only `cancelled` / `refunded` open the credit-note gate, auto-record a return, and arm the reversal lock; the other 5 negatives don't.
- **Stock restore vs `tracking = no`** — restore runs only if the product still participates in inventory tracking; deleted-product or `tracking = no` cases skip the restore silently.

## Where it applies

The shared rules apply on every transition INTO one of the 7 negative statuses; the auto-created return and the reversal lock apply to `cancelled` and `refunded` only. The surface spans accounting, stock, fulfillment, returns, and payment-gateway integrations.

### The 7 negative statuses

| Status | Source | Manually settable? |
|--------|--------|-------------------|
| `voided` | Gateway (auth released) | No (filtered out of dropdown) |
| `timeouted` | Gateway timeout | No |
| `cancelled` | Merchant action or banned-IP auto-rule | **Yes** |
| `failed` | Gateway rejection | No |
| `refunded` | Merchant refund or gateway event | **Yes** |
| `chargebacked` | Bank-initiated | No |
| `disputed` | Merchant flag or gateway event | No |

Only `cancelled` and `refunded` are reachable from the merchant's dropdown ([[order-status-transitions]]). The other 5 are gateway-driven and emitted only by payment-provider sync — see [[order-status-auto-transitions]].

### Shared rules

#### 1. Excluded from revenue / income / segment reports

Analytics dashboards, customer LTV, segment counts, and "income" totals automatically drop orders in any of the 7 negative statuses.

Reporting consequence: when a `paid` order is refunded, the revenue figure recomputes on the next report read (totals are not snapshot-frozen). Historical reports reflect the order's *current* status, not its status at report-render time.

#### 2. Excluded from "fulfilled but not completed" counts

If the order is `fulfilled` but its status is negative, it shows in a different bucket from `fulfilled` + positive-status. This matters for operational dashboards counting work-in-progress.

#### 3. The discount usage figure falls

When an order leaves the counted state (e.g., `paid → refunded`), the next recount of that discount's `uses` no longer counts it and the per-customer cap reopens — see the recount mechanism in [[order-status-side-effects]]. This is what lets a customer who refunded reuse the same one-time discount code: the slot is recycled.

#### 4. Trigger stock restore

If the order had decremented stock (per [[inventory-decrement-timing]]), transitioning into a negative status restores it. The restore tracks per-line whether decrement actually ran, so it won't double-credit — see [[inventory-restock]].

Restore is **blocked while the order's status is `paid`, `authorized` or `completed`** — those statuses always count as "stock is out". So the return of stock happens on the move into the negative status, not before.

If the product has been DELETED since the order was placed, or its `tracking` flag was toggled to `no` after the order decremented, the stock-restore step is skipped silently — the transition succeeds but no stock is added back.

#### 5. Fulfillment reset to `not_fulfilled`

When the merchant (or a gateway event) flips an order into a negative status, the platform also clears `status_fulfillment` from `fulfilled` back to `not_fulfilled` **in the same save**. The merchant sees both fields change with one click; this does **not** fire a separate webhook — the single `order.updated` carries both new values.

#### 6. Payment-authorisation release at the gateway

When a status change moves an order into ANY negative status AND the latest payment has a non-empty `authorize_amount` (an active pre-auth hold at the gateway), the platform calls the gateway to release the funds upstream — automatically, with no separate "release hold" button. If the gateway call fails, the order's status still changes locally but the hold may not release — the merchant must contact the gateway manually.

#### 7. `cancelled` / `refunded` on a committed sale auto-records a return

Only these two of the seven do this. When the order was a **committed sale** — already invoiced, or coming from a positive / committed status such as `paid` — moving it to `cancelled` or `refunded` makes the platform record a return for it automatically: created straight as **`returned`**, with source `refund` and created by the system, covering the whole (or the remaining) quantity. No credit note is required for this to happen, and it is idempotent — toggling the status back and forth does not pile up returns.

A plain cancel of a never-committed order (an unpaid, uninvoiced `pending` one) creates no return.

**Merchant-visible consequence:** those auto-created returns are real return records, so a merchant who cancels paid orders sees them in the *Returns over time* reporting even though no goods came back and no credit note was issued. See [[orders-returns-lifecycle]].

#### 8. The reversal lock — a committed cancellation is one-way

Once a `cancelled` / `refunded` order carries a **return record or an issued credit number**, its status is **locked**. From then on the only status change accepted is a toggle between `cancelled` and `refunded` (so the merchant can correct "cancelled" to "refunded" once the money actually goes back, or vice versa). Anything else — re-opening the order to `paid`, `pending`, a custom status — is refused with *"The order is locked after a cancellation/refund — its status can no longer be changed."*

The reason is fiscal: reversing an issued credit note requires a debit note, not a status flip.

Two things this is **not**:

- It is not a lock on a plain cancellation. A `pending` order cancelled by mistake has no return record and no credit number, so it still moves back to `pending` normally.
- It does not lock the order's **payments** — the actual money refund can still be processed. A delayed gateway notification can also still correct a spurious cancel, because the system's own recovery path does not go through this check.

### Custom statuses don't get any of this

A custom status ([[order-status-custom]]) — even one the merchant names "Lost in shipping" or "Returned to warehouse" — does NOT participate in these rules. It will:

- Count in revenue reports.
- NOT trigger stock restore.
- NOT drop out of the discount-uses recount.
- NOT reset fulfillment.
- NOT release the payment authorisation at the gateway.
- NOT record a return.

If the merchant wants the order excluded from revenue / treated as a "real" cancellation, they must move it to one of the 7 built-in negative statuses (typically `cancelled` or `refunded`).

### Credit-note interaction

The credit-note flow on [[orders-credit]] is gated by status being `cancelled` OR `refunded` (two of the 7 negatives) AND an invoice number already populated. Common workflow: merchant issues invoice while `paid` → refunds the order (moves to `refunded`) → issues credit note (gate now open). The credit note re-uses the order's invoice number as its credit-number reference per the [[settings-invoicing]] numbering scheme.

Once that credit number exists, the reversal lock above is armed — the order can no longer be moved back to `paid`.

## Related

- [[order-status-workflow]] — hub.
- [[order-status-taxonomy]] — full taxonomy including positive statuses.
- [[order-status-side-effects]] — the standard cascade that ALL transitions fire.
- [[order-status-custom]] — why custom statuses don't participate.
- [[order-status-auto-transitions]] — gateway-driven negative transitions.
- [[orders-credit]] — credit-note flow gated by `cancelled` / `refunded`.
- [[orders-returns-lifecycle]] — the auto-created system return and how it shows in return reporting.
- [[orders-history]] — audit trail of negative transitions.
- [[inventory-restock]] — the stock-restore mechanism.
- [[marketing-discounts]] — the `uses` figure recounted lower on transition into negative.
- [[settings-cart]] — `order_status_for_quantity_decrease` (controls whether stock was decremented to begin with).
- [[settings-invoicing]] — credit-note numbering scheme.
- [[payment-status]] — separate field tracking money lifecycle.

## Open Questions

None.
