---
type: concept
nav_path: "Concept → Backups and restore"
route_name: ""
route_path: ""
aliases: ["Backups", "Backup and restore", "Store backups", "Disaster recovery", "Restore from backup", "Safety backup", "Daily backup", "Backup retention", "Бекъп", "Резервно копие", "Възстановяване на магазина", "Възстановяване от бекъп"]
tags: [backups, ops, disaster-recovery, plan-feature, concepts]
plan_gates: ["backups", "partial_restore"]
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Backups and restore

## Definition

**Backups and restore** is the CloudCart-managed data-protection system that snapshots the merchant's entire store database every day, holds those snapshots for the retention window the merchant has purchased, and lets the merchant roll the live store back to any of those snapshots via the [[settings-backups]] screen. The whole feature is a **plan-gated paid add-on** — backups are NOT a free platform service. The merchant's plan must include the `backups` plan-feature AND the merchant must be actively subscribed to the backups pack; without both, the [[settings-backups]] screen shows a marketing splash and a checkout flow instead of the list of available backups.

Two restore modes exist. **Full restore** replaces the entire store's database with the snapshot — every product, customer, order, setting reverts to its state at the time of the chosen backup, and anything created or edited since the backup is **lost**. **Partial restore** is a separate add-on subscription (`partial_restore` pack on top of the base `backups` pack) that lets the merchant pick which of nine data segments to restore — and it is **append-only**: only records missing from the live store are restored from the backup, existing records are NEVER overwritten. Before every restore (full or partial), the platform auto-creates a **safety backup** of the current state so the merchant has an automatic rollback point if the restore turns out badly.

The most-asked operational questions are **what's gated** (see [[backup-restore-subscription-gates]]) and **what gets lost on a full restore** (see [[backup-restore-full-restore]]).

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[backup-restore-cadence-content]] — daily auto-snapshot cadence (no manual trigger); what's in a backup (full DB); file-manager media exclusion; not-retroactive rule.
- [[backup-restore-subscription-gates]] — the three-layer gate (plan-feature, active subscription, partial-restore add-on); ACTIVE / PAST_DUE access window; subscription lapse → loss of access; per-store scoping on multi-store accounts.
- [[backup-restore-retention]] — retention window per subscription pack (7 / 30 / 60 / 90 days); Extend Period upgrade; off-platform storage opacity; no merchant download.
- [[backup-restore-full-restore]] — replaces everything; maintenance-mode storefront downtime; post-backup data loss; inventory implications; no cancellation from admin.
- [[backup-restore-partial-restore]] — append-only mode; the nine selectable segments and their dependency enforcement; storefront stays live; cannot undo edits.
- [[backup-restore-safety-backup]] — auto-created before every restore; counts toward retention; auto-deleted on cancelled restore; second-chance rollback after a bad restore.
- [[backup-restore-concurrency]] — only one restore at a time per store; 2FA gate to start any restore; cancellation behaviour (partial only); `settings.backups` permission row.

## Scope

Covered across the 7 sub-pages:

- Daily-snapshot cadence + what's in / NOT in a backup.
- Retention window + the rules that hide old or pre-subscription backups.
- Three subscription gates.
- Full and partial restore mechanics.
- Safety backups as automatic rollback points.
- Restore concurrency, 2FA gate, cancellation rules, permission gating.

What it does NOT cover:

- The **per-row UI** of [[settings-backups]] — that's the feature-page topic.
- **Manual data export** via Products / Orders / Customers → Export — a separate platform feature.
- **Code / theme / file-manager media backups** downloadable by the merchant — none exist.

## Contrasts

- **Backups vs. Manual exports**: backups are CloudCart-managed snapshots of the full database, NOT downloadable. Manual exports (Products / Orders / Customers → Export) are merchant-initiated CSV / XLSX exports of one entity type, downloadable, and CANNOT be used as a restore source.
- **Full restore vs. Partial restore**: full restore REPLACES everything (storefront goes down, all post-backup data lost). Partial restore ADDS missing records (storefront stays up, existing data preserved). Full restore can undo edits; partial restore cannot. See [[backup-restore-full-restore]] vs [[backup-restore-partial-restore]].
- **Safety backup vs. Daily backup**: both appear in the same list, distinguished by the **safety** badge. Daily backups are auto-created on the daily schedule; safety backups right BEFORE every restore as a rollback point. Both age out under the same retention window. See [[backup-restore-safety-backup]].
- **Backups vs. CSV import re-upload**: re-uploading the original CSV recreates the products by data shape but DOES NOT restore original IDs, the historical order / cart references, SEO URL handles, or anything tied to row IDs. Only a backup restore recovers the exact pre-import state.
- **Backups vs. Browser history / undo**: there is NO undo button in CloudCart's admin and no "revert last action" feature. Only a backup restore (full or partial) recovers deleted data.
- **Backups feature subscription vs. CloudCart plan**: the plan determines IF backups is available (plan-level gate); the subscription is a SEPARATE recurring purchase on top of the plan. See [[backup-restore-subscription-gates]].

## Where it applies

### Admin-side surfaces (merchant sees these)

- [[settings-backups]] — the only admin screen for backups. Shows the list of available backups when subscribed, the marketing splash + checkout when not. Per-row Restore and Partial Restore actions. Extend period and Subscribe to Partial Restore buttons in the header.

### Adjacent surfaces

- [[settings-staff]] — the `settings.backups` permission row in the staff Access tree (visible only when the plan includes backups). See [[backup-restore-concurrency]] for the permission rule.
- [[settings-queue-view]] — restore jobs (full and partial) run on the platform queue and may appear here during a long-running restore.
- [[settings-files]] — file-manager media is stored separately from the store database. A restore reverts only the database; media files are NOT time-rewound (deleted media won't be re-uploaded just because a database row referencing it is restored). See [[backup-restore-cadence-content]].
- [[plan]] — the merchant's plan must include the `backups` and (optionally) `partial_restore` plan-features.

### Entities

- [[backup]] — entity page for an individual backup record.

### Concepts

- [[plan-gates]] — explains the plan-feature gating mechanism that this whole system depends on.
- [[notification-delivery]] — the restore job is a long-running background process; there's no automatic "restore complete" email to the merchant (the merchant must check [[settings-backups]] manually).

## Related

- [[settings-backups]] — the admin screen for backups.
- [[backup]] — the backup entity.
- [[plan-gates]] — plan-feature gating that controls visibility of this whole system.
- [[plan]] — `backups` and `partial_restore` are plan-features on the merchant's plan.
- [[settings-staff]] — `settings.backups` permission row is conditionally hidden when the plan doesn't include backups.
- [[settings-queue-view]] — long-running restore jobs may surface here.
- [[settings-files]] — file-manager media files are NOT rolled back by a restore.
- [[notification-delivery]] — no automated merchant notification on restore complete; merchant must check manually.
- [[background-queue-inventory]] — catalogue of all background processes; covers the daily backup-snapshot job timing and where long-running restore jobs appear.

## Open Questions

- ⏸️ The exact maintenance window for a "large" store — depends on the store's database size and infrastructure throughput; CloudCart doesn't publish a per-store estimate. Merchants with large catalogs (100k+ products) should expect minutes of downtime; smaller stores typically seconds. See [[backup-restore-full-restore]].

All other previously-flagged questions resolved or distributed to sub-pages.
