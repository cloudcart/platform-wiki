---
type: feature
nav_path: "Settings → Geo Zones"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo Zones", "Geographic zones", "Shipping zones", "Tax zones", "Geo-зони", "Гео зони", "Региони"]
tags: [settings, geo, shipping, tax, zones]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 11
---
# Geo Zones

## Purpose

A geographic-grouping screen where the merchant defines named "zones" — arbitrary collections of countries, regions, cities, neighborhoods, polygons (custom-drawn areas), distance-from-a-point rules, or postal-code patterns — that can be referenced from shipping methods, tax rules, and discount rules to apply a setting only to customers in those zones. Page header: *"CloudCart allows the grouping of countries into Geo Zones (regions) regardless of their geographic location."*

Each zone is a name plus one or more **rules**. Each rule is a `(operation, location)` pair (e.g., *"all addresses in Bulgaria"*, *"only Sofia city"*, *"all countries except Germany"*, *"polygon: warehouse-1-area"*, *"within 50 km of point (X, Y)"*, *"post codes 1000-1999 in Bulgaria"*). Multiple rules in one zone are **OR-combined**.

A Google Maps API key on [[settings-cart]] unlocks the Google Places autocomplete and 8 of the 11 zone-rule operations — see [[settings-geo-zones-google-maps]].

## Where to find it

Sidebar → Settings → **Geo Zones**.

The page's breadcrumb reads "Settings → Geo Zones" (with active sub-action label appended on add / edit). The route is `/admin/settings/geo-zones` (list root) or `/add` / `/edit/:id`. The header icon is the globe-africa icon.

## Sub-screens

| Label | Route name | Route path |
|-------|------------|------------|
| Geo Zones (root) | `geo_zones.settings.main` | `/admin/settings/geo-zones` |
| List | `geo_zones.settings` | `/admin/settings/geo-zones` |
| Add | `geo_zones_add.settings` | `/admin/settings/geo-zones/add` |
| Edit | `geo_zones_edit.settings` | `/admin/settings/geo-zones/edit/:id` |

## Sub-pages (in this cluster)

Split into seven aspect pages — drill into the aspect that matches the question, don't read every page.

- [[settings-geo-zones-operations]] — the 11 operation types (`OPERATION_ALL_IN_COUNTRY`, `OPERATION_ONLY_REGION`, `OPERATION_POLYGON`, `OPERATION_DISTANCE`, `OPERATION_POST_CODE`, etc.), per-row location inputs, OR-combination rule.
- [[settings-geo-zones-post-codes]] — operation 11 syntax (exact / wildcard / range), GR space-stripping, range-numeric-only rule, `*` → `LIKE %` translation.
- [[settings-geo-zones-google-maps]] — `google_map_api_key` gating: 3-of-11 operations without a key, Places autocomplete, per-country remapping (TR / CZ / GB / US-NY), Geonames region backfill.
- [[settings-geo-zones-polygon-distance]] — operations 9 and 10: `ST_Contains` point-in-polygon and `ST_Distance_Sphere` spherical-distance.
- [[settings-geo-zones-matching]] — runtime: MaxMind GeoIP pre-population, country + region requirement, per-consumer conflict rules, US ASCII city-match.
- [[settings-geo-zones-deletion-cascade]] — `ON DELETE SET NULL` on outbound FKs; `ON DELETE CASCADE` on polygon / distance → silent zone-rule removal; no FK-protection error.
- [[settings-geo-zones-save-semantics]] — `name` max 191; `values` required; form fully replaces rules; IDs change between saves; cache invalidates; no queue / webhook / notification.

## What the merchant can do here

- **List view**: see all zones in one table (zone name + per-row Edit / Delete), sort / filter / paginate (default sort: id descending), bulk-select rows and bulk-delete via the standard table action, click **+ New Geo zone** in the page header to navigate to the Add form.
- **Add / Edit form**: enter a **Geo zone name** (free text — e.g., "EU", "Sofia city", "Plovdiv delivery zone"), add rules with **+** (each OR-combined), remove with **×**, **Save**. Merchant is redirected back to the list after save.

What the merchant CANNOT do here:

