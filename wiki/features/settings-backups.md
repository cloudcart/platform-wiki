---
type: feature
nav_path: "Settings → Backup & Restore"
route_name: backups.settings.main
route_path: /admin/settings/backups
aliases: ["Backups", "Backup & Restore", "Daily backups", "Partial restore", "Бекъп", "Възстановяване", "Резервно копие"]
tags: [settings, backups, restore, subscription, plan-feature]
plan_gates: ["backups", "partial_restore"]
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Backup & Restore

## Purpose

A subscription-gated feature where the merchant manages automatic daily backups of the entire store (products, orders, customers, settings, etc.) and can restore the store from any backup. Two restore modes exist: **full restore** replaces all current data with the backup's snapshot (and runs the storefront in maintenance mode); **partial restore** (separate add-on) lets the merchant pick specific data segments and add only missing records — existing records are never overwritten.

The feature is **NOT free** — it requires both a plan that includes the `backups` feature AND an active `SiteSubscription` for that pack. Without both, the merchant sees a marketing splash + checkout CTA instead of the list. Partial restore is a further `partial_restore` add-on pack.

## Where to find it

Sidebar → Settings → **Backup & Restore**. Route `/admin/settings/backups` (list) or `/admin/settings/backups/:backupId/partial-restore` (per-backup segment picker). Breadcrumb reads "Settings → Backup & Restore" (with "Partial Restore" appended on the partial flow).

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[settings-backups-subscription-gates]] — the three-layer gate (plan feature, `backups` subscription, `partial_restore` add-on), retention-pack pricing in days, `PAST_DUE` grace, and the marketing-splash copy.
- [[settings-backups-list-view]] — the paginated backups table when subscribed: columns (`backup_date`, `file_size_formatted`, server, safety badge, `created_at`), per-row Restore / Partial Restore buttons, and the **Extend period** header CTA.
- [[settings-backups-full-restore]] — the destructive replace-everything mode: confirmation modal, storefront maintenance flag, non-cancellable execution, and the `system7` queue.
- [[settings-backups-partial-restore]] — the 15-segment picker page, `depends_on` resolution, `INSERT IGNORE` additive semantics, soft-deleted product un-delete step, and the temporary db-services database.
- [[settings-backups-safety-backup]] — the `is_safety=true` pre-restore snapshot auto-created before every restore, retention rules, and auto-deletion on partial-restore cancel.
- [[settings-backups-2fa-gate]] — the mandatory `Cc2FaAction` challenge for both restore types, action keys `restore_backup` / `partial_restore_backup`, single-use hash mechanics.
- [[settings-backups-restore-progress]] — the active-restore banner, 5-second polling cadence, the internal step labels surfaced live, the Cancel modal (partial only), and the completion email.

## What the merchant can do here

High-level capabilities (each aspect page details the mechanics):

- **Subscribe / upgrade** — buy the `backups` pack, buy the `partial_restore` add-on, or upgrade to a longer-retention pack via **Extend period**. See [[settings-backups-subscription-gates]].
- **Browse backups** — see every backup inside the retention window, with safety badges marking pre-restore snapshots. See [[settings-backups-list-view]].
- **Trigger a full restore** — click **Restore** on any row → confirm → pass 2FA → wait through maintenance mode. See [[settings-backups-full-restore]].
- **Trigger a partial restore** — click **Partial Restore** on any row → pick segments → confirm → pass 2FA → wait (no maintenance). See [[settings-backups-partial-restore]].
- **Watch progress** — live banner with the current step; for partial restores, optionally cancel. See [[settings-backups-restore-progress]].

### What the merchant CANNOT do here

- Trigger a backup manually — daily cadence is platform-managed; no "back up now" button.
- Download a backup file — restores are server-side; raw file is not exposed.
- View backup contents (no browser).
- Schedule a restore for later — restores fire immediately on confirmation.
- Restore to a different store — backups are scoped to the merchant's own site.
- Cancel a full restore — only partial restores can be cancelled.

## Settings & fields

Top-level UI lives in two places: the list page (when subscribed) and the partial-restore picker (per-backup). Detailed column / segment tables live in the aspect pages.

### Top-level meta fields surfaced to the UI

