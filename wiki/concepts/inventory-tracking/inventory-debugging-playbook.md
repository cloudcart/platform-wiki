---
type: concept
nav_path: "Concept → Inventory tracking → Debugging playbook"
aliases: ["Inventory debugging playbook", "Stock changed and we didn't change it", "Stock support investigation", "Unexpected stock change", "Stock drift investigation", "Inventory support workflow"]
tags: [catalog, inventory, stock, support, debugging, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (variant model, decrement timing, restock, oversell, bundle stock, multi-warehouse).

# Inventory — support playbook (unexpected stock changes)

## Definition

The most common merchant complaint about inventory is *"product X was sold, but now it's showing as available again — nobody on our team touched it"* (or the symmetric: *"the stock dropped without an order"*). **It is practically impossible for the platform to silently change `quantity`** — every change writes an entry to the product's [[products-change-log|Change log]] with an explicit Initiator. When a merchant asserts otherwise, the Assistant's job is NOT to agree — it's to investigate.

This page is the **6-step investigation workflow** for these tickets.

## Scope

Covered:

- The 6-step diagnostic walk through the Change log + cross-references.
- The Initiator decoding table (admin user / `api2` / order edit / import / CC Console).
- Anti-patterns that fail these tickets.

Not covered here:

- The general inventory model — see [[inventory-tracking]] hub.
- The Change log modal itself (UI / columns / filters) — see [[products-change-log]].
- Specific causes — see the decrement-timing, restock, and multi-warehouse aspect pages.

## Contrasts

- **Investigate, NOT agree** — when a merchant says "no one changed it", open the Change log and find the actor. Agreeing without checking is the top reason support agents fail these tickets.
- **The platform DOES track stock movements** — there's no dedicated `stock_movements` log, but every `quantity` change is captured in the parent product's [[products-change-log|Change log]]. Believing there's no audit trail is the next-most-common reason these tickets stall.
- **Change log on the product, NOT the variant** — variant-quantity diffs are recorded against the parent product's Change log, under a `variants.updated` block. Look at the parent product, not the individual variant.

## Where it applies

### Step 1 — Open the product's Change log

From [[products-products]], find the affected product, click the **history icon** in the row actions cell (or open the editor → header dropdown → **Change log**). The icon is green when entries exist.

Read entries newest-first. Find any entry whose `Changes` column mentions a `variants.updated` block matching the affected SKU, and note: **when** it happened (timestamp), **which field** changed (before / after value), and **the Initiator** (the actor — see decoding below).

In the overwhelming majority of these tickets, **the Change log answers the question directly**. Do NOT skip this step.

### Step 2 — Decode the Initiator

| Initiator name | Action | What to tell the merchant |
|---|---|---|
| *<admin user email / name>* | `Update` / `Create` / `Delete` | One of the merchant's admins changed it through the admin UI. The merchant can ask that user. |
| *<admin user>* | `Bulk` | The change came from a bulk operation on [[products-products]] or a Bulk Update from [[products-inventory]]. |
| *<system source>* | `Order` — rendered as *"Edit from order #N"* link | The product was added / edited / removed from inside an order. **Click the link** to open the order; the line edit is in [[orders-history]] there. Common in this scenario: the merchant edited the order's line items after fulfillment. |
| `api2` | `Update` / `Create` / `Delete` | An **external integration** wrote to the product via the [[api-products|JSON-API v2]]. To find which integration, cross-reference [[settings-api-keys]] for last-used timestamps in the same time window. |
| *<import source>* (e.g., `csv_import_<id>`, `xml_sync`) | `Update` | A CSV / XML / ERP **import or sync job** wrote to the product. Check the relevant app's settings ([[apps-csv-import]] / [[apps-xml-sync]] / ERP integration) for the schedule and the source file. |
| any actor with `(CC Console: <name>)` suffix | any | A **CloudCart support engineer** acted via CC Console impersonation. If the merchant didn't authorise this, escalate to the support team. |

### Step 3 — Cross-reference with the order

If Step 2 reveals an *"Edit from order #N"* entry, open the order at `/admin/orders/details/N` and:

- Read [[orders-history]] — every line-item operation has an entry (`order_product_added`, `order_product_edit`, `order_product_removed`) with timestamp + actor.
- Check status transitions — any move out of a stock-decrementing status (`paid` / `pending`, per [[settings-cart]] `order_status_for_quantity_decrease`) automatically returns stock; see [[inventory-restock]].
- Check refunds — refunds trigger automatic stock restoration (visible as the Variant `quantity` diff back in the Change log).

### Step 4 — Cross-reference with the store-wide decrement setting

Read the merchant's [[settings-cart]] `order_status_for_quantity_decrease` value (Settings → Cart → "I want to decrease product quantity when the status is"):

- **`paid`** (default) — stock decrements only when an order reaches `paid + fulfilled`. Pending orders do NOT touch stock. If the complaint is *"the order was placed yesterday but stock didn't drop"*, this is the answer.
- **`pending`** — stock decrements at submission. Cancelling a pending order automatically restocks.

A common misunderstanding: the merchant assumes stock dropped at order placement when the setting is `paid`. The Change log shows the actual timing. See [[inventory-decrement-timing]] for the full matrix.

### Step 5 — Check for multi-warehouse / external syncs

If the store has [[apps-store-locations]] (multi-warehouse) or any ERP / dropshipping integration ([[apps-microbg]], [[apps-microinvest]], [[apps-fgo]], [[apps-smart-bill]], [[apps-emag-sync]], etc.), the per-Variant `quantity` is written from outside CloudCart on a schedule. The Change log shows these writes with the integration's source identifier as Initiator. **The merchant may have installed an app months ago and forgotten** — the Change log surfaces the truth. See [[inventory-multi-warehouse]] for the common sync patterns.

### Step 6 — Confirm there's no other actor

Only if Steps 1–5 produce no plausible explanation:

- Initiator is one of the merchant's own admins → the merchant should ask that admin.
- Initiator is `api2` or a sync source → the merchant should audit their installed integrations.
- The Change log shows the expected automatic decrement / restore from order status transitions → explain the rule + cite [[settings-cart]] `order_status_for_quantity_decrease` and [[inventory-restock]].
- NO entry within the suspect window AND current stock truly does not match an admin's expectation → escalate to engineering. This is rare; the platform writes the entry on every save path, so a **missing entry is itself diagnostic**.

### What the Assistant should NOT do

- **Do NOT agree** that "no one changed it" before opening the Change log. Every change has an actor.
- **Do NOT claim** the platform "doesn't track stock movements" — it does, through the product's Change log.
- **Do NOT promise** the issue is a platform bug when the Change log clearly shows an integration / order-edit / bulk operation as the actor.

## Related

- [[inventory-tracking]] — hub.
- [[inventory-variant-model]] — the per-Variant `quantity` field that all changes hit.
- [[inventory-decrement-timing]] — when stock comes off; key suspect in Step 4.
- [[inventory-restock]] — when stock goes back; key suspect in Step 3.
- [[inventory-multi-warehouse]] — external syncs that show as Initiator in Step 5.
- [[products-change-log]] — the Change log modal reference + full Initiator decoding.
- [[settings-cart]] — `order_status_for_quantity_decrease` setting.
- [[settings-api-keys]] — to map `api2` Initiator back to a specific integration.
- [[orders-details]] / [[orders-history]] / [[orders-products]] — for Step 3 cross-reference.
- [[apps-csv-import]] / [[apps-xml-sync]] — import paths.
- [[apps-store-locations]] / [[apps-microbg]] / [[apps-microinvest]] / [[apps-fgo]] / [[apps-smart-bill]] / [[apps-emag-sync]] — sync sources to audit in Step 5.

## Open Questions

None.
