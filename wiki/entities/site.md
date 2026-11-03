---
type: entity
nav_path: "Entity → Site"
aliases: ["Site", "Store", "Store instance", "Shop", "Tenant", "Storefront", "Магазин", "Сайт", "Онлайн магазин"]
tags: [multistore, settings, entity, core, tenancy]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Site (Store)

## Identity

A **Site** is the merchant's complete store instance on CloudCart — the single tenant record that ties together everything the merchant owns on the platform: the storefront the customer browses, the admin panel the merchant logs into, every product / customer / order / setting / theme / app installation / discount / page that belongs to the business, the active subscription [[plan|Plan]], the attached [[domain|Domains]], and the per-store identity (name, primary email, currency, language, country). The Site is the **unit of multi-tenancy** in CloudCart: every other entity in the platform either belongs to one Site (an order, a product, a customer) or is shared across Sites (a Plan definition, a country list, a payment-provider catalog). When the platform serves a storefront page or an admin panel request, the first thing the routing layer does is **resolve the request's hostname to a Site** — and from there every downstream query is scoped to that Site's data. See [[site-entity-tenancy-resolution]].

Most CloudCart merchants own exactly **one Site per account** — one shop, one URL, one set of products. The platform also ships a multi-storefront capability where a single account can host multiple storefronts (each appearing as its own Site to the resolver), but for the typical merchant the Site = the account = the business. The Site is created at signup, suspended when the merchant lapses, and lives indefinitely while the merchant remains a customer — there is NO merchant-facing "delete Site" button. See [[site-entity-lifecycle]].

A Site is distinct from a [[domain|Domain]] (a Site can have many Domains attached), distinct from an [[account|Account]] (the merchant's billing identity that owns the Site), distinct from a [[plan|Plan]] (the catalog tier the Site is on), and distinct from a [[design|storefront / theme]] (the visual layer customers see — the Site can swap themes without losing data). The full belongs-to / has-many graph is on [[site-entity-relationships]].

This page is the **hub** for the Site entity. The substantive content lives in 5 aspect pages — drill into the one that matches the question.

## Aliases

- **Site** — the canonical platform term, used in support tickets ("your Site ID", "Site settings").
- **Store** — the customer-facing term in the admin UI ("Store settings", "Store details").
- **Store instance** / **Shop** — interchangeable phrasings.
- **Tenant** — used when emphasising the multi-tenancy architecture (one merchant = one tenant = one Site).
- **Storefront** — informally the customer-facing side of the Site (vs the admin panel).
- **Магазин** (standard BG term) / **Сайт** / **Онлайн магазин** — Bulgarian labels used interchangeably in the BG admin.

## Key Attributes

Five aspect pages own the substantive detail. This hub gives the top-level shape — drill in.

### Sub-pages (in this cluster)

- [[site-entity-identity-config]] — the immutable identifiers (Site ID, handle / `<handle>.cloudcart.net` subdomain) and the editable Site-wide identity ([[settings-general]] values: name, email, currency, language, country, timezone, unit system); the settings-cascade rule (one set of values feeds every customer-facing surface).
- [[site-entity-tenancy-resolution]] — the multi-tenancy model; how the hostname resolves to exactly one Site per request; the Site ID as the integration anchor for Webhooks + API; the multilang sister-site pattern (one Site per language, billed independently).
- [[site-entity-lifecycle]] — the phases (signup → active trial → active paid → suspended → reactivated → account closure); suspension causes; "suspension is reversible, deletion is not"; in-flight carts survive suspension.
- [[site-entity-relationships]] — the belongs-to / has-many graph (Account, Plan, Domains, Staff, every business entity, Backups); what a Site is NOT (shared / movable / cloneable from the admin); the active-Plan-drives-every-gate rule.
- [[site-entity-maintenance-data]] — maintenance mode (merchant-controlled, distinct from suspension); the Site-scoped backup rule; no self-serve full-Site export; the fixed-at-signup CloudCart subdomain + handle-rename-is-support-only rule.

### Top-level shape (orientation only)

| Aspect of the Site | Lives on |
|--------------------|----------|
| Who it is (name, email, currency, language, country, Site ID, handle) | [[site-entity-identity-config]] |
| How a request becomes "this Site" + multilang | [[site-entity-tenancy-resolution]] |
| Where it is in its life (signup → suspended → closure) | [[site-entity-lifecycle]] |
| What it owns / what owns it | [[site-entity-relationships]] |
| Maintenance, backups, data export, subdomain | [[site-entity-maintenance-data]] |

The Site also carries hundreds of granular per-store settings rows (cart behaviour, checkout fields, statuses, invoice numbering, payment providers, shipping providers, taxes, etc.) — each managed in its own [[settings]] sub-screen and all writing Site-level rows. See [[site-entity-identity-config]] for the cascade rule.

## Where it appears

- [[settings-general]] — Site identity (name, email, currency, language, country, timezone, units, copyright) and several Site-wide toggles (maintenance, order locking, admin security key).
- [[settings-domains]] — Domain attachment / primary-domain selection / SSL management. Drives hostname resolution.
- [[settings-cart]] / [[settings-statuses]] / [[settings-invoicing]] / etc. — all settings sub-screens write Site-level rows.
- [[settings-backups]] — Site-scoped backup snapshots (when the backups subscription is active).
- [[settings-staff]] — staff members who can log into THIS Site's admin panel.
- [[settings-api-keys]] / [[settings-hooks]] — Site ID chip in the header; API Keys and Webhooks are Site-scoped.
- [[plans]] / [[plans-purchase]] — the Plan catalog and purchase flow for the Site's active Plan.
- [[design]] / [[design-themes]] — storefront design surfaces; theme is a Site-level selection.
- [[account]] — the Account that owns the Site; billing identity sits there.

## Related

### Related entities

- [[account]] — the Account that owns the Site. Billing identity, payment methods, owner's email live there.
- [[plan]] — the catalog tier the Site is currently on; drives every gate check.
- [[plan-feature]] — per-feature restriction values that the Site's active Plan exposes.
- [[domain]] — Domain rows attached to the Site; one primary, others as aliases or always-present fallback.
- [[backup]] — daily snapshots of the Site's data (when the backups subscription is active).
- [[staff-member]] — staff who can log into the Site's admin panel.
- [[design]] — the storefront design hub; theme is a Site-level selection.

### Cross-cutting concepts

- [[plan-gates]] — every gate check resolves against the Site's active Plan.
- [[backups-and-restore]] — the Site-scoped backup-and-restore pipeline.
- [[notification-delivery]] — outbound email / SMS / Webhook / admin alerts all originate per-Site.

## Open Questions

No outstanding questions on the hub — all items resolved or distributed to aspect pages.
