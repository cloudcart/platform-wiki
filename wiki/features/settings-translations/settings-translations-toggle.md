---
type: feature
nav_path: "Settings → Translations → System-labels toggle"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["System labels toggle", "Enable system labels", "Disable system labels", "translations_active", "Master translation switch", "Системни етикети"]
tags: [settings, translations, i18n, toggle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-translations]]. See the hub for related aspects (table, filters, reset, scoping, side-effects, permissions).

# Translations — system-labels toggle

## Purpose

The master switch at the top of [[settings-translations]] that decides whether the storefront actually uses the merchant's custom translation overrides, or falls back to the platform's shipped defaults. Toggling does **not** delete the merchant's accumulated overrides — when the switch is OFF the platform simply bypasses them; turning the switch back ON resumes applying them. The same confirm-modal component is also reused for the destructive "Reset all to default" action.

## Where to find it

Sidebar → Settings → **Translations**. The toggle is the button in the page header next to the status badge.

## What the merchant can do here

- See the **status badge** next to the page title: **ON** (system labels enabled — custom translations applied) or **OFF** (system labels disabled — defaults used).
- Click the master toggle button. The button label is dynamic:
  - *"Enable system labels"* when the toggle is currently OFF.
  - *"Disable system labels"* when the toggle is currently ON.
- Confirm the action in the confirm modal that opens (different copy depending on direction).
- See a success toast on completion; the page re-fetches the table afterwards.

## Settings & fields

### Status badge

| Element | What it shows |
|---------|---------------|
| **Badge** | ON / OFF indicator for the `translations_active` setting. |

### Toggle button + confirm modal — three modes

The page uses a single confirm modal whose title / message / OK-callback is set dynamically before opening. The same component is reused for the "Reset all" action — see [[settings-translations-reset]] for mode 3.

**Mode 1: Enable system labels** (when `translations_active === 'no'`)

| Element | Content |
|---------|---------|
| **Title** | *"Enable system labels"* |
| **Message** | *"All of your translated labels are going to be visible on your store, after disabling the system ones"* |
| **Confirm** | *"OK"* (primary). Calls the switch endpoint with `state=yes`. |

The message phrasing is slightly counter-intuitive — the "system ones" being disabled refers to the platform defaults; "your translated labels" refers to the merchant's overrides about to become active. The Assistant should clarify this for confused merchants.

**Mode 2: Disable system labels** (when `translations_active === 'yes'`)

| Element | Content |
|---------|---------|
| **Title** | *"Disable system labels"* |
| **Message** | *"All system labels are going to be visible on your store. Are you sure you want to proceed?"* |
| **Confirm** | *"OK"* (primary). Calls the switch endpoint with `state=no`. |

In both modes the modal shows a loader spinner on the confirm button while the mutation is in flight. On success, the modal closes, the table re-fetches, and a success toast fires.

## Business rules

### The toggle preserves overrides — it never deletes them

When the merchant flips system labels to OFF (`translations_active=no`), the platform stops reading custom translations and shows defaults everywhere on the storefront. The merchant's custom values are **NOT deleted** — they stay in the database and reappear the moment the toggle is flipped back ON. Useful as a quick "show me what the original storefront looks like" diagnostic without losing accumulated customisation work.

### "System labels = active" means MERCHANT translations apply (counter-intuitive naming)

The label "Enable system labels" can read backwards. The setting is the storefront-translation override system; turning it ON activates the merchant's overrides. Turning it OFF means the platform's shipped (system) defaults take over. Merchants who read "Disable system labels" as "stop showing standard CloudCart text" are correct in effect — the standard text gets replaced by their custom text once the override system is active.

### Toggle effect is immediate after cache flush

The switch endpoint flushes the translation cache so the storefront sees the new state on the next request. If a CDN sits in front of the storefront, the merchant may still see the old wording briefly until the CDN cache for that page expires. See [[settings-translations-side-effects]] for the cache flow.

### No partial toggle — site-wide all-or-nothing

The toggle operates at site level. There is no per-language or per-theme switch. When ON, every override across every `(locale, theme)` combination for the site is applied; when OFF, all are bypassed simultaneously.

### Storefront-only — admin labels have their own (separate) toggle

This switch controls only the **storefront** translation override system. The admin panel uses a separate toggle (managed by a different endpoint) that is **not** exposed in this Settings → Translations screen. See [[settings-translations-permissions]] for the storefront-vs-admin split.

## Related

- [[settings-translations]] — hub.
- [[settings-translations-reset]] — reuses the same confirm-modal component for "Reset all to default".
- [[settings-translations-side-effects]] — the cache flush + Artisan command chain triggered by the toggle.
- [[settings-translations-scoping]] — what gets applied when the toggle is ON (locale × theme).
- [[settings-translations-permissions]] — the storefront-vs-admin scope distinction.
- [[settings-general]] — Storefront Language picker; a separate switch from this one.

## Open questions

None.
