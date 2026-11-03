---
type: feature
nav_path: "Settings → Notifications to administrators → Permissions & locale"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["Admin notifications permission", "settings.general permission scope", "Locale-filtered notifications table", "Why is my notifications list shorter", "Who can manage admin notifications"]
tags: [settings, notifications, permissions, i18n]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-admin-notifications]]. See the hub for the other aspects (master switch, per-type toggles, mandatory three, recipient routing, delivery queue, alert triggers).

# Admin notifications — permissions and locale

## Purpose

Two cross-cutting rules govern who can access [[settings-admin-notifications]] and what the notifications table shows:

- **Permission gate** — the page is gated by the same `settings.general` permission scope that gates [[settings-general]]. There is no dedicated "admin notifications" permission. A moderator with General-settings access can also flip admin notification toggles, and vice versa.
- **Locale filter** — the table only shows notifications that have a language record in the admin panel's currently selected language. Switching to a less-translated language can cause some rows to disappear.

## Where to find it

Neither rule has its own UI on the [[settings-admin-notifications]] page — they're observable behaviours rather than configurable settings:

- The permission gate is checked at page load. A user without `settings.general` access either doesn't see the navigation entry or gets redirected on direct URL access.
- The locale filter applies to the table render — rows are dropped silently with no "X rows hidden due to locale" indicator.

The permission itself is granted on [[settings-staff]] when configuring a Moderator account. The admin panel language is set per-user on the admin's own profile menu.

## What the merchant can do here

- Grant or revoke `settings.general` access for moderators on [[settings-staff]] — this also grants/revokes their ability to flip admin notification toggles.
- Change the admin panel language (per-user) and observe whether the rows in the notifications table are affected.

The merchant cannot:

- Grant `settings.admin-notifications` as a standalone permission. No such permission exists. The bundling with `settings.general` is hard-coded.
- See or override which translations are missing for which languages from this page. (The translation set is a CloudCart-managed concern.)

## Settings & fields

| Aspect | Where it's configured | What it does |
|--------|----------------------|--------------|
| **`settings.general` permission scope** | [[settings-staff]] → Edit moderator → Permissions | Grants the moderator access to BOTH [[settings-general]] and [[settings-admin-notifications]]. Cannot be split. |
| **Admin panel language** | Per-user, in the admin profile dropdown | Determines which notification rows appear in the table (rows without a translation in this language are hidden). |

## Modals and sub-flows

None on this page.

## Business rules

### Permission gate uses `settings.general`, NOT a dedicated permission (verify)

The admin notifications page is gated by the `settings,settings.general` permission scope — the SAME permission that gates the [[settings-general]] page. A moderator who has been granted "General settings" access on [[settings-staff]] can ALSO turn admin notification toggles on/off. There is no separate "admin notifications" permission. Practical effect: there's no way to grant a moderator the ability to manage General settings without also letting them silence admin alerts (or vice versa) — the two are bundled.

Operational guidance:

- If the merchant wants to lock down admin notifications (e.g., to ensure no moderator can silence low-stock alerts), the only option is to revoke `settings.general` for that moderator. That also locks them out of General settings — which may not be what the merchant intends.
- If the merchant trusts a moderator to manage General settings, they're also trusting them with the admin notification toggles by transitivity.
- The Administrator role has all permissions and can always access this page.

### Locale filter — rows without a translation in the current language are hidden

The Vue table only shows notifications that have a language record in the admin panel's currently selected language. If the admin panel language is changed to a locale that doesn't have translations for all 17 notification templates, some rows will be missing from the table.

This is uncommon — CloudCart ships translations for the major admin-panel languages — but explains why the list could appear shorter for less-common admin panel languages. Practical guidance:

- If a merchant reports "I'm missing rows in the notifications table", first check the admin panel language. Switching back to Bulgarian or English typically restores the full set.
- A row hidden by the locale filter still **functions** in dispatch — the underlying `mail_<label>` setting is still honored. The hide is purely cosmetic at the table render level.

### Per-store install can add rows (the hidden 18th)

Independent of locale: the table can include an 18th row (`product_review_added`) when the Product Reviews app is installed for the store. So row count = base set ∩ available-translations + per-store-app rows. See [[admin-notifications-per-type-toggles]].

### Sidebar entry is currently NOT shown

A separate side-effect of the permission / nav layer: the "Notifications to administrators" link is currently commented out of the Settings sidebar sub-menu. The page is live at its direct URL but isn't surfaced in the navigation tree. So even a user with `settings.general` access must navigate to `/admin/settings/admin-notifications` directly or be deep-linked there. This is a UX issue independent of the permission rule but discoverable in the same area of the system.

### No per-permission UI to inspect this

There is no admin screen that says "this page requires permission X". The permission requirement is a backend route guard. Merchants who want to confirm which moderator can do what must inspect each moderator's permission set on [[settings-staff]].

## Related

- [[settings-admin-notifications]] — hub.
- [[settings-staff]] — where moderator permissions are granted.
- [[settings-general]] — the other page gated by the same `settings.general` scope.
- [[merchant-roles]] — Administrator vs Moderator role distinction.
- [[admin-notifications-per-type-toggles]] — per-row visibility (locale + per-store-app considerations).

## Open questions

- The exact permission scope string is documented from May 2026 audit notes; the current production permission code should be confirmed against the route guard. `(verify)`
- Whether the sidebar entry will be re-enabled in a future release (vs intentionally hidden long-term) is currently unknown. `(verify)`
