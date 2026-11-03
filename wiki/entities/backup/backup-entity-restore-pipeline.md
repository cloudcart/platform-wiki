---
type: entity
aliases: ["Backup restore pipeline", "Full restore", "Partial restore", "Restore segments", "Restore dependencies", "Restore 2FA", "Restore cancellation", "Safety backup before restore", "One restore at a time"]
tags: [settings, ops, backups, restore, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[backup]]. See the hub for the other aspects (identity, attributes, lifecycle, gating, storage and scope).

# Backup — Restore pipeline

## Identity

A **restore** is how the merchant actually USES a Backup. Two modes exist: **full restore** (replaces the entire database with the snapshot, takes the storefront down with maintenance mode) and **partial restore** (additive only — fills in missing records for the segments the merchant picks, no downtime). Both are gated by two-factor verification, both auto-create a safety Backup of the pre-restore state, and only one restore (full OR partial) can run at a time per Site.

The Backup file itself is never modified by a restore — the source `.sql.gz` is read-only against the restore. After the restore completes, the source Backup remains in the list and can be restored from again.

## Aliases

- **Restore** — the platform term.
- **Full restore** — replaces everything.
- **Partial restore** — segment-picker, additive.
- **Restore pipeline** — the platform job that runs the restore.
- **Safety backup** — the pre-restore snapshot auto-created at the start of every restore.

## Key Attributes

The two restore modes side-by-side:

| Behaviour | Full restore | Partial restore |
|-----------|--------------|-----------------|
| **What it does** | Replaces everything with the snapshot. | Adds ONLY records missing from the live store, for the picked segments. Never overwrites. |
| **Storefront downtime** | YES — maintenance mode on for the whole job. | NO — storefront stays live. |
| **2FA required** | YES. | YES. |
| **Pre-restore safety Backup** | YES. | YES. |
| **Cancellable from admin** | NO. | YES — via [[settings-queue-view]]. |
| **Plan gate** | Backups subscription. | `partial_restore` add-on ON TOP — see [[backup-entity-gating]]. |
| **One restore at a time** | YES — system-wide per Site. | YES — same lock. |

## Full restore — replaces EVERYTHING, takes storefront DOWN

A full restore is **NOT zero-downtime**. The restore job steps:

1. Auto-creates a fresh safety Backup of the current state (`is_safety=true`).
2. Enables **maintenance mode** on the storefront — customers visiting see the maintenance page.
3. Downloads the chosen Backup file from off-platform storage to a temporary location.
4. Decompresses the `.sql.gz` file.
5. Imports the SQL into the live database — every product / order / customer / setting is replaced with the snapshot.
6. Verifies.
7. Disables maintenance mode.

For a typical store this takes minutes to a half-hour; for very large stores (100k+ products, millions of orders) an hour or more. **Anything the merchant or customers created since the chosen Backup is gone** — including orders placed during the restore window. Warn the team and pause campaigns before initiating a full restore.

## Partial restore — additive only, no storefront downtime

The optional `partial_restore` add-on adds a per-Backup **Partial Restore** action that opens a segment-picker form. The merchant ticks which of **9 data segments** to restore — and only records MISSING from the live store are added. Existing records are NEVER overwritten:

| Segment | What it covers (merchant-facing) | Auto-requires |
|---------|----------------------------------|---------------|
| **Categories** | Product categories + category-access restrictions | — |
| **Vendors** | Brand / vendor records | — |
| **Customer Groups** | Customer-group definitions | — |
| **Properties** | Product properties (color, size, material) + their option lists | Categories |
| **Products** | Products + variants + all attached product data (parameters, quantities, bundles, collections, files, banners, labels, smart selections, linked products, quantity discounts, upsell / cross-sell, tags, suppliers) | Categories, Vendors, Properties |
| **Customers** | Customer accounts + addresses + custom fields + saved cards + tags | Customer Groups |
| **Orders** | Orders + line items + addresses + discounts + fulfillments + payments + shipping + history | Customers, Products |
| **Discounts** | Discount rules + codes + Pro discount targets + cart rules | Customer Groups |
| **Pages** | CMS pages + content + page-history snapshots | — |

The picker shows dependencies visually and auto-selects required segments. The platform also **enforces dependencies server-side** — submitting `Orders` without `Customers` and `Products` is REJECTED. So the merchant cannot accidentally start an inconsistent partial restore.

Partial restore is **append-only**: it can recover deleted records but cannot undo edits to existing ones. To recover from an edit, the merchant needs a full restore (with data loss for everything after the Backup).

Like full restore, partial restore also creates a safety Backup before running. The storefront stays live throughout.

## Two-factor verification required to start any restore

Both the full Restore and Partial Restore actions REQUIRE a 2FA verification step before the job is dispatched. The merchant requests a one-time code, enters it, and only then does the restore job get enqueued. A request with a missing or expired verification returns 422 *"Two-factor verification required."* This applies to every restore — there is no "remember device" or skip for trusted admins.

## Only partial restores are cancellable

The merchant can cancel a running **partial** restore via the queue / active-restore banner; cancellation:

- Drops the queued job.
- Removes any orphaned temporary databases the partial restore created.
- Deletes the safety Backup that was auto-created for the cancelled restore (so a cancelled partial restore leaves no trace in the list — see [[backup-entity-lifecycle]]).

Full restores **cannot be cancelled from the admin panel** — the cancel endpoint returns 422 *"Only partial restores can be cancelled."* If a full restore is in trouble, the merchant must contact CloudCart support.

## One restore at a time — per Site

Only ONE restore (full OR partial) can run at a time per Site. If one is in progress, the merchant sees *"A restore is already in progress. Please wait for it to complete before starting a new one."* and the start button is blocked. The lock is system-wide — a partial restore blocks a parallel full restore and vice versa.

## Safety Backup before EVERY restore

Before every restore, the platform auto-creates a safety Backup of the pre-restore state. Safety Backups appear in the same [[settings-backups]] list with the safety badge, count toward the retention window, are auto-deleted on partial-restore cancellation (so cancelled partial restores leave no trace), and can be restored from the same way as a daily Backup.

## Where it appears

- [[settings-backups]] — per-row Restore and Partial Restore actions launch the pipeline.
- [[settings-queue-view]] — long-running restore jobs surface here during execution; partial-restore cancellation lives here.

## Related

- [[backup]] — hub.
- [[backup-entity-gating]] — `partial_restore` add-on gate that unlocks Partial Restore.
- [[backup-entity-lifecycle]] — pre-restore safety Backup creation + cancelled-restore auto-delete.
- [[backups-and-restore]] — concept-level pipeline overview.
- [[settings-queue-view]] — the queue surface.

## Open Questions

- Whether the `<handle>.cloudcart.net` SSL behaviour during a full restore (when maintenance mode is on) keeps serving the maintenance page on HTTPS — verify that customers don't see TLS errors during the restore window. `(verify)`
