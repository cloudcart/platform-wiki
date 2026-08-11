---
type: feature
nav_path: "Products → Products → Change log (launch points)"
route_name: ""
route_path: "/admin/products/products-new (modal launcher)"
aliases: ["Product change log launch", "Change log button", "Change log icon", "Launch change log", "History icon", "Чейндж лог бутон"]
tags: [catalog, products, audit, history, launcher]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, variants matrix, bulk actions, AI content, known issues).

# Products — Change log launch points

## Purpose

This page is a **pointer**, not a full feature page. The Change log modal itself (per-field diff history, Initiator decoding, paginate / load-all behaviour, modal table columns) is fully documented on its own page: **[[products-change-log]]**.

This aspect exists to record the two places on the Products list / editor where the modal is launched from — so the support agent can answer *"how do I open the change log?"* without context-switching.

## Where to find it

The modal opens from two places — both anchored to a specific product:

1. **[[products-list-view|Products list]]** → row actions cell → **history icon** (clock-arrow icon, label *"Change log"*). The icon is **green** when the product has at least one log entry, and **greyed out** when there are zero entries.
2. **[[products-editor|Edit product]]** → header dropdown (the kebab menu next to Save) → **Change log**.

Same modal in both cases. The modal title is the product's name. The modal is also used for [[bundles-list|Bundles]] (the `type` prop accepts `"product"` or `"bundle"`).

## What the merchant can do here

Open the modal. That is all this aspect covers — for everything the modal does (columns, pagination, Initiator decoding, single-entry detail modal), read **[[products-change-log]]** in full.

## Settings & fields

The icon's visual state on [[products-list-view]] reflects log presence:

- **Green** clock-arrow icon → the product has ≥ 1 change-log entry.
- **Greyed out** → no entries (the product has never been edited since creation, OR all entries were cascade-deleted with the product but the product survived a restore).

The editor header dropdown's Change log entry is always present (no icon-state indicator); clicking it on a product with no entries opens the modal in its empty state.

## Business rules

### The Change log is the first place to look for "stock changed and we didn't change it"

When a merchant asks *"my stock dropped (or returned) and nobody on my team changed it"* — the modal's **Initiator** column surfaces the actual actor: an admin user's name, the literal string `api2` (for JSON-API v2 writes), a CloudCart support staff name (CC Console impersonation), or an inline *"Edit from order #N"* link (when an order edit changed the stock). See [[products-change-log]] for the full Initiator decoding table and the [[inventory-debugging-playbook]] 6-step diagnostic.

### Long-text fields show as placeholders

The Change log records `description` / `short_description` with the placeholder `"To long"` rather than the full value — see [[products-change-log]] for the rationale and the workaround.

### Hard delete purges the log

Deleting the product cascades to its change-log entries — see [[products-known-issues]] for the cascade table.

## Related

- [[products-change-log]] — the actual Change log modal page (per-field diff history, columns, pagination, Initiator decoding).
- [[products-products]] — hub.
- [[products-list-view]] — origin point #1 (row history icon).
- [[products-editor]] — origin point #2 (header dropdown).
- [[inventory-debugging-playbook]] — the 6-step diagnostic that uses the Change log to investigate unexpected stock changes.
- [[bundles-list]] — the same modal is used for bundles via the `type` prop.

## Open questions

None.
