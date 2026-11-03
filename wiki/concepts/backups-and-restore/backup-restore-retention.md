---
type: concept
nav_path: "Concept → Backups and restore → Retention and storage"
aliases: ["Backup retention window", "Backup retention pack", "Extend Period backups", "Backup storage location", "Backup file download", "Опациозен бекъп", "Период на пазене на бекъпите"]
tags: [backups, ops, retention, storage, concepts]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[backups-and-restore]]. See the hub for the other aspects (cadence, subscription gates, full restore, partial restore, safety backup, concurrency).

# Backups — retention and storage

## Definition

Each backup-subscription pack sells a specific **retention window** measured in days. The retention window is the maximum age of a backup the merchant can see on [[settings-backups]]; anything older is hidden and eventually purged. Typical packs sell 7, 30, 60, or 90 days of history. When a longer-retention pack is available on the merchant's plan, the **Extend period** button appears in the [[settings-backups]] header and clicks through to an upgrade flow that increases the retention window for future backups.

Backups themselves are stored off-platform — physically on a separate storage location managed by CloudCart infrastructure. The merchant cannot download a backup file, cannot view its contents, cannot see where it lives, and cannot restore a backup to a different store. All interaction with the file happens server-side via the Restore action on [[settings-backups]].

The single most-asked retention question is "why don't I see backups from before my subscription started?" — see [[backup-restore-cadence-content]] for the not-retroactive rule. The second is "why is the older backup gone?" — see the *Two visibility rules* section below.

## Scope

Covered:

- The retention window in days, sold per pack.
- The two combined rules that limit the visible list (age + subscription start).
- The Extend Period upgrade flow on [[settings-backups]].
- The off-platform storage model and what's opaque to the merchant.
- The no-download / no-export rule and how to get exportable data instead.

Not covered here:

- The daily snapshot cadence — see [[backup-restore-cadence-content]].
- The three-layer subscription gate — see [[backup-restore-subscription-gates]].
- Safety-backup retention behaviour (same window applies) — see [[backup-restore-safety-backup]].

## Contrasts

- **Retention window vs. subscription duration**: retention is "how many days of past backups are visible at any given moment" (rolling window). Subscription duration is "how long the merchant has been paying" (cumulative). A merchant on a 30-day pack who has been subscribed for two years sees backups from the last 30 days — not from two years ago.
- **Backup retention vs. order / data retention**: the retention window is for backup *snapshots*, not for the underlying order or customer data, which is kept until the merchant deletes it.
- **Off-platform storage vs. file-manager media storage**: backups live on a separate location managed for disaster recovery. [[settings-files]] media lives on a different file-storage system; the two are unrelated.

## Where it applies

### Retention — paid per-pack in days, hides anything older

Two combined rules limit the visible list on [[settings-backups]]:

- Backups **older than the retention window** are hidden from the list and eventually purged from storage.
- Backups from **before the merchant's subscription start date** are hidden too — backup history is NOT retroactive. See [[backup-restore-cadence-content]].

A merchant on a 30-day pack who subscribes today sees yesterday's backup tomorrow, and after 30 days of subscription will see the full 30-day rolling window. A merchant on a 7-day pack always sees at most the last 7 days regardless of how long they've been subscribed.

### Extend Period upgrade

When a longer-retention pack is available on the merchant's plan, the **Extend period** button appears in the [[settings-backups]] header. Clicking it opens an upgrade flow that:

- Increases the retention window for **future** backups.
- Does NOT retroactively recover already-purged backups that were lost under the old shorter window.
- Takes effect immediately for new daily snapshots and for safety backups taken from now on.

Practical guidance: a merchant about to do a high-stakes restore (a botched bulk import, a hack recovery) should consider extending their retention pack first — this preserves the safety backup the restore will auto-create. See [[backup-restore-safety-backup]] for why this matters.

### Storage — off-platform, opaque to the merchant

Backup files are physically stored on a separate off-platform storage location managed by CloudCart infrastructure (the database backups are compressed SQL dumps; CloudCart manages encryption / replication / off-site safety). The merchant cannot:

- Download a backup file directly to their own computer.
- View the file's contents in a browser.
- See where the file lives (the "Server" column in the backup list is informational only — meaningful for CloudCart support diagnostics, irrelevant to the merchant).
- Restore a backup to a DIFFERENT store (backups are scoped to the merchant's own store).

The merchant's only interaction with the file is to click **Restore** on the [[settings-backups]] list — the restore pipeline downloads the file server-side, decompresses it, and imports it into the live database.

### No download of backup files

The merchant cannot download a raw backup file. There is no "export backup as ZIP / SQL / CSV" button anywhere on [[settings-backups]] or anywhere else in the admin. All restoration runs server-side; backups never leave CloudCart infrastructure.

For a portable export of store data the merchant must use the platform's separate export pipeline (Products → Export, Orders → Export, Customers → Export) — NOT this system. Exports cover one entity type at a time, produce a downloadable CSV / XLSX file, and cannot be used to "restore" via [[settings-backups]].

### Server column is informational only

The list on [[settings-backups]] includes a "Server" column showing which CloudCart backend server stored the file. This is **informational only** for CloudCart support diagnostics — the merchant cannot act on it, and restore performs equally regardless of which server holds the file. Merchants should ignore the column unless support staff explicitly asks for it.

## Related

- [[backups-and-restore]] — hub.
- [[settings-backups]] — the admin screen with the Extend Period button.
- [[backup-restore-cadence-content]] — daily cadence + not-retroactive rule.
- [[backup-restore-subscription-gates]] — the subscription that pays for the retention pack.
- [[backup-restore-safety-backup]] — safety backups also age out under the same window.
- [[backup]] — the backup entity.

## Open Questions

None — all previously-flagged items in this aspect resolved.
