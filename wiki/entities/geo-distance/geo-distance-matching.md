---
type: entity
aliases: ["Geo Distance matching", "Distance great-circle match", "Haversine distance match", "Distance inputs to zones", "Tax ignores distance", "Гео разстояние — съвпадение"]
tags: [shipping, settings, geo, distance, radius, matching, tax, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-distance]]. See the hub for the other aspects (model, units, lifecycle).

# Geo Distance — checkout matching

## Identity

**Matching** is how a saved Geo Distance turns into a yes/no answer at checkout: given the customer's shipping address, is it inside the circle? The platform geocodes the address, computes the **great-circle distance** from the record's center to the customer's coordinates, and compares it against the radius. A distance never gates anything on its own — it only contributes to a [[geo-zone|Geo Zone]] match, which is what shipping methods, payments, discounts, fees, and Cart Rules actually consume.

This page covers **the runtime match, its performance and accuracy, the inputs-to-zones rule, and the tax-engine exception**. The stored fields are on [[geo-distance-model]]; the unit semantics of the radius are on [[geo-distance-units]].

## Aliases

- "Geo Distance matching" / "Distance great-circle match" — the wiki terms.
- "Haversine distance match" — the spherical-law-of-cosines computation.
- "Distance inputs to zones" — the rule that distances are never consumed directly.
- "Tax ignores distance" — the country-only tax-matching exception.
- Bulgarian: "Гео разстояние — съвпадение".

## Key Attributes

| Aspect | Behaviour | Notes |
|--------|-----------|-------|
| **Match function** | Great-circle (spherical law of cosines) center → customer coordinates | One haversine call per record. Constant-time, single-digit milliseconds per record. |
| **Comparison unit** | Always **metres** internally | Imperial stores compare against `distance_in_meters` (see [[geo-distance-units]]). |
| **Customer coordinates** | Geocoded shipping address (Google Places or stored from earlier geocoding) | Used at checkout and at cart-display time for the pre-login storefront default. |
| **Result combination** | OR-combined with the zone's other rules | A customer inside any referenced radius contributes to the zone match. |

### Distances are INPUTS to zones, never consumed directly

No shipping method, tax rule, payment provider, discount, fee, customer group, or Cart Rule has a `distance_id` field. All of them reference [[geo-zone|Geo Zones]]; the distance entry shows up only as a rule entry in a zone's rule list (operation 10). This separation lets the merchant define the center + radius ONCE and reuse it from many zones, and it keeps the consuming features oblivious to the underlying geometry.

### Matching is great-circle distance against the customer's coordinates

At checkout (and at cart-display time for the pre-login storefront default), the platform geocodes the customer's shipping address and computes the great-circle distance from the record's center `(lat, lng)` to the customer's coordinates. If the result is ≤ the record's radius in metres, the customer matches this distance rule and (combined with the zone's OR logic) contributes to the zone match. Computation is single-haversine-per-record — constant-time.

### Tax matching IGNORES distance rules — country-only rule applies

A critical interaction with [[tax-computation]]: the tax engine looks at ONLY country-level rules in a Geo Zone. A zone whose only rule is a distance — even an excellent one — matches **NO tax**. To use the same zone for both tax AND shipping (the common case), the merchant adds a separate country rule (operation 1) to the zone so the tax engine can match it on the country side while shipping uses the distance for finer targeting. See [[geo-zone]] business rules and [[tax-computation]].

### Performance scales linearly — cheap per record

Each customer checkout iterates the merchant's distance records referenced from geo zones and runs one haversine per record. The math is constant-time per record (no geometry-intersection cost as with [[geo-polygon|polygons]]), so 100+ distance records add only a few milliseconds to checkout latency. For coverage areas well-approximated by a circle, distance records are the cheaper choice than polygons.

### Accuracy of the great-circle math

The source unit is always metres (after the `unit_system` conversion). The result, when surfaced to the merchant, is converted to the store's unit system (kilometres for `metric`, miles for `imperial`, nautical miles for `N`) before display. Accuracy is on the order of metres at city scale — completely acceptable for delivery-radius decisions. Edge cases (above ~75° latitude, or a radius crossing the date line / poles) lose precision but are not real-world concerns for any normal e-commerce delivery zone.

## Where it appears

- [[settings-geo-zones]] — where a distance becomes a zone rule (operation 10) that the match feeds into.
- [[settings-shipping]] — shipping methods consume the zone match.
- [[settings-taxes]] — tax rules consume zones, but the match here is country-only (distances ignored).
- [[marketing-discounts]] — discounts can restrict to zones that reference distances.

## Related

- [[geo-distance]] — hub.
- [[geo-distance-units]] — why the match always runs in metres (`distance_in_meters`).
- [[geo-zone]] — the container whose OR-combined rules the distance match feeds.
- [[geo-polygon]] — sibling input with a costlier point-in-polygon match.
- [[geo-targeting]] — end-to-end concept of how zones / polygons / distances combine.
- [[shipping-calculation]] — how zones gate shipping quotes.
- [[tax-computation]] — the country-only tax-matching rule that makes distances invisible to tax.

## Open Questions

- ⏸️ **Geocoding fallback when Google Maps is unset** — distances require coordinates for the customer's address. Without a Google Maps API key, the platform falls back to a bundled coordinate dataset (see [[geo-zone]] / [[geo-targeting]]), but the exact coverage / accuracy of that dataset is not published. (verify)
