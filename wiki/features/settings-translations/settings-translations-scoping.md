---
type: feature
nav_path: "Settings → Translations → Scoping (locale × theme)"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["Translation scope", "Locale and theme dimensions", "English fallback translations", "Theme-shipped translations", "Multi-language translation override workflow"]
tags: [settings, translations, i18n, scope, multi-language]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-translations]]. See the hub for related aspects (toggle, table, filters, reset, side-effects, permissions).

# Translations — `(locale, theme)` scoping

## Purpose

Every translation override the merchant saves is scoped to **two dimensions simultaneously**: the storefront language (`locale`) and the active storefront theme (`theme`). Switching either dimension surfaces a different override pool. English is the hard-coded fallback default language — there is no merchant-facing fallback-language picker. Themes can ship their own translation files that override the global defaults, which is why the theme dimension matters as much as locale.

## Where to find it

Sidebar → Settings → **Translations**. The scope is determined by:

- The **Storefront Language** set in [[settings-general]] → Language Settings.
- The **active storefront theme** (set via the Themes feature).

## What the merchant can do here

- Override translations for the **current** `(locale, theme)` combination — what the table displays.
- Switch storefront language in [[settings-general]] to override for a different language.
- Switch the active theme to override for a different theme's defaults.

What the merchant CANNOT do here:

- See or edit overrides for a different `(locale, theme)` in the same view.
- Set a fallback language other than English — English is hard-coded.
- Migrate overrides from one language or theme to another in one action.
- Export / import overrides as CSV for bulk porting.

## Settings & fields

This aspect doesn't add new UI controls — it documents the implicit scope every save operates under.

### Scope dimensions per override row

| Dimension | Source | Effect |
|-----------|--------|--------|
| `locale` | Current storefront language from [[settings-general]] | Overrides made on language A do not apply when storefront serves language B. |
| `theme` | Active storefront theme | Overrides made on theme A do not apply when theme B becomes active. |

### Default-value composition (what shows in the Default column)

When the platform builds the Default column for the merchant, it composes the value from a chain of files:

1. **English** (`lang/en/sf.php`) — loaded first if the site language is not English. Acts as the universal fallback.
2. **Site language** (`lang/<lang>/sf.php`) — loaded on top, overrides English where it has a key.
3. **Theme-shipped translations** — if the active theme ships its own `lang.php` file at `<theme>/translations/<lang>/lang.php`, those keys are merged into the defaults under the namespace `<theme_name>::lang.<key>`.

A key that exists in English but is missing in (say) Bulgarian shows the English text as the default. A key the active theme defines overrides the global default for that namespace.

## Business rules

### Overrides are scoped to BOTH `(locale, theme)` — not just `locale`

The unit of scope is the pair, not either dimension alone. Three practical consequences:

- A merchant who maintains a Bulgarian + an English storefront (two locales, one theme) must redo every override per language.
- A merchant who switches themes loses access to their previous theme's overrides. The overrides remain in the database scoped to the old theme — switching back restores them — but they do not migrate to the new theme.
- A merchant who maintains two languages × two themes must do 4× the override work to fully translate the store.

This is one of the most confusing parts of the page for merchants. The Assistant should clarify it explicitly whenever a merchant reports "I translated everything and it's still showing the old text".

### English is the hard-coded fallback — there is no picker

The platform always loads English (`lang/en/sf.php`) first when the site language is non-English. There is **no merchant-facing fallback-language picker**. Keys that exist only in English appear with English text in the Default column even on a Bulgarian site; merchants who want them to read in Bulgarian must add an override row.

### Theme-shipped translations create different "defaults" per theme

Themes can ship their own `lang.php` file with keys under their own namespace (e.g., the platform code). These are merged into the defaults the merchant sees on the Translations table. Two implications:

- The "Default" column for theme A may differ from theme B for the same key, because each theme can ship its own translation file.
- Switching themes loads a different default-set. The merchant's overrides for theme A do not migrate to theme B — they remain in the DB but are not applied while theme B is active.

Theme-shipped translations are loaded once at the time the list endpoint runs and merged into the defaults.

### Switching storefront language runs `db:translation --command=append` automatically

When the merchant changes the storefront language in [[settings-general]] → Language Settings, the platform fires `db:translation --command=append` to load the new language's translation pool from the file system into the database. This is what makes a freshly-changed language's defaults appear in the Translations table.

This is also why a freshly-added language can show English-shaped defaults at first: if the file for that language is partial or missing, the fallback chain (`English → site language → theme`) fills the gap.

The Assistant should note: the storefront language change does **not** migrate overrides from the old language. Each language needs its own override pass.

### `(site_id, locale, theme)` is the cache + DB key

The translation row is keyed by `(site_id, locale, theme)`. The translation cache uses the same composite key. Saves / resets flush the cache for the current key only; other `(locale, theme)` combinations' caches are untouched (but are flushed by tag anyway — see [[settings-translations-side-effects]]).

### Storefront-language change does NOT migrate overrides

When the merchant changes the storefront language, the platform loads the new language's defaults but does not copy the merchant's old-language overrides into the new locale. The old-language overrides remain stored, scoped to the old locale; they apply again if the merchant switches back. The Assistant should warn merchants who are reorganising storefronts not to assume their work carries over automatically.

## Related

- [[settings-translations]] — hub.
- [[settings-translations-table]] — the table operates on rows from the current `(locale, theme)` only.
- [[settings-translations-reset]] — per-row / bulk reset scopes to current `(locale, theme)`; reset-all sweeps every locale of the current theme.
- [[settings-translations-side-effects]] — `db:translation --command=append` fires on storefront-language change.
- [[settings-general]] — Storefront Language picker; switching it changes the scope of this screen.
- [[multi-language]] — concept page on how multi-language storefronts work platform-wide.

## Open questions

None.
