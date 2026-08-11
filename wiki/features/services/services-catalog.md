---
type: feature
nav_path: "Sidebar → Services → Catalog list"
route_name: admin.services.list
route_path: /admin/services
aliases: ["Services catalog", "Services list", "Browse services", "Каталог на услуги"]
tags: [services, catalog, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[services]]. See the hub for related aspects (purchase flow, routes, billing periods, catalog controls, known gaps).

# Services — catalog list view

## Purpose

This page covers the **catalog list view** at `/admin/services` — what the merchant sees when they click **Services** in the sidebar. It is a read-only catalog of paid services curated by CloudCart's commercial team: the merchant browses categories, ticks one or many service rows, watches the running total update live, then clicks **Order** to start the purchase flow.

The catalog is distinct from **store plans** (see [[plans]]) and **paid apps** (see [[apps]]). What ends up here is professional / expert-services work (Design, Migration, Hosting, Platform → System service groups) and other agency-style add-ons sold by CloudCart and its partner network.

## Where to find it

- Sidebar → **Services** entry (visible to store owners; staff / moderator roles do not see this menu link).
- Route: `admin.services.list` at `/admin/services`.
- Some in-app flows skip this catalog and jump straight to the purchase confirmation step — see [[services-routes]] for the upstream-flow path.

## What the merchant can do here

- Browse the catalog grouped by category (Design, Migration, Hosting, Platform → System, etc.).
- Tick **one or many services** at the same time and see the running total update live below the list.
- Click **Order** to start the purchase flow (the form POSTs ticked `service[]` checkboxes to `admin.promo.services` — see [[services-routes]]).
- Use the inline "Add invoice details" / "Add payment method" prompts (rendered by the purchase confirmation step) to fill in missing [[billing-invoicing]] / [[billing-cards]] before completing the purchase.

## Settings & fields

The catalog screen has no merchant-editable settings — it is a catalog browser. Each catalog row exposes:

| Element | What it does | Notes |
|---------|--------------|-------|
| **Service group title** | The category heading the service appears under. | Examples in the catalog: `Design`, `Migration`, `Hosting`, `Platform → System`. Groups can be nested (parent → child). Services without a group appear ungrouped at the bottom. |
| **Service name** | Translated to the merchant's locale (`bg` / `en` / etc.). | Multi-language — the merchant sees the name in whichever language their admin panel is set to. Falls back to the source language if no translation is available. |
| **Price** | Shown in the merchant's currency, per the merchant's currency configuration. | Formatted with the merchant's currency sign + position. Followed by `/ <billing_period>` — see [[services-billing-cycles]]. |
| **Checkbox** (`service[]`) | Tick to add the service to the basket. | Multiple services can be selected on the same submit. |
| **Total** | Running sum of the checked services, updated live as the merchant ticks / unticks. | Footer line: *"Total"* (`global.total_sum`) + the sum in the merchant's currency. Element id: `price-to-be-paid-form`. |

The catalog footer also shows the *"All prices are without VAT"* footnote (`payment.no_vat`) — VAT is added at invoice time, see [[services-billing-cycles]] for the VAT-display rules.

## Business rules

### Visibility filters

A service appears on the catalog screen iff:

- `public = 1` (visible flag), AND
- `archived = 0` (not retired).

Internal-only services (not yet launched, partner-only, A / B tests, etc.) carry `public = 0` and are NOT shown on this screen. See [[services-catalog-controls]] for the full set of catalog flags.

### Catalog is curated by CloudCart, not the merchant

The merchant **cannot add their own services to the catalog**. What appears is what CloudCart has marked `public = 1` and not `archived`. The list is ordered by the `sort_order` value set by CloudCart's commercial team. See [[services-catalog-controls]].

### Country filtering NOT applied to the catalog query

The service data model supports country-limitation records, but the catalog query in this screen does NOT enforce them — every public service is shown to every merchant regardless of billing country. This is a known gap; see [[services-known-gaps]].

### Form submit goes to the admin-promo checkout, NOT to the services purchase pair

The catalog `<form id="serviceForm">` POSTs the ticked `service[]` checkboxes to **`admin.promo.services`** (the shared admin-promo checkout). The `/admin/services/purchase` + `/admin/services/buy` route pair documented under [[services-purchase-flow]] is used by **upstream flows** (e.g. paid mailboxes), not by the catalog's Order button. See [[services-routes]] for the full entry-point matrix.

## How it works (verified against backend)

### Catalog query

Services flagged `public = 1, archived = 0`, ordered by `sort_order`, grouped by service group (`group_id`). Services without a group appear ungrouped. Storage lives on the shared CloudCart-wide `cc_gate.services` table — NOT on the merchant's own DB. See [[services-catalog-controls]] for the full per-row field list.

### Modals & sub-flows on this view

The list template renders the catalog as nested `ServiceGroup` accordion-style sections:

- **Service group title** — the group / category name (e.g. *Design*, *Migration*, *Hosting*, *Platform → System*). Nested parents stack.
- **Service row** — checkbox (`name="service[]"` with the service ID as the value) + service name (translated) + price + period label.
- **Total** — running sum at the bottom of the form, updated live by client-side JS as the merchant ticks / unticks.

Footer: a **Total** running-sum line + a *"All prices are without VAT"* footnote + an **Order** button (`global.order_btn`, `btn-primary`). The Order button submits `serviceForm` to `admin.promo.services`.

## Related

- [[services]] — hub.
- [[services-routes]] — entry-point matrix (catalog Order vs single-service link vs upstream flow).
- [[services-purchase-flow]] — what happens after Order.
- [[services-billing-cycles]] — `once` / `month` / `year` / `2years` semantics + VAT display.
- [[services-catalog-controls]] — per-row `public` / `archived` / `sort_order` / `ecosystem` / `tag`.
- [[services-known-gaps]] — country filter not applied, silent activation failure, no self-service refund.
- [[plans]] — separate billing surface for the SaaS tier.
- [[apps]] — separate billing surface for functional add-ons.

## Open questions

None.
