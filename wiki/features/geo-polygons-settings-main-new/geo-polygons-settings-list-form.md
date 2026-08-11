---
type: feature
nav_path: "Settings → Geo polygons → List / Add / Edit"
route_name: geo_polygons.settings.new
route_path: /admin/settings/geo-polygons-new
aliases: ["Geo polygons list", "Add polygon", "Edit polygon", "Polygon name field"]
tags: [settings, geo, polygons, shipping, maps]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Geo polygons — list, Add, and Edit

> Part of [[geo-polygons-settings-main-new]]. See the hub for related aspects (drawing limits, zone integration, delete cascade).

## Purpose

The day-to-day screens of the Geo polygons feature: the **list** of saved polygons, and the **Add / Edit form** where the merchant names a polygon and outlines it on a Google Map. A polygon is a single named, closed shape that other screens reference to scope shipping, taxes, and discounts to customers inside the drawn area.

## Where to find it

Sidebar → Settings → **Geo polygons**. The list lives at `/admin/settings/geo-polygons-new`. From the list, **+ New Geo polygon** opens the Add form (`/admin/settings/geo-polygons-new/add`); clicking a polygon name opens the Edit form (`/admin/settings/geo-polygons-new/edit/:id`).

The breadcrumb is built dynamically: **Settings → Geo polygons → (Add Polygon | Edit Polygon)** depending on the active route. A tabs strip shows a single "Polygons" tab, plus a conditional "Add Polygon" / "Edit Polygon" tab when on a create/edit route.

| Label | Route name | Route path |
|-------|------------|------------|
| Geo polygons (root) | `geo_polygons.settings.main.new` | `/admin/settings/geo-polygons-new` |
| List | `geo_polygons.settings.new` | `/admin/settings/geo-polygons-new` |
| Add | `geo_polygons_add.settings.new` | `/admin/settings/geo-polygons-new/add` |
| Edit | `geo_polygons_edit.settings.new` | `/admin/settings/geo-polygons-new/edit/:id` |

## What the merchant can do here

### List view
- See all polygons by **Polygon name** with per-row Edit (click the name) and Delete (per-row trash icon) actions.
- Use the global free-text `query` search and standard pagination.
- Click **+ New Geo polygon** in the page header (or in the "No result" empty state) to open the Add form.

### Add / Edit form
- Type a **Polygon name** (free text, e.g. "Sofia center", "Plovdiv delivery area", "Warehouse #1 service zone").
- Outline the polygon with the Google Map drawing tools (see [[geo-polygons-settings-drawing-limits]] for the full drawing mechanics and limits).
- Customise the polygon colour using the rectangles on the right side of the map.
- Save: the merchant is redirected back to the list on success. Delete shows toast *"Deleted successfully"*.

The default list sort is `id DESC` (newest first). The list is **not** sortable / filterable beyond the global text search.

## Settings & fields

### List table

| Column | Notes |
|--------|-------|
| **Polygon name** (`name`) | Click navigates to the Edit form. |
| **(actions)** | Per-row Remove (trash icon). Toast on success: *"Deleted successfully"*. |

### Add / Edit form

| Field | What it does | Notes |
|-------|--------------|-------|
| **Polygon name** (`name`) | Display name for the polygon. | Required (Zod min 1 — *"The Polygon name field is required"*). Multi-line input allowed. Placeholder: *"Add the name of the Polygon. Example: Paris or France"*. |
| **Drawing area** (`area`) | The polygon coordinates, serialized via the Google Map drawing tool. | Required in practice (a polygon with no outline cannot be saved meaningfully). Stored as the Google Maps JSON representation of the shape. Editing later loads the existing outline as editable. |

The Add / Edit page is a single settings box with one section: the `name` input, a separator, then the map module block. The form ref defaults to `{ name: '', area: {} }`. On Edit, the page loads the existing row, sets `name` + `area`, then becomes ready after a short delay so the map module has time to mount. On save, the payload is just `{ name, area }` — no other fields.

## Business rules

### Validation
- `name` — required, non-empty (*"The Polygon name field is required"*).
- `area` — permissive client-side validation (`z.any`); the server enforces the rest. A polygon with no drawn outline is not meaningfully saveable.

### Save / delete are synchronous
Creating, updating, or deleting a polygon is purely synchronous — no background jobs, no admin notifications, no webhooks fired from this page. Saving a polygon flushes the geo-polygon cache so the next geo-zone evaluation at checkout uses the new coordinates (standard Settings cache behaviour).

### Permission
Standard settings-area permission applies. There is no granular per-feature permission distinct from the parent [[settings]] area.

### Delete is destructive to dependent rules
Deleting a polygon silently removes the polygon rule from any geo zone that referenced it — see [[geo-polygons-settings-delete-cascade]] for the verified cascade behaviour and merchant-visible effect.

## Related

- [[geo-polygons-settings-main-new]] — hub.
- [[settings]] — parent settings hub.
- [[settings-geo-zones]] — geo zones reference polygons defined here.
- [[geo-polygon]] — entity page.

## Open questions

_None — list + form surfaces verified against the modern Vue + API layer._
