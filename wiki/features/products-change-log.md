---
type: feature
nav_path: "Products → (any product) → Change log"
route_name: ""
route_path: "/admin/products (modal)"
aliases: ["Product change log", "Product history", "Product edit log", "Change log modal", "Product audit trail", "Чейндж лог на продукт", "История на продукт", "Аудит на промени"]
tags: [catalog, products, audit, history, debugging, support]
plan_gates: []
created: 2026-06-08
updated: 2026-06-10
source_count: 4
---
# Products → Change log

## Purpose

The **Change log** is a modal that shows, for one product (or bundle), a paginated **per-field diff history** of every change ever made to that product — who made the change, when, which field, the old value, and the new value. It is the **first place to look** when a merchant says *"my stock dropped (or returned) and nobody on my team changed it"* — the modal surfaces the actual actor (an admin user's name, the literal string `api2` for JSON-API v2 writes, a CloudCart support staff name when CC Console impersonation was used, or an inline "Edit from order #N" link when the change came from an order edit).

The Change log is the merchant's audit trail for **a single product's master record + all of its variants** — quantity, price, SKU, barcode, tags, options, status, active flag, threshold, tracking, `continue_selling`, vendor, category, images, dimensions, and the per-variant equivalents of each.

This page is the **hub** for the Change-log cluster. It covers the launch points and the headline rules; the detailed mechanics live in three aspect pages listed below.

## Sub-pages (in this cluster)

- [[products-change-log-initiator]] — the Initiator column: how to decode who/what made each change (`api2`, admin user, `Bulk`, "Edit from order #N", CC Console impersonation, import sources). The support-critical column.
- [[products-change-log-fields]] — what is and isn't logged; the 3-column diff table; `variants.updated` blocks; the `"To long"` placeholder for long-text fields; single-entry detail modal; pagination + Load all.
- [[products-change-log-rules]] — entry lifecycle (one save = one entry), read-only / no-revert, purge on product hard-delete, retention, and the permission model.

## Where to find it

The modal opens from two places — both anchored to a specific product:

1. **Products list** ([[products-products]]) → row actions cell → **history icon** (clock-arrow icon, label *"Change log"*). The icon is **green** when the product has at least one log entry, and **greyed out** when there are zero entries.
2. **Products list** → click a product to open the editor → **header dropdown** (the kebab menu next to Save) → **Change log**.

Same modal in both cases. The modal title is the product's name. The modal is also used for [[bundles-list|Bundles]] (the `type` prop accepts `"product"` or `"bundle"`). The launch icons themselves are detailed on [[products-change-log-link]].

## What the merchant can do here

- See every change ever made to this product, newest first — full diff mechanics on [[products-change-log-fields]].
- Click any row to open the **single-entry detail modal** (expanded diff for one change).
- Paginate 25 entries per page; toggle **Load all** to fetch the full history in one request.
- Read the **Initiator** column to identify the source of each change — decoding on [[products-change-log-initiator]].
- Cross-reference timestamps with order numbers, refund history, and API integration logs.

### What the merchant CANNOT do here

- Edit a log entry, or revert a past change with one click. The history is read-only — see [[products-change-log-rules]].
- Delete a single entry. Hard-deleting the product purges its entire change log automatically.
- Filter by field name or actor inside the modal, or export to CSV.

## Settings & fields

The modal renders a 3-column table — **Date added** (timestamp), **Changes** (per-field before/after diff), and **Initiator** (who/what caused it). The full column reference, the `variants.updated` grouping, the `"To long"` placeholder, and the single-entry detail modal are on [[products-change-log-fields]]. The Initiator column's decoding table is on [[products-change-log-initiator]].

## Business rules

- **One save = one entry.** A multi-field save produces a single entry listing all diffs; the platform never splits one save into multiple rows. See [[products-change-log-rules]].
- **Variant changes are logged on the PARENT product.** A Variant has no log of its own; its diffs appear under `variants.updated` on the parent — see [[products-change-log-fields]] and [[inventory-variant-model]].
- **The actor is always recorded.** Admin user / `Bulk` / `api2` / "Edit from order #N" / CC Console / import source — full decoding on [[products-change-log-initiator]].
- **Read-only + purged on hard-delete.** No revert; soft-deleted products keep their log, hard-delete purges it. See [[products-change-log-rules]].

## Related

- [[products-products]] — the products list where the modal is launched from.
- [[products-change-log-link]] — the launch icons (history icon + editor dropdown) on the products list.
- [[product]] — the product entity. The change log is a property of one product record.
- [[variant]] — variant changes are logged under the parent product (`variants.updated` block).
- [[inventory-tracking]] — the conceptual page for stock; the Change log is the primary debugging tool for stock-related support tickets.
- [[inventory-debugging-playbook]] — the 6-step "stock changed and we didn't change it" workflow that leans on this modal.
- [[orders-products]] — order-edit operations produce change-log entries with `action = order` and a clickable "Edit from order #N" link.
- [[orders-history]] — the order's own audit log (separate from the product change log).
- [[api-products]] — JSON-API v2 writes register `initiator.name = "api2"` in this log.
- [[settings-api-keys]] — when the actor is `api2`, the merchant disambiguates which integration ran the call here.
- [[apps-csv-import]] / [[apps-xml-sync]] — import jobs register themselves as the initiator with their source identifier.
- [[order-processing-pipeline]] — Stage 2 stock movement; the modal complements this by showing WHO triggered the variant-quantity diff.

## Open questions

- None at the hub level — aspect-specific uncertainties live on each sub-page.
