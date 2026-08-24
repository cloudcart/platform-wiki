---
type: feature
nav_path: "Orders → Details → Products"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order products section", "Order summary products", "Order line items", "Order line edit", "Per-line discount", "Add product to order"]
tags: [orders, order-details, products, line-edit, discount]
plan_gates: []
created: 2026-06-10
updated: 2026-08-03
source_count: 3
---

> Part of [[orders-details]]. See the hub for the other aspects (header, addresses, payment, shipping, history, actions, known issues).

# Order details — Products section

## Purpose

The main content area of the order details page — the products table that lists every line item on the order, with per-row actions to edit quantity, override price, add or remove a line-level discount, edit per-item / per-order options, and remove the line. A `+` button under the table opens the **Add product** picker. Below the table sit the comments and totals panels and the order-level discount slot.

This page documents the SECTION as it appears on order details. The full field-by-field reference for line edits, additions, deletions, and the per-line discount modal lives on [[orders-products]].

## Where to find it

The middle of `/admin/orders/details/<order_id>`, below the header and above the action rows (Payment, Shipping, Fulfillment).

## What the merchant can do here

### Products table

A three-row layout per line:

- **Image + name** — click either to open the product editor in [[products-products]].
- **Import-source icon** — a line whose product originated from an import shows a small icon next to its name: an **XML** badge (tooltip = the source feed name) for products brought in via [[apps-xml-import|XML Import]] / [[apps-xml-sync|XML Sync]], or an app-keyed badge (tooltip = the import source) for products from another app import. Manually-added / catalogue products show no icon — so the icon is a quick "where did this product come from" cue on the order.
- **Single price, quantity, line total** — read-only columns.
- **Per-row metadata** — SKU, barcode, variant parameters, line-level options (length / square / engraving / gift-wrap), digital files, applied discounts, fulfillment status indicator (see [[orders-details-shipping]] for the badge states).
- **Per-row settings cog** — appears only for **non-invoiced**, non-fulfilled pending / paid / authorized orders with non-fulfilled, non-digital lines. The cog opens a menu (see below). **An invoiced order has no cog at all** — see Business rules.

### Per-row cog menu

| Menu item | When visible | What it does |
|---|---|---|
| **Edit** | Always (when the cog is visible — i.e. the order is **not invoiced**, is pending / paid / authorized, and not fulfilled) | Opens the [[orders-products]] edit modal — quantity, price override, per-line options, per-order options. |
| **Add product discount** | Line has NO existing manual discount AND isn't MSRP | Opens the line-discount modal — see [[orders-products]] for the full field catalogue (type: flat / percent, amount mask). |
| **Remove product discount** | Line has ≥1 discount | If line has multiple stacked discounts, opens a picker panel asking WHICH to remove. If single discount, fires a direct delete confirmation. |
| **Remove product** | Always (cog visible) | Deletes the line. Restocks the line's variant if it had been decremented — see [[inventory-restock]]. |
| **Fulfillment popover** | Line has fulfillment metadata | Opens a small modal showing the fulfilment details for ONE specific line (read-only — no partial-fulfilment controls). |

### Add product (below the table)

The `+` button under the products table opens an **Add product** browser:

- **Wide modal** (`data-modal-ajax`) when not in preview mode.
- **Side-panel** when in preview mode.
- **Content**: searchable, paginated grid of every catalog product / variant, with a quantity input + **Add** button per row. Same filters as the main product list.

The added line shows up immediately in the order summary; on success the summary, history, and preview reload. Full field catalogue: [[orders-products]].

### Order-level discount slot

A `+` button on the order summary opens **Add order discount** — a separate modal (NOT the line-discount modal):

- **Discount source** select: *(blank)* / **Existing discount** / **Manual discount**.
- **Existing discount target** — list of merchant's defined discount campaigns (visible only when source = Existing). If the merchant has no eligible discounts, an *"No discounts available"* alert shows instead.
- **Manual discount type** — `flat` / `percent` (visible only when source = Manual).
- **Manual discount value** — currency / percent mask input.

Visibility: only when no existing order-level discount AND no shipping discount. Full flow: [[orders-discount-add]].

### Two-column footer below the table

