---
type: feature
nav_path: "Design → Modules → Cross-cutting → Storage"
route_name: admin.storefront.widget_save
route_path: /admin/storefront/widgets
aliases: ["Module storage", "Module settings storage", "Module JSON blob", "Per-instance settings", "Module overlay", "Sister-site module overlay", "Theme modules block storage", "Orphaned module settings"]
tags: [design, modules, storage, theme]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Storefront Modules — Storage

> Part of [[design-modules]]. See the hub for the other cross-cutting aspects (instance model, tabs / groups, save / reset, cache invalidation, gating).

## Purpose

How module settings are PERSISTED, and how three sources of module data merge at read time to produce the final view the merchant sees on the Modules screen. The storage layering is identical for every module category (content, products, layout, blog, etc.) — this aspect is the single canonical reference.

Use this aspect when investigating: *"my homepage banner settings disappeared after switching themes"*, *"the special-store override for this client isn't taking effect"*, *"I edited the module but the storefront shows the old value"*, *"why does the database still have settings for a module I can't see?"*.

## Where to find it

The storage layer is **invisible** to the merchant — no admin surface manages it directly. This page documents it for support-investigation purposes. The Save / Reset / Cancel actions on `/admin/storefront/widgets/{mapping}` are the only merchant-driven writes to this layer — see [[design-modules-cross-save-reset]] for the action UI.

## What the merchant can do here

- **Save** an editable module — upserts a row in the per-site module storage with the new JSON, then bumps the per-site cache key (see [[design-modules-cross-cache-invalidation]]).
- **Reset** an editable module — deletes the merchant's saved row, falling back to theme defaults.
- See changes on the next storefront request — no manual cache clear required.

The merchant CANNOT manage the underlying storage / cache directly — there is no admin "Clear module cache" button, no "List orphaned modules" surface, no "Restore deleted settings" surface.

## Settings & fields

There are no settings on this aspect — it documents the layering.

### Storage — three sources merged at read time

A module instance the merchant sees on the Modules screen is actually the merge of THREE layers, **last write wins per field**:

1. **Theme JSON** — declares the instance name, the underlying module `map` (e.g., `extra.social`, `product.filters`, `extra.text`), the default `settings`, the `editable` flag, and the optional `category` / `group` keys. Lives with the theme files; only changes when CloudCart ships a new theme version or a custom theme. (verify exact file path)
2. **Sister-site overlay** (`site_widgets.site_<site_id>` config) — a per-store override file that can ADD or REPLACE instances for one specific store. This is how special-store carve-outs are layered on top of the theme defaults without forking the theme. Cloud-side; merchant doesn't manage it. (verify)
3. **Merchant saves** (database `front_widget` row per instance) — one row per instance keyed by `mapping` (= instance name) + `settings` JSON blob + `global` flag. Reset deletes this row; Save upserts it. (verify)

When the merchant opens a module, the platform reads the theme JSON, merges the sister-site overlay, then layers the merchant's saved JSON on top.

### Settings are stored as JSON per instance

Each instance's settings are one JSON blob keyed by the instance name (e.g., `homeText1`). The same module TYPE can be instanced multiple times (e.g., `homeText1`, `homeText2`, `homeText3` all use `extra.text`) — each instance has its own JSON blob, independent of the others. See [[design-modules-cross-instance-model]] for the instance / type model.

### Orphaned settings on theme switch

Settings for an instance that's been REMOVED from the active theme remain in the database but are **never read** — they're orphaned. If the merchant later switches back to the original theme (or to a different theme that declares the same instance name), the saved settings re-activate. Instance names that don't exist in the new theme stay orphaned indefinitely — there's no merchant-facing "Clean up orphaned modules" surface. (verify behaviour on theme re-switch)

### What's in the JSON blob

The fields per blob depend on the module TYPE. Examples:

- `extra.banner` — `banners` array (1–24 entries, each with `image_type`, `src`, `link_to`, `link_target`, `caption`, `open_new_tab`, optional `type: script` with `html`), `banner_amount`, `banners_per_row`, `enable_slider`, `enable_gallery`.
- `extra.carousel` — `amount`, `full_width`, `caption`, `controls`, `indicators`, `animate`, `autoplay_interval`.
- `extra.text` — `content` (TinyMCE rich-text HTML).
- `extra.backgroundImage` — `image` (uploaded asset reference).
- `layout.header` — `header_template`, `menu_type`, `mobile_menu_type`, plus toggles.
- `navigation.links` — `links` array (each: `name`, `url` or `route`, `open_new_tab`, `icon`).

The exact key names are validated against the module type's restrictions on save — see [[design-modules-cross-save-reset]].

## Business rules

### The module catalogue is defined by the active theme

What appears on `/admin/storefront/widgets` is **theme-defined**. The sister-site overlay can ADD or REPLACE instances; the merchant's saved JSON only edits existing instances. Switching themes via [[design-themes]] replaces the catalogue — orphaned settings linger in the database but are not editable.

### Last write wins per field — across all three layers

Field-level merge, not blob-level replace. So if the theme declares `extra.banner` with `banner_amount = 4` and the merchant saves `banner_amount = 6`, the merchant's value wins for `banner_amount` while every other unset field falls back to the theme default. There is no "partial overlay vs full overlay" mode — merge is always per-field.

### Save validates against the module type's restrictions

Fields not declared in the module type's restrictions are **silently dropped** before persisting — a hand-crafted POST with extra keys can't widen the stored JSON. Validation rules and error reporting are documented on [[design-modules-cross-save-reset]].

### Reset deletes the saved row, restores theme defaults

**Reset module** deletes the merchant's row from `front_widget` (or equivalent) — the module falls back to whatever the theme config declares. There is no "undo reset" — the merchant must re-enter their custom values. For modules that share a global Configuration group (rare — typically the `productsRelated` family), reset also re-publishes that shared group with the module class's defaults. (verify)

### Special-store overlays are read-only from the merchant view

The sister-site overlay is configured outside the merchant admin (typically by CloudCart staff for special-client onboarding). The merchant sees the overlaid instance list as if it were part of the theme — they can edit the merchant-save layer on top of it but cannot edit the overlay itself. (verify)

## Related

- [[design-modules]] — hub.
- [[design-modules-cross-instance-model]] — instance vs type; what the `{mapping}` key in the saved row refers to.
- [[design-modules-cross-save-reset]] — the Save / Reset / Cancel actions that write to this layer.
- [[design-modules-cross-cache-invalidation]] — the cache layer in front of this storage.
- [[design-modules-cross-gating]] — how the `editable: no` flag in the theme JSON suppresses the edit form.
- [[design-themes]] — the source of layer 1 (theme JSON).

## Open questions

- 📡 **Database table / file paths.** The `front_widget` table name, the sister-site config path, and the theme `modules` block file are documented from prior verification — exact storage locations to be re-confirmed against current code. (verify)
- ⏸️ **Reset of modules sharing a Configuration group.** The `productsRelated` family is said to share a global group on reset — re-verify against current backend. (verify)
- 📡 **Orphan cleanup.** Whether orphaned saved settings are ever garbage-collected (e.g., on long theme inactivity) is unclear. (verify)
