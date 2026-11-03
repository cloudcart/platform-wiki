---
type: entity
nav_path: "Entity → Site → Maintenance & data"
aliases: ["Site maintenance mode", "Store maintenance mode", "maintenance", "IP whitelist bypass", "Site backup scope", "Backup scope", "No full-Site export", "Site data export", "Handle rename", "CloudCart subdomain fixed", "Поддръжка на магазина", "Износ на данни"]
tags: [multistore, settings, entity, core, maintenance, backups]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[site]]. See the hub for the other aspects (identity & config, tenancy & resolution, lifecycle, relationships).

# Site — Maintenance & data

## Identity

This aspect covers the **operational toggles and data-boundary rules** of a Site: maintenance mode (a merchant-controlled "store temporarily closed" switch, distinct from suspension), the Site-scoped backup rule (a backup of Site A cannot restore into Site B), the absence of a self-serve full-Site export, and the fixed-at-signup CloudCart subdomain plus the support-only handle-rename path. These are the rules a merchant hits when they want to take the store offline for planned work, move data between stores, or change the store's URL identity.

## Aliases

- **Maintenance mode** (`maintenance`) — the merchant-controlled store-offline toggle.
- **IP whitelist bypass** — the merchant's own IP that can preview the store during maintenance.
- **Backup scope** — the per-Site boundary on backup / restore.
- **Handle rename** — the support-only change of the `<handle>.cloudcart.net` identifier.

## Key Attributes

### Maintenance mode is a separate, merchant-controlled toggle

Maintenance mode (controlled on [[settings-general]]) is independent of suspension (see [[site-entity-lifecycle]]). The merchant uses it for planned downtime (theme switch, big bulk-import, etc.) and can whitelist their own IP so they can preview the storefront while customers see the maintenance page. When ON, the storefront shows a maintenance page. Maintenance is also enabled **AUTOMATICALLY** during a full backup restore (per [[settings-backups]]) and removed when the restore completes.

### Backups respect Site scope

Backups are scoped to the Site — a backup of Site A cannot be restored into Site B. There is no merchant-facing "migrate Site to another account" via backups. The platform's restore pipeline writes back into the same Site's database tables. Backups are also per-Site across a multilang setup (backing up one sister Site does NOT back up the others — see [[site-entity-tenancy-resolution]]). See [[backup]] and [[backups-and-restore]].

### No self-serve full-Site data export

There is no single self-serve "download all my data" button. The merchant can export individual entities (products / customers / orders / etc.) via each entity's own CSV export action while the Site is still active. **Full-account data export on closure is a support-led process** — the merchant requests a backup snapshot via support before closure (see [[site-entity-lifecycle]] for the closure phase).

### The CloudCart subdomain is fixed at signup

The `<handle>.cloudcart.net` fallback subdomain is assigned when the Site is created and is NOT editable from anywhere in the admin panel. The merchant who wants a different storefront URL attaches a custom Domain via [[settings-domains]] and sets it as primary — the CloudCart subdomain stays as a permanent fallback URL.

### Site handle rename is not merchant-initiated

Merchant-initiated rename is **NOT supported anywhere** in the admin panel — the rename flow lives only in CloudCart-internal admin / support tools. The merchant's workaround is to attach a custom Domain via [[settings-domains]]; the `<handle>.cloudcart.net` subdomain stays as a permanent fallback. (The handle / Site ID identifiers themselves are documented on [[site-entity-identity-config]].)

## Where it appears

- [[settings-general]] — the maintenance-mode toggle + IP whitelist.
- [[settings-backups]] — Site-scoped backup snapshots; auto-maintenance during restore.
- [[settings-domains]] — custom-domain attachment (the handle-rename workaround).
- [[products-products]] / [[customers]] / [[orders]] — per-entity CSV export actions (the only self-serve export path).

## Related

- [[site]] — hub.
- [[settings-general]] — maintenance toggle + IP whitelist.
- [[settings-backups]] — the Site-scoped backup screen + auto-maintenance during restore.
- [[backup]] — Backup entity; per-Site scope.
- [[backups-and-restore]] — the restore pipeline that auto-enables maintenance.
- [[settings-domains]] — custom domain → the handle-rename workaround.

## Open Questions

No outstanding questions.
