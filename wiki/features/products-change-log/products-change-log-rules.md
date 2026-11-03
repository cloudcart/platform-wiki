---
type: feature
nav_path: "Products → (any product) → Change log → entry rules, retention & access"
route_name: ""
route_path: "/admin/products (modal)"
aliases: ["Change log rules", "Change log retention", "Change log purge", "One save one entry", "Change log read-only", "Cannot revert change log", "Change log permission", "Hard-delete purges log", "Изтриване на чейндж лог", "Право за чейндж лог"]
tags: [catalog, products, audit, history, debugging, support]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[products-change-log]]. See the hub for the other aspects (initiator decoding, logged fields).

# Products → Change log → Entry rules, retention & access

## Purpose

This aspect documents the **lifecycle and access rules** of the [[products-change-log|Change log]]: how entries are created (one per save), why the history is strictly read-only, what happens to the log when the product is deleted, how long entries are kept, and who can open the modal. It answers *"can I undo a change from here?"*, *"will I still see the history after I delete the product?"*, and *"who on my team can read this?"*.

## Where to find it

These rules apply to the [[products-change-log|Change log]] modal regardless of where it is launched — the [[products-products]] list row history icon or the product editor header dropdown. See the hub [[products-change-log]] for the launch points.

## What the merchant can do here

- Rely on a complete, chronological audit trail for one product — every save produces exactly one entry.
- Open the log for soft-deleted products (within the 10-day window) and still read full history.
- Open the log as any admin user who can see the products list (no separate permission to grant).

### What the merchant CANNOT do here

- Edit a log entry — the history is read-only.
- Revert a past change with one click — to undo, the merchant manually re-applies the old value in the product editor.
- Delete a single entry — there is no per-entry delete.
- Recover the log after the product is hard-deleted — the entire log is purged with the product.

## Settings & fields

This aspect has no editable controls — the Change log is read-only end to end. The fields shown in each entry (Date added / Changes / Initiator) are documented on [[products-change-log-fields]] and [[products-change-log-initiator]].

## Business rules

### Every product save creates exactly one entry — multi-field saves are NOT split

When the merchant changes 5 fields in one save through the editor, the change log writes ONE entry whose `Changes` column lists all 5 diffs. The platform does NOT create 5 separate rows. Same for API saves and bulk operations — one save = one entry, regardless of how many fields the save touched. (How those diffs render is on [[products-change-log-fields]]; who the save is attributed to is on [[products-change-log-initiator]].)

### The history is read-only — no edit, no one-click revert

The merchant cannot edit or delete an entry, and there is no revert button. To undo a past change, the merchant reads the old value from the diff and manually re-applies it in the product editor. The single-entry detail view (see [[products-change-log-fields]]) is also read-only.

### Hard-deleting the product purges its log

When a product is hard-deleted (after the soft-delete window expires, or via the API), the entire change log for that product is purged at the same time. The merchant cannot recover the history after hard-delete. Soft-deleted products (within the 10-day window — see [[product|Product]]) still have their log intact and viewable.

### Storage / retention

Log entries are written to the platform's logging store (separate from the operational database) and are retained for the lifetime of the product. The change log is part of the same record cluster that drives "did this product ever get edited" indicators elsewhere in the admin. Volume-wise, a product touched by a busy XML sync (e.g., hourly stock pushes) accumulates ~24 entries per day per stock-changed SKU; high-volume merchants should leave **Load all** OFF and paginate (see [[products-change-log-fields]]).

### Permission

Visible to all admin users who can see the products list. There is no separate ACL — if a merchant admin can see the products list, they can open the change log.

## Related

- [[products-change-log]] — hub.
- [[product]] — the product entity; the 10-day soft-delete window governs when the log survives a delete.
- [[products-products]] — the products list / editor where deletes and saves originate.
- [[products-change-log-fields]] — how each entry's diff is rendered and paginated.
- [[products-change-log-initiator]] — who each entry is attributed to.

## Open questions

- Retention beyond product hard-delete — for compliance investigations, whether a backup can be pulled after the cluster-level purge is not exposed in the merchant UI. (verify)
