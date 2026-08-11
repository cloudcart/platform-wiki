---
type: feature
nav_path: "Products → Properties → Programmatic access"
route_name: categories.property
route_path: /admin/products/property
aliases: ["Properties API", "Properties programmatic access", "Properties plan gate", "Properties webhooks", "Properties side effects"]
tags: [products, properties, api, json-api-v2, plan-gates, side-effects]
plan_gates: ["category_properties"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-property]]. See the hub for the other aspects (list view, wizard, categories, values, merge, business rules).

# Properties — programmatic access & plan gates

## Purpose

The non-UI surfaces of property management: the JSON-API v2 endpoints external integrations call to read / write properties, the side effects shared between admin and API saves, the plan-feature gate that controls property-creation access, and the data-shape facts that differ between what the admin UI exposes and what the platform actually supports.

## Where to find it

This aspect has no dedicated screen. The plan-gate redirect target is `/admin/plan/feature/category_properties`. The JSON-API v2 endpoints listed below are off-platform — see [[json-api-v2]] for the base URL, authentication headers, and rate-limit headers.

These rules apply to every property-related write path:

- The admin Properties UI ([[products-property-list-view]], [[products-property-wizard]], [[products-property-categories]], [[products-property-values]], [[products-property-merge]]).
- The JSON-API v2 endpoints (see Endpoints below).
- Bulk operations launched from [[apps-csv-import]] and similar import surfaces.

## What the merchant can do here

Nothing directly from a merchant-facing screen — this aspect documents the SURFACES rather than the UI. Integrations use it to write properties at scale; the support agent reads it to confirm whether a property change could have originated from outside the admin.

## Settings & fields

The relevant field reference is the **Property record fields** table below. Validation rules + caps are documented on [[products-property-business-rules]] and they enforce identically on the API path.

## Business rules

The cross-cutting business rules live on [[products-property-business-rules]] and are enforced on this path too. Aspects unique to the programmatic surface follow below.

## JSON-API v2 endpoints

The data managed by the admin Properties pages can also be read, created, updated, or deleted via **JSON-API v2**:

- [[api-properties]] — the property definition: `name`, `type`, `is_visible`, `active`, `sort`, `url_handle`, `dec_points`, and the M2M category attachment.
- [[api-property-options]] — the discrete option values under each Checkbox-type property.

See [[json-api-v2]] for authentication, rate limit, and the broader side-effects principle.

## Side effects (shared between admin and API)

A POST / PATCH / DELETE through JSON-API v2 fires **the same** storefront and cache effects as the admin save:

- **Storefront search-engine re-index** for affected products — the new filter behaviour is reflected immediately for customers.
- **`categories_properties.keys.v1` cache invalidation** when a property is created OR an existing property's URL handle changes. So a merchant who renames a property URL handle via API gets immediate effect on the storefront — no manual cache flush needed.
- **Same validations enforce on the API path:**
  - **Type-locked-after-create** — see [[products-property-business-rules]].
  - **Range-must-be-all-numeric** — *"There are values to the property which are not a number"*.
  - **191-character name cap** on both property name and value name.
  - **Delete-blocked-while-in-use** — bulk-delete returns 422 with the list of in-use names just like the admin grid: *"Some properties still has products: `<comma-separated-names>`"*.
- **Merge values** initiated via API runs the same transactional flow as the admin modal — see [[products-property-merge]] (re-point → dedupe → carry external mappings → delete merged-out → ES re-sync).
- **Detaching a category does NOT cascade-delete per-product values** on either path — orphan values remain in storage.

## Plan gate

This feature is gated by the `category_properties` plan-feature key. See [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]].

| Mapping | Shape | What it controls |
|---|---|---|
| `category_properties` | Boolean (URL access) | The `/admin/category/property/create` URL is access-gated by this plan-feature. Without it, the merchant cannot open the create-property wizard — visiting the URL redirects to `/admin/plan/feature/category_properties` for the per-feature upsell. The Properties list page itself remains visible (so existing properties can still be inspected / activated / deactivated / deleted), but the **+ Add property** flow is the gated entry point. |

**Boolean gate behaviour:** redirects to a plan-upgrade or per-feature pack-purchase panel rather than imposing a numeric cap. Per-property values, M2M category attachments, and value-merge actions on existing properties are NOT separately gated — they are governed only by the merchant's `products` permission scope. See [[plan-vs-feature-pack]] for the pack-vs-upgrade decision.

## Surface gap — backend supports more types than the UI exposes

The platform's data layer accepts **four** property types — `checkbox`, `select`, `radio`, and `range` — but the merchant-facing wizard only offers **Checkbox** and **Range**. Properties of type `select` or `radio` can exist (e.g., from older imports), but no UI surface lets the merchant create them; treat the wizard's two-option choice as authoritative.

**Recommendation for integrations:** new properties created through [[api-properties]] should default to `checkbox` or `range` to match what the merchant can subsequently manage in the admin Vue page. `select` / `radio` records lack a Vue edit surface and require API maintenance.

## Property record fields (verified)

Each property record stores 10 fields total:

| Field | Purpose |
|---|---|
| `name` | Display name. Max 191 chars. |
| `type` | Property type (`checkbox` / `range` / `select` / `radio`). Locked after create. |
| `is_visible` | Storefront visibility (the "Use as filter" toggle). |
| `active` | Active flag (the on / off soft-deactivation toggle). |
| `sort` | Sort priority (lower = higher in filter sidebar). |
| `url_handle` | URL slug for filter URLs. Unique across properties. |
| `dec_points` | Decimal points for numeric / range properties. Default 2 when null. |
| `width` / `height` | Value-image dimensions (set per property, applied to every value). |
| `max_thumb_size` | Max thumbnail size for value images. |
| `image` (guarded) | Image upload — not mass-assignable. |

## Property → Category → Product data flow

- **Property ↔ Category** — many-to-many between properties and categories.
- **Property options** — discrete option values defined under the property.
- **Property values** — the per-product value (the assigned option for a specific product).

The flow: **Property defines structure → attached to Categories → applied to Products via the per-product property value.**

When the merchant detaches a category from a property via [[products-property-categories]] or the API, the Property ↔ Category link is removed. **Per-product property values likely PRESERVE as orphan data** (verify) — the platform doesn't cascade-delete values on category detach. Same on the API path.

## Equivalent UI mapping

| API endpoint | Equivalent admin UI |
|---|---|
| `POST /api/v2/properties` | [[products-property-wizard]] step 1 (create property record). |
| `PATCH /api/v2/properties/{id}` | Edit property modal launched from [[products-property-list-view]]. |
| `DELETE /api/v2/properties/{id}` | Per-row Delete or bulk Delete on [[products-property-list-view]]. |
| `POST` / `PATCH` / `DELETE` on `/api/v2/property-options` | [[products-property-values]]. |
| Merge endpoint | [[products-property-merge]] modal. |
| Category attach / detach | [[products-property-categories]]. |

## Related

- [[products-property]] — hub.
- [[products-property-business-rules]] — validation rules enforced on this path too.
- [[products-property-merge]] — transactional merge runs from the API the same way.
- [[api-properties]] — JSON-API v2 resource for the property definition.
- [[api-property-options]] — JSON-API v2 resource for the discrete option values.
- [[json-api-v2]] — auth, rate limit, side-effects principle.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-feature gating model.
- [[settings-hooks]] — webhook surface (relevant when consumers care about property changes).
- [[apps-csv-import]] — bulk-create properties + values via CSV (shares the same side effects).

## Open questions

- Confirm whether per-product property values become orphan data on category detach also via the JSON-API v2 path with the exact same persistence as the admin path (verify).
