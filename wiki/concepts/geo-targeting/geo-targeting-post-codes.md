---
type: concept
nav_path: "Concept → Geo targeting → Post codes"
aliases: ["Post code zones", "Postal code patterns", "Post-code pattern syntax", "OPERATION_POST_CODE", "Wildcard post codes", "Post-code range", "Пощенски кодове", "Пощенски код шаблони"]
tags: [shipping, geo, post-codes, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[geo-targeting]]. See the hub for the other aspects (zones, polygons, distances, IP detection, feature resolution, address resolution).

# Geo targeting — Post codes

## Definition

Operation 11 (`OPERATION_POST_CODE`) inside a [[geo-targeting-zones|zone]] matches the customer's address by **post code pattern within a specified country**. A post-code rule has two inputs:

1. A **country picker** — restricts matching to addresses in that country.
2. A **post-code pattern list** — comma-separated, where each entry is one of three forms (exact, wildcard, range).

Post-code matching is purely **textual** on the address's `post_code` field — no geocoding or coordinates involved. This makes it the most robust primitive for stores whose customers reliably enter post codes but where geocoding is unreliable.

## Scope

Covered:

- The three pattern forms (exact, wildcard, range) and their composition rules.
- Validation constraints (numeric-only ranges, inverted-range rejection).
- The country constraint pairing.
- When to pick post code over polygon or distance.

Not covered:

- The 11 zone operation types — see [[geo-targeting-zones]].
- Polygons / distances — see [[geo-targeting-polygons]] / [[geo-targeting-distances]].

## Contrasts

- **Post code vs Polygon** — post code is a textual match on the address's `post_code` field. Polygon is a spatial match on geocoded coordinates. Post code works without geocoding; polygon works for addresses with no clean post code. See [[geo-targeting-polygons]].
- **Post code vs Distance** — both can express "within a delivery area", but post code is textual while distance is haversine. Pick post code when your delivery areas align with post-code boundaries; pick distance when they don't. See [[geo-targeting-distances]].
- **Exact vs Wildcard vs Range** — three forms, freely mixable in one comma-separated input.

## Pattern syntax

For operation 11, the input is a **comma-separated list**. Each entry is one of three forms:

- **Exact** — `1000` matches only that exact code.
- **Wildcard** — `*` anywhere in the string. `80*` matches anything starting with `80`. `*ER` matches anything ending with `ER`. Wildcards work with alphanumerics.
- **Range** — `<from>....<to>` (FOUR dots). E.g., `1000....1999`. Both ends must be NUMERIC; the lower bound must be less than the upper bound. Alphanumeric ranges (`A1000....A1999`) are rejected. Inverted ranges (`1999....1000`) are rejected.

Mixed example: `1000....1999,80*,90*,ER9875` is accepted — a numeric range, two wildcards, and one exact alphanumeric code.

## Country pairing

The post-code rule always carries a country picker. The match is **post code AND country** as an atomic operation-11 rule — even though the zone's other rules are OR-combined with this one. This means a UK pattern `SW*` in a rule paired with country `BG` will never match (BG addresses don't have post codes starting with `SW`).

To match the SAME post-code pattern across multiple countries, create **one rule per country** in the same zone (OR-combined). Example: a "Major-city centres" zone could contain rule 1 = (BG, `1000....1999`), rule 2 = (GR, `1*`), rule 3 = (RO, `01*`).

## Example — post-code-based local fulfillment

Setup:

- Zone "BG post codes 1000-1999" — operation 11 (country = BG, post codes = `1000....1999`). For tax, also add operation 1 (country = BG); see [[geo-targeting-feature-resolution]].
- Shipping method "Inner city express" scoped to this zone.

Result:

- Customer with post code 1500 → method matches → appears at checkout.
- Customer with post code 4000 → method doesn't match → hidden.

## Example — mixed exact, wildcard, range

A zone targeting a custom catchment in the UK:

- Operation 11 (country = GB, post codes = `SW1*,W1*,EC1A 1AA,N1....N9`).

This matches:

- Any post code starting with `SW1` (`SW1A`, `SW1V 4QQ`, etc.).
- Any post code starting with `W1`.
- The exact code `EC1A 1AA`.
- Numeric post codes `N1` through `N9`. (verify — alphanumeric range validation may reject this; if so, the merchant lists each as an exact / wildcard entry.)

## When to pick post code

- The merchant has a clean post-code list from a carrier (e.g., "we deliver to these 800 post codes").
- Geocoding is unreliable in the country (no Google Places coverage, or address fields are messy).
- The delivery boundaries align with post-code blocks rather than physical distance.
- The merchant wants to enable / disable a catchment by editing a list rather than re-drawing a shape.

## Where it applies

- [[settings-geo-zones]] — operation 11 lives in the zone-rule selector.
- [[geo-zone]] — zones with operation-11 rules.
- [[settings-shipping]] — post-code-scoped shipping methods.
- [[settings-taxes]] — tax matching IGNORES the post-code part of the rule and uses only the country — see [[geo-targeting-feature-resolution]].

## Related

- [[geo-targeting]] — hub.
- [[settings-geo-zones]] — zone management UI.
- [[geo-targeting-zones]] — operation 11 in the full operation table.
- [[geo-targeting-polygons]] — alternative spatial primitive.
- [[geo-targeting-distances]] — alternative spatial primitive.
- [[geo-targeting-feature-resolution]] — why tax ignores the post-code component.
- [[geo-zone]] — entity page.

## Open Questions

- ⏸️ **Alphanumeric range validation.** UK-style post codes like `N1....N9` should logically work but the documented constraint says "both ends must be NUMERIC". If the validator interprets the alphabetic prefix as non-numeric and rejects, the merchant must list each prefix as a separate exact / wildcard entry. (verify with the validator on `settings-geo-zones`)
