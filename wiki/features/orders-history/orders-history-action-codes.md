---
type: feature
nav_path: "Orders → Order details → History → Action codes"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history action codes", "History action types", "Order audit action map", "History sub-templates", "Кодове на действия — история"]
tags: [orders, history, audit, action-codes, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-history]]. See the hub for the other aspects (timeline UI, record model, synthetic entries, enrichment, acting party, API & triggers).

# Order history — action codes & sub-templates

## Purpose

The catalogue of **action types** the audit log records — both the numeric `action` code stored on each row and the named sub-template that renders the expandable detail panel. This is the reference a support agent uses to decode *"what does this entry mean?"* and *"why does this row show a product name?"*.

## Where to find it

These codes / templates surface inside the History panel on [[orders-details]] — see [[orders-history-timeline-ui]] for the rendering. There is no separate screen; this page documents the underlying taxonomy.

## What the merchant can do here

The merchant reads and (for `action_string` rows) expands entries. They cannot add, edit, or remap action codes — the taxonomy is platform-defined. Apps can register **new** action types (the pick_and_pack app does), which is the only way the catalogue grows; see Business rules.

## Settings & fields

### Action code map (verified — 62 codes, numbered up to 63)

The platform defines **62 numbered action codes** covering the full order lifecycle. The highest number in use is **63**; **code 23 is not assigned to anything** (it is the one gap in the sequence). Notable ranges (verbatim):

- **1–8:** order add / close / cancel / reopen / open / fulfilled / archive / unarchive
- **9–15:** shipping address changes (change / edit / reposition / add)
- **12–17:** billing address + customer changes
- **18–22:** confirmation email + payment events (paid / refunded / partial refund / voided)
- **24–29:** product CRUD + note edits + fulfillment events
- **30–33:** discount adds / removes (per-product and order-level)
- **34–49:** order status transitions (new / cancelled / abandoned / completed / shipping / pending / voided / timeouted / failed / refunded / chargebacked / paid / disputed / fulfillment-remove / receipt-sent / authorized)
- **50–57:** app + order-level events (ERP send success / error, pick-and-pack, custom status, lock / unlock, modification remove, currency convert)
- **58–63:** the **returns** block, added with the returns feature — return issued (58), return received (59), return credit note (60), return cancelled (61), exchange created (62), return refunded (63). See [[orders-details-returns]] and [[orders-returns]].

### What is NOT logged

Several things a merchant might look for have **no action code at all**, so they never appear in the timeline:

- **Notify-customer toggle** — flipping the switch is silent, so "who turned emails off?" is unanswerable from the log. See [[orders-notify-customer-toggle]].
- **Waybill generation** on its own — the fulfillment-add entry (code 27) is the closest proxy.
- **Invoice-number generation** and standalone **credit-note creation** — visible only indirectly, via the return entries.

### Expandable sub-templates (30)

When a row has an `action_string`, the expanded body renders the matching sub-template (`history/<action_string>.tpl`):

| Action sub-template | What it details |
|---|---|
| `order_add` | Initial order creation. |
| `order_address_add` / `order_address_add_shipping` | New address added. |
| `order_address_change` / `order_address_edit` | Address swap or in-place edit. |
| `order_address_reposition` | Address geo-coordinate change. |
| `order_currency_convert` | Currency conversion event (BGN→EUR, etc.). |
| `order_customer_edit` | Customer info changed on the order. |
| `order_discount_add` / `order_discount_remove` | Order-level discount changes. |
| `order_fulfillment_add` | A fulfillment was generated. |
| `order_notes_edit` | Note text changed. |
| `order_payment_paid` | Payment marked as paid (amount, status, date). |
| `order_product_added` / `order_product_edit` / `order_product_removed` | Product line changes. |
| `order_product_discount_add` / `order_product_discount_remove` | Line-level discount changes. |
| `order_product_modification_remove` | Line modification removed. |
| `order_receipt_sent` | Receipt sent to customer. |
| `order_shipping_change` | Shipping provider changed. |
| `pick_and_pack` | Pick-and-pack app event. |
| `return_issued` / `return_received` / `return_credit_note` / `return_cancelled` / `return_refunded` | The stages of an order return — see [[orders-details-returns]]. |
| `exchange_created` | A return was settled as an exchange; links to the replacement order. |
| `send_erp_error` / `send_erp_success` | ERP integration dispatch result. |

Note that the lock / unlock codes (54 / 55) have **no** sub-template — they render as a plain line with no expandable detail.

## Business rules

### Codes 21 + 22 are PAYMENT events, not products (verified — corrects an earlier claim)

The wiki originally documented codes 21 + 22 as *product added / removed*. **Verified:** code **21 = `order_payment_partially_refunded`** and **22 = `order_payment_voided`**. The template special-case that appends a product name to these rows exists because a partial-refund / void can be scoped to a **specific product line** — the template renders that line's product name (from `message_data.order_product.name`) so the merchant immediately sees **which** item was refunded / voided:

> `<message>` : *"Product Name"*

**Product add / remove are codes 24 and 25** respectively — they have **no** name-appending special-case in the template.

### Custom status uses code 53 with a live name lookup

Code **53** (custom status applied) stores the status KEY in `message` and resolves the display name from the merchant's status taxonomy at view time — so renaming or deleting a custom status changes how old entries read. The full live-lookup behaviour is documented in [[orders-history-enrichment]].

### Apps extend the catalogue

Adding a new action type requires adding a sub-template file and setting `action_string` on the row's data. This is an extensible audit-log pattern — apps (e.g., pick_and_pack, ERP connectors via [[apps]]) register their own action types using their app namespace.

### Side effects

None — reading codes is a pure read.

## Related

- [[orders-history]] — hub.
- [[orders-history-timeline-ui]] — how these codes render in the timeline.
- [[orders-history-enrichment]] — code 53 live status-name lookup + action 27 waybill join.
- [[orders-history-record-model]] — where the `action` code is stored.
- [[orders-details-returns]] — the returns surface behind codes 58–63.
- [[orders-notify-customer-toggle]] — an action deliberately NOT logged.
- [[apps]] — apps that register custom action types.

## Open questions

None.
