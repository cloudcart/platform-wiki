---
type: concept
nav_path: "Concept → Geo targeting → Zones"
aliases: ["Geo Zones", "Geo zone operations", "Zone rules", "Zone operation types", "OPERATION_ALL_IN_COUNTRY", "OPERATION_ONLY_REGION", "OPERATION_POLYGON", "OPERATION_DISTANCE", "OPERATION_POST_CODE", "Гео-зони", "Операции в зона"]
tags: [shipping, tax, geo, zones, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[geo-targeting]]. See the hub for the other aspects (polygons, distances, post-codes, IP detection, feature resolution, address resolution).

# Geo targeting — Zones

## Definition

A **Geo Zone** is the merchant-facing unit that other features (shipping, tax, discounts, fees, customer groups, Cart Rules) reference to scope themselves geographically. A zone is a **named bag of rules**, where each rule is one `(operation, location)` pair and **rules within a zone are OR-combined**.

A zone has:

- A merchant-set `name` (e.g., "EU", "Bulgaria", "Sofia delivery area"). The name is store-wide; see [[geo-targeting-address-resolution]] for the non-translatability rule.
- One or more **rules** of the 11 operation types below.

Zones are managed at [[settings-geo-zones]].

## Scope

Covered here:

- The 11 zone-rule operation types and their inputs.
- The OR-semantics inside a single zone (and the same OR-semantics across multiple zones referenced by one feature).
- When to use which operation.
- The "AND-of-locations" workaround (no AND inside a zone).

Not covered:

- Polygon-input mechanics — see [[geo-targeting-polygons]].
- Distance-input mechanics — see [[geo-targeting-distances]].
- Post-code pattern syntax — see [[geo-targeting-post-codes]].
- Which feature uses zone matches how — see [[geo-targeting-feature-resolution]].

## Contrasts

- **Rules within a zone (OR) vs. zones referenced by a feature (also OR)** — both sides OR. No AND at either level. For AND, use a single compound operation (e.g., operation 5 = country + region + city) or a polygon.
- **Zone vs. Polygon / Distance** — the zone is what consuming features reference. Polygons and Distances are INPUTS to zone rules (operations 9 and 10), never referenced directly by shipping / tax / discount.
- **Operation 1 (country) vs. operation 5 (country+region+city)** — operation 1 matches every address in the country. Operation 5 is an atomic country+region+city AND-rule (the only built-in AND).
- **Exclusion operations (3, 4, 6, 8)** vs. inclusion operations — exclusions encode "all of X except Y" without needing two rules.

## The 11 operation types

| ID | Constant | Match logic | Inputs |
|----|----------|-------------|--------|
| **1** | `OPERATION_ALL_IN_COUNTRY` | Match every address in country X. | Country picker |
| **2** | `OPERATION_ONLY_REGION` | Match only addresses in region Y of country X. | Country + region |
| **3** | `OPERATION_ALL_IN_COUNTRY_WITHOUT_REGION` | Match every address in country X EXCEPT region Y. | Country + region |
| **4** | `OPERATION_ALL_NOT_COUNTRY` | Match every address NOT in country X. | Country picker |
| **5** | `OPERATION_ALL_CITY` | Match only addresses in city Z of region Y in country X. | Country + region + city |
| **6** | `OPERATION_ALL_NOT_CITY` | Match every address in region Y of country X EXCEPT city Z. | Country + region + city |
| **7** | `OPERATION_ALL_STREET` | Match only addresses in neighborhood W of city Z. | Country + region + city + neighborhood |
| **8** | `OPERATION_ALL_NOT_STREET` | Match every address in city Z EXCEPT neighborhood W. | Same as 7 |
| **9** | `OPERATION_POLYGON` | Match addresses inside polygon P. | Polygon reference — see [[geo-targeting-polygons]] |
| **10** | `OPERATION_DISTANCE` | Match addresses within radius R of point Q. | Distance reference — see [[geo-targeting-distances]] |
| **11** | `OPERATION_POST_CODE` | Match addresses with post code matching pattern P in country X. | Country + post-code pattern — see [[geo-targeting-post-codes]] |

## Picking the right operation

| Need | Use |
|------|-----|
| Specific city / region / country | Operation 1 / 2 / 5 with the dropdown picker. |
| Custom-drawn area (e.g., "this neighborhood, but cropped at the river") | Polygon (operation 9). |
| "Within X km of my warehouse" | Distance (operation 10). |
| Post-code list / pattern (e.g., "Sofia post codes 1000-1999") | Post code (operation 11). |
| "All of Bulgaria except Sofia" | Operations 1 + 6 OR a single operation 3 (exclude region). |
| "Within 30 km of either of my two warehouses" | Two distance entries + one zone referencing both via separate rules (OR-combined). |

## Where it applies

- [[settings-geo-zones]] — the zone management screen; lists every zone and provides the add/edit form.
- [[settings-shipping]] — each shipping method picks one zone (or "rest of world") in the form's "Target" + "Geo zone" fields.
- [[settings-taxes]] — each tax rule picks one zone. Note that tax matching ignores all non-country operations — see [[geo-targeting-feature-resolution]].
- [[settings-payment-providers]] — payment-method fees can scope to a zone.
- [[marketing-discounts]] — discounts can restrict to a zone (or use customer-group regionalisation).
- [[customers-custom-groups]] — customer groups can be region-restricted via a zone reference.
- [[apps-cart-rules]] — Cart Rules can branch on geo via a zone reference.

## Zone can't enforce AND-of-rules — use other features

Within a single zone, rules are OR-combined. There's no AND. So "Bulgaria AND Sofia" isn't expressible as two rules in one zone (which would mean "Bulgaria OR Sofia" = all of Bulgaria). Instead:

- Use a single rule of operation 5 (city) which combines country + region + city as ONE atomic rule.
- OR use a polygon that geographically constrains the area — see [[geo-targeting-polygons]].
- OR split into two zones and let the consuming feature reference both (works only for shipping / fees / discounts that allow multi-zone reference).

## Example — three EU markets with a shared shipping carrier

Setup:

- Zone "Bulgaria" — operation 1 (country = BG).
- Zone "Germany" — operation 1 (country = DE).
- Zone "France" — operation 1 (country = FR).
- One shipping method per country, all using the same carrier (e.g., DHL) but scoped to the respective zone.
- One tax rule per zone with the country's VAT rate.

Result:

- Bulgarian customer sees only the BG DHL method and BG VAT.
- German customer sees only the DE DHL method and DE VAT.
- French customer sees only the FR DHL method and FR VAT.

## Related

- [[geo-targeting]] — hub.
- [[settings-geo-zones]] — zone management UI.
- [[geo-zone]] — entity page.
- [[geo-targeting-polygons]] — polygon input to operation 9.
- [[geo-targeting-distances]] — distance input to operation 10.
- [[geo-targeting-post-codes]] — pattern syntax for operation 11.
- [[geo-targeting-feature-resolution]] — how each consuming feature uses zone matches.
- [[settings-shipping]] / [[settings-taxes]] / [[marketing-discounts]] — primary consumers.

## Open Questions

None.
