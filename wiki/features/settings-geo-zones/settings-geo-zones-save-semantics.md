---
type: feature
nav_path: "Settings → Geo Zones → Save semantics"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo zone save", "Geo zone form save", "Geo zone validation", "Geo zone name translation", "Geo zone Geonames fallback"]
tags: [settings, geo, zones, save, validation, form]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-geo-zones]]. See the hub for the other aspects (operations, post-codes, Maps, polygon/distance, matching, deletion-cascade).

# Geo Zones — Save semantics (form save, validation, side effects)

## Purpose

Saving a Geo Zone is fully synchronous — no queue, no webhook, no admin notification — but the save flow does several things that surprise merchants if they don't know about them:

- The form **fully replaces** every rule row and every post-code pattern on save (delete-then-create-all). Rule IDs change between saves.
- The system auto-backfills missing region data via a **Geonames API lookup** for city / neighborhood operations — and if Geonames fails, the rule silently saves but **never matches** at runtime.
- The `name` field is store-scoped, max 191 chars, and **not per-language translatable**.
- The `values` array is required — a zone with zero rules cannot be saved.
- The geo-zone lookup cache invalidates on save.

This aspect documents the exact save mechanics and validation rules so support can answer "why didn't my changes apply" questions.

## Where to find it

Sidebar → Settings → **Geo Zones** → **+ New Geo zone** (or click an existing zone name) → fill the form → **Save** in the page header.

The Add / Edit screens share the same layout (Edit pre-fills from the existing zone). The form is rendered as a **full sub-page** inside the Settings shell (not a centered modal), with the standard **Cancel** and **Save** buttons at the top-right of the page header. Sub-tabs read: *List* / *Add Geo zone* (or *Edit Geo zone*).

## What the merchant can do here

- Save a new zone or an edit to an existing zone.
- See validation errors inline on the form when the request fails.
- After save, the merchant is redirected back to the list.

What the merchant CANNOT do:

- Save a zone with zero rules — the **+** to remove the last row is hidden on the first rule to enforce this.
- Save a zone whose `name` exceeds 191 characters.
- Save an inverted or non-numeric post-code range (operation 11) — see [[settings-geo-zones-post-codes]].
- Translate the zone name per language — see business rules.

## Settings & fields

| Field | What it does | Notes |
|-------|--------------|-------|
| **Geo zone name** (`name`) | The merchant's display name for the zone. | Required. Multi-line allowed at the input level. Placeholder: *"Add Geo zone name, e.g. Paris or France"*. Max 191 chars. |
| **Rules (dynamic group)** | One row per `(operation, location)` rule. | First row mandatory and has no **×** icon. Each additional row preceded by an **OR** label, with an **×** delete icon on the right. |

Validation summary:

- `name` is **required** and **max:191**.
- `values` (the rules array) is **required** — zero-rule zones rejected.
- Each row's `operation` must be one of `1..11`.
- Operation-specific location field requirements (country / region / city / polygon_id / distance_id / post_code) are enforced per row.
- Post-code patterns validate per [[settings-geo-zones-post-codes]] (range bounds numeric and ordered).

## Business rules

### Form save fully replaces every rule — no partial updates

On save, every existing rule row is deleted and then re-created from the submitted form. This means:

- An **update is functionally "delete-then-create-all"**. Rules retain no history.
- The **IDs of rule rows change between saves** — a rule that was id=42 before will be id=85 after.
- Post-code patterns are also fully replaced on save — see [[settings-geo-zones-post-codes]].
- If two administrators save the form concurrently, the **last write fully wins**; intermediate states are lost.
- Only the location fields each operation needs are persisted; extra fields are dropped on submit.

### City-scoped operations auto-backfill region via Geonames — silent-failure mode

When saving operations 5/6/7/8 (city or neighborhood scoped) without a region (`admin_zone_1_iso`) supplied, the system triggers a **Geonames API lookup** to resolve the missing region for the given country + city. This matters because runtime matching requires region to match — without it, the rule **silently matches nothing**. See [[settings-geo-zones-matching]] for the region requirement.

Hidden consequences (verified 2026-06-11):

- **The rule still saves** when the region lookup fails — the backfill returns early and `admin_zone_1_iso` stays empty on the row.
- A platform log line is written: **`"GeoZoneValues saved without admin_zone_1_iso; geo-zone will not match in checkout"`** (with zone, operation, country, and city context). This is the support team's needle for *"I configured a city zone and shipping disappeared"* tickets.
- The lookup has a **5-second timeout** (3 s in development), **single attempt, no retry**; on timeout/error a separate log entry is written and the rule still saves without a region.
- **The merchant gets no admin-side warning** — the failure is silent in the UI, and the call adds up to 5 s of latency to the save per affected row.

A distinct second log line marks the timeout / error case (vs. the silent city-not-recognised case), so support can tell "lookup was unreachable" from "city wasn't matched".

### Operation 1 clears `admin_zone_1_iso` on save

When the merchant changes a rule's operation to `1` (Includes country), the save clears the region fields `admin_zone_1_iso` and `admin_zone_1_name`. So switching from a country+region rule to "whole country" cleans up the now-unused region values automatically.

### Zone names are NOT per-language translatable

A geo zone is store-scoped with a single `name` value — **no per-language field, no translation override**. The name the merchant enters appears the same in every storefront language and every admin language. There is **no path through [[settings-translations]] to override geo-zone names per locale**.

**Practical guidance for multi-language merchants**: pick a name that works across all their storefront languages (e.g., a single-word country code or a brand-style label) since it shows verbatim everywhere.

### Side effects of save — entirely synchronous

CRUD on Geo Zones is **fully synchronous**: no background jobs queued, no admin notifications produced. On save:

- The geo-zone lookup cache is invalidated, so the next shipping / tax / discount computation sees the updated zones immediately — changes take effect on the very next cart / checkout request.
- **No webhook event fires** for geo-zone changes (`geo_zone.created` / `geo_zone.updated` are **not** part of the [[settings-hooks]] event catalogue).
- An optional Geonames network call happens only when saving operations 5/6/7/8 without a region.

### FK-protected delete? NO — see deletion cascade

The earlier wiki claim that "delete is FK-protected — must remove dependents first" is **incorrect**. Delete actually CASCADES / sets NULL silently — see [[settings-geo-zones-deletion-cascade]] for the full story.

### Permission

This page sits under the standard Settings permission scope — the same access control as the rest of Settings governs who can create, edit, and delete geo zones.

## Related

- [[settings-geo-zones]] — hub.
- [[settings-geo-zones-operations]] — the 11 operations the save populates per rule row.
- [[settings-geo-zones-post-codes]] — pattern rows are also fully-replaced on save.
- [[settings-geo-zones-google-maps]] — Google Places fills the fields that the save flow then persists.
- [[settings-geo-zones-matching]] — why the silent Geonames-fail produces a non-matching zone.
- [[settings-geo-zones-deletion-cascade]] — delete is NOT FK-protected, despite the legacy claim.
- [[settings-translations]] — does NOT cover geo-zone name translation.
- [[settings-hooks]] — geo-zone events are not in the webhook catalogue.
- [[geo-zone]] — entity page.

## Open questions

None — silent-failure log line and timeout (5 s prod / 3 s dev) verified against backend 2026-06-11.
