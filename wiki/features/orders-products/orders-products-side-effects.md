---
type: feature
nav_path: "Orders → Order details → Products → Side effects"
route_name: admin.orders.products.update
route_path: /admin/orders/action/products/:order_id
aliases: ["Order line side effects", "Order line history entries", "Order line panel reload", "Order line webhook", "Recalculation cascade", "Order row lock"]
tags: [orders, products, line-items, side-effects, history, webhooks, recalculation, ajax]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-products]]. See the hub for the other aspects (add, edit, delete, line discount, fulfillment popover, stock effects).

# Order products — Side effects

## Purpose

Catalogue of **everything the platform does** when a successful POST runs on any of the order-product CRUD routes (`store`, `update`, `delete`, `store-discount`, `delete-discount`, `delete-modifications`). Covers the recalculation cascade, AJAX panel-reload chain, history-entry action keys, webhook gating (drafts skip), customer-notify behaviour, and the database row lock.

## Where to find it

Cross-cutting. These side effects fire on every successful POST to any of the routes under `/admin/orders/action/products/{order_id}/`. The merchant observes them indirectly:

- On [[orders-history]] — the history entries.
- On [[orders-details]] — the multi-panel refresh.
- On the receiver of [[settings-hooks]] — the webhooks.
- On the customer's inbox — the auto-notify email (add only).

## What the merchant can do here

Nothing — these are platform behaviours. The merchant observes them in support investigations: trace events via [[orders-history]] action keys, verify the panel refresh, and audit who changed what via `Initiator` on [[products-change-log]] for the linked stock changes.

## Settings & fields

### Recalculation cascade — what gets recomputed on every save

Every product / discount change triggers, in order:

1. **Line totals** — per-line subtotal × quantity.
2. **Order subtotal** — sum of all line totals.
3. **Tax recalculation** — per [[settings-taxes]] (delete-and-recompute pattern; see Business rules).
4. **Shipping recalculation** — if weight / dimensions changed, the courier quote API is re-run; may update the shipping line silently.
5. **Discount re-evaluation** — minimum-order-total rules may newly qualify (or stop qualifying).

The merchant should expect totals to update on every save.

### AJAX panel reload chain (per route)

After each successful save, the platform fires `cc.ajax.reload` on a specific set of sub-panels:

| Route | Reloaded panels |
|---|---|
| `admin.orders.products.store` (add) | `#order_preview` (preview mode only), `#order_summary`, `#order_customer`, `#order_shipping_address`, `#order_billing_address` |
| `admin.orders.products.update` (edit) | `#order_preview`, `#order_summary`, `#order_history` |
| `admin.orders.products.delete` (delete) | (verify) `#order_preview`, `#order_summary`, `#order_history` |
| `admin.orders.products.store-discount` (add line discount) | `#order_preview`, `#order_summary`, `#order_history` |
| `admin.orders.products.delete-discount` (remove line discount) | `#order_preview`, `#order_summary`, `#order_history` |

The merchant sees a near-instant UI update without a full page reload.

### History action keys — per action

Each successful action writes one [[orders-history]] entry with a specific `action_string`:

| Action code | `action_string` | Triggered by |
|---|---|---|
| 24 | `order_product_added` | Add a line via `store`. |
| 25 | `order_product_removed` | Delete a line via `delete`. |
| 29 | `order_product_edit` | Edit a line via `update` (quantity / price / options). |
| 30 | `order_product_discount_add` | Add a per-line discount via `store-discount`. |
| 32 | `order_product_discount_remove` | Remove a per-line discount via `delete-discount`. |
| 56 | `order_product_modification_remove` | Remove a per-line modification via `delete-modifications`. |

The Assistant can decode any one of these action strings to the originating route + the field-set that drove the change.

### Webhook — `order.updated` (NOT for drafts)

Every successful add / edit / delete / discount-add / discount-remove on a NON-DRAFT order fires `order.updated` via [[settings-hooks]]. The webhook payload reflects the post-save state of the order.

