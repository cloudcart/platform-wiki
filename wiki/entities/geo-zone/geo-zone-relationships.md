---
type: entity
nav_path: "Entity → Geo Zone → Relationships"
aliases: ["Geo Zone relationships", "Zone consumers", "Zone inputs", "What references a Geo Zone", "Polygon and distance as inputs"]
tags: [entity, geo, zones, relationships, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

# Geo Zone — Relationships

> Part of [[geo-zone]]. See the hub for related aspects (fields, operations, post-code syntax, lifecycle, matching rules).

## Identity

A geo zone is a **shared primitive** — many features REFERENCE it (shipping methods, tax rules, payment providers, discounts, Cart Rules, customer groups) and TWO entities feed INTO it ([[geo-polygon|polygons]] and [[geo-distance|distances]] are inputs to specific operation types). This page catalogues both directions: what reads a zone and what a zone reads.

The zone is NOT a tax rule, NOT a shipping method, NOT a country list. It is the merchant's labelled grouping that those entities point at. Conversely, polygons and distances are NOT consumed directly by shipping / tax / discounts — they exist solely to enrich zones.

## Aliases

- "Geo Zone relationships" / "Zone consumers" — what binds to a zone.
- "Zone inputs" / "Polygon and distance as inputs" — what feeds INTO a zone.
- "What references a Geo Zone" — common support-ticket phrasing.

## Key Attributes

### A Geo Zone has many...

| Relationship | Meaning |
|--------------|---------|
| **Geo rules** | Each rule is one `(operation, location)` pair. Rules are OR-combined within the zone. The first rule is mandatory; the merchant can add unlimited additional rows. See [[geo-zone-fields]]. |

### A Geo Zone REFERENCES (inputs)...

| Input entity | Via | Notes |
|--------------|-----|-------|
| **[[geo-polygon|Geo Polygons]]** | Operation 9 (POLYGON) | Points at a drawn shape defined separately on [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]]. Polygons are INPUTS to zone rules, not consumed directly by shipping / tax / discounts. One polygon can be referenced by many zones. |
| **[[geo-distance|Geo Distances]]** | Operation 10 (DISTANCE) | Points at a center + radius entry defined separately on [[settings-geo-distances]]. **Radius is stored in METERS, not kilometers** — 30 km = `30000`. This is the most common merchant misconfiguration. One distance can be referenced by many zones. |

### A Geo Zone IS REFERENCED BY (consumers)...

| Consumer | Where | Notes |
|----------|-------|-------|
| **[[shipping-provider\|Shipping methods]]** | [[settings-shipping]] | Each shipping method scopes to ONE zone (or "rest of world"). Same method across multiple zones requires multiple method copies today. |
| **Tax rules** | [[settings-taxes]] | Each tax rule scopes to ONE zone (or "rest of world"). **Tax matching uses ONLY country rules in the zone** — region / city / polygon / distance / post-code rules are IGNORED by the tax engine. See [[geo-zone-matching-rules]] + [[tax-computation]]. |
| **[[payment-provider\|Payment providers]]** | [[settings-payment-providers]] | Providers can have country / region scoping that uses zones for availability and fee stacking. |
| **[[discount\|Discounts]]** | [[marketing-discounts]] | Discounts can restrict to specific zones via "Regions" or via [[customer-group]] region restriction. |
| **Cart Rules** | [[apps-cart-rules]] | Cart Rules can target by geo for arbitrary logic (e.g., *"force a specific shipping method for Sofia customers"*). |
| **[[customer-group\|Customer Groups]]** | [[customers-custom-groups]] | Groups can be region-restricted for wholesale / VIP pricing per location. |
| **[[cart]]** | At checkout | The cart resolves the customer's current zone for display in cart line items. |
| **[[order]]** | At submit | The order snapshots the matched zones for VAT, shipping method, and fees that fired. |

### A Geo Zone is NOT...

- **A polygon or distance** — see [[geo-polygon]] / [[geo-distance]]. Those are INPUTS to zone rules, not first-class consumers of customer addresses. Polygons and distances exist solely to enrich zones.
- **A tax rule** — see [[settings-taxes]]. A tax rule REFERENCES a zone but is its own entity.
- **A shipping method** — see [[settings-shipping]]. A shipping method REFERENCES a zone but is its own entity.
- **A country list** — a zone can carry many country rules (or none — when it's polygon / distance / post-code only), but the zone is the merchant's labelled grouping, not the country itself.

### Sharing primitives across zones

One polygon or one distance can back many zones. Typical patterns:

- **Shared delivery polygon** — the merchant draws "City of Plovdiv extended area" once and references it from three zones: one for shipping (free delivery), one for cash-on-delivery availability, one for a 10 % discount Cart Rule.
- **Shared distance** — *"30 km from the warehouse"* defined once, referenced by both a same-day-delivery zone and a free-shipping zone.

When the merchant edits the polygon's shape or the distance's radius, **every** zone referencing it updates immediately — no need to re-save each zone (see [[geo-zone-lifecycle]]).

### FK-protected deletion of inputs

Deleting a polygon or distance that's referenced by a geo zone is **FK-blocked or cascade-warned**. The merchant must unbind from zones first. The exact behaviour (hard block with error message vs cascade warning with proceed option) is one of the open questions on [[geo-polygon]] / [[geo-distance]].

## Where it appears

- [[settings-geo-zones]] — the zone management screen shows the zone definition.
- [[settings-shipping]] — shipping method form has a zone picker.
- [[settings-taxes]] — tax rule form has a zone picker.
- [[settings-payment-providers]] — payment provider settings can include a zone scope.
- [[marketing-discounts]] — discount form's "Regions" rules reference zones.
- [[apps-cart-rules]] — Cart Rule conditions can reference zones.
- [[customers-custom-groups]] — customer-group restrictions can reference zones.
- [[checkout-flow]] — where consumers query the zone match.
- [[orders-details]] — order's snapshotted zone determines analytics + re-quote.

## Related

- [[geo-zone]] — hub.
- [[geo-zone-fields]] — the rule-level inputs that hold the polygon / distance references.
- [[geo-zone-operations]] — operation 9 (polygon) and operation 10 (distance) — the two operations that consume inputs.
- [[geo-zone-matching-rules]] — how consumers resolve the customer against the zone at runtime.
- [[geo-zone-lifecycle]] — FK-protected delete (both for the zone itself and its polygon / distance inputs).
- [[geo-polygon]] — input entity for operation 9.
- [[geo-distance]] — input entity for operation 10.
- [[shipping-provider]] — primary consumer.
- [[payment-provider]] — secondary consumer.
- [[customer-group]] — region-restricted groups.
- [[discount]] — region-restricted discounts.

## Open Questions

- ⏸️ Whether the zone form surfaces a "used by N shipping methods / M tax rules / ..." badge so the merchant can see consumers at a glance before editing — not documented.
- ⏸️ Whether deleting a polygon or distance that's referenced ALSO surfaces which zones reference it (vs a generic "cannot delete — has references" message).