| Meta key | Drives |
|----------|--------|
| `feature_enabled` | Whether the merchant's PLAN includes the `backups` feature. False = upgrade-to-higher-plan prompt. |
| `subscribed` | Whether the merchant currently has an Active or Past-due `backups` `SiteSubscription`. False = marketing splash. |
| `partial_restore_subscribed` | Whether the merchant has the `partial_restore` add-on subscription. |
| `partial_restore_pack` | Whether a `partial_restore` pack is offered on the merchant's current plan. |
| `has_upgrade` | Whether a longer-retention pack is available — drives the **Extend period** button. |
| `has_active_restore` | Whether a restore is currently running — drives the banner + button disabling. |

See [[settings-backups-list-view]] for the list-table columns and [[settings-backups-partial-restore]] for the 15 segment keys + `depends_on` tree.

## Business rules

Cluster-wide invariants. Each rule is detailed in its aspect page:

- **Three-layer subscription gate** — plan-feature + `backups` subscription + (for partial) `partial_restore` add-on. `Active` or `PAST_DUE` grants access; cancellation drops access at the next billing date. See [[settings-backups-subscription-gates]].
- **No retroactive backups** — backup history starts at subscription activation; pre-subscription daily backups (if any exist on platform storage) are hidden from the list. See [[settings-backups-subscription-gates]].
- **Daily automatic cadence** — backups are taken every day automatically; no in-UI scheduler.
- **Retention window = subscription pack's `value` in days** — typical packs sell 7 / 30 / 60 / 90 days. The list cutoff is the platform code. See [[settings-backups-subscription-gates]].
- **Full restore replaces everything** — every product, order, customer, setting is overwritten by the snapshot. Files / images stored in the Files section are NOT affected. See [[settings-backups-full-restore]].
- **Partial restore is additive only** — only missing records are added; existing rows stay untouched (technically: `INSERT IGNORE`). Cannot undo edits to existing records. See [[settings-backups-partial-restore]].
- **Safety backup before every restore** — auto-created pre-restore snapshot tagged `is_safety=true`. Counts toward the same retention window. Auto-deleted when a partial restore is cancelled. See [[settings-backups-safety-backup]].
- **Mandatory 2FA on every restore call** — both `restore_backup` and `partial_restore_backup` actions require a verified single-use 2FA task hash. No 2FA configured = cannot restore. See [[settings-backups-2fa-gate]].
- **Only one restore at a time** — `has_active_restore` blocks new starts on every entry point.
- **Full restore is NOT cancellable** — the cancel endpoint explicitly rejects `full` type. Only partial restores can be aborted via the banner's Cancel button.
- **Storefront maintenance during full restore only** — full restore flips the `eu_cc_router.sites.maintenance` flag; partial restore leaves the store online.
- **Permission row hidden when plan lacks the feature** — the `settings.backups` permission row in [[settings-staff]] is silently hidden when the plan doesn't enable backups.
- **Completion email** — every restore (success or failure) emails the store owner using the merchant's locale.

## Plan gates

This feature is gated by two plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]). Detailed behaviour lives in [[settings-backups-subscription-gates]].

| Mapping | Shape | What it controls |
|---|---|---|
| `backups` | Plan-level boolean + paid `SiteSubscription` with `value` = retention days | Enables the list, full-restore controls, and access to the full feature. |
| `partial_restore` | Separate paid `SiteSubscription` add-on | Enables the Partial Restore button + the per-backup partial-restore route. |

## Related

- [[settings]] — parent hub.
- [[settings-staff]] — `settings.backups` permission row is conditionally hidden when the plan lacks the feature.
- [[settings-queue-view]] — restore jobs run on the `system7` queue and may surface there.
- [[account-cc2fa]] — the merchant's underlying 2FA configuration that gates restore calls.
- [[plan]] — `backups` and `partial_restore` plan features.
- [[plan-gates]] — concept page on plan-based feature gating.
- [[plan-vs-feature-pack]] — how subscriptions extend plan capabilities.
- [[settings-files]] — file-manager assets are NOT affected by database restores.
- [[backup]] — entity page.
- [[backups-and-restore]] — concept page on platform-wide backup behaviour.
- [[background-queue-inventory]] — catalogue of background processes; covers the daily backup snapshot schedule and where restore jobs surface while running.
- [[subscription-lifecycle]] — `Active` / `PAST_DUE` / cancellation transitions that govern access to this feature.

## Open questions

None — all previously-flagged items resolved or distributed to aspect pages.
