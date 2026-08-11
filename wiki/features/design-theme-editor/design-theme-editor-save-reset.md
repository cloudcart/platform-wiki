---
type: feature
nav_path: "Design → Theme Editor → Save & Reset"
route_name: admin.css.builder
route_path: /admin/builder
aliases: ["Theme save", "Theme reset", "Reset theme", "Save theme", "Save all variables", "Theme customisation reset"]
tags: [design, theme, customization, save, reset]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[design-theme-editor]]. See the hub for the other aspects (variables & types, colours, typography, images, CSS compile, live preview & deep-links).

# Theme Editor — Save & Reset

## Purpose

The Theme Editor has exactly two write operations — **Save theme** (commit the merchant's edits) and **Reset theme** (revert everything to the theme's shipped defaults). Both operate on the full variable set across all three sub-tabs (Colours / Typography / Images) — there is no per-sub-tab or per-variable save. This aspect documents the save / reset semantics and the validation gap merchants need to know about.

## Where to find it

`/admin/builder` — both buttons sit in the sidebar's footer of the Theme Editor:

- **Save theme** — bottom-right of the sidebar; always visible.
- **Reset theme** — bottom-left of the sidebar; only visible AFTER the merchant has made at least one customisation. A theme with the shipped defaults intact hides the Reset button.

Sub-routes:

| Action | Route name | Path | Method |
|--------|------------|------|--------|
| Save edited variables | — (same as editor) | `/admin/builder` | POST |
| Reset all customisations | `admin.css.reset` | `/admin/builder/reset` | GET |

## What the merchant can do here

- **Save the entire form** (all colours + all fonts + all image variables) in one shot via **Save theme**. Success message: *"Theme settings successfully edited"*. The live-preview iframe auto-reloads.
- **Reset all customisations** to the theme's shipped defaults in a single transaction via **Reset theme**. Confirmation modal: *"Are you sure you want to reset this theme?"*. Success message: *"Theme settings successfully reset"*. The merchant is redirected back to `/admin/builder` so the panel re-renders with defaults.
- **NOT save just one section** — the form is monolithic; one Save submits everything. A hand-crafted partial POST would wipe the unsubmitted variables (see *Business rules*).
- **NOT revert just one variable** — Reset wipes every customisation in one shot. To revert one colour, the merchant must remember its old value and re-save the form.
- **NOT undo a Save** — once saved, the previous customisation set is gone (replaced row-by-row). The merchant must either remember the previous values, or Reset to defaults and start over.

## Settings & fields

### Save POST shape

The form submits a flat nested array:

```
data[<type>][<parameter>] = <value>
```

Examples:

```
data[color][color-main-background] = #FFFFFF
data[color][color-buttons-primary-text] = #1A8B3F
data[font-family][font-family-titles] = Montserrat
data[font-weight][font-weight-titles] = 700
data[image][image-orientation] = 133.33%
```

The save handler iterates this array, dispatches on `type`, and writes one storage row per variable (see [[design-theme-editor-variables]] for the row shape).

### Reset endpoint

| Aspect | Value |
|--------|-------|
| Route | `admin.css.reset` |
| Path | `/admin/builder/reset` |
| Method | GET |
| Response | JSON `{status: 'ok'}` on success; `{status: 'error', msg: <exception message>}` on failure. |
| UI confirmation | Modal prompt *"Are you sure you want to reset this theme?"* |
| Atomic | Yes — wrapped in a DB transaction with rollback on error. |

## Business rules

### Save replaces the full customisation set (delete-then-insert)

The save handler:

