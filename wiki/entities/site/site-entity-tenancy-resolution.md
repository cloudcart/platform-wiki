---
type: entity
nav_path: "Entity → Site → Tenancy & resolution"
aliases: ["Site tenancy", "Multi-tenancy", "Hostname resolution", "Site resolution", "One Site per request", "Site ID integration anchor", "Multilang sister sites", "Sister Site", "Multi-storefront", "Tenant resolution", "Резолюция на магазин по домейн"]
tags: [multistore, tenancy, entity, core, resolution]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[site]]. See the hub for the other aspects (identity & config, lifecycle, relationships, maintenance & data).

# Site — Tenancy & resolution

## Identity

This aspect covers **how a request becomes "this Site"** — the multi-tenancy model, hostname-to-Site resolution, the Site ID as the integration anchor for Webhooks and API calls, and the multilang sister-site pattern where one Account owns several Sites. The Site is CloudCart's **unit of multi-tenancy**: every business entity belongs to exactly one Site, and every storefront / admin request is scoped to exactly one Site for its entire duration.

## Aliases

- **Multi-tenancy** — one merchant = one tenant = one Site (typically).
- **Hostname resolution** — matching the request's `Host` header to a Site's Domain rows.
- **Site ID integration anchor** — the identifier Webhooks and API calls carry to name the store.
- **Sister Site** / **multilang sister sites** — separate Sites under one Account, one per language.
- **Multi-storefront** — the capability for one Account to host multiple storefronts.

## Key Attributes

### One Site per Account (typically)

Standard CloudCart accounts own exactly one Site — one shop, one URL, one set of products. The platform supports **multi-storefront** mode where a single account can host multiple storefronts (each appearing as its own Site to the request resolver). For the typical merchant the simplification *Site = Account = Business* holds. The owning-Account relationship and the "a Site is not movable/shared between accounts" rules are on [[site-entity-relationships]].

### Hostname resolution determines the Site

Every storefront and admin-panel request is dispatched through a resolution layer that matches the request's `Host` header against the Sites' Domain rows. The matched Site becomes the request's "current Site" — every downstream database query, settings read, theme render, etc. is scoped to that Site. There is NO multi-Site context per request: **one request = one Site**. The `<handle>.cloudcart.net` fallback subdomain and any attached custom Domains all resolve to the same Site. See [[domain]] for how Domain rows are attached and which one is primary.

### Site ID is the integration anchor

Every Webhook delivery carries the Site ID context (so the receiver knows which store the event came from). Every API call from an integration sends the Site ID alongside the [[api-key|API Key]] for authentication. The Site ID is shown as a chip in the page header on [[settings-api-keys]], [[settings-hooks]], and several developer-facing screens for easy copying. Because the Site ID is immutable (see [[site-entity-identity-config]]), integrations can rely on it as a stable key across the Site's whole lifetime.

### Multilang sister sites are separate Sites

The [[apps-multilang]] multilang feature creates **one Site per language** (a separate Site for the EN storefront vs the BG storefront vs the DE storefront, all under one Account). Each sister Site has its own Site ID, its own primary Domain, its own settings, and its own data tables — they are NOT views on a shared dataset. The multilang sync mechanism translates / copies content between them on the merchant's schedule.

**Each sister Site is billed independently.** One Account can own multiple Sites (the multilang setup), but each Site has its own active [[plan|Plan]] subscription, its own subscription cycle, its own invoices. Backups are also per-Site — backing up Site A does NOT back up Site B (see [[site-entity-maintenance-data]]).

Because each sister Site resolves from its own primary Domain, hostname resolution naturally routes a customer to the correct language Site — there is no per-request language switch on a shared tenant; the language *is* the Site.

## Where it appears

- [[settings-domains]] — Domain attachment / primary-domain selection; the input to hostname resolution.
- [[settings-api-keys]] / [[settings-hooks]] — Site ID chip; API + Webhook scoping.
- [[apps-multilang]] — creates and syncs sister Sites (one per language).
- [[json-api-v2]] — API calls scoped by Site ID + API Key.
- [[plans-purchase]] — each sister Site purchases its own Plan.

## Related

- [[site]] — hub.
- [[domain]] — Domain rows; the matchable hostnames per Site.
- [[account]] — the Account that can own one or several (sister) Sites.
- [[apps-multilang]] — multilang sister-site creation + sync.
- [[api-key]] — paired with the Site ID for API authentication.
- [[plan]] — each Site (including each sister) has its own active Plan.
- [[json-api-v2]] — the API that uses the Site ID as the integration anchor.

## Open Questions

No outstanding questions.
