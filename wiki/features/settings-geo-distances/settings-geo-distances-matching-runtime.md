---
type: feature
nav_path: "Settings → Geo distances → Runtime matching"
route_name: geo_distances.settings
route_path: /admin/settings/geo-distances
aliases: ["Geo distances runtime", "ST_Distance_Sphere", "Geo distance checkout match", "Geo distance cache", "Geo distance haversine", "Spherical law of cosines"]
tags: [settings, geo, distance, runtime, checkout, mysql, spatial]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-distances]]. See the hub for the other aspects (list/form, units, map module, storage, defaults, deletion).

# Geo distances — runtime matching at checkout

## Purpose

A saved distance entry only matters at checkout time, when the platform compares the customer's shipping-address coordinates against every distance the customer's matched zones reference. This aspect documents how the match actually runs (a native spherical-distance computation in the database, not in application code), the integration via geo-zone operation 10, the cache invalidation behaviour on save, and the scaling characteristics.

## Where to find it

Runtime matching is automatic and invisible — there is no merchant-facing UI for it. The merchant edits distance entries on [[settings-geo-distances-list-add|the form]], references them from a [[settings-geo-zones|geo zone]] rule of operation 10 (`OPERATION_DISTANCE`), and the platform handles the rest at every checkout.

## What the merchant can do here

Nothing directly — runtime matching has no merchant-facing controls. Indirectly the merchant influences matching by:

- Creating / editing / deleting entries on [[settings-geo-distances-list-add]] (changes the centre or radius).
- Referencing distance entries from one or more [[settings-geo-zones|geo zones]] (operation 10).
- Configuring shipping methods, taxes, or discounts to scope to those zones.

## Settings & fields

There are no settings on this aspect. The matching behaviour is hard-coded against the spatial schema documented in [[settings-geo-distances-storage-spatial]].

## Business rules

### The match is computed by a native spherical-distance function in the database

The actual "is the customer within this radius?" decision is **not** computed in application code. The platform:

1. Geocodes the customer's shipping address to `(lat, lng)` (via the same Google Maps service or stored from an earlier geocoding step).
2. Builds a point from the customer's `(lat, lng)`.
3. Computes the spherical-earth distance between the stored centre point and the customer point directly in the database, against the spatial-indexed centre-point column.
4. Compares the result against the entry's `distance_in_meters` column.
5. If `result ≤ distance_in_meters`, the rule matches; otherwise it does not.

The spherical-earth distance function returns metres between two points on a sphere of mean earth radius. Two practical consequences for merchants:

- Performance is excellent because the centre-point column is spatial-indexed, letting the database filter candidates by geometry. Hundreds of distance entries scan in single-digit milliseconds.
- The earth model is a sphere (not WGS84 ellipsoid). Accuracy is within ~0.5% for typical e-commerce distances — not a real-world concern.

### Accuracy model — spherical, ~0.5% off Vincenty

The spherical model differs from Vincenty's ellipsoidal formula by under 0.5% for distances up to several thousand kilometres — well within the radii merchants typically configure. Practical accuracy at city scale is on the order of metres, completely acceptable for delivery-radius decisions.

Edge case (not a real-world concern): at very high latitudes (above ~75°) and when the radius crosses the date line / poles, the spherical model loses precision. For any normal e-commerce delivery zone this is irrelevant — see [[settings-geo-distances-storage-spatial]].

### Match uses `distance_in_meters`, not raw `distance`

The runtime match always uses `distance_in_meters` — the meters-normalised column. The raw `distance` column (the integer the merchant typed) is irrelevant at match time. So whether the merchant typed metres on a metric store or feet on an imperial store (see [[settings-geo-distances-distance-units]]), the resulting match is consistent — both stores end up comparing metres to metres.

### Integration with geo zones — operation 10 (`OPERATION_DISTANCE`)

Distance entries are **not directly referenced** by shipping, tax, or discount features. They are an input to a [[settings-geo-zones|geo zone]] **rule** of operation 10. The merchant:

1. Saves a distance entry here.
2. Creates or edits a geo zone on [[settings-geo-zones]].
3. Adds a rule with operation `10` (`OPERATION_DISTANCE`) referencing the distance entry via `distance_id` FK.
4. Configures a shipping method / tax rule / discount to scope to that zone.

At checkout, the platform evaluates the zone's rules against the customer's address; the operation-10 rule resolves "within radius" via the runtime match described above.

See [[geo-targeting-distances]] for the full geo-targeting flow that consumes this match.

### Cache invalidation on save

Saves flush the geo-distance lookup cache so the next checkout zone-match request sees the updated values **immediately**. There is no eventual-consistency window — a merchant who changes a radius can refresh the storefront / checkout and see the new behaviour right away. The cache layer exists for performance (so a hot checkout path doesn't re-query the schema on every request) but does not cause staleness.

### Performance at scale — linear, but cheap per record

Each customer checkout iterates the merchant's distance entries referenced from matched geo zones and computes one `ST_Distance_Sphere` per record. The math is constant-time per record (no geometry intersection cost as with polygons), so:

- 10 distance entries → < 1 ms.
- 100 distance entries → a few ms.
- 1000+ distance entries → still well within the checkout-latency budget.

The spatial index makes the **filter step** sub-linear (the database prunes candidates by their bounding box), so the worst-case linear scan rarely happens in practice.

### Distances vs polygons — cost model

For coverage areas that are well-approximated by a circle, distance entries are the **cheaper** runtime choice:

- One haversine per record (constant time).
- Spatial index pruning (sub-linear in entry count).

Polygons (see [[geo-polygons-settings-main-new]]) require point-in-polygon containment, which is O(vertex count) per polygon — significantly more expensive for complex shapes. For circular service areas, prefer distance entries; for irregular shapes (e.g., a city's irregular delivery boundary), use polygons.

## Related

- [[settings-geo-distances]] — hub.
- [[settings-geo-distances-storage-spatial]] — the `point` spatial column + spatial index this runtime path uses.
- [[settings-geo-distances-distance-units]] — why `distance_in_meters` is the match comparator (not raw `distance`).
- [[settings-geo-zones]] — operation 10 (`OPERATION_DISTANCE`) — the zone-rule integration point.
- [[geo-targeting]] — the cross-cutting concept that consumes this match.
- [[geo-targeting-distances]] — distance-specific geo-targeting mechanics.
- [[shipping-calculation]] — the calculator that calls this match at checkout.
- [[shipping-calc-geo-gating]] — distance + polygon geo-gating in the shipping calculator.
- [[tax-computation]] — taxes also consume this match.
- [[geo-polygons-settings-main-new]] — the polygon alternative; same runtime call point.

## Open questions

- (verify) Whether the cache layer is per-merchant or global; the merchant impact is the same either way.

