---
type: feature
nav_path: "Products → (any product) → Change log → Initiator column"
route_name: ""
route_path: "/admin/products (modal)"
aliases: ["Change log initiator", "Who changed my product", "Change log actor", "Initiator decoding", "api2 actor", "CC Console change", "Edit from order link", "Кой промени продукта", "Инициатор на промяна"]
tags: [catalog, products, audit, history, debugging, support]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-change-log]]. See the hub for the other aspects (logged fields, business rules).

# Products → Change log → Initiator

## Purpose

The **Initiator** column of the [[products-change-log|Change log]] modal answers the single question that drives almost every change-log support ticket: **who or what changed this product?** It is the column the merchant reads when stock dropped (or returned) and nobody on the team admits to touching it. The Initiator cell decodes the actual actor — an admin user's name, the literal string `api2` for JSON-API v2 writes, a CloudCart support staff name when CC Console impersonation was used, an import source, or an inline **"Edit from order #N"** link when the change came from an order edit.

## Where to find it

It is the rightmost (third) column of the Change log table — open the modal from the [[products-products]] list (row history icon) or the product editor's header dropdown, then read across each row. See [[products-change-log]] for the launch points.

## What the merchant can do here

- Read the **Initiator** cell on any row to identify the source of that change.
- Click the **"Edit from order #N"** link (when present) to jump to the originating order at `/admin/orders/details/N`.
- Cross-reference an `api2` entry against [[settings-api-keys]] to find which integration ran the call.
- Escalate to support when a `(CC Console: <name>)` suffix appears on a change the merchant didn't authorise.

### What the merchant CANNOT do here

- Filter the list by actor — the merchant scrolls the chronological list and reads each Initiator cell.
- See WHICH specific API key made an `api2` call from inside this modal — that disambiguation happens on [[settings-api-keys]].
- See the support engineer's reason for a CC Console change — only that one occurred.

## Settings & fields

The Initiator cell stacks up to three things vertically:

1. The actor's **name** — an admin user's `log_name`, the literal `api2`, a system / import source identifier, or empty for some legacy entries.
2. An optional **"(CC Console: <name>)"** suffix — present when a CloudCart support engineer was logged in via CC Console impersonation at the time of the change.
3. The **action** — a single word or short phrase describing what the actor did.

### Initiator decoding (the critical column for support investigation)

| Initiator name | Action | What it means |
|---|---|---|
| *<admin user email or name>* | `Update` / `Create` / `Delete` | The merchant or one of their admins changed the product through the regular admin UI. |
| *<admin user>* | `Bulk` | The change came from a bulk action on [[products-products]] (mass publish / mass tag / bulk inventory update / etc.). |
| `api2` | `Update` / `Create` / `Delete` | An external integration wrote to this product through the [[api-products\|Products JSON-API v2 endpoint]]. The integration's specific API key is captured separately in the platform's audit log. |
| *<staff name>* | `Update` / `Create` | A merchant admin acted on the product. |
| *<system source>* | `Order` | An order-edit operation changed the product. The action renders as a **clickable link**: **"Edit from order #N"** pointing to `/admin/orders/details/N` — the merchant clicks through to see the originating order. This is the case for *productAdd*, *productEdit*, and *productRemove* operations triggered from [[orders-products]] (the order detail's Products tab). |
| *<import source>* | `Update` | A CSV / XML / ERP import wrote to the product. Specifically, the [[apps-csv-import]] / [[apps-xml-sync]] / ERP-app integrations register themselves as the initiator with the import's source identifier. |
| *<empty>* with `(CC Console: <name>)` | any | A CloudCart support engineer made the change via CC Console. The merchant did NOT make this change — escalate to support if the merchant didn't authorise it. |

## Business rules

### `api2` actor = JSON-API v2 wrote the product

Every write through the [[api-products|Products JSON-API v2 endpoint]] (POST / PATCH / DELETE) registers `initiator.name = "api2"`. The platform's API key audit (separate from this modal) captures WHICH specific API key made the call — the merchant's [[settings-api-keys]] page shows last-used timestamps per key. For ticket investigation, seeing `api2` here means "an external integration did this — check which integrations are active and which API keys are in use".

### Order-edit changes link back to the order

When a merchant edits the line items of an order ([[orders-products]] → +Add / Edit / Remove product), the per-line edit also writes an entry into the AFFECTED PRODUCT's change log with `action = order`. The modal renders that action as a clickable link **"Edit from order #N"** pointing to `/admin/orders/details/N`. This is critical for the *"who reduced my stock"* investigation — the product change log surfaces the originating order directly. The diff itself (which field changed) is described under [[products-change-log-fields]].

### CC Console impersonation is surfaced as a suffix

When CloudCart support staff is logged in via CC Console impersonation, the Initiator column appends `(CC Console: <staff name>)`. If the merchant sees this on a change they didn't expect, escalate to support to investigate. This is the only way to distinguish a real merchant-user action from a support-engineer action when the action would otherwise look identical in the log.

### Bulk operations name the action `Bulk`

Mass publish, mass tag, bulk-quantity update from [[products-inventory]], change vendor, change category, etc. all register their entries with `action = Bulk`. The merchant identifies the operator from the Initiator name column. The set of fields changed in one bulk save is still collapsed into a single entry — see [[products-change-log-fields]].

### Import sources self-register

A CSV / XML / ERP import writes entries whose Initiator is the import's source identifier and whose action is `Update`. A product touched by a busy XML sync (e.g., hourly stock pushes) accumulates a steady stream of such entries — see [[products-change-log-rules]] for the volume note.

## Related

- [[products-change-log]] — hub.
- [[products-products]] — the products list where the modal launches from.
- [[orders-products]] — order-edit operations produce `action = order` entries with the "Edit from order #N" link.
- [[orders-details]] — the order detail the "Edit from order #N" link points to.
- [[api-products]] — JSON-API v2 writes register `initiator.name = "api2"`.
- [[settings-api-keys]] — when the actor is `api2`, the merchant disambiguates which integration ran the call here.
- [[apps-csv-import]] / [[apps-xml-sync]] — import jobs register themselves as the initiator with their source identifier.
- [[inventory-debugging-playbook]] — the 6-step "stock changed and we didn't change it" workflow that leans on this column.

## Open questions

- For an `api2` entry, surfacing the specific API key name directly in the modal (instead of requiring a separate [[settings-api-keys]] lookup) is not currently supported. (verify)
