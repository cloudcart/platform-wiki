---
type: entity
nav_path: "Entity → Geo Zone → Fields"
aliases: ["Geo Zone fields", "Geo Zone attributes", "Geo Zone schema", "Geo Zone data model", "Zone name + rules"]
tags: [entity, geo, zones, fields, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

# Geo Zone — Fields

> Part of [[geo-zone]]. See the hub for related aspects (operations, post-code syntax, relationships, lifecycle, matching rules).

## Identity

The verbatim attribute catalogue for the [[geo-zone|Geo Zone]] entity — what the merchant edits on the Add / Edit form on [[settings-geo-zones]], the validation strings the platform applies, and the per-rule input fields that change based on which operation type is picked.

A zone has TWO levels of fields: zone-level (the label + a list of rules) and rule-level (the operation type plus inputs whose shape depends on that operation). This page covers both.

## Aliases

- "Geo Zone fields" / "Geo Zone attributes" — common merchant-facing references in support tickets.
- "Geo Zone schema" / "Geo Zone data model" — when devs ask about the columns.
- "Zone name + rules" — describes the two-level shape directly.

## Key Attributes

### Zone-level fields

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Name** | Display name | Required. Free text. Placeholder: *"Add Geo zone name, e.g. Paris or France"*. Store-wide, NOT per-language translatable — same name in every storefront language and every admin language. Multi-language merchants should pick a name that works across all storefronts (a country code, a brand-style label). |
| **Rules** (`values[]`) | One or more `(operation, location)` pairs | First row mandatory; the merchant can add unlimited additional rows via *"+ Add rule"*. Rules within a zone are OR-combined — match ANY rule = match the zone. See [[geo-zone-matching-rules]]. |
| **Sort / display order** | Inferred from creation date | The List view on [[settings-geo-zones]] sorts newest-first by default. No merchant-controllable sort field on the zone itself. |
| **Active** | Implicit (existence) | Zones don't have an explicit Active / Inactive toggle. They exist or they don't. Soft-disable = delete the zone — but consumers must be unbound first (FK-protected; see [[geo-zone-lifecycle]]). |

Zone names are NOT per-language translatable — there is no `locale` field, no override path through [[settings-translations]]. The same name appears verbatim in every storefront language and every admin language.

### Rule-level fields (per row)

Each rule is one `(operation, location)` pair. The **Operation type** picker drives which input fields are shown next.

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Operation type** | One of 11 operation IDs | See the table on [[geo-zone-operations]] for the full list. Picker label: *"Choose operation"*. |
| **Country** | ISO 3166-1 alpha-2 code (e.g., `BG`, `DE`, `GB`) | Shown for operations 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 11. Normalised on save — variants like "United Kingdom" / "UK" / "GB" all resolve to `GB`. |
| **Region** | Administrative region within the country | Shown for operations 2 / 3 / 5 / 6 / 7 / 8. Populated from CloudCart's bundled ISO 3166-2 data. |
| **City** | City within the region | Shown for operations 5 / 6 / 7 / 8. Populated from CloudCart's bundled city tables. Smaller towns may not have a dropdown entry — for those, post-code (operation 11) or polygon (operation 9) is the alternative. |
| **Neighborhood / Street** | Sub-city locality | Shown for operations 7 / 8 only. |
| **Polygon reference** | `polygon_id` referencing a [[geo-polygon|Geo Polygon]] | Shown for operation 9 only. The polygon itself defines the coordinates — see [[geo-polygons-settings-main-new]]. |
| **Distance reference** | `distance_id` referencing a [[geo-distance|Geo Distance]] | Shown for operation 10 only. The distance entry stores center + radius — see [[settings-geo-distances]]. |
| **Post codes** | Comma-separated list of patterns | Shown for operation 11 only. Mixed list of exact codes, wildcards, and four-dot ranges — see [[geo-zone-post-code-syntax]]. |

### Validation rules

- **Name** required; rejected when empty.
- **At least one rule** required; the first row cannot be left blank.
- **Country** required for all operations except 9 (polygon) and 10 (distance).
- **Region** required when the operation type targets a region (2 / 3) or a sub-region (5 / 6 / 7 / 8).
- **Polygon / distance references** are FK-protected — the referenced [[geo-polygon|polygon]] / [[geo-distance|distance]] must exist. If the merchant deletes the underlying polygon / distance, the platform blocks the delete (see [[geo-zone-lifecycle]]).
- **Post-code patterns** have their own validation grammar — see [[geo-zone-post-code-syntax]].

## Where it appears

- [[settings-geo-zones]] — the management screen (List view + Organize / Add / Edit form). The form renders zone-level fields then a repeating rules block.
- [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]] — where the polygon side of a `polygon_id` reference is created.
- [[settings-geo-distances]] — where the distance side of a `distance_id` reference is created.

## Related

- [[geo-zone]] — hub.
- [[geo-zone-operations]] — what each of the 11 operation types matches and which inputs they accept.
- [[geo-zone-post-code-syntax]] — the post-code pattern grammar for operation 11.
- [[geo-zone-lifecycle]] — save / edit / delete semantics for the fields documented here.
- [[geo-zone-matching-rules]] — how the rule list is evaluated at runtime.
- [[geo-polygon]] — the entity the `polygon_id` reference points to.
- [[geo-distance]] — the entity the `distance_id` reference points to.
- [[settings-translations]] — does NOT have a zone-name override path.

## Open Questions

- ⏸️ Whether the form blocks save when a region / city dropdown comes back empty for the chosen country (e.g., very small countries with no city dataset) — coverage limits aren't documented.
