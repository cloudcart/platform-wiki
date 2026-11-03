---
type: feature
nav_path: "Settings → Translations → Table & inline edit"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["Translations table", "Inline edit", "Per-row Save", "Translation override row", "Label column", "Translation column", "is_translated"]
tags: [settings, translations, i18n, table]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-translations]]. See the hub for related aspects (toggle, filters, reset, scoping, side-effects, permissions).

# Translations — table & inline edit

## Purpose

The body of the Translations screen is a three-column table where every translatable system label appears as a row. The merchant types their custom wording directly into the **Translation** column on the same row; a per-row **Save** button appears only when the row's value has changed. There is no draft / Save-All flow — each row is saved independently and synchronously.

## Where to find it

Sidebar → Settings → **Translations**. The table fills the page below the header bar.

## What the merchant can do here

- See every translatable string in the store as one row.
- Inline-edit the **Translation** column directly in the row (2-row textarea).
- Save a single row via the **Save** button that appears on change.
- Reset a single row via the row's reset (`fal fa-undo`) button — see [[settings-translations-reset]].
- Search by key / value via the standard table search.
- Sort and paginate.
- Bulk-select rows via the checkbox column — enables bulk-reset (see [[settings-translations-reset]]).

What the merchant CANNOT do here:

- Add a new translation key — only existing keys are editable.
- Edit the **Label** column (key + default).
- Save all changed rows at once — each row has its own Save button.
- Autosave on blur or Enter — the Save button must be clicked explicitly.

## Settings & fields

### Translations table — three columns

The rendered table has only THREE columns. The platform's translation key (`label`), default value, and namespace are all surfaced in the single **Label** column's cell content — not separated. The "Section" filter is a top-of-table filter dropdown, not its own column (see [[settings-translations-filters]]).

| Column | What it shows | Editable? |
|--------|---------------|-----------|
| **Label** | The platform's internal translation key (e.g., `*::cart.add_to_cart`) with the default value rendered alongside in the cell. The Section name is derived from the label prefix and used to drive the Section filter — but it's not a separate column. | No |
| **Translation** | The merchant's custom override; empty when no override is set. Inline-editable as a 2-row textarea. The row tracks `prevTranslation` so the Save button only appears when the value has changed. | Yes (inline) |
| **Actions** | **Save** button (shown only when the translation differs from `prevTranslation`) + reset-single button (icon `fal fa-undo`, see [[settings-translations-reset]]). | Click actions |

### Per-row Save (inline, no modal)

The Save button next to the inline textarea appears ONLY when the current value differs from the previously-saved value (`data.translation !== data.prevTranslation`). Clicking it:

- POSTs the updated row to the save endpoint.
- On success: updates `prevTranslation = translation`, sets `is_translated = 1`, fires a *"Translation saved"* toast, and the Save button hides again.
- On error: surfaces an error toast; the row visually reverts.

### `is_translated` flag

Each translation row carries an `is_translated` flag, set to true on save IF the override differs from the platform's default translation. Reset sets it back to false. This flag drives the **Modified / Not modified** filter (see [[settings-translations-filters]]) — it's specifically a "does the current override differ from the platform default" flag, not a "did anyone touch this" flag.

So an override whose text happens to match the platform default is still considered "not modified" for filter purposes.

## Business rules

### No autosave, no Save-All — each row is its own commit

Editing a row reveals the per-row Save button (hidden when value equals `prevTranslation`, shown once changed). The merchant must click Save to commit. There is **no autosave on blur/Enter** and no batch / draft flow. This is intentional — the save handler runs synchronously and triggers cache flushes and a `js:data-generate` rebuild per call (see [[settings-translations-side-effects]]); batching would change the cache semantics.

### Saves are slower than typical "save and continue" UX

Each save runs background Artisan commands inline (see [[settings-translations-side-effects]]). On a store with many translations the merchant may notice a second or two per edit. For mass translation work the merchant is better off making a planned list of changes and applying them in a single focused session.

### Label column is not editable — only the override is

The Label column shows the platform's translation key + the default value. Neither is editable from this screen. To "return to default", the merchant resets the row (see [[settings-translations-reset]]).

### Section is derived from Label — not a separate column

The Label cell contains both the key (e.g. `*::cart.add_to_cart`) and the default value. The "Section" displayed in the filter is computed from the namespace + first dot-separated key segment — see [[settings-translations-filters]] for the derivation rule. The merchant does not pick a section when overriding; it follows the key.

### Standard table primitives apply

Search, sort, pagination, and bulk-select all use the platform's standard table primitives — same UX as elsewhere in the admin panel. Bulk-select enables the bulk-reset action documented on [[settings-translations-reset]].

## Related

- [[settings-translations]] — hub.
- [[settings-translations-filters]] — Modified / Section filter behaviour.
- [[settings-translations-reset]] — per-row and bulk reset actions exposed via the Actions column and bulk-action bar.
- [[settings-translations-side-effects]] — what each Save triggers (cache flush + Artisan commands).
- [[settings-translations-scoping]] — the `(locale, theme)` scope each saved row belongs to.

## Open questions

None.
