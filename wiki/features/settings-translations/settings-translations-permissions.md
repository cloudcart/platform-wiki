---
type: feature
nav_path: "Settings → Translations → Permissions & scope"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["Translations permissions", "store.translations permission", "Storefront vs admin labels", "admin_translations", "Translation scope (UI surface)"]
tags: [settings, translations, i18n, permissions, scope]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-translations]]. See the hub for related aspects (toggle, table, filters, reset, scoping, side-effects).

# Translations — permissions & UI scope

## Purpose

Two related-but-different boundaries govern what [[settings-translations]] can and cannot do: a **permission gate** (who can access the page) and a **UI surface scope** (what part of CloudCart the page actually translates). Both surface frequently in support — the page is gated by the `store.translations` permission, and merchants regularly ask "I translated 'Order' here but my admin sidebar still says 'Order'". The answer to the second question is that the screen is **storefront-only**; admin-panel labels use a separate system with no merchant UI.

## Where to find it

Sidebar → Settings → **Translations**. The permission grant is managed from [[settings-staff]].

## What the merchant can do here

- Visit and edit the Translations page IF they hold either the broad **Settings** permission OR the specific **Translations** (`store.translations`) grant.
- Customise storefront-facing labels only (customer-visible UI on the customer storefront).

What the merchant CANNOT do here:

- Edit admin-panel labels (sidebar, modal titles, button text inside the admin) — these use a separate system not exposed in this page.
- Edit invoice template strings — see [[settings-invoicing]].
- Edit admin-notification email subjects — those use [[settings-admin-notifications]] templates.
- Edit order / shipping / payment status labels — those are renamed on [[settings-statuses]] with their own override mechanic.

## Settings & fields

### Permission gate

| Property | Value |
|----------|-------|
| **Permission key** | `store.translations` |
| **Permission group** | `settings` |
| **Granted from** | [[settings-staff]] → role / member permissions |
| **Owners** | Always pass (bypass the permission check). |
| **Moderators** | Need either broad **Settings** OR specific **Translations** (`store.translations`) grant. |

The Translations route group is gated by the standard permission middleware. Moderators without the grant get a 403 / "not authorised" response when trying to view or modify translations.

### UI surface affected by this page

| Surface | Translatable here? | Where to manage instead |
|---------|--------------------|--------------------------|
| **Storefront customer-facing labels** (buttons, validation, headings, email subjects sent to customers) | YES | This page. |
| **Admin-panel labels** (sidebar, buttons, modal titles inside the admin) | NO | Admin Panel Language picker in [[settings-general]] only — no per-row edit UI. |
| **Order / shipping / payment status labels** | NO | [[settings-statuses]] — separate override mechanic. |
| **Invoice template strings** | NO | [[settings-invoicing]] — separate templating system. |
| **Admin notification email subjects** | NO | [[settings-admin-notifications]] — template strings managed there. |

## Business rules

### Owners bypass permission; moderators need the grant

Permission resolution follows the standard moderator-permission pattern: the owner always passes, while a moderator passes only if they hold either broad **Settings** or specific **Translations**. The grant is added from [[settings-staff]] under the member's role configuration.

This makes Translations one of the screens where a merchant can safely delegate "make our store sound natural in Bulgarian" to a non-owner staff member without granting them other Settings access.

### Storefront-only — admin labels are a SEPARATE system

This page only manages **storefront** translations. The admin panel uses a separate `admin_translations` setting controlled by a different endpoint that is **NOT exposed** in this Settings → Translations screen. A merchant who wants to rename "Order" everywhere — both customer-facing and admin-facing — has to:

1. Use this page for the storefront.
2. Live with the platform's admin labels in whatever language the merchant selected via the Admin Panel Language picker in [[settings-general]].

There is **no merchant-accessible UI** for editing admin labels per row. The Assistant should set this expectation clearly when a merchant reports "I translated this label but my admin sidebar didn't change".

### No CSV export / import, no audit trail, no version history

There is no bulk CSV export or import path for translations. A merchant translating into many languages must override one row at a time per `(locale, theme)` combination (see [[settings-translations-scoping]]). Likewise, there is no audit trail of who changed which translation when — overrides are written in place, and the previous value is not retained. A row that gets corrupted (e.g., copy-paste error) cannot be rolled back from the UI.

### `store.translations` does NOT include `settings.general` access

The permission gate is narrow. Holding `store.translations` lets the moderator edit translation rows; it does NOT let them change the Storefront Language or Admin Panel Language in [[settings-general]]. A moderator whose role only grants `store.translations` is limited to overriding strings in the current `(locale, theme)` — they cannot switch languages to translate a different one without an additional permission grant.

### No plan gate — the page is available on every plan

The page does not have a plan-tier gate. Every merchant on every CloudCart plan can use Translations. (Multi-language storefronts may have their own plan gates governed by [[settings-general]], but the override mechanic itself is universal.)

### Status labels are NOT translatable from this page

The merchant-facing order / shipping / payment status names (e.g., "Pending", "Paid", "Shipped") have their own override UI on [[settings-statuses]]. They do not appear as translation keys on this Translations page. Merchants asking "where do I rename Pending to Чакаща?" should be directed to [[settings-statuses]], not here.

### Invoice text + admin notification subjects are SEPARATE systems

[[settings-invoicing]] manages invoice template strings (customer-facing PDF / printed invoices). [[settings-admin-notifications]] manages admin notification email subjects. Neither is affected by edits on this Translations page; the Assistant should redirect merchants to the correct screen for those surfaces.

## Related

- [[settings-translations]] — hub.
- [[settings-translations-scoping]] — `(locale, theme)` dimensions the permission gate operates within.
- [[settings-translations-toggle]] — the master switch controlled by the same permission.
- [[settings-staff]] — where `store.translations` is granted.
- [[settings-general]] — Storefront Language and Admin Panel Language pickers; the only "translation" of the admin panel available to merchants.
- [[settings-statuses]] — order / shipping / payment status label overrides (separate mechanic).
- [[settings-invoicing]] — invoice template strings (separate system).
- [[settings-admin-notifications]] — admin notification email subjects (separate templates).

## Open questions

None.
