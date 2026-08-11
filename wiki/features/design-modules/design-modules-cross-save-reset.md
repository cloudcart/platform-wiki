---
type: feature
nav_path: "Design → Modules → Cross-cutting → Save and reset"
route_name: admin.storefront.widget_save
route_path: /admin/storefront/widgets
aliases: ["Save module", "Reset module", "Cancel module", "Module save pipeline", "Module reset pipeline", "Module validation", "Module restrictions", "widget_save", "widget_reset", "widget_load", "blog_panel"]
tags: [design, modules, save, reset, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Storefront Modules — Save and reset

> Part of [[design-modules]]. See the hub for the other cross-cutting aspects (instance model, storage, tabs / groups, cache invalidation, gating).

## Purpose

Three buttons control every module editor — **Save module**, **Reset module**, **Cancel**. This aspect documents the pipeline behind each one (validation, persistence, default restoration) plus the two supporting routes (`widget_load` for inline "+ Add" rows; `blog_panel` for the embedded blog-module picker).

Use this aspect when investigating: *"my module save returned a field error"*, *"reset wiped settings I didn't want to lose"*, *"the + Add Banner button isn't appending a new row"*, *"how does the validation know which fields are allowed?"*.

## Where to find it

Sidebar → **Design** → **Modules** → click any editable module card. The three action buttons sit at the top of the edit side panel.

| Action | Route name | Path | Method |
|--------|------------|------|--------|
| Save module settings | `admin.storefront.widget_save` | `/admin/storefront/widgets/{mapping}/save` | `POST` |
| Reset module to defaults | `admin.storefront.widget_reset` | `/admin/storefront/widgets/{mapping}/reset` | (verify method) |
| Load a sub-template (partial) | `admin.storefront.widget_load` | `/admin/storefront/widgets/{mapping}/{template}/load` | `GET` |
| Blog modules side panel | `admin.storefront.widget.blog_panel` | `/admin/storefront/widgets/blog/panel` | `GET` |

## What the merchant can do here

Three buttons at the top of every module edit panel:

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists the form input to the module's saved settings | None | *"Module successfully edited"* |
| **Reset module** | Wipes the merchant's saved settings — the module reverts to the theme-shipped defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

Additional in-form actions:

- For modules with repeating rows (`extra.banner` banners, `navigation.links` link list), an inline **+ Add** button appends a new row by fetching a `widget_load` partial. The row is added to the form DOM; nothing is persisted until **Save module** is clicked.
- For modules in the `blog` tab, an embedded "blog module picker" can be opened via the `blog_panel` route — used by the page-builder and a few admin areas that want the blog-module list without opening the full module grid.

## Settings & fields

### Save pipeline — per-type restriction validation

When the merchant clicks **Save module**, the server validates the submitted POST body against the module type's declared restrictions:

- Each module type declares a restriction map — a flat `key → validation-rule` dictionary.
- Fields submitted but NOT in the restrictions map are **silently dropped** before persistence. A hand-crafted POST with extra keys cannot widen the stored JSON.
- Remaining fields are validated against their rules. Validation errors are returned as field-level errors keyed by the form-input name, with array notation for nested fields (e.g., `banners[1][src]` for the banner-row image source).
- On success the row is upserted into the per-instance storage (see [[design-modules-cross-storage]]), the per-site cache key is bumped (see [[design-modules-cross-cache-invalidation]]), and the success message *"Module successfully edited"* is returned.

### Reset pipeline — defaults restored, no undo

**Reset module** deletes the merchant's saved settings row for the instance:

- The module falls back to whatever the theme config declares as defaults.
- For modules that expose a shared Configuration group (rare — typically the `productsRelated` family), reset also re-publishes that shared group with the module class's defaults. So on those modules reset is more than per-instance — it restores defaults at the global level too. (verify)
- The per-site cache key is bumped (see [[design-modules-cross-cache-invalidation]]).
- There is no "undo reset" — the merchant must re-enter their custom values.
- The reset confirmation prompt reads: *"Are you sure you want to reset this module?"*.

### Cancel — purely client-side

**Cancel** closes the side panel without saving. No request is sent. Unsaved edits are discarded.

### `widget_load` — inline partial fetch for "+ Add" rows

The `admin.storefront.widget_load` route (`/admin/storefront/widgets/{mapping}/{template}/load`) renders a sub-template fragment of a specific module's includes (e.g., the per-link `link.tpl` partial, or a per-banner row partial). It is used by the Banner / Navigation-Links forms to dynamically add a new row when the merchant clicks **+ Add**. It is **not** a "load a different module's settings as a preset" route — it just fetches the empty-row HTML for client-side append. (verify template-name set)

### `blog_panel` — embedded blog-module picker

The `admin.storefront.widget.blog_panel` route (`/admin/storefront/widgets/blog/panel`) opens a dedicated side panel listing just the blog-tab modules. This is used by other admin areas (e.g., the page builder when adding a `blog-list` block to a Dynamic page) that want to open the blog-module picker without opening the full module grid.

## Business rules

### Validation runs server-side, per module type

Restrictions are declared per module type (e.g., `extra.banner` declares its own list of allowed keys). Two modules of the same type share the restriction map; two instances of the same type also share it. Unknown keys never reach storage.

### Field-level errors use the form-input name with array notation

Nested fields (banner rows, link rows) report errors with bracket syntax — `banners[3][caption]` for the 4th banner's caption field. The form re-renders with the error message inline next to the offending field.

### Reset is non-recoverable

Reset deletes the saved row outright — there is no "trash" or "undo" surface. Merchants who want to keep a backup of their custom settings should export them out-of-band (no admin "Export module settings" surface exists). (verify)

### `widget_load` is read-only — no settings transfer

The `widget_load` route only renders an empty-row partial. It does not copy settings from one instance to another. The merchant who wants to duplicate a banner row currently re-enters the fields manually.

### Side effects: storefront cache regenerates immediately

Both Save and Reset bump the per-site cache key, so storefront pickup is on the next request. Full pipeline in [[design-modules-cross-cache-invalidation]].

### Gating affects whether Save and Reset succeed

Saving or opening a paid module without the required plan feature throws a plan-payment-required error; saving an `editable: no` instance returns HTTP 404 from the edit URL (which means Save / Reset are unreachable in the first place). See [[design-modules-cross-gating]].

## Related

- [[design-modules]] — hub.
- [[design-modules-cross-instance-model]] — what `{mapping}` resolves to.
- [[design-modules-cross-storage]] — the storage layer Save writes to / Reset deletes from.
- [[design-modules-cross-cache-invalidation]] — the cache layer flushed after each Save / Reset.
- [[design-modules-cross-gating]] — why Save / Reset can fail with 404 or plan-payment-required.
- [[marketing-landing-pages]] — the page-builder admin where `blog_panel` is consumed.

## Open questions

- 📡 **Reset HTTP method.** The `widget_reset` route's HTTP verb (POST vs GET) to be confirmed against the controller. (verify)
- ⏸️ **Shared Configuration group on reset.** The `productsRelated` family is documented as sharing a global Configuration group restored on reset — needs re-verification. (verify)
- 📡 **Sub-template set on `widget_load`.** The exhaustive list of `{template}` values accepted by `widget_load` is theme-specific — to be enumerated. (verify)
