---
type: feature
nav_path: "Settings → Taxes and fees → VAT rules"
route_name: taxes.create
route_path: /admin/settings/taxes/tax/:id?
aliases: ["VAT rules", "Tax type rules", "VAT precedence", "Regional VAT", "Rest-of-world VAT", "Country-level matching", "Auto-Global companion tax", "Country-limit side effect"]
tags: [settings, taxes, vat, geo-zones]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-taxes]]. See the hub for the other aspects (fees, overrides, pricing display, OSS / no-VAT, validation, integrations).

# Taxes and fees — VAT rules (`vat=yes`)

## Purpose

Documents how a **VAT-type tax** (`vat=yes`) is configured, scoped to geo zones, and picked at checkout. VAT rules are the rate the storefront applies to products (and optionally shipping) based on where the customer is. Unlike fees, **exactly ONE VAT rule wins per order** — they do NOT stack. Several non-obvious behaviours make VAT setup error-prone in CloudCart; this page is the canonical reference.

## Where to find it

Settings → Taxes and fees → **+ Add new → Add Tax**, OR click any existing row whose type badge says **Tax**. Form route: `/admin/settings/taxes/tax/:id?`.

## What the merchant can do here

In the Tax form:

- Set **Name** + **Rate** (`tax`). Rate type toggles between **percent** and **flat** — for VAT, percent is the usual choice.
- Choose **target scope** via the *"Make the tax Global"* switch:
  - **ON** → `target=restofworld` (applies to every customer not matched by a more specific regional tax).
  - **OFF** → `target=regions` → pick one zone from the **Geo zone** dropdown (server-paginated against `/admin/geo-zones`).
- Toggle the **"One Stop Shop"** switch (`oss_registration`) — only visible when `type=tax` AND the regions sub-form is open. See [[settings-taxes-oss-no-vat]].
- Configure **Per-region overrides** and **Per-category overrides** — see [[settings-taxes-overrides]].
- Set **`price_with_vat`** (inclusive vs exclusive display) and **`shipping`** (does this VAT apply to shipping too) — see [[settings-taxes-pricing-display]].
- Set **`without_vat_reasons`** + **`without_vat_reasons_non_eu`** — see [[settings-taxes-oss-no-vat]].

## Settings & fields

Tax-specific fields (the rest are shared with fees — see the [[settings-taxes]] hub):

| Field | Value | Notes |
|-------|-------|-------|
| `vat` | `yes` | Auto-set from the "Add Tax" type card; **NOT user-toggleable** after create. |
| `target` | `regions` \| `restofworld` | The switch label is *"Make the tax Global"*. |
| `geo_zone_id` | FK to `geo_zones` | Required when `target=regions`. Cleared client-side when the merchant flips the switch ON. |
| `oss_registration` | nullable / boolean | Presence-based: stored `true` when the field is included, `false` when omitted. |

## Business rules

### VAT precedence — single winner, regional beats global, newest wins

When the platform computes tax for a customer's order, it picks **exactly ONE** VAT rule:

1. **Regional taxes always beat rest-of-world.** A tax scoped to a specific geo zone wins over a generic *"rest of world"* tax whenever the customer's country falls inside that zone. The rest-of-world tax is the fallback when nothing more specific matches.
2. **Between two regional taxes that both match the customer's country, the most recently created tax wins.** There is **NO** *"most-specific zone"* logic. If two zones both include Bulgaria and both have an active VAT tax, the merchant gets the newer one applied.

So merchants should be careful when defining overlapping zones. If a cleanup is needed, the practical pattern is to **delete and re-create** the desired tax so its creation order becomes the most recent.

> In normal flow the save-time `unique_geozone` validator (see [[settings-taxes-validation]]) prevents creating two VATs on the same zone — so the *"newest wins"* rule only fires for stores whose data was edited directly in the database or imported with pre-existing overlap.

### Country-level matching only — granular zone operations are ignored

A subtle but important rule: **for tax matching, the platform only looks at the country selector inside each zone**. The richer geo-zone operations (city, region, neighborhood, polygon, distance-from-point, post code) are **NOT** considered when finding the applicable tax.

So a zone like *"only Sofia city in Bulgaria"* (operation type 5 / Includes only city X) will **NOT** match a tax for a Bulgarian customer **unless** that zone ALSO contains a country-level rule (*"Includes country Bulgaria"*). Zones built purely from city / region / polygon / distance / post-code rules with **NO** country rule will silently match nothing at the tax level.

This means: the richer geo-zone operations (cities, polygons, distances, post-codes) are used by [[shipping]] and [[discount-stacking]] but **NOT** by tax computation.

### Server-side enforcement: ONE global VAT and ONE per zone

The save endpoint runs a `unique_geozone` validator BEFORE allowing a new VAT through:

- If `target=restofworld` (no `geo_zone_id`), the merchant can only have ONE rest-of-world VAT tax. A second one fails with *"You already have a global store VAT tax - `[name of the conflicting tax]`"*.
- If `target=regions`, the merchant can only have ONE VAT tax per geo zone. A second VAT pointing at the same `geo_zone_id` fails with *"You already have a VAT tax - `[name of the conflicting tax]`"*.
- Fees (`vat=no`) are **unconstrained** — see [[settings-taxes-fees]].

### Automatic "Global" companion tax on first regional VAT

When the merchant creates a regional VAT tax (`target=regions` + `vat=yes`) AND there is **NO** existing global rest-of-world VAT, the platform automatically creates a SECOND tax record copying the same rate, named **`[original name] - Global`**, with `target=restofworld` and `geo_zone_id=null`. Per-category and per-region overrides are copied too (with descriptions suffixed *"- Global"*). This guarantees customers outside the regional zone always have a fallback VAT instead of getting zero VAT silently.

Merchants who only sell domestically won't notice this; cross-border merchants will see two taxes after their first save and can edit / delete the auto-created Global one if they want different behaviour.

### Hidden country-limit side effect — VAT-only setups restrict billing-address countries

When **ANY** VAT tax has `target=regions` AND there is **NO** `target=restofworld` VAT tax, the platform's `getBillingAddressCountriesLimit` returns ONLY the countries listed inside those regional zones — and the storefront's billing-address country picker is restricted to that set. Adding a rest-of-world VAT (or removing the regional ones) opens the picker to all countries again.

So merchants who define a Bulgaria-only VAT with no global fallback **inadvertently lock the storefront's billing-address country dropdown to Bulgaria**. This is intentional — it prevents the storefront from accepting orders that would have no applicable VAT.

### Caching + side effects

Saving a VAT tax flushes the platform Settings cache so the next checkout / order-creation uses the new rule immediately. No queue, no notifications, no webhooks fired from this page. The VAT rule is also consumed by several integrations — see [[settings-taxes-integrations]] for the full list.

## Related

- [[settings-taxes]] — hub.
- [[settings-geo-zones]] — defines the zones VAT rules can target; required prerequisite.
- [[settings-cart]] — `invoicing_address` decides which address is used for the geo-zone match.
- [[settings-general]] — `operation_country` is the default VAT jurisdiction when OSS is not enabled.
- [[shipping]] — uses the richer (non-country) zone operations the VAT engine ignores.
- [[discount-stacking]] — also uses the richer zone operations.
- [[tax]] — entity page.
- [[tax-computation]] — concept page on the full checkout-time math.

## Open questions

None.
