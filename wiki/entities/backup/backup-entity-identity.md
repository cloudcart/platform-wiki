---
type: entity
aliases: ["Backup identity", "What a Backup is", "Daily backup vs safety backup", "Backup flavors", "Restore point definition", "Backup not retroactive"]
tags: [settings, ops, backups, restore, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[backup]]. See the hub for the other aspects (attributes, lifecycle, gating, restore pipeline, storage and scope).

# Backup — Identity

## Identity

A **Backup** is a single point-in-time snapshot of the merchant's [[site|Site]] data — the full store database captured as a `.sql.gz` file and stored on a separate off-platform storage location managed by CloudCart infrastructure. One Backup = the entire store database. There is no "partial backup" or "selective backup" — the merchant cannot pick which entities to include. Granular control happens only at RESTORE time via the Partial Restore segment picker (see [[backup-entity-restore-pipeline]]).

The snapshot captures: products with variants and parameters, categories, vendors, customers and their addresses, orders with line items and discounts and fulfillments and payments and history, customer groups, properties, discounts, pages, blog content, settings, and all the merchant-configured data the platform uses internally.

A Backup is the merchant's primary **disaster-recovery artifact** — the only way to recover from accidental deletes, botched bulk imports, malware / hijacked-admin damage, or catastrophic data loss is to restore from a Backup via [[settings-backups]]. There is NO undo button anywhere in the admin; no "revert last action" affordance; no browser-history-style rollback. Backups are the rollback mechanism.

## Aliases

- **Backup** — the canonical platform term used in the admin UI ("Backup & Restore") and across the wiki.
- **Store backup** — emphasises Site-scope.
- **Daily backup** — the daily auto-snapshot variant.
- **Safety backup** — the variant auto-created before every restore as a rollback point; distinguished by the safety badge.
- **Snapshot** — informal phrasing.
- **Restore point** — phrasing used when explaining the merchant-facing concept (a point in time the store can revert to).
- Bulgarian: **Бекъп** (standard), **Резервно копие**, **Снимка на магазина** (informal).

## Key Attributes

Backups exist in exactly two flavors:

| Flavor | When it's created | `is_safety` | Surfaces |
|--------|-------------------|-------------|----------|
| **Daily backup** | Every day automatically, while the merchant's backups subscription is active | `false` | Appears in [[settings-backups]] list with no badge. |
| **Safety backup** | Automatically, right before every full or partial restore | `true` | Appears in the same list with a **safety** badge. |

Both flavors:

- Live in the same list on [[settings-backups]] and are sorted by `backup_date` descending (newest first).
- Age out under the same retention rules (see [[backup-entity-lifecycle]]).
- Can be restored from in the same way.

The safety classification is derived from the snapshot's stored filename containing `_safety`. The merchant does not pick which flavor to create — both are platform-managed.

A Backup is NOT:

- **Created on-demand by the merchant.** There is NO "back up now" button. The daily schedule is platform-managed; cadence is once a day per subscribed Site, no UI to change it.
- **Downloadable.** There is NO "export backup as ZIP / SQL / CSV" button anywhere. The merchant cannot pull a Backup file onto their own computer.
- **Viewable.** The merchant cannot open a Backup in a browser to see what's inside.
- **Mergeable across Sites.** A Backup of Site A cannot be restored into Site B — Backups are Site-scoped end-to-end.
- **Editable.** Backups are read-only artifacts; the merchant cannot rename, re-tag, or partial-delete them.
- **Named.** No merchant-supplied label; identified only by date + safety badge.

## Backups are NOT retroactive

The marketing splash on [[settings-backups]] makes this explicit: *"Backup history starts from the moment the service is activated and does not include past data."* If the merchant subscribes today, the first Backup will be **tomorrow** — yesterday's snapshot does not exist.

Merchants planning a risky migration (theme switch, big bulk-import, mass-edit) should subscribe AND wait at least 24 hours BEFORE the operation so they have at least one Backup to roll back to. Backups taken before the merchant's subscription start date are also hidden from the list — only post-subscription Backups are surfaced.

## Backup vs other recovery mechanisms

A Backup is distinct from:

- **Manual exports** (Orders → Export, Customers → Export, and the per-order ordered-products export) — merchant-initiated CSV / XLSX files covering ONE entity type, downloadable, NOT usable for restore. (There is no product-catalogue CSV export screen; to get the catalogue out, the merchant builds an [[apps-xml-feed|XML product feed]] or uses the [[apps-google-sheets|Google Sheets app]].)
- **CSV import re-upload** — recreating products from the original CSV restores the data shape but NOT the original IDs, historical order / cart references to those products, SEO URL handles, or anything else tied to row IDs. Only a Backup restore recovers the exact pre-state.
- **Order / product change logs** — change logs ([[products-change-log]]) record what changed but cannot reverse a change; only a Backup restore can roll back the underlying record.

## Where it appears

- [[settings-backups]] — the master list where both daily and safety Backups appear with the **safety** badge distinguishing them.
- [[backup-entity-attributes]] — the full attribute table per Backup row.
- [[backup-entity-lifecycle]] — how the two flavors come into existence and how they age out together.

## Related

- [[backup]] — hub.
- [[backups-and-restore]] — concept-level explanation of the Backup-and-restore pipeline.
- [[site]] — the Site whose data is snapshotted; Site-scoped end-to-end.
- [[settings-backups]] — the admin screen where Backups are listed and restored.

## Open Questions

None.
