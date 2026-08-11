---
type: feature
nav_path: "Settings → Backup & Restore → Partial restore"
route_name: backups.partial-restore
route_path: /admin/settings/backups/:backupId/partial-restore
aliases: ["Partial restore", "Segment picker", "Selective restore", "Restore segments", "Soft-deleted product recovery"]
tags: [settings, backups, restore, partial-restore, segments]
plan_gates: ["backups", "partial_restore"]
created: 2026-06-10
updated: 2026-06-11
source_count: 5
---

> Part of [[settings-backups]]. See the hub for the other aspects.

# Backups — partial restore

## Purpose

A **partial restore** lets the merchant pick specific data segments (Products, Orders, Customers, etc.) from a backup and restore only those. It is **append-only**: existing records are never overwritten — only records missing from the live store are added. This makes it useful for recovering deleted records, but it cannot undo edits to records that still exist. It requires the separate `partial_restore` add-on subscription on top of the base `backups` subscription. Unlike full restore, it does NOT put the storefront into maintenance mode — the store stays online while the restore runs.

## Where to find it

Sidebar → Settings → **Backup & Restore** → **Partial Restore** button on any backup row → `/admin/settings/backups/{backupId}/partial-restore`. The button appears only when `meta.partial_restore_subscribed=true` ([[settings-backups-subscription-gates]]).

## What the merchant can do here

- Tick the segments to restore from the 15-card grid; use **Select all** / **Deselect all**.
- See dependencies auto-tick and acquire a lock icon when a dependent segment is picked.
- Click **Restore selected segments** → confirmation modal → 2FA challenge → dispatch.
- Cancel an in-progress partial restore via the active-restore banner's Cancel button ([[settings-backups-restore-progress]]).

## Settings & fields

### Segment picker page layout

- Blue info callout at the top: *"Only missing records will be restored"* + *"Existing data in your store will not be overwritten. A safety backup will be created before restoring."*
- Header: *"Select segments to restore"* + **Select all** / **Deselect all** buttons.
- A 3-column grid (1 / 2 columns on mobile / tablet) of **15 segment cards** — each with a checkbox, label, `(N tables)` count, and (where applicable) a *"Requires: `{label-list}`"* line.
- Footer counter: `{N} segments selected ({M} auto-selected as dependencies)` + **Restore selected segments** primary button (disabled until a segment is picked, or while another restore runs).
- Active-restore banner when `meta.has_active_restore=true`: *"A restore is already in progress. Please wait for it to complete before starting a new one."* — cards are disabled.

### The 15 data segments

Segment keys, labels, dependencies, and coverage:

| Segment key | Label | Depends on | Covers |
|---|---|---|---|
| `categories` | Categories | — | Categories + category-access restrictions. |
| `vendors` | Vendors | — | Brand / vendor records. |
| `customer_groups` | Customer Groups | — | Customer-group definitions. |
| `properties` | Properties | categories | Property definitions (color, size, material…) + option lists. |
| `products` | Products | categories, vendors, properties | Products + variants + everything attached (parameters, quantities, bundles, collections, images, labels, statuses, custom filters, quantity discounts, upsell / cross-sell, tags, suppliers, Google Shopping mappings, etc.). Largest segment by far. |
| `customers` | Customers | customer_groups | Customer accounts + addresses + custom fields + saved cards + password-reset codes + tags + subscriber linkage. |
| `orders` | Orders | customers, products, shipping | Orders + line items + addresses + meta + applied discounts + fulfillments and returns + status history + payments + shipping + taxes + totals + banned-IP records. |
| `discounts` | Discounts | customer_groups | Discount rules + codes + Pro discount targets + customer / group links + advanced cart rules. |
| `pages` | Pages | — | CMS pages + content + history snapshots. |
| `blogs` | Blogs | — | Blog posts + articles + tags + comments. |
| `shipping` | Shipping | — | Shipping providers + rates + boxes + tracking. |
| `subscribers_and_segments` | Subscribers & Segments | — | Subscribers + RFM scoring + Messenger subscribers. |
| `campaigns` | Campaigns | subscribers_and_segments | Campaigns + actions + logs + saved templates. |
| `settings` | Settings | — | Geo zones, taxes, navigations, redirects, logos, banners, hooks, API keys, GDPR records, admins, 2FA codes. |
| `apps` | Apps | — | App settings + per-app data tables (Barsy, Colibri, XML-feed, etc.). |

