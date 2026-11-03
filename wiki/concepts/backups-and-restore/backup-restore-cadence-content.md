---
type: concept
nav_path: "Concept → Backups and restore → Cadence and content"
aliases: ["Daily backup cadence", "What's in a backup", "Backup content", "Backup schedule", "No manual backup", "Backups not retroactive", "Дневен бекъп", "Какво се запазва в бекъпа"]
tags: [backups, ops, cadence, snapshot, concepts]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[backups-and-restore]]. See the hub for the other aspects (subscription gates, retention, full restore, partial restore, safety backup, concurrency).

# Backups — cadence and content

## Definition

CloudCart takes a backup of every subscribed store **every day, automatically**. The cadence is platform-managed; the merchant cannot force a manual "back up now" from the admin UI, cannot change the schedule, and there is no scheduler control on [[settings-backups]] — backups just appear in the list each day. The daily backup is a snapshot of the merchant's **full store database**, captured as a compressed SQL dump and stored off-platform (see [[backup-restore-retention]] for the storage model).

The "no manual trigger" rule is one of the two most-misunderstood aspects of the feature. A merchant about to do a risky operation (mass edit, big import, theme switch) cannot click a button to take a fresh backup right beforehand — they get whatever yesterday's snapshot captured. The mitigation is to subscribe AND wait at least 24 hours before any risky operation, so at least one snapshot exists.

The other most-misunderstood aspect is **what's in a backup vs what's NOT**. The snapshot covers the database (records, settings, content) but does NOT roll back file-manager media files on a restore — see *File-manager media excluded* below.

## Scope

Covered:

- The daily-snapshot cadence (one per day, per subscribed store, fully automated).
- The merchant's lack of a manual "back up now" trigger and lack of schedule control.
- The full list of what's in a database backup (products, orders, customers, settings, content).
- The file-manager media exclusion and the broken-image-link side-effect on restore.
- The "not retroactive" rule (no snapshots from before the subscription start date).

Not covered here:

- How long backups are kept — see [[backup-restore-retention]].
- The three-layer gate that controls whether the backup is even taken — see [[backup-restore-subscription-gates]].
- The off-platform storage model — see [[backup-restore-retention]].
- Restore mechanics — see [[backup-restore-full-restore]] and [[backup-restore-partial-restore]].

## Contrasts

- **Daily backup vs. Safety backup**: both appear in the same list; the daily backup is auto-created on the schedule, the [[backup-restore-safety-backup]] is auto-created before every restore.
- **Daily backup vs. Manual export**: backups capture the whole database and are NOT downloadable. Manual exports (Products → Export, Orders → Export) cover one table at a time and ARE downloadable, but cannot be used as a restore source.
- **Database backup vs. File-manager media**: only the database is rolled back on restore. Media files in [[settings-files]] are stored separately and stay in current state — see *File-manager media excluded* below.

## Where it applies

### Daily automatic backups — no manual trigger

CloudCart takes a backup of every subscribed store **every day, automatically**. The cadence is platform-managed; the merchant cannot:

- Trigger a manual "back up now" from anywhere in the admin.
- Change the daily schedule.
- See a scheduler control on [[settings-backups]].

The merchant's interaction with the schedule is read-only: open [[settings-backups]] and check whether yesterday's row appears in the list.

### What gets backed up — the entire store database

The daily backup captures the merchant's full store database:

- Products with variants and parameters
- Categories, vendors, properties
- Customers and their addresses, customer groups
- Orders with line items, discounts, fulfillments, payments, history
- Discounts (rules, codes, Pro discounts, cart rules)
- Pages, blog content
- All merchant-configured settings (notifications, shipping, payment, branding, etc.)
- Plus all merchant-configured data the platform uses internally

The snapshot is a single point-in-time view of everything the merchant has built. There is no "partial backup" or "selective backup" — the merchant cannot choose which entities to include. Granular control happens only at RESTORE time via the [[backup-restore-partial-restore]] segment picker.

### File-manager media excluded from the database backup

File-manager media assets (product photos, CMS-page images, branding assets) live in CloudCart's separate file storage and are backed up at the file-storage level — NOT as part of the database backup. The database snapshot stores the file *references* (paths, filenames) but the binary files remain in current state at file-storage level.

**A restore reverts database records to the snapshot but does NOT roll media files back in time.** If a media file was deleted from [[settings-files]] AFTER the snapshot, the database row referencing it will be restored but the underlying file will be missing — a broken image link. Merchants restoring older snapshots should expect some image links to fail if files have been cleaned up in the interim.

### Backups are not retroactive

The marketing splash on [[settings-backups]] makes this explicit: *"Backup history starts from the moment the service is activated and does not include past data."* If the merchant subscribes today, the first backup will be **tomorrow** — yesterday's snapshot does not exist. The platform does NOT keep pre-subscription snapshots even if it took backups daily before the merchant subscribed; pre-subscription rows are filtered out of the merchant's list.

Practical guidance for risky operations:

- A merchant planning a theme switch, big bulk-import, or mass-edit should subscribe to backups AND wait at least 24 hours BEFORE the operation.
- Without that wait, no snapshot exists to roll back to.
- Subscribing AND running the risky operation the same day = no usable rollback point.

### Backups are scoped per store

Each store on a multi-store account has its OWN backup history — see [[backup-restore-subscription-gates]] for the per-store subscription rule.

## Related

- [[backups-and-restore]] — hub.
- [[settings-backups]] — the admin screen that lists the daily backups.
- [[settings-files]] — file-manager media files; NOT in the database backup.
- [[backup-restore-retention]] — how long these daily snapshots are kept.
- [[backup-restore-subscription-gates]] — the gates that control whether daily backups are taken.
- [[backup-restore-safety-backup]] — the other backup variant that appears in the same list.
- [[backup]] — the backup entity.

## Open Questions

None — all previously-flagged items in this aspect resolved.
