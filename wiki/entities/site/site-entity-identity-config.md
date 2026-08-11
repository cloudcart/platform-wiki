---
type: entity
nav_path: "Entity → Site → Identity & configuration"
aliases: ["Site identity", "Store identity", "Site settings", "Store name", "site_name", "site_email", "Store currency", "Storefront language", "language_cp", "Site handle", "Site ID", "Store country", "Store timezone", "unit_system", "Settings cascade", "Идентичност на магазина"]
tags: [multistore, settings, entity, core, identity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[site]]. See the hub for the other aspects (tenancy & resolution, lifecycle, relationships, maintenance & data).

# Site — Identity & configuration

## Identity

This aspect covers **who the Site is** — the identifiers the platform assigns at signup (immutable) plus the store-wide identity values the merchant edits on [[settings-general]]. These values define the store across every customer-facing surface: the storefront, checkout, transactional emails, invoices, exports, and the admin UI header. There is exactly **one** set of these values per Site, and they cascade — the merchant edits them once and every downstream surface reads them. There is no per-product / per-customer / per-order override of the Site's currency or language on a single-Site shop.

The values split into two groups: **assigned-at-signup-and-fixed** (Site ID, handle) versus **merchant-editable** (name, email, currency, language, country, timezone, units).

## Aliases

- **Site ID** — the immutable numeric identifier; the integration anchor (see [[site-entity-tenancy-resolution]]).
- **Handle / slug** — the merchant-visible identifier used in the `<handle>.cloudcart.net` fallback subdomain.
- **Store name** (`site_name`), **Primary email** (`site_email`) — the editable identity fields.
- **Settings cascade** — the rule that Site-level settings feed every customer-facing surface.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Site ID** | n/a (assigned at signup, immutable) | Unique numeric identifier the platform uses internally. Shown as a chip on [[settings-hooks]], [[settings-api-keys]], and several developer-facing screens. The integration anchor — see [[site-entity-tenancy-resolution]]. |
| **Handle / slug** | n/a (chosen at signup, very rarely changeable) | The identifier in the `<handle>.cloudcart.net` fallback subdomain. Renaming requires CloudCart support — see [[site-entity-maintenance-data]]. |
| **Store name** (`site_name`) | Editable on [[settings-general]] | Displayed in transactional emails, invoices, meta titles, the admin UI header. Required. |
| **Primary email** (`site_email`) | Editable on [[settings-general]] via two-step confirmation | The store's outgoing email From address and recipient of admin notifications. Changing it goes through a double-code confirmation flow. |
| **Currency** (`currency`) | Editable on [[settings-general]] | The Site's display currency (ISO code). New orders snapshot this; existing orders keep their original currency. |
| **Storefront language** (`language`) + **admin-panel language** (`language_cp`) | Editable on [[settings-general]] | Storefront language drives the customer experience; admin language drives the merchant's UI. Independent. |
| **Country of operation** (`country`) | Editable on [[settings-general]] | Affects regional defaults (date format, weights, tax behaviour), payment-provider availability, [[plan|Plan]] catalog filter, invoicing entity. |
| **Timezone** (`timezone`) | Editable on [[settings-general]] | All stored timestamps are interpreted in this zone for display. |
| **Unit system** (`unit_system`) | Editable on [[settings-general]] | `metric` or `imperial`. Drives weight / dimension display. |

The Site also carries hundreds of granular per-store settings rows (cart behaviour, checkout fields, statuses, invoice numbering, payment providers, shipping providers, taxes, etc.) — each managed in its own [[settings]] sub-screen.

### Settings cascade from Site-level

The merchant's edits in [[settings-general]] (currency, language, timezone, country, units) are stored at the Site level and read by every customer-facing surface (storefront, checkout, emails, invoices, exports) and every internal job (analytics aggregation, webhook payload formatting, etc.). There is no per-product / per-customer / per-order currency override on a single-Site shop — the Site's currency is the Site's currency. (Per-order currency exists as a SNAPSHOT — see [[order]] — but that captures the Site's currency at order time, not a different currency at edit time.)

### The CloudCart subdomain is fixed at signup

The `<handle>.cloudcart.net` fallback subdomain is assigned when the Site is created and is NOT editable from anywhere in the admin panel. The merchant who wants a different storefront URL attaches a custom Domain via [[settings-domains]] and sets it as primary — the CloudCart subdomain stays as a permanent fallback URL. The full handle-rename rule is on [[site-entity-maintenance-data]].

## Where it appears

- [[settings-general]] — the primary editing surface for name, email, currency, language, country, timezone, units, copyright.
- [[settings-domains]] — custom-domain attachment; the merchant's path to a non-default storefront URL.
- [[settings-api-keys]] / [[settings-hooks]] — Site ID chip shown in the header for copying.
- [[order]] — snapshots the Site's currency / language / unit system at order time.
- [[settings-invoicing]] — reads the Site identity for invoice header / numbering.

## Related

- [[site]] — hub.
- [[settings-general]] — the editing surface for all identity values.
- [[settings-domains]] — custom domain → non-default storefront URL.
- [[domain]] — Domain entity (the `<handle>.cloudcart.net` fallback plus custom domains).
- [[account]] — the owning Account (billing identity, separate from Site identity).
- [[plan]] — the country value filters the Plan catalog.

## Open Questions

No outstanding questions.