- Define AND-combined rules within a single zone — use a multi-field operation (operation 5 already constrains country + region + city) or combine via the consumer side.
- Import zones via CSV / bulk upload.
- Visually verify on a map — no overview map; only the per-rule Places autocomplete when Maps is configured.
- Translate zone names per language — see [[settings-geo-zones-save-semantics]].

## Settings & fields (summary)

For the field-by-field catalogue, drill into the aspect pages. Top-level summary:

| Block | Field | Notes |
|-------|-------|-------|
| **Header** | **Geo zone name** (`name`) text input | Required. Max 191 chars. Placeholder: *"Add Geo zone name, e.g. Paris or France"*. See [[settings-geo-zones-save-semantics]]. |
| **Rules** | Dynamic group of `(operation, location)` rows | First row mandatory; **+** to add, **×** to remove additional rows. See [[settings-geo-zones-operations]] for the 11 operations. |

## Business rules (summary)

Each cross-cutting rule is documented on its own aspect page. Slim summary:

- **Rules within a zone are OR-combined** — no AND at the zone level. See [[settings-geo-zones-operations]].
- **Without a Maps key, only 3 of 11 operations are available** (`1`, `4`, `11`); ops 2/3/5/6/7/8/9/10 are gated. See [[settings-geo-zones-google-maps]].
- **Customer must have BOTH country AND region resolved for most rules to evaluate** — `scopeZone` falls through to "only unrestricted methods" otherwise. See [[settings-geo-zones-matching]].
- **Conflicting-zone resolution differs per consumer**: shipping offers ALL matches; tax picks the SINGLE most-recently-created VAT rule; discounts STACK. See [[settings-geo-zones-matching]].
- **Delete CASCADES silently** — `ON DELETE SET NULL` on zone → consuming shipping / tax / discount (silently widens); `ON DELETE CASCADE` on polygon / distance → silent zone-rule removal. No FK-protection error. See [[settings-geo-zones-deletion-cascade]].
- **Save fully replaces rules** — delete-then-create-all; rule IDs change between saves; concurrent saves last-write-wins. See [[settings-geo-zones-save-semantics]].
- **City / neighborhood ops auto-backfill region via Geonames** — silent failure mode if Geonames returns nothing. See [[settings-geo-zones-save-semantics]].
- **Saving flushes the geo-zone lookup cache** — next cart / checkout sees the new zones. No queue, no webhook, no notification.

### Permissions

Sits under the standard settings permission scope. The bulk-delete endpoint URL is `/admin/api/core/settings/geo-zones` (DELETE) — protected by the same middleware as the rest of Settings (`hasApiPermission:settings,...`).

### Consumed across shipping, tax, and discounts

Geo zones are referenced from shipping methods ([[shipping]]), tax rules ([[settings-taxes]]), discount targets ([[discount-stacking]]), the cart ([[settings-cart]]) for line-item zone display, and the order ([[order]]) for VAT-zone matching at checkout. Deleting or renaming a zone has downstream effects across these — see [[settings-geo-zones-deletion-cascade]].

## Related

- [[settings]] — parent hub.
- [[settings-cart]] — Google Maps API key (Box: Google Maps) + `invoicing_address` that decides billing vs shipping for matching.
- [[settings-general]] — store default country used as the GeoIP fallback.
- [[geo-polygons-settings-main-new]] — operation 9 polygons defined there.
- [[settings-geo-distances]] — operation 10 distance entries defined there.
- [[settings-taxes]] — tax rules use geo zones to scope rates by region.
- [[settings-taxes-vat-rules]] — VAT single-winner precedence detail.
- [[shipping]] — shipping methods reference geo zones to scope availability.
- [[discount-stacking]] — discounts can scope to zones.
- [[settings-translations]] — does NOT cover geo-zone name translation.
- [[settings-hooks]] — no `geo_zone.*` webhook events fire from this page.
- [[geo-zone]] — entity page.
- [[geo-polygon]] — entity page.
- [[geo-distance]] — entity page.
- [[geo-targeting]] — concept page on how shipping / tax / discounts use zones at runtime.
- [[shipping-calculation]] — concept page; references zones during shipping cost computation.
- [[tax-computation]] — concept page; references zones during tax computation.
- [[checkout-flow]] — concept page; where matching happens in the order pipeline.

## Open questions

None.
