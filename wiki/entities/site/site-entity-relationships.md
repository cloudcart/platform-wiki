---
type: entity
nav_path: "Entity → Site → Relationships"
aliases: ["Site relationships", "Store relationships", "Site belongs to Account", "Site has many", "Site ownership", "Site not movable", "Site not cloneable", "Active plan drives gates", "Връзки на магазина"]
tags: [multistore, entity, core, relationships]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[site]]. See the hub for the other aspects (identity & config, tenancy & resolution, lifecycle, maintenance & data).

# Site — Relationships

## Identity

This aspect covers **what the Site owns and what owns it** — the belongs-to / has-many graph that makes the Site the centre of CloudCart's data model. It also covers the negative rules (what a Site is NOT: shared, movable, or cloneable from the admin) and the single most consequential relationship for the merchant's day-to-day: the active [[plan|Plan]], which drives every gate check in the admin panel.

## Aliases

- **Owning Account** — the one [[account|Account]] a Site belongs to.
- **Active Plan** — the single Plan that drives every gate.
- **Has-many** — Domains, Staff, and every business entity scoped to the Site.

## Key Attributes

### A Site belongs-to / has-many

A Site:

- **Belongs to one** [[account|Account]] — the merchant's billing identity. Standard accounts own exactly one Site (a multilang setup is the exception — see [[site-entity-tenancy-resolution]]).
- **Has one active** [[plan|Plan]] — drives every plan-gate check via [[plan-gates]].
- **Has many** [[domain|Domains]] — one primary plus zero-or-more aliases plus the always-present `<handle>.cloudcart.net` subdomain.
- **Has many** [[staff-member|Staff members]] — the merchant + any moderators who can log into the admin panel.
- **Has many** of EVERY business entity — [[product|Products]], [[customer|Customers]], [[order|Orders]], [[cart|Carts]], [[discount|Discounts]], [[category|Categories]], [[vendor|Vendors]], [[invoice|Invoices]], [[webhook|Webhooks]], [[api-key|API Keys]], [[apps|Apps]], [[campaign|Campaigns]], [[subscriber|Subscribers]], etc.
- **Has many** [[backup|Backups]] (when the backups subscription is active) — daily snapshots of all the above. See [[site-entity-maintenance-data]].
- **Has many** [[import-task|Import Tasks]] in the audit log, all scoped to this Site.
- **Belongs to one** issuer company — the CloudCart legal entity invoicing this Site (BG / DE / etc.), set at signup based on country. Drives which [[plan|Plans]] appear in the catalog (country-specific vs global).

### A Site is NOT

- **Shared across accounts** — each Site has exactly one owning Account. Multi-staff is achieved via [[settings-staff|Staff members]] on a single Site, not by sharing the Site between accounts.
- **Movable between accounts** — Site ownership transfer is a CloudCart-support-led process; there is no admin-panel button.
- **Cloneable from the admin** — there is no merchant-facing "duplicate this Site" action. Sister sites under multilang sync are created through [[apps-multilang]], NOT as full Site clones.

### The active Plan drives EVERY gate

Every plan-gate check on every admin screen (number of products allowed, SSL availability, partial-restore availability, custom-domain count, XML sync availability, etc.) resolves against the Site's active [[plan|Plan]] mapping per [[plan-gates]]. Exactly **ONE** active Plan per Site at any time. Changing the Plan changes what the merchant can do — instantly. There is no Plan-change cooldown; the new caps apply on the next request.

## Where it appears

- [[account]] — the owning Account; billing identity sits there.
- [[plans]] / [[plans-purchase]] — the Plan catalog and purchase flow for the Site's active Plan.
- [[settings-domains]] — the Site's Domain rows.
- [[settings-staff]] — the Site's staff members.
- [[settings-api-keys]] / [[settings-hooks]] — Site-scoped API Keys + Webhooks.

## Related

- [[site]] — hub.
- [[account]] — the one Account a Site belongs to.
- [[plan]] — the single active Plan; drives every gate.
- [[plan-feature]] — per-feature restriction values the active Plan exposes.
- [[plan-gates]] — where the gate checks resolve against the active Plan.
- [[domain]] — has-many Domain rows.
- [[staff-member]] — has-many staff members.
- [[backup]] — has-many backups (when the backups subscription is active).
- [[apps-multilang]] — the only path to a "sister" Site (not a clone).

## Open Questions

No outstanding questions.
