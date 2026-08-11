---
type: concept
nav_path: "Concept → Backups and restore → Full restore"
aliases: ["Full restore", "Restore from backup", "Database replacement restore", "Maintenance mode restore", "Storefront downtime restore", "Възстановяване на целия магазин", "Пълно възстановяване"]
tags: [backups, ops, restore, full-restore, downtime, concepts]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[backups-and-restore]]. See the hub for the other aspects (cadence, subscription gates, retention, partial restore, safety backup, concurrency).

# Backups — full restore

## Definition

A **full restore** replaces the entire store's database with the snapshot — every product, customer, order, setting, page, and discount reverts to its state at the time of the chosen backup. Anything created or edited since the backup is **lost** with no merge / preserve option. The storefront goes down for the duration via maintenance mode; customers visiting the store see CloudCart's maintenance page, not the catalog. This is **NOT zero-downtime**.

A full restore is the only way to undo edits to existing records — [[backup-restore-partial-restore]] is append-only and cannot overwrite existing data. So the merchant needing to "roll back the bulk price-edit I did yesterday" needs a full restore (with all the post-backup data loss that implies), not a partial one.

The most-asked operational question is "how long does the storefront stay down?" — see the *Storefront maintenance window* section below. The second is "what about the orders that came in after the backup?" — those are **gone**; see *Post-backup data destruction*.

## Scope

Covered:

- The full-restore pipeline (maintenance mode → safety backup → download → decompress → import → verify → maintenance off).
- The storefront downtime and per-store-size estimates.
- The post-backup data loss (orders, edits, customer signups).
- The inventory-recalculation implications after a cross-order-window restore.
- The no-cancellation-from-admin rule for full restores.
- Practical guidance for scheduling and customer communication.

Not covered here:

- The additive / partial restore mode — see [[backup-restore-partial-restore]].
- The safety backup auto-creation — see [[backup-restore-safety-backup]].
- 2FA gate and concurrency rules — see [[backup-restore-concurrency]].

## Contrasts

- **Full restore vs. Partial restore**: full replaces everything (storefront down, post-backup data lost); partial adds missing records only (storefront stays up, existing data preserved). Full can undo edits; partial cannot. See [[backup-restore-partial-restore]].
- **Full restore vs. Safety backup rollback**: a safety backup IS a daily-style backup auto-created right before a restore. Restoring from a safety backup IS a full restore (or partial) against that earlier snapshot. See [[backup-restore-safety-backup]].
- **Full restore vs. Cancelling the restore**: full restores **cannot be cancelled** from the admin once started. Only partial restores can be cancelled. See [[backup-restore-concurrency]].

## Where it applies

### Full restore — replaces everything, takes the storefront DOWN

A full restore is **NOT zero-downtime**. The restore job:

1. **Enables maintenance mode** on the storefront — customers visiting the store see the platform's maintenance page, not the catalog. Existing carts are interrupted; checkout is blocked.
2. Creates a **safety backup** of the current state and adds it to the backup list with the safety badge. See [[backup-restore-safety-backup]].
3. Downloads the chosen backup file from off-platform storage to a temporary location.
4. Decompresses the file (typically `.sql.gz`).
5. Imports the SQL into the live database — every product / order / customer / setting is **replaced** with the snapshot.
6. Verifies the restored database.
7. **Disables maintenance mode** — storefront comes back up.

Everything the merchant or customers created since the chosen backup is **gone** after step 5.

### Storefront maintenance window

The storefront DOES go down during a full restore (maintenance mode is enabled before the database import and removed only after verification). Expected windows:

- **Typical store** (a few thousand products, a few thousand orders): minutes to a half-hour.
- **Very large store** (100k+ products, millions of orders): an hour or more.

Practical guidance for scheduling:

- Schedule restores during low-traffic hours (overnight, very early morning).
- Warn active customers via their own channels (newsletter, social media) BEFORE the restore — NOT via the storefront, it'll be showing the maintenance page.
- Do NOT start a restore in the middle of a sale / promotion / Black Friday traffic.
- Do NOT start a restore right before a known peak (an ad campaign launch, an influencer post).

### Post-backup data destruction

Restoring to yesterday's snapshot means TODAY's data is gone. There is no "merge" or "preserve recent data" option for full restore. What's lost: orders placed after the backup, new customers registered after the backup, edits to customer / product / settings records, bulk-import results applied after the backup.

If preserving recent data matters more than rolling back edits, the merchant should use [[backup-restore-partial-restore]] for the specific segment that needs recovery — but partial restore is append-only, so it only recovers DELETED records, not edits.

### Stock / inventory implications after a full restore

A full restore also restores inventory levels to the snapshot. If the merchant restored from a backup taken before today's orders:

- The order data is gone (those orders never happened from the platform's perspective).
- Inventory shows the pre-order levels.
- BUT the actual physical stock on the shelf may have been picked / packed / shipped for those vanished orders.

The platform has no record those orders ever existed, so the merchant should **manually audit inventory after a restore that crosses an order window** — comparing physical stock to the restored quantity for any SKU that sold between the backup and the restore. See [[inventory-tracking]] for the per-Variant audit approach.

### Full restores cannot be cancelled from admin

Once started, a full restore CANNOT be cancelled from the admin panel. The Cancel action on a running restore (visible via [[settings-queue-view]] or the active-restore banner on [[settings-backups]]) accepts only partial restores; cancelling a full restore returns a validation error. If a full restore is in trouble, the merchant must contact CloudCart support. The cancellation rules are documented in [[backup-restore-concurrency]].

This is intentional — a full restore that's partway through a SQL import would leave the database in an inconsistent state if killed mid-import. The platform forces the restore to run to completion or be reverted by CloudCart support manually.

### Recovering from a bad full restore

If the restore completed but the result is bad, the path forward is to restore again — from the safety backup that the platform auto-created in step 2. The rollback window is limited by retention. See [[backup-restore-safety-backup]].

## Related

- [[backups-and-restore]] — hub.
- [[settings-backups]] — the admin screen with the Restore action.
- [[settings-queue-view]] — where the running restore job surfaces.
- [[backup-restore-partial-restore]] — the additive alternative (no downtime, append-only).
- [[backup-restore-safety-backup]] — the auto-created rollback point.
- [[backup-restore-concurrency]] — the 2FA gate, one-at-a-time rule, and cancellation rules.
- [[backup-restore-retention]] — how long the safety backup stays available for rollback.
- [[inventory-tracking]] — manual inventory audit after a cross-order-window restore.
- [[notification-delivery]] — no automated "restore complete" email; the merchant polls.

## Open Questions

- ⏸️ The exact maintenance window for a "large" store — depends on the store's database size and infrastructure throughput; CloudCart doesn't publish a per-store estimate. Merchants with large catalogs (100k+ products) should expect minutes of downtime; smaller stores typically seconds.
- ⏸️ Whether the storefront's TLS / HTTPS keeps serving the maintenance page cleanly during the restore window — verify that customers don't see TLS errors when CloudCart serves the maintenance page over HTTPS during a long restore. (verify)
