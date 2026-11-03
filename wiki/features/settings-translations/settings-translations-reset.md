---
type: feature
nav_path: "Settings → Translations → Reset paths"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["Reset translation", "Reset to default", "Reset all to default", "Bulk reset translations", "db:translation append", "db:translation replace"]
tags: [settings, translations, i18n, reset]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-translations]]. See the hub for related aspects (toggle, table, filters, scoping, side-effects, permissions).

# Translations — reset paths

## Purpose

[[settings-translations]] exposes **three** reset paths with different blast radii: a per-row reset (one override at a time), a bulk reset (selected rows), and a "Reset all to default" (every override across every language for the current site's current theme). Per-row / bulk reset is non-destructive at the cluster level — only the targeted rows lose their override. "Reset all" is destructive and irreversible — it truncates every override and reloads the file-based defaults.

The three paths also differ in which background command they run: per-row / bulk run `db:translation --command=append`; reset-all runs `db:translation --command=replace --force`.

## Where to find it

Sidebar → Settings → **Translations**.

- **Per-row reset** — the `fal fa-undo` icon button on each table row's Actions column.
- **Bulk reset** — select rows via the checkbox column, then click **Reset to default** in the bulk-action bar.
- **Reset all to default** — the button in the table header.

## What the merchant can do here

- Reset a single row to platform default via the row's reset button.
- Bulk-select multiple rows and reset them in one action.
- Reset every override in the store via the header button (destructive).
- Cancel each action via the confirm modal before it commits.

What the merchant CANNOT do here:

- Undo a reset. Once an override is deleted there is no version history.
- Scope "Reset all" to one language only — the action runs at site level (see Business rules).

## Settings & fields

### Per-row reset confirm

The per-row Reset button opens a small inline confirm component:

| Element | Content |
|---------|---------|
| **Label** | *"Reset default text?"* |
| **Confirm button** | *"Reset"*. |
| **Disabled state** | Greyed out when `is_translated === 0` (no override exists). |
| **Loader** | Spinner while the per-row reset is in flight. |

On confirm, the request hits `POST /admin/api/core/settings/translations/reset` with `{ids: [<this row's id>]}`. Success toast: *"Translation reset successully"* (typo present in the codebase).

### Bulk-reset confirm

Selecting one or more rows via the table's checkbox column enables a bulk-action bar. The single bulk action is **Reset to default**:

| Element | Content |
|---------|---------|
| **Bulk-action label** | *"Reset to default"* (with `fal fa-undo` icon). |
| **Confirm title** | *"Reset selected texts to default?"* |
| **Confirm yes/no** | *"Reset"* / *"No"*. |
| **Success toast** | *"Deleted successfully"*. |
| **Error toast** | *"Error while deleting"*. |
| **Endpoint** | `POST /admin/api/core/settings/translations/reset` with the selected IDs. |

The success message reads "Deleted" because the underlying operation is a hard delete of the override rows (no "soft delete"). On success the table is re-fetched and the selection clears.

### Reset-all confirm modal — Mode 3 of the shared confirm modal

| Element | Content |
|---------|---------|
| **Title** | *"Reset all texts to default?"* |
| **Message** | *"Quam tellus platea pharetra a semper fermentum pretium. Turpis turpis et sed proin sapien. Rhoncus elit odio purus a elit morbi. Adipiscing."* (Lorem ipsum placeholder copy — has not been replaced with real copy yet `(verify)`). |
| **Confirm** | *"OK"* (primary). Runs the reset-all action server-side. |

The modal shows a loader spinner while the mutation is in flight. On success it closes, the table re-fetches, and a success toast fires.

The same confirm-modal component is also used for the system-labels toggle (modes 1 and 2) — see [[settings-translations-toggle]].

## Business rules

### Per-row / bulk reset deletes only the selected override rows

`POST /admin/api/core/settings/translations/reset` removes the override rows for the IDs provided. The default value is then shown for those keys. Other overrides — for other keys, or for other `(locale, theme)` combinations — are untouched.

### "Reset all to default" is site-wide, NOT just the visible language

The "Reset all" path is **destructive**: it truncates ALL overrides for the current site, then re-loads the file-based defaults. There is no per-language scoping on this path — the command runs at site level, which means **every language's overrides for the current theme are wiped**, not just the language the merchant is viewing. (The site-language scope of the table on screen is misleading here — the action is broader than the visible rows suggest.)

The Assistant should warn merchants explicitly about this scope mismatch before they click "Reset all to default", especially merchants who have invested significant translation work on multiple languages.

### Per-row / bulk runs `db:translation --command=append`

Both per-row and bulk reset trigger `db:translation --command=append --site=<id> --force` after deleting the override rows. The `append` mode synchronises the database against the on-disk language files for the current site — re-loading defaults for the deleted keys.

A plain edit (i.e., updating an override, not resetting it) does NOT run `db:translation`. The Artisan call only fires when a row is being reset back to default.

### Reset-all runs `db:translation --command=replace --force`

The `replace` mode is the destructive one — it truncates the overrides table for the site and reloads from disk. This is what makes "Reset all" irreversible.

### Both reset paths run `js:data-generate` after the DB sync

Every reset (per-row, bulk, or all) regenerates the storefront's pre-built data asset that bundles translations + currency + miscellaneous front-end constants. This runs synchronously inside the reset handler — see [[settings-translations-side-effects]] for the cache-flush + Artisan-command chain.

### Bulk reset is implemented as a DELETE on selected rows

The bulk path runs a `destroy` against the selected IDs, then re-appends defaults from the file. This is why the action's confirmation reads *"Reset selected texts to default?"* even though server-side the rows are physically removed — there is no "soft delete" for overrides.

### Cancelled bulk-reset preserves selection state

If the merchant opens the bulk-reset confirm modal and clicks the cancel/No button, the table's row selection is preserved — the merchant can re-open the confirm or pick a different bulk action. Selection clears only on successful completion.

### `(locale, theme)` scope of resets follows the current view

Per-row and bulk resets delete overrides for the currently-viewed `(locale, theme)` combination. To clear overrides for a different language or theme, the merchant must first switch the storefront language in [[settings-general]] (or the active theme) and then perform the resets in that context. Reset-all is the only path that operates beyond the visible row set — see [[settings-translations-scoping]].

## Related

- [[settings-translations]] — hub.
- [[settings-translations-toggle]] — same confirm-modal component is reused for the system-labels toggle.
- [[settings-translations-table]] — `is_translated` flag that enables/disables the per-row reset button.
- [[settings-translations-side-effects]] — the cache flush + Artisan command chain triggered by each reset path.
- [[settings-translations-scoping]] — `(locale, theme)` dimensions that determine what reset-all sweeps.

## Open questions

- The reset-all confirm modal still shows Lorem ipsum placeholder copy in the message body `(verify)` — should be replaced with real warning text mentioning the site-wide blast radius.
