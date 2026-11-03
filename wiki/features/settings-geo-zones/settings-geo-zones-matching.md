---
type: feature
nav_path: "Settings → Geo Zones → Runtime matching"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo zone matching", "Geo zone runtime", "Geo zone resolution", "MaxMind GeoIP", "Conflicting zones", "Zone winner rule"]
tags: [settings, geo, zones, matching, runtime, shipping, tax, discount]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-zones]]. See the hub for the other aspects (operations, post-codes, Maps, polygon/distance, deletion-cascade, save-semantics).

# Geo Zones — Runtime matching (how zones resolve at checkout)

## Purpose

Once the merchant defines zones, the platform must decide at cart-display / checkout time **which zones match the current customer**. The matcher considers the customer's resolved country / region / city / lat / lng / post code against every zone's rules. The result is then handed to consuming features — shipping methods, tax rules, discount targets — each of which has its **own conflict-resolution rule** when multiple zones match the same customer.

This aspect documents the matching mechanics: pre-population from MaxMind GeoIP, the country+region requirement, the per-feature conflict resolution, the US city special-case, and the "approximate shipping cost" shown in cart for guests.

## Where to find it

This is not a screen — it is the runtime behaviour that fires whenever the cart / checkout page renders, whenever shipping cost is computed, and whenever tax / fee lines are produced on an order.

## What the merchant can do here

- Define overlapping or non-overlapping zones on **Settings → Geo Zones** and rely on the per-consumer conflict rules described below.
- Configure which address (billing vs shipping) drives matching via `invoicing_address` on [[settings-cart]]. The selected address is the one used for matching geo zones.

## Settings & fields

The runtime matcher reads the customer's resolved location, populated from these sources (in order):

| Source | Fields populated | When |
|--------|-----------------|------|
| Customer's typed address (cart / checkout) | country, region, city, lat, lng, post code | As the customer fills the address form. |
| MaxMind GeoIP IP lookup | country ← IP-resolved country; region ← first subdivision; lat, lng ← geo-IP location | At session start, before any address typed. |
| Store default country setting on [[settings-general]] | country fallback | Only if MaxMind has no data for the IP. |

## Business rules

### Customer must have BOTH country AND region resolved for most rules to evaluate

The matcher only runs full geo-zone logic for shipping / tax / discount when **both country AND region (state)** are resolved on the customer's address. If either is empty, **only rules without any geo-zone restriction are returned**.

So a customer at the "country only" stage of the address form (no region yet) sees only the unrestricted methods, even if a country-only-rule zone would technically match. **The customer experience: as they fill more of the address form, more shipping / tax options can become available.**

This also explains why the city / neighborhood operations (5, 6, 7, 8) require region to be auto-backfilled via Geonames at save time — see [[settings-geo-zones-google-maps]] and [[settings-geo-zones-save-semantics]].

### Customer geo info defaults from MaxMind GeoIP

At session start (before the customer enters any address), the location is **pre-populated from MaxMind GeoIP** lookups on the customer's IP (country, region, lat/lng — see the table above). So country / region-based shipping or tax rules can be evaluated **before the customer types anything** if MaxMind has data for their IP. This drives the **"approximate shipping cost"** displayed in cart for guests. If MaxMind has no data for the IP, the platform falls back to the store's default country on [[settings-general]].

### `invoicing_address` decides whether billing or shipping drives matching

The `invoicing_address` setting on [[settings-cart]] picks the billing vs the shipping address as the one that feeds the matcher. Changing it can change which taxes / shipping / discounts apply — important for stores serving multiple jurisdictions.

### 2-stage filtering — broad pre-filter, then per-rule evaluation

The matcher works in two stages:

1. **Broad pre-filter** — limits candidates to zones whose country / region already loosely match the customer.
2. **Per-rule evaluation** — iterates the candidates and runs the rule-specific match (post-code pattern, polygon containment, distance, city compare) — see [[settings-geo-zones-polygon-distance]] for the spatial rules.

This keeps checkout latency low even with hundreds of zones — full match-rule iteration only runs against the trimmed candidate list.

### City matching for US addresses uses the city name (not the internal city ID)

For operations 5/6 (city in / not in), the matcher special-cases the United States: instead of comparing CloudCart's internal city ID, it compares the unaccented city name. So a US zone rule for "Springfield, IL" matches any customer whose city normalises to "Springfield" in IL. For all other countries, the internal city ID is the strict match. Reason: US locale data has multiple entries for the same city, so a name match is more reliable.

### Conflicting-zone resolution differs per consumer feature

When a customer's address matches multiple zones, the resolution depends on which feature is consuming the match:

- **Shipping methods**: ALL matched shipping options are offered to the customer at checkout. The customer picks one. If two zones each gate a different shipping method, both methods appear.
- **Tax rules** ([[settings-taxes]] "Resolved details"): the platform picks **exactly ONE** VAT-type tax — the **most recently created rule wins** when two zones both match. Non-VAT fees stack additively across all matching zones.
- **Discount targets**: a customer who matches multiple geo-scoped discounts can have all of them applied if each discount independently qualifies (subject to the discount-stacking rules — see [[discount-stacking]]).

So merchants should be careful when defining overlapping zones — for VAT/tax purposes there's a clear winner rule, for shipping/discounts the behaviour is additive.

### Performance scales linearly with zone count

The matcher iterates each defined zone's rules at checkout / cart-display time. Each rule type (country, region, city, neighborhood, polygon, distance, post-code) runs a fast indexed lookup, so even a merchant with hundreds of zones sees iteration cost on the order of milliseconds.

### Cache invalidation on save

Saving zones invalidates the geo-zone lookup cache, so the next shipping / tax computation sees the updated zones immediately — newly added zones take effect right away. No queue delay, no admin notification. See [[settings-geo-zones-save-semantics]].

## Related

- [[settings-geo-zones]] — hub.
- [[settings-geo-zones-operations]] — the operation catalogue the matcher evaluates per rule.
- [[settings-geo-zones-post-codes]] — post-code pattern matching.
- [[settings-geo-zones-polygon-distance]] — polygon-containment and distance matching invoked from the matcher.
- [[settings-geo-zones-google-maps]] — region auto-backfill via Geonames ensures matching can succeed for city-scoped rules.
- [[settings-geo-zones-save-semantics]] — what the silent-fail rule looks like when region is missing.
- [[settings-cart]] — `invoicing_address` (billing vs shipping for matching).
- [[settings-general]] — store default country fallback.
- [[settings-taxes]] — single-winner VAT precedence ("most recently created wins" between two regional matches).
- [[settings-taxes-vat-rules]] — VAT-specific precedence detail.
- [[shipping]] — shipping methods reference zones; ALL matched methods are offered.
- [[discount-stacking]] — discount rules can scope to zones and stack with other matches.
- [[checkout-flow]] — where matching happens in the order pipeline.
- [[geo-targeting]] — concept page on how shipping / tax / discounts use zones at runtime.

## Open questions

None.
