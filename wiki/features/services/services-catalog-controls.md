---
type: feature
nav_path: "Sidebar → Services → Catalog row controls"
route_name: admin.services.list
route_path: /admin/services
aliases: ["Services catalog row", "Service public flag", "Service archived flag", "Service sort_order", "Service ecosystem flag", "Service groups", "Service tag"]
tags: [services, catalog, controls, visibility]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[services]]. See the hub for related aspects (catalog, purchase flow, routes, billing cycles, known gaps).

# Services — per-row catalog controls

## Purpose

This page documents **what fields on a service row decide whether the merchant sees it, where it appears, and how it is grouped**. The merchant cannot edit these — they are set by CloudCart's commercial team on the shared catalog. This is the reference the LLM uses to answer *"why doesn't this service show up?"* or *"why does this service appear in the Migration group?"*.

## Where to find it

- Per-row controls are rendered on [[services-catalog]] (`/admin/services`) — group title + sort order + Recommended badge `(verify)`.
- The fields themselves are not editable from the merchant admin — the management UI is CloudCart-staff-only and is out of scope for this wiki (see Business rules).

## What the merchant can do here

Nothing — the catalog is read-only for the merchant. The merchant's only lever is to ask CloudCart's commercial team to publish, retire, reorder, or recategorise a service.

## Settings & fields

Storage: services live on a shared CloudCart-wide table — `cc_gate.services` (one row per service) — NOT on the merchant's own DB. Fields verified on the row:

| Field | Type / values | Effect |
|-------|---------------|--------|
| `name` | Translatable string | Displayed name. Multi-language (`bg` / `en` / etc.). Falls back to source language if no translation. |
| `description` | Translatable string | Shown on the [[services-purchase-flow]] confirmation step alongside the name. Multi-language. |
| `price` | Integer (source-currency cents) | Base price. Displayed value is converted to the merchant's currency — see [[services-billing-cycles]]. |
| `currency` | ISO code (typically `EUR`) | Source currency for the invoice amount — see [[services-billing-cycles]]. |
| `billing_cycle` | `null` / `1` / `12` / `24` / other | Charge cadence — see [[services-billing-cycles]] for the full mapping. |
| `public` | `0` / `1` | Visible flag. `1` → row appears on the catalog. `0` → internal-only (not yet launched, partner-only, A / B tests). |
| `archived` | `0` / `1` | Retired flag. `1` → row is hidden from the catalog (legacy). |
| `sort_order` | Integer | Catalog ordering. Lower = earlier. Set by CloudCart's commercial team. |
| `group_id` | FK → `ServiceGroup` | Category grouping. Nestable (parent → child). Services without a `group_id` appear ungrouped at the bottom. |
| `ecosystem` | Flag | In-house vs partner-delivered. Does NOT visually separate rows on the catalog; affects only how CloudCart's commercial team handles the order on the back office. |
| `tag` | String, e.g. `Recommended` | Used by SOME other catalog views; the main list does not visually expose tags `(verify)`. |

### Service groups

Each service belongs to a `ServiceGroup` row (with optional nested parents). The catalog query does `->groupBy('group_id')`. Examples present in the catalog: `Design`, `Migration`, `Hosting`, `Platform → System`. Services without a group appear ungrouped at the bottom.

## Business rules

### `public = 1` AND `archived = 0` is required for visibility

A row appears on `/admin/services` iff:

- `public = 1` AND
- `archived = 0`.

No other field gates visibility on the catalog query — see [[services-catalog]] for the query shape.

### Country-limitation records exist on the row but are NOT enforced

The service data model supports country-limitation records (the same machinery used by apps), but the catalog query in this screen does NOT enforce them — `filterByInvoicingCountry` is NOT called. Every public service is shown to every merchant regardless of billing country. This is a known gap; see [[services-known-gaps]].

### Catalog management UI is internal — out of scope for this wiki

The management UI that lets CloudCart's commercial team create / edit / publish / archive / sort / group services is a CloudCart-staff-only admin surface and is NOT documented in this wiki. Merchants never reach it. The merchant-facing catalog is the read-only result of those internal edits.

### `ecosystem` flag does NOT change the merchant's purchase flow

A service marked `ecosystem` (partner-delivered) goes through the same Pay Now flow as an in-house service — see [[services-purchase-flow]]. The flag affects only how CloudCart's commercial team handles the order on the back office. From the merchant's point of view, the purchase experience is identical.

### `tag` is not visually exposed on the main list

The `tag` field (e.g. `Recommended`) is used by SOME other catalog views but the main `/admin/services` list does not visually surface it `(verify)`. The LLM should not promise the merchant they will see a Recommended badge on this list.

## How it works (verified against backend)

### Catalog query (shape)

The list view fetches all rows where `public = 1` AND `archived = 0`, orders by `sort_order`, and groups the results by `group_id` for rendering into nested `ServiceGroup` sections. No country filter is applied — see [[services-known-gaps]].

### Source of truth

The `cc_gate.services` table is shared CloudCart-wide. The merchant's own site DB does NOT replicate it — the catalog is fetched live from the central gate. This is why the merchant cannot edit catalog rows: they are not theirs.

## Related

- [[services]] — hub.
- [[services-catalog]] — list view that consumes these fields.
- [[services-billing-cycles]] — how `billing_cycle` + `currency` + `price` translate to merchant charges.
- [[services-known-gaps]] — country-filter not applied; `tag` not exposed on the main list.
- [[services-purchase-flow]] — Pay Now flow that consumes the row's `price` + `currency` + `billing_cycle`.
- [[apps]] — sibling catalog that DOES apply country filtering (contrast).

## Open questions

- Confirm `Recommended` and other `tag` values are visible on any current merchant-facing surface `(verify)`.
