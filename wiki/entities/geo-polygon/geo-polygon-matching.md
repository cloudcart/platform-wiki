---
type: entity
aliases: ["Geo Polygon matching", "Point-in-polygon matching", "Polygon address matching", "Polygon zone match", "Polygon tax gotcha", "Гео полигон — съвпадение"]
tags: [shipping, settings, geo, polygons, maps, matching, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-polygon]]. See the hub for the other aspects (model, lifecycle, delete cascade).

# Geo Polygon — address matching

## Identity

A **Geo Polygon match** is the runtime test that decides whether a given customer address falls inside a drawn outline. At checkout (and at cart-display time for the pre-login storefront default), the platform geocodes the customer's shipping address and runs a standard **point-in-polygon** test against each polygon referenced by each relevant [[geo-zone|Geo Zone]]. The match contributes to that zone's overall OR-combination of rules — the polygon itself never gates anything directly. The polygon merely tells the zone *"addresses inside THIS shape count as inside the zone."*

This page covers **how a polygon is matched and the surprising tax interaction**. What the record stores is on [[geo-polygon-model]]; the create / edit flow is on [[geo-polygon-lifecycle]].

## Aliases

- "Geo Polygon matching" / "Point-in-polygon matching" — the wiki terms for the runtime test.
- "Polygon tax gotcha" — the most common support topic: a polygon-only zone matches no tax.
- Bulgarian: "Гео полигон — съвпадение".

## Key Attributes

| Aspect | Behaviour | Notes |
|--------|-----------|-------|
| **Test type** | Point-in-polygon | The customer's geocoded coordinate is tested against the polygon's `{lat, lng}` outline. |
| **Combination within a zone** | OR | A zone with multiple operation-9 rules matches if the address is inside ANY referenced polygon. |
| **Tax matching** | IGNORES polygons | The tax engine uses ONLY country-level rules — a polygon-only zone matches no tax. See below. |
| **Cost driver** | Polygon count × vertex count | Each checkout iterates referenced polygons, one point-in-polygon test per polygon. |

### Matching is point-in-polygon against the customer's coordinates

At checkout (and at cart-display time for the pre-login storefront default), the platform geocodes the customer's shipping address (via Google Places or stored from an earlier geocoding) and runs a standard point-in-polygon test against each polygon referenced by each relevant Geo Zone. The match contributes to the zone's overall OR-combination. Computation is geometry-index backed and stays in single-digit milliseconds for typical polygon counts.

### Polygons are INPUTS to zones, never consumed directly

No shipping method, tax rule, payment provider, discount, fee, customer group, or Cart Rule has a `polygon_id` field. All of them reference [[geo-zone|Geo Zones]]; the polygon shows up only as an entry in a zone's rule list (operation 9). This separation lets the merchant draw the shape ONCE (see [[geo-polygon-model]]) and reuse it from many zones, and it keeps the consuming features oblivious to the underlying geometry.

### Tax matching IGNORES polygon rules — country-only rule applies

A critical interaction with [[tax-computation]]: the tax engine looks at ONLY country-level rules in a Geo Zone. A zone whose only rule is a polygon — even an excellent, surgically-drawn one — matches NO tax. To use the same zone for both tax AND shipping (the common case), the merchant adds a separate country rule (operation 1) to the zone so the tax engine can match it on the country side while shipping uses the polygon for finer targeting. This is the single most common merchant misconfiguration with polygons. See [[geo-zone]] business rules and [[tax-computation]].

### Performance scales with polygon count and vertex count

Each customer checkout iterates referenced polygons and runs a point-in-polygon test per polygon. Polygons with hundreds of vertices cost more than simple shapes; many polygons cost more than few. For typical merchants the cost stays in single-digit milliseconds, but very detailed shapes drawn over many zones can add latency. There is no in-page warning about polygon complexity.

### Customers are matched, not subscribed

A Geo Polygon is **NOT consumed by [[customer|Customers]] directly** — the polygon is matched against the customer's address coordinates at checkout (via the point-in-polygon test) only when the address-resolution layer is asking on behalf of a zone. The customer record has no link to a polygon.

## Where it appears

- [[settings-geo-zones]] — where the polygon becomes an operation-9 rule that the matching engine evaluates.
- [[settings-shipping]] — shipping methods read the zone match (including the polygon side).
- [[settings-taxes]] — tax rules read the zone match but IGNORE the polygon side (country-only).
- [[marketing-discounts]] — discounts can restrict to zones whose match includes the polygon side.

## Related

- [[geo-polygon]] — hub.
- [[geo-polygon-model]] — the stored `area` JSON that the test reads.
- [[geo-zone]] — the container that OR-combines the polygon match with its other rules.
- [[geo-targeting]] — concept page on how Zones / Polygons / Distances combine end-to-end.
- [[tax-computation]] — explains the country-only rule that makes polygons invisible to the tax engine.
- [[shipping-calculation]] — how zones (and polygons through them) gate shipping quotes.
- [[customer]] — matched at checkout, never linked to a polygon directly.

## Open Questions

- ⏸️ **Self-intersecting polygons** — what happens when a polygon is drawn as a figure-8 or otherwise self-intersects? Standard point-in-polygon implementations vary on this case (even-odd vs winding-number rules). (verify)
