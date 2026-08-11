---
type: entity
nav_path: "Entity → Tax / Fee → Overrides"
aliases: ["Tax overrides", "Per-region override", "Per-category override", "Tax exceptions", "Regions Exceptions box", "Categories Exceptions box"]
tags: [entity, taxes, vat, overrides, exceptions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax]]. See the hub for the other aspects (attributes, VAT vs Fee, order snapshot, validation, business rules).

# Tax / Fee — per-region + per-category overrides

## Identity

After the matching VAT rule is picked (see [[tax-rate-selection]]), two override layers swap in a different rate **per line item**: per-region overrides (rate varies by sub-region within the zone) and per-category overrides (rate varies by the product's category). Both are stored in the same `tax_overrides` table — distinguished by which columns are populated — and both attach only to **Tax** rows (Fees have no overrides).

This is where merchants encode rules like "20% VAT base, but 9% on Books and 0% on Pharmacy", or "20% base everywhere in the EU, but 21% in Cyprus specifically".

## Aliases

- **Per-region override** — the Regions Exceptions box rows.
- **Per-category override** — the Categories Exceptions box rows.
- **Tax exceptions** — umbrella term in the admin UI.

## Key Attributes

### Per-region overrides (`regions[]`)

| Field | Notes |
|-------|-------|
| Visible | Only when **Google Maps API key is configured** AND `geo_zone_id` is picked. |
| `state_iso_2` | The matched region's ISO-2 sub-region code. |
| `text` | The place name (Google Places autocomplete display). |
| Rate | Different rate per sub-region within the zone. |

Each row uses Google Places autocomplete to identify the sub-region. Without the maps API key, the box is hidden and the merchant cannot create regional sub-overrides.

### Per-category overrides (`categories[]`)

| Field | Required? | Notes |
|-------|-----------|-------|
| **Description** | Yes | Free-text label shown on the override row. |
| **Category** | Yes | One of the merchant's [[category|categories]]. |
| **Region** | Only if target = `regions` AND maps key configured | Combines region + category for a sub-region-specific override. |
| **Amount** | Yes | The override rate. |

Always visible on the Tax form (no maps-key gate).

## Precedence ladder

When a cart line is taxed, the engine walks the override list in this order and uses the FIRST match (the older wiki claim *"per-category beats per-region beats base"* understated the nuance — the verified ladder is below; see [[tax-overrides]] for the runtime walk):

1. **Combined category + region match** — sorted by `category_id DESC`, picks the line's primary category combined with its resolved region. Most-specific wins.
2. **Category-only match** — line's primary category has an override (no region constraint).
3. **Region-only match** — fires only when **NO** category override matched the line's category. The region-only override does NOT layer on top of a category match.
4. **Base rate** — the rule's `tax` value.

Each cart line is evaluated independently. A 5-line order can end up with five different effective rates if categories / regions split that way.

## Important gotchas

### Per-category override matches the PRIMARY category only

The tax engine matches the product's PRIMARY category (the `category_id` field on the product, NOT the additional category memberships in the pivot). If the primary category has an override, that override applies; if not, the base rate applies. Membership in a secondary category with a tax override does NOT trigger that override.

A merchant who moves a product from "Books" (9%) to "General" (20%) as primary, while keeping "Books" as secondary, will tax the product at 20%.

### Region override needs the maps API key

Without a configured Google Maps API key, the Regions Exceptions box is hidden entirely. Per-category overrides still work (they have no maps dependency), but per-region overrides cannot be created — even if the underlying zone has sub-region rules.

### Region-only loses to category-only

The merchant intuition "I set a Cyprus override, so all Cyprus customers get that rate" is wrong if the cart line's primary category ALSO has its own category-only override. Category-only wins over region-only in the precedence ladder above.

To force a region-only behaviour, the merchant must either (a) remove the category-only override, or (b) create a category+region combined override that matches.

### Overrides live in `tax_overrides` (with timestamps)

Unlike the parent `taxes` row (no `created_at` / `updated_at`), the `tax_overrides` table DOES carry timestamps. This is the only place inside the entity where edit times are recorded.

### No bulk import of overrides

There is no CSV path for overrides — each row is added through the form's repeatable box. A merchant migrating dozens of category overrides re-enters them one at a time, or asks CloudCart support for a bulk insert.

## Where it appears

- [[settings-taxes]] — Regions Exceptions box + Categories Exceptions box on the Tax edit form.
- [[tax]] — entity hub.
- [[orders-details]] — order totals show the resolved per-line rate after overrides apply.

## Related

- [[tax]] — hub.
- [[tax-entity-attributes]] — `regions[]` and `categories[]` field rows.
- [[tax-overrides]] — runtime walk through the override layer.
- [[tax-rate-selection]] — picks the matching VAT rule BEFORE overrides fire.
- [[category]] — the category entity referenced by category overrides.
- [[geo-zone]] — sub-region rules inside the zone (only country rules drive matching; sub-region rules drive per-region overrides via Google Places).
- [[settings-taxes]] — management screen.

## Open Questions

None.