Merchants CAN partial-restore "just settings" or "just shipping" — both are pickable segments.

### Dependency UI behaviour

Ticking a segment with dependencies auto-ticks its dependency segments, which acquire a **lock icon** (`fa-lock`, tooltip *"Required by selected segments"*) and cannot be un-ticked while the dependent is still selected. A selected card's border and background tint change.

### Partial-restore confirmation modal

Opens after **Restore selected segments**. **Title**: *"Partial Restore"*. **Body**: *"You are about to restore the following segments: `<segment-name-list>`"* + *"Only missing records will be added. Existing data will not be modified."* + a blue info callout *"A safety backup will be created before restoring."* **Yes** + **No** buttons (same as full restore).

Yes opens the 2FA challenge modal ([[settings-backups-2fa-gate]]). On success the merchant returns to the backups list with a *"Partial restore initiated"* toast and the active-restore banner ([[settings-backups-restore-progress]]).

## Business rules

### Partial restore is additive ONLY

Restoring a segment only adds records missing from the live store. Records that already exist are silently skipped, not updated — preserved as-is even if they differ from the backup. Example: if the merchant renamed a category AFTER the backup, partial-restoring categories will NOT bring back the old name. To undo edits to existing records, use [[settings-backups-full-restore]] (data loss).

### Dependencies are auto-included even via the API

Before the restore runs, the selection is expanded to include all parent segments. Selecting only `orders` automatically pulls in `customer_groups, customers, products, vendors, properties, categories, shipping`. The API enforces this — submitting `orders` without its parents is rejected.

### Soft-deleted products are reactivated when restoring Products

A dedicated step runs only for the Products segment: products marked deleted in the live store but NOT deleted in the backup are un-deleted and reactivated. This is what "brings back deleted products" — the record still exists (so the additive import skips it), so this step reactivates it instead. It works only for soft-deleted products (still present, just hidden as deleted); products purged entirely are simply re-inserted from the backup under their original ID.

### Partial restore does NOT enable maintenance mode

Unlike full restore, it leaves storefront maintenance untouched. Because only missing records are added (no destructive write phase), customers can't see inconsistent data.

### Cancellation is supported (unlike full restore)

A running partial restore can be cancelled via the active-restore banner's Cancel button. Cancellation cleans up the temporary working data, deletes the safety backup auto-created for this restore, and marks the request cancelled. The live store's state then depends on how far the restore got — possibly partially restored, possibly not started. See [[settings-backups-restore-progress]] for the cancel modal and step labels.

### Safety backup and mandatory 2FA

Like full restore, a safety snapshot is created before the import phase ([[settings-backups-safety-backup]]). Every partial-restore call (`POST /backups/{id}/partial-restore`) also requires a verified single-use 2FA challenge with action `partial_restore_backup` ([[settings-backups-2fa-gate]]).

## Related

- [[settings-backups]] — hub.
- [[settings-backups-subscription-gates]] — the separate `partial_restore` add-on subscription required for this mode.
- [[settings-backups-full-restore]] — the alternative when "only missing rows" is not enough.
- [[settings-backups-safety-backup]] — the pre-restore safety snapshot.
- [[settings-backups-2fa-gate]] — `partial_restore_backup` action key.
- [[settings-backups-restore-progress]] — the active-restore banner and Cancel button for partial restores.
- [[products-products]] — soft-deleted-product mechanics referenced above.

## Open questions

- Whether the `apps` segment covers third-party apps' data dirs outside the database (verify).
- Behaviour when a restored row references an excluded parent — verify skip vs error.
