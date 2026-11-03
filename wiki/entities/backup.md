---
type: entity
aliases: ["Backup", "Store backup", "Daily backup", "Safety backup", "Snapshot", "Reserve copy", "Restore point", "Бекъп", "Резервно копие", "Снимка на магазина"]
tags: [settings, ops, backups, restore, plan-feature, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---

# Backup

## Identity

A **Backup** is a single point-in-time snapshot of the merchant's [[site|Site]] data — the full store database (products with variants and parameters, categories, vendors, customers and their addresses, orders with line items and discounts and fulfillments and payments and history, customer groups, properties, discounts, pages, blog content, settings, and all the merchant-configured data the platform uses internally) captured as a `.sql.gz` file and stored on a separate off-platform storage location managed by CloudCart infrastructure.

Backups exist in two flavors: **daily auto-backups** taken every day automatically while the merchant's backups subscription is active, and **safety backups** auto-created right before every full or partial restore as a rollback point — both flavors appear in the same list on [[settings-backups]], distinguished only by the **safety** badge. The merchant cannot trigger a Backup manually (there is no "back up now" button), cannot download a Backup file, cannot view its contents in a browser, and cannot restore a Backup to a different Site. See [[backup-entity-identity]] for the full daily-vs-safety contrast and what a Backup is NOT.

A Backup is the merchant's primary **disaster-recovery artifact** — there is NO undo button anywhere in the admin, no "revert last action" affordance, no browser-history rollback. Backups are the rollback mechanism. They are also a **paid plan-gated add-on** with three independent gates: the [[plan|Plan]] must include `backups`, the merchant must subscribe to the Backups service, and the optional Partial Restore mode needs a separate `partial_restore` pack. See [[backup-entity-gating]].

## Aliases

- **Backup** — the canonical platform term used in the admin UI ("Backup & Restore") and across the wiki.
- **Store backup** — emphasises Site-scope.
- **Daily backup** — the daily auto-snapshot variant.
- **Safety backup** — the variant auto-created before every restore as a rollback point; distinguished by the safety badge.
- **Snapshot** — informal phrasing.
- **Restore point** — phrasing used when explaining the merchant-facing concept (a point in time the store can revert to).
- Bulgarian: **Бекъп** (standard), **Резервно копие**, **Снимка на магазина** (informal).

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[backup-entity-identity]] — what a Backup IS, the daily vs safety flavors, the "not retroactive" rule, the contrast with manual CSV exports.
- [[backup-entity-attributes]] — the per-Backup fields the merchant sees in the list (ID, date, file size, server, safety flag, retention).
- [[backup-entity-lifecycle]] — daily creation → pre-restore creation → visible → used → aged-out → subscription-lapse, plus cancelled-restore auto-cleanup.
- [[backup-entity-gating]] — the three independent gates (Plan feature, Backups subscription, `partial_restore` add-on), staff permission, `PAST_DUE` grace.
- [[backup-entity-restore-pipeline]] — full restore (replaces everything, maintenance mode) vs partial restore (additive, 9 segments, dependencies), safety backup, 2FA, cancellation rules.
- [[backup-entity-storage-and-scope]] — off-platform opaque storage, file-manager media is NOT in the DB Backup, no webhook events, no completion notification, stock-after-restore audit warning.

## Key Attributes

Backups carry a small set of merchant-visible fields plus a few platform-internal ones. The full attribute table is on [[backup-entity-attributes]]; the rough shape is: Backup ID (auto), backup date (default-sort key), file size (formatted + raw KB), server (informational), safety flag (drives the badge), created-at, and the dynamic retention window dictated by the merchant's specific Backups-subscription pack.

A Backup is NOT downloadable, NOT viewable, NOT named (no merchant-supplied label), NOT tag-able, NOT shareable across Sites. The merchant's only interaction with a Backup is to click its **Restore** or **Partial Restore** action on the [[settings-backups]] list.

## Where it appears

- [[settings-backups]] — the master management screen. Shows the list of available Backups, the marketing splash + checkout when not subscribed, the per-row Restore and Partial Restore actions, the Extend Period and Subscribe to Partial Restore buttons in the header.
- [[settings-queue-view]] — long-running restore jobs (full and partial) run on the platform queue and surface here during execution.
- [[settings-staff]] — `settings.backups` permission row is conditionally hidden when the Plan doesn't include backups (see [[backup-entity-gating]]).

## Related

### Related entities

- [[site]] — the Site whose data is snapshotted; Site-scoped end-to-end.
- [[plan]] — `backups` and `partial_restore` plan-features gate access to this whole system.
- [[plan-feature]] — the Backups subscription is a plan-feature subscription on top of the base [[plan|Plan]].
- [[product]] / [[customer]] / [[order]] / [[category]] / [[vendor]] / [[discount]] / [[blog-article]] — all included in the Backup snapshot.
- [[admin-notification]] — no automated "restore complete" alert is raised (see [[backup-entity-storage-and-scope]]).

### Cross-cutting concepts

- [[backups-and-restore]] — the concept page that explains the full Backup-and-restore pipeline (daily cadence, partial restore, safety Backups, retention, subscription lapse).
- [[plan-gates]] — plan-feature gating that controls visibility of this whole system.
- [[notification-delivery]] — relevant for understanding why no automated email goes out on restore completion (the merchant polls).
- [[import-pipeline]] — the bulk-import pipeline that often motivates merchants needing a Backup (a botched import is a primary "I need to restore" scenario).

## Open Questions

- Whether the `<handle>.cloudcart.net` SSL behaviour during a full restore (when maintenance mode is on) keeps serving the maintenance page on HTTPS — verify that customers don't see TLS errors during the restore window. See [[backup-entity-restore-pipeline]].
