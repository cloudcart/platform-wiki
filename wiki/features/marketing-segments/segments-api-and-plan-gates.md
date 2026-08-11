---
type: feature
nav_path: "Marketing → Segments → API & plan gates"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segments API", "Segments plan gates", "segments feature key", "subscribers feature key", "subscribers-rfm feature key", "rfm_interval", "bestseller_period"]
tags: [marketing, segments, api, plan-gates, rfm]
plan_gates: ["segments", "subscribers", "subscribers-rfm"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-segments]]. See the hub for related aspects (list page, types, rebuild mechanics).

# Segments — API access & plan gates

## Purpose

This aspect documents the **programmatic access surface** (JSON-API v2, read-only) and the **three plan-feature gates** that control segments — `segments`, `subscribers`, `subscribers-rfm` — plus the server-side validation rules for the segment-wide settings panel (`rfm_interval`, `bestseller_period`).

## Where to find it

- Programmatic access: [[api-segments]] under [[json-api-v2]].
- Plan-feature settings: admin → **Plan** → **Feature packs** (see [[plan-features]], [[plan-vs-feature-pack]]).
- RFM / bestseller settings panel: adjacent to the segments list on [[segments-list-page]].

## What the merchant can do here

- Read the segment list / a single segment / a segment's current subscribers via JSON-API v2.
- Upgrade the plan or buy a feature pack to lift the `segments` or `subscribers` cap.
- Tune the RFM lookback window (`rfm_interval`) and bestseller window (`bestseller_period`) — defaults work for most catalogs; only change when explicitly tuning RFM cohorts.

## Settings & fields

### Plan-gate mapping table

This feature is gated by three plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `segments` | Numeric (max Automated segments) | Per-plan cap on the number of **Automated** segments. One-time (`regular`) segments do NOT count toward this cap. The "Add segment" precursor popup shows the *"Automated (X of Y)"* counter; over-cap triggers the per-feature purchase modal at [[plan-features]]. Add-on packs extend the cap via [[plan-vs-feature-pack]]. |
| `subscribers` | Numeric (max marketable subscribers) | Per-plan cap on the number of subscribers the platform will EVALUATE in segments. Implementation uses a stored `subscribers.max_id` setting, NOT a `LIMIT` on every query — see [[segments-rebuild-mechanics]] § Subscriber-cap implementation. Over-cap subscribers exist in the database but are silently excluded from segment matching until the merchant upgrades or buys a pack. Error string: *"You reached the limit of feature **Subscribers - :limit** — To continue you should purchase a feature pack or upgrade to a plan with higher limits!"*. The editor's red plan-limit banner (with **Buy package** → `/admin/plan/feature?mapping=subscribers`) appears only for Automated segments. |
| `subscribers-rfm` | Boolean | Whether the segment editor exposes the `subscriber.rfm` condition (RFM bucket targeting — Recency / Frequency / Monetary value). Default `restricted = 1` in the platform code. When off, the RFM condition does not appear in the condition picker (see [[segments-conditions]]). Cannot be extended via pack — requires a plan upgrade. |

When over cap, the merchant is redirected to the per-feature upsell at [[plan-features]]. Numeric gates (`segments`, `subscribers`) extend via packs ([[plan-vs-feature-pack]]); boolean gates (`subscribers-rfm`) require a plan upgrade. App-provided conditions (e.g., `apps.others.product_review.subscriber_segments.*`) appear in the picker only when the owning app is installed and active — that is an app-availability filter, NOT a plan gate.

### Per-segment subscriber-limit caveat

Each segment that uses the `planLimit` condition will only process the first:limit of:total subscribers (help text: *"This segment will use the first:limit of the:total subscribers."*).

### "Remaining" counter

The plan's segment-count cap is shown next to the "Add segment" button as a "remaining" counter via `/admin/common/remaining/segments`.

### Server-side validation rules — the platform code (create / update)

- **`channel`** — required, must equal the literal value `cloudcart`. The platform stores segments tagged with a channel string so future channel-specific segment types can coexist; today the only allowed value is `cloudcart`.
- **`conditions.conditions`** — required, must be a non-empty array, AND must pass the custom `conditionsValidate` extension. Empty body returns *"You must have at least one row with conditions"*. See [[marketing-segments-editor]] § "Validation lifecycle" for the full per-field error map.

### Server-side validation rules — settings panel

The segment-wide settings endpoint controls RFM and bestseller windows, surfaced as a small settings panel adjacent to the segments list:

- **`rfm_interval`** — required, integer, **min 7, max 360 days**. This is the lookback window the RFM analyzer uses when bucketing subscribers (Recency / Frequency / Monetary). Less than 7 days gives noisy buckets; more than 360 days is rejected because the platform's RFM math doesn't smooth long-tail decay correctly.
- **`bestseller_period`** — required, integer, **min 7, max 360 days**. The window used to compute "bestseller" tagging when bestseller-based segment conditions are present.

Both values default to platform-wide defaults on a fresh store. The merchant changes them only when explicitly tuning RFM cohorts or bestseller cadence — the defaults work for most catalogs.

## Business rules

### JSON-API v2 access is read-only

Segments are exposed via **JSON-API v2** at [[api-segments]] — but **read-only**. The API supports:

- `GET` on the segment list.
- `GET` on a single segment.
- `GET` on the per-segment subscriber membership (`/api/v2/segments/{id}/subscribers`).

**`POST` / `PATCH` / `DELETE` are NOT supported** — segments cannot be created or edited via API because the `conditions` rule tree is a structured nested data structure that only the visual builder on [[marketing-segments-editor]] knows how to author.

### Hidden fields on API responses

The schema also hides `conditions`, `conditions_formatted`, `inactive_errors`, `processing`, and `deleted_at` from API responses.

### Integrations workflow

Integrations typically use the API endpoint for:

- Enumerating segments for an external picker UI.
- Reading a segment's current subscriber list for downstream targeting.
- Monitoring `subscribers_count` / `campaigns_count` for reporting.
- Checking `active` state before triggering an external send.

Membership changes are **NOT pushed via webhook** — integrations must poll. To programmatically create audiences, integrations use [[api-subscribers]] + [[api-subscribers-tags]] and define an Automated segment in the admin panel with a tag-based rule.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

### Over-cap interception

The "Add segment" popup intercepts the over-cap case **before** opening the editor — the merchant sees the upsell modal instead. See [[segments-create-popup]] § Automated counter.

## Related

- [[marketing-segments]] — hub.
- [[api-segments]] — JSON-API v2 read-only resource.
- [[json-api-v2]] — auth, rate limits, side-effects principle.
- [[api-subscribers]] / [[api-subscribers-tags]] — used for programmatic audience-building via tag conditions.
- [[plan-features]] — per-feature upsell modal.
- [[plan-vs-feature-pack]] — pack vs plan-upgrade rules.
- [[plan-gates]] — overall plan-gates model.
- [[segments-rebuild-mechanics]] — `subscribers.max_id` enforcement detail.
- [[segments-conditions]] — `subscriber.rfm` condition hidden when `subscribers-rfm` is off.
- [[segments-create-popup]] — over-cap interception flow.

## Open questions

None.