- **Comments** (admin-only note) — see [[orders-details-actions]] for the Save flow.
- **Totals** — subtotal + shipping + discount + tax + total. A small lock / unlock icon next to the shipping subtotal toggles the **Recalculate lock** — see [[orders-details-actions]].

## Settings & fields

The products section reads from the order's line items. The fields on each line are NOT directly editable from this page's table — every edit goes through the per-row cog → modal flow on [[orders-products]].

Per-product price overrides, per-item option price overrides, and per-order option price overrides are all set on the line-edit modal. Discount values (flat vs percent) and amounts are set on the line-discount modal. The current values are reflected on the line row after save.

## Business rules

### 🔴 An INVOICED order can no longer be edited — at all

**Once an invoice number has been issued for the order, the line-item editing UI disappears entirely** — no per-row cog, no **Add product**. This is a fiscal rule (Наредба Н-18): the fiscal document is already out, so quantities, prices, and discounts can no longer be changed on the order itself. **It applies regardless of the order's status (paid or unpaid) and regardless of fulfilment** — so **un-fulfilling / marking the order as not shipped does NOT re-open editing**, because the block is the invoice, not the fulfilment state.

To change what the customer actually receives after an invoice exists, the correction goes through a **credit note / return** ([[orders-returns]] → [[orders-credit]]), not an order edit. To sell an additional item, create a **new order** for it (it gets its own invoice).

### Line edit is otherwise gated on status + fulfilment

When the order is **not** invoiced, the per-row cog is rendered ONLY for **pending / paid / authorized** orders that are NOT fulfilled, with non-digital, non-fulfilled lines. For completed / cancelled / refunded / archived orders the table is read-only.

So the full condition for the editing UI is: **no invoice number** AND status ∈ `pending` / `paid` / `authorized` AND the order is not fulfilled.

### Removing a line restocks the variant

When the merchant removes a line via the cog → **Remove product**, the platform calls the restock path — if the line had been decremented from stock (per [[inventory-decrement-timing]]), its variant `quantity` is incremented back. The change is recorded on the product's [[products-change-log]] with `action = order` so the merchant can trace it.

### Adding a line does NOT auto-decrement at submit

The platform's standard decrement timing (set via `order_status_for_quantity_decrease` on [[settings-cart]]) decides when stock comes off — and it gates the add, too. **The added line decrements its stock immediately ONLY if the order's current status already qualifies** under the setting (or the order is already fulfilled): with `order_status_for_quantity_decrease = paid` the order must be `paid` / `authorized` / `completed`; with `= pending` those plus `pending`. Otherwise the new line is left undecremented (`tracked = no`) and comes off later when the order reaches a qualifying status. So adding a line to a `pending` order on a "decrement at `paid`" store does NOT touch stock yet; adding it to an already-`paid` order does so on the spot. See [[inventory-decrement-timing]].

### Manual discount vs existing discount

The **Existing discount picker is currently commented out in the code** for the per-line discount modal — only manual line discounts are exposed today. The merchant can still pick existing campaigns from the order-level discount modal.

### Discount "modifications" — cascading line entries

When an order-level discount is applied, the platform creates cascading line-level entries (called "modifications") that mirror the discount across individual lines. Removing a single line's discount entry is handled by the `delete-modification` route; removing the parent discount uses `delete-discount`. The merchant doesn't see the distinction directly — the cog menu picks the right route automatically. See [[orders-discount-add]] for the full flow.

### Side effects of line save

Every per-line save (edit / add / remove / add-discount / remove-discount) reloads `#order_preview`, `#order_summary`, `#order_history` panels. The save also runs the order's totals recompute (unless the **Recalculate lock** is engaged — see [[orders-details-actions]]) and fires the `order.updated` webhook via [[settings-hooks]].

## Related

- [[orders-details]] — hub.
- [[orders-products]] — full per-line edit field catalogue (canonical detail page).
- [[orders-discount-add]] — order-level + line-level discount flow.
- [[orders-ordered-products]] — the cross-order ordered-products report.
- [[products-products]] — clicking a product image / name opens the product editor here.
- [[inventory-decrement-timing]] — when adding / editing lines affects stock.
- [[inventory-restock]] — when removing lines restocks the variant.
- [[products-change-log]] — line-edit audit trail on the product side.
- [[marketing-discounts]] — definitions of the "existing discount" campaigns surfaced in the order-level picker.

## Open questions

None.
