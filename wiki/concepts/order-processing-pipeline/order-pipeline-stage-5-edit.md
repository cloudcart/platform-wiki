---
type: concept
nav_path: "Concept → Order processing pipeline → Stage 5 Edit"
aliases: ["Order edit side-effects", "Stage 5 manual edits", "productAdd productEdit productRemove", "Order line edit", "Edit discount on order", "shippingChange", "editNote", "Archive order"]
tags: [orders, lifecycle, edits, side-effects, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-processing-pipeline]]. See the hub for the other aspects (placement, status transitions, payment sync, fulfillment, edge cases).

# Order pipeline — Stage 5: Manual edits on an existing order

## Definition

**Stage 5** fires when the merchant edits an already-placed order from [[orders-details]] — adds a product line, edits a quantity, removes a discount, changes the shipping method or address, edits a note, archives the order. Each edit fires a **focused event** that runs the relevant side-effects, and — on a **non-draft** order — most edits also fire an **`order.updated` webhook** right then (verified 2026-06-13: the edit controllers call the order's hook trigger, which delivers `order.updated` to any active subscriber). So a session of edits produces **one `order.updated` per edit**, not a single deferred broadcast. Exceptions: **archive / unarchive** and **customer change** do NOT fire the hook, and **draft orders** (`is_draft`) fire no events or webhooks until confirmed.

## Scope

Covered:

- The complete edit-to-side-effects matrix.
- Order total recalculation (always synchronous).
- Which edits fire an `order.updated` webhook (most do) vs which don't (archive / customer change / draft), and what that means for external integrations.
- Per-line discount add / remove and Cart-Rule modification removal.
- Archive / unarchive history rows.

Not covered here:

- Stock decrement / restock mechanics — see [[inventory-restock]] and [[inventory-decrement-timing]].
- The shipping method picker UI — see [[orders-shipping-waybill]].
- Discount stacking math — see [[discount-stacking]].
- Customer email template management — see [[marketing-omnichannel-mails-list|Customer mails settings]].

## Contrasts

- **Per-line edit vs status change** — a per-line edit changes the order's contents without changing its status, yet it still fires its own `order.updated` webhook (non-draft orders). A status change (Stage 2) additionally runs the full status chain (customer email, stock at canonical statuses, etc.) on top of the same `order.updated`.
- **Edit during draft vs edit on confirmed order** — in draft mode (`is_draft` meta present) NO events or webhooks fan out at all. Once the order is confirmed, every qualifying edit fires its focused event AND an `order.updated` webhook.
- **Synchronous total recalc vs queued lifetime-spend** — the order's total is recalculated synchronously on every line-item or discount edit, so the merchant sees the new total immediately on [[orders-details]]. The customer's lifetime spend is queued (cascades when the next status change runs).

## Where it applies

Every editable surface on [[orders-details]] enters here:

- [[orders-products]] — add / edit / remove product lines.
- Per-line discount controls on the order — add manual / add existing platform discount / remove.
- Cart-Rule modification controls (per-line) — remove only; add happens automatically from [[apps-cart-rules]] at placement.
- Shipping method picker (the picker on [[orders-shipping-waybill]]).
- Note editor (admin-only or customer-visible).
- Archive / Unarchive toggle.

### The edit-to-side-effect matrix

| Edit | History row written | Stock adjustment | Customer email | `order.updated` webhook |
|---|---|---|---|---|
| Add product line ([[orders-products]] → **+ Add**) | `productAdd` | Decrement **only if the order's current status already qualifies** under its snapshotted `order_status_for_quantity_decrease` (or it's fulfilled); otherwise deferred to that transition — see [[inventory-decrement-timing]] | Queued: *"product added to your order"* (if `notify_customer`) | **Yes**, fired inline on save |
| Edit product line (quantity / price) | `productEdit` (with before / after / dirty-fields snapshot) | Delta-adjustment (if quantity changed AND the order's status qualifies for decrement) | No | **Yes**, inline on save (only if a field actually changed) |
| Remove product line | `productRemove` | Restock (if product had `tracked=yes`) | No (template not implemented) | **Yes**, inline on save |
| Add per-line discount (manual fixed amount OR existing platform discount) | `orderProductDiscountAddManual` / `orderProductDiscountAddExisting` | No | No | **Yes**, inline |
| Remove per-line discount | `orderProductDiscountRemove` | No | No | **Yes**, inline |
| Remove Cart-Rule modification (per-line) | `orderProductModificationRemove` (`app: cart-rules`) | No | No | **Yes**, inline |
| Change shipping method | `shippingChange` (with before / after) | No | No | **Yes** |
| **Change payment method** (`admin.orders.payment.change`) | new payment row (status reset to initiated) | No | No | **No** (the provider-change action doesn't trigger the hook) |
| Edit note (admin-only or customer-visible) | `editNote` | No | No | **Yes** |
| Archive / Unarchive order | `archive` (`order_archived` / `order_unarchived`) | No | No | **No** (archive doesn't trigger the hook) |

(Also: editing the **shipping / billing address** and adding / removing an **order-level discount** fire `order.updated` too; **changing the customer** does not. Draft orders fire nothing.)

**The order's total is recalculated synchronously on every line-item or discount edit** (the platform's order-total recalculator). The merchant sees the new total immediately on [[orders-details]].

**Changing the payment method is a distinct recalculation path** — not an inert provider swap. It re-derives the payment-linked fee (COD surcharge), the per-provider discount, payment-tied free shipping, the payer side, and any payment-targeted Cart Rules, and re-quotes shipping — unless the order is recalc-locked (paid by default). The full set of conditions the payment method carries into the total, and the lock, are documented on [[order-pipeline-recalculation]].

### What fires on adding / changing a product line

**Adding a product** (`+ Add`):

- **Stock check (can block the add).** If the variant is stock-tracked and not oversell-enabled (`tracking = yes`, `continue_selling = no`) and the on-hand quantity is below the requested quantity, the add is **rejected** with *"not enough quantity"* — the line is not created. (Stock-location stores check the quantity in the order's zone shops.)
- **Auto-applies the variant's active catalogue discount** — if the product currently has an active discount whose price beats the line price, it is attached to the new line automatically, and the applicable order-product discounts are (re)created for the line.
- Fires the product-add chain (decrement per [[inventory-decrement-timing]], the `productAdd` history row, the *"product added"* email when `notify_customer`) **and** the `order.updated` webhook, inline on save.

**Changing a product line** (quantity / price / options):

- **Stock check on a quantity increase** — same rule: a larger quantity is rejected if on-hand can't cover the *additional* amount (and the line isn't oversell-enabled).
- **Re-computes the line discount** for the new quantity / price (percent / fixed).
- Saves only the changed fields and fires the edit event (before / after / dirty snapshot) **and** the `order.updated` webhook **only if something actually changed** — a no-op save fires nothing.

### How edits fan out webhooks

Each qualifying edit fires its **own** `order.updated` webhook to any **active** `order.updated` subscriber ([[settings-hooks]]) — there is no batching. So a merchant who edits 5 lines, removes 2 discounts, and changes the shipping method produces **8 separate `order.updated` events**, not one deferred broadcast. **All** of them fire inline on save — product-line edits are not routed onto a separate queue; whether a given delivery then happens synchronously or is handed to a background job is a property of the individual **subscription**, not of the kind of edit. The event leaves the platform only when an active `order.updated` webhook actually exists — with no subscriber, nothing is dispatched.

What does **NOT** fire `order.updated`: **archive / unarchive**, **change customer**, **change payment method**, and any edit on a **draft** order. For those, an external integration sees the change only at the next status change (Stage 2) or by polling [[json-api-v2|JSON-API v2]].

The history rows are written immediately and visible on [[orders-details]] under the History tab regardless of webhook delivery.

### Edits that DO have an immediate customer-visible effect

The only edit that queues a customer email at edit time is **Add product line** — the "product added to your order" template. All other edits are silent to the customer; they only learn about the change if and when a subsequent status email is queued (Stage 2 step 10) and the template body summarises the new totals.

## Related

- [[order-processing-pipeline]] — hub.
- [[order-pipeline-recalculation]] — the full recalculation & freeze model (esp. what a payment-method change re-derives, and the `recalculate_locked` lock).
- [[order-pipeline-stage-2-status]] — the next status change is when accumulated edits get broadcast.
- [[order-pipeline-stage-4-fulfillment]] — fulfillment-add also broadcasts the current state.
- [[order-pipeline-known-edge-cases]] — edits-during-draft, missing-template edge cases.
- [[orders-details]] — the edit surface itself.
- [[orders-products]] — line-item edit screen.
- [[orders-history]] — where the edit history rows render.
- [[orders-shipping-waybill]] — shipping method picker + waybill surface.
- [[orders-notify-customer]] — `notify_customer` gating for the "product added" email.
- [[inventory-restock]] — restock semantics on product-remove.
- [[inventory-decrement-timing]] — decrement on product-add and delta-adjust on quantity edit.
- [[discount-stacking]] — how per-line discounts interact with order-level discounts.
- [[apps-cart-rules]] — Cart-Rule modifications applied at placement.
- [[json-api-v2]] — polling fallback for integrations that need to see edits.

## Open Questions

- **`productRemove` customer email** — the "product removed from your order" template is currently noted as not implemented; confirm whether this is a planned addition or intentional (verify).
- **Archive triggers analytics changes** — confirm whether archiving an order excludes it from [[analytics-pipeline|analytics]] aggregates immediately or at the next aggregation pass (verify).
