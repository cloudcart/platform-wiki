---
type: feature
nav_path: "Settings → Translations"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["Translations", "System labels", "Storefront translations", "Custom labels", "Преводи", "Системни етикети"]
tags: [settings, translations, i18n, labels]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---
# Translations

## Purpose

A screen where the merchant overrides the platform's built-in UI strings (button labels, headings, error messages, etc.) shown to customers on the storefront. The merchant gets a table of every translatable system label with its key, the default text per language, and an editable "translation" column where they can substitute their own wording.

A master switch decides whether the merchant's overrides are actually applied: when "system labels" are **enabled**, the platform reads the merchant's custom translations first; when **disabled**, only the platform defaults are used (the overrides stay in the database but are bypassed). Reset paths exist at three granularities: per-row, bulk-selected, and "Reset all to default" for the entire store.

This hub orients the merchant on what the screen is for. The screen has several distinct behaviours that the Assistant should drill into separately — see the sub-pages below.

## Where to find it

Sidebar → Settings → **Translations**.

The page's breadcrumb reads "Settings → Translations". The route is `/admin/settings/translations`. The header icon is the language icon.

## What the merchant can do here

- See a **status badge** next to the page title: ON (system labels enabled — custom translations applied) or OFF (defaults used).
- Toggle the master switch via the header button — see [[settings-translations-toggle]].
- See and inline-edit every translatable string in a table — see [[settings-translations-table]].
- Filter by **Modified / Not modified** and by **Section** — see [[settings-translations-filters]].
- Reset at three levels (per-row, bulk-selected, reset-all) — see [[settings-translations-reset]].

What the merchant CANNOT do here:

- Add a translation key for a string the platform doesn't already expose — only existing translation keys are editable.
- Edit the default value — only the override is editable.
- Set overrides per language × theme from one place — the screen operates against the current `(locale, theme)` only; see [[settings-translations-scoping]].
- Export / import translations as CSV.
- Edit admin-panel labels — those use a separate system; see [[settings-translations-permissions]].

## Sub-pages (in this cluster)

- [[settings-translations-toggle]] — master switch (system labels ON/OFF), the three confirm-modal modes (enable, disable, reset-all), what each toggle controls.
- [[settings-translations-table]] — three-column table (Label / Translation / Actions), inline-editable textarea, per-row Save (no autosave, no Save-All).
- [[settings-translations-filters]] — Modified / Section filters; how the Section dropdown is derived from each label's section metadata and `*::` label prefixes.
- [[settings-translations-reset]] — per-row reset, bulk reset, and "Reset all to default"; how each path maps to the different translation-rebuild modes.
- [[settings-translations-scoping]] — `(locale, theme)` dimensions; English fallback hard-coded; theme-shipped translation files; multi-language override workflow.
- [[settings-translations-side-effects]] — synchronous rebuild tasks per save (storefront data-asset regeneration and a translation-table rebuild), an internal translation cache with 7200 s TTL, cache flush by tag, no queue, no webhooks.
- [[settings-translations-permissions]] — `store.translations` permission grant; storefront-only scope; admin-panel labels managed via a separate (non-merchant) system.

## Settings & fields

The page renders a header bar with the status badge + toggle button, a filter bar, and the translations table. Detailed field-level documentation lives on the aspect pages:

- **Page header** (status badge + Enable/Disable button) → [[settings-translations-toggle]].
- **Translations table** (three columns + inline edit) → [[settings-translations-table]].
- **Filters** (Modified, Section) → [[settings-translations-filters]].
- **Reset controls** (per-row, bulk, all) → [[settings-translations-reset]].

## Business rules

The screen's most important cross-cutting rules — each is expanded in the relevant aspect page:

- **Overrides survive the master toggle.** Flipping system labels OFF stops applying overrides but does **not** delete them; flipping back ON restores the merchant's accumulated work. See [[settings-translations-toggle]].
- **Two reset levels are not symmetric.** Per-row / bulk reset deletes only the selected override rows; "Reset all to default" truncates **every** override for the current site (across all languages of the current theme). See [[settings-translations-reset]].
- **Storefront only.** This page customises customer-facing labels. Admin-panel labels use a separate, non-merchant-accessible system. See [[settings-translations-permissions]].
- **Overrides are scoped to `(locale, theme)`.** Switching the storefront language in [[settings-general]] or switching themes loads a different override pool. To translate one key into multiple languages × themes, the merchant must repeat the override per combination. See [[settings-translations-scoping]].
- **Saves are synchronous and chatty.** Every save regenerates the storefront data asset and (on resets) rebuilds the translation table inline — saves are slower than a typical "save and continue" UX, and 100 successive edits trigger 100 cache flushes. See [[settings-translations-side-effects]].
- **Permission is gated by `store.translations`.** Moderators need either broad **Settings** or the specific **Translations** grant from [[settings-staff]]. Owners always pass. See [[settings-translations-permissions]].
- **English is the hard-coded fallback default.** On a non-English site, keys missing from the local language file render with English text in the Default column — there is no merchant-facing "fallback language picker". See [[settings-translations-scoping]].

## Related

- [[settings]] — parent hub.
- [[settings-general]] — Storefront Language and Admin Panel Language settings; storefront language change triggers a translation pool append.
- [[multi-language]] — concept page on how multi-language storefronts work platform-wide.
- [[settings-statuses]] — order / shipping / payment status labels are renamed on that screen separately (not via this page), with a similar override mechanic.
- [[settings-invoicing]] — invoice template strings are customised separately; this page does not affect invoice text.
- [[settings-admin-notifications]] — admin-notification email subjects render with their own template strings (not affected by this page).
- [[settings-staff]] — `store.translations` permission grant.

## Open questions

(All previously listed open questions have been resolved — see the aspect pages' "How it works" notes.)