1. Iterates the submitted `data[type][parameter] = value` array.
2. Builds one row per variable: `{parameter, value, type, template}` (with `template` = active theme's slug).
3. **Wipes ALL existing variable rows for the active theme** in storage.
4. Bulk-inserts the new set fresh.

This means a variable that was previously saved but is **not in the current submit** gets reset to its theme-shipped default. In practice the form always submits every variable visible in the editor, so this is invisible to the merchant. But a hand-crafted partial POST would wipe everything not included — there is no merge with the existing rows.

### Reset wipes every customisation atomically

Reset runs inside a single database transaction:

1. Deletes every theme-variable row for the active theme.
2. Recompiles the storefront stylesheet from the theme's defaults (see [[design-theme-editor-css-compile]]).

If recompilation fails, the deletion is rolled back so the merchant's customisations are not lost mid-failure. The merchant sees an error message reporting the failure. Reset is therefore "all or nothing" — partial reset is impossible.

### Reset button is hidden until at least one customisation exists

The Reset theme button is rendered only AFTER the merchant has made at least one change to the shipped defaults. A theme with the defaults intact does not show the button. This prevents accidental "reset a theme that has nothing to reset" clicks.

### No per-variable validation server-side

The save handler does NOT validate variable values against allowed ranges. The editor's dropdowns / pickers are the only validation layer:

- The font-size dropdown offers only `10px` to `72px` — a hand-crafted POST with `200px` would still save.
- The colour picker accepts only hex / RGB — a hand-crafted POST with garbage would still save.
- The image-orientation CUSTOM fields accept positive integers — a hand-crafted POST with `999999%` would still save.

In every case the storefront might render badly, but the save itself does not block. Verify this is still the validation surface in current builds.

### Variables are per-theme — switching themes preserves but hides

Save / Reset operate on the **active theme's** variable rows. Switching to a different theme via [[design-themes]] hides the current customisations because the new theme's variable list is different. The previous theme's rows remain in storage; switching back to the original theme reveals them again. This is what the `template` column in the storage row enforces — partition per theme. See [[design-theme-editor-variables]] for the row shape.

### Defaults-merge ALSO writes synchronisations to storage on load

The load-time merge of theme defaults with merchant overrides is NOT just an in-memory union — it mutates the merchant's storage rows. When the editor loads:

- **New variables** declared by the theme that the merchant has no row for are **inserted** into `front_theme` with the default value.
- **Saved rows** for variables the theme no longer declares are **deleted** from `front_theme`.

This drift-correction runs on every editor open, so a merchant who opens the editor after a theme update has their storage silently re-aligned. No notification is shown. (This means a theme update can change what the merchant "has saved" without an explicit Save click.)

### Cache invalidation runs on every Save and Reset

Both Save and Reset trigger:

- A cache-invalidation event on the variable read model (the back-end's cached variable read is flushed).
- A fresh UNIX timestamp stamped on the merchant's `stylesheet_version` setting — appended to the storefront's `<link rel="stylesheet">` URL as `?<timestamp>` so browser / Cloudflare caches invalidate the moment the merchant saves. See [[design-theme-editor-css-compile]] for the recompile pipeline.

### Save also rebuilds `google_fonts_url`

Every Save rebuilds the merchant's `google_fonts_url` setting from scratch by walking every variable of `type: font-family` and including its chosen value with its associated weight(s). Reset clears the URL back to the theme's default font set. See [[design-theme-editor-typography]] for the URL shape.

### Permission

Save and Reset are gated by the same `store.builder` permission key as the editor itself (also satisfied by the broader `store` key). A staff role without this permission cannot reach the editor and therefore cannot Save or Reset.

## Related

- [[design-theme-editor]] — hub.
- [[design-theme-editor-variables]] — variable types and storage row shape that Save / Reset writes.
- [[design-theme-editor-colors]] — colour-variable sub-tab.
- [[design-theme-editor-typography]] — font-variable sub-tab + `google_fonts_url` setting.
- [[design-theme-editor-images]] — image-variable sub-tab.
- [[design-theme-editor-css-compile]] — server-side stylesheet recompile that Save / Reset trigger.
- [[design-theme-editor-preview-deeplinks]] — iframe auto-reload after successful save.

## Open questions

- Whether server-side per-variable validation (range / regex per type) is on a known roadmap (verify).