**Drafts skip the webhook.** For draft orders (created via [[orders-add]] but not yet finalised), `order.updated` does NOT fire on any line action — integrations don't see draft-line activity. Webhooks resume firing once the draft is finalised.

Stock-side webhooks (`product.updated`) DO fire on draft line edits — see [[orders-products-stock-effects]] — because the variant moves independently of the order's draft state.

### Customer auto-notify — ADD only

The platform sends a notification email to the customer (using the order's `notify_customer` setting) **only** for product ADD events. Edit and remove do NOT email the customer. For comms on edit / remove / discount changes, the merchant uses [[orders-notify-customer]] manually.

### Database row lock on the order during product mutation

The platform takes a **DB row lock** on the order record for the duration of every line-CRUD route. This serialises concurrent edits — if two merchants try to add products to the same order at the same time, one waits for the other. Prevents race conditions in totals recalculation; can briefly block other routes that need to write the order.

## Business rules

### `cc.ajax.reload` fires AFTER the response

Panel reload events fire on `ajaxForm` success — the merchant sees the refresh only once the server has committed. No optimistic UI; on failure the panels stay on the pre-save state.

### Tax delete-and-recompute keeps totals consistent

The platform deletes ALL non-product-level VAT tax records and re-computes them on every line save (not just adjusts existing ones). Avoids tax-record drift on address / variant / quantity changes. Line-level tax records survive.

### Shipping re-quote can change the shipping total silently

A weight or value change triggers a courier-quote API call. The new rate replaces the order's shipping line. Merchant should verify the shipping total after any line edit — no notification banner.

### Bundle-related discounts auto-cleanup

When a bundle line is deleted, the platform removes discounts attached to OTHER lines in the same bundle. Prevents orphan bundle discounts on surviving lines. See [[orders-products-delete]].

### Drafts skip BOTH `order.updated` AND customer-notify

Draft orders skip the `order.updated` webhook AND the customer-notify email — the order isn't yet "real" to the customer. Both resume once finalised.

### Refund-after-modification — no auto credit note

Removing a line from a paid order does NOT auto-issue a credit note. Totals update, but the credit note + refund are separate merchant actions via [[orders-credit]].

### JSON-API v2 surfaces the result, NOT the mutation path

Line-item CRUD is admin-panel-only. JSON-API v2 exposes line items as the read-only [[api-order-products]] resource. Every rich state-aware gate (fulfilled-line lock, last-product-blocked, digital-duplicate-blocked, override-price flag, already-has-discount gate, bundle-cascade, stock-validation) lives in admin code only. See [[json-api-v2]] for the read-vs-mutate principle.

## Related

- [[orders-products]] — hub.
- [[orders-products-add]] — the only action that fires the customer auto-notify.
- [[orders-products-edit]] — quantity / price / discount-value diff.
- [[orders-products-delete]] — restore + bundle cascade.
- [[orders-products-line-discount]] — discount-specific history action keys.
- [[orders-products-stock-effects]] — `product.updated` webhook + search-index re-index ripple.
- [[orders-details]] — host of the panels reloaded by `cc.ajax.reload`.
- [[orders-history]] — where the action keys land.
- [[settings-hooks]] — `order.updated` + `product.updated` webhook config.
- [[settings-taxes]] — tax delete-and-recompute pattern.
- [[orders-notify-customer]] — manual customer comms (the only path for edit / remove notifications).
- [[orders-credit]] — credit-note flow on paid-order modification.
- [[api-order-products]] — read-only JSON-API v2 resource for line items.
- [[json-api-v2]] — read-vs-mutate principle.
- [[order-processing-pipeline]] — full status-transition pipeline (these line-CRUD side-effects feed in).
- [[inventory-debugging-playbook]] — cross-reference Initiator + action key in support tickets.

## Open questions

- Confirm the exact `cc.ajax.reload` panel set on `delete` and `delete-discount` (verify).
