---
type: feature
nav_path: "Settings → Store settings → Security"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Admin security key", "Security key rotation", "sessionKeyGuard", "Force admin logout", "Crypt session key", "Сесиен ключ", "Принудителен изход на администраторите"]
tags: [settings, general, security, admin-sessions, session-rotation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-general]]. See the hub for related aspects (store details, locale, language, maintenance, product badges, operational toggles, industry multi-select).

# Store settings — Security (admin security key)

## Purpose

The Security box exposes a single action — rotate the **admin security key** (`sessionKeyGuard`). Rotating it invalidates **all currently signed-in Administrators and Moderators** on their next request by changing the session cookie name pattern the server expects. Customer sessions are unaffected.

It is the merchant's nuclear option for revoking admin access without touching individual Staff records: useful when a Moderator's laptop is stolen, after a suspected credential leak, or as routine security rotation.

> The right-side info panel reads: *"Admin security key for crypt session — When modified, all administrators will be decomposed by the administrative panel"* (i.e., logged out).

Rendered by a dedicated `SettingsGeneralSecurity` component (the rotate button lives here, separate from the main form).

## Where to find it

Sidebar → Settings → **Store settings** → Security box (sits under the shared "Security and maintenance" header alongside [[settings-general-maintenance]]).

## What the merchant can do here

- Rotate the admin security key — a single button that generates a new value and saves it.
- See a confirmation that the key was changed.

That's it. There is no field to manually enter a value, no schedule, no preview, and no per-user variant.

## Settings & fields

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Rotate admin security key** (button → writes `sessionKeyGuard`) | Generates a new random value, persists it as `sessionKeyGuard`, and triggers session invalidation on every active admin's next request. | Single button. Confirmation toast on success. |

The underlying value (`sessionKeyGuard`) is a setting key, not a column on the Site record.

## Business rules

### Rotating the admin security key invalidates all admin sessions immediately

CloudCart's custom session guard uses `sha1(sessionKeyGuard)` as part of the admin session cookie name AND the "remember me" cookie name (in the `site` and `sitecp` namespaces). When the key changes:

- All currently signed-in Administrators and Moderators are logged out on their next request (their cookies no longer match the expected name).
- Persistent "remember me" tokens are also invalidated.
- **Customer sessions are NOT affected** — this is admin-only. Customers stay logged in to their accounts.
- Effectively **one-way**: the merchant can set the key back to the old value, but sessions invalidated in the meantime stay dead (the cookies were already discarded by the browser or rejected by the server).

Useful for:

- Revoking access if a Moderator's machine is stolen.
- Suspected credential leak.
- Routine security rotation (e.g., quarterly).
- Forcing all staff to re-authenticate after a permission policy change.

### The merchant rotating the key also logs THEMSELVES out

The Administrator who clicks the rotate button is included in the "all admins logged out" effect — their next request will fail authentication and bounce to the login screen. So the rotate action is a self-inflicted logout in addition to a force-logout of everyone else. Practical impact: the merchant should be ready to log back in immediately after rotating.

### Distinct from `settings-staff`'s Force sign-out button

This is a separate mechanism from the per-store [[settings-staff]] **Force sign out** action. Both achieve the same end-result for admin sessions, but the mechanisms differ:

- **`sessionKeyGuard` rotation (this box)** — invalidates sessions by changing the cookie name pattern. Cookies stay valid until they expire on the client; the server simply stops recognizing them.
- **[[settings-staff]] Force sign out** — actively deletes the session records server-side (more audit-friendly because the act is recorded against the admin user).

For an immediate, audit-friendly mass logout the Force sign out button on [[settings-staff]] is the better tool. The `sessionKeyGuard` rotation is the right tool when the goal is to ALSO invalidate "remember me" tokens that might have been exfiltrated.

### No plan-gating

This box is not gated by any plan-feature. Every active merchant can rotate the key.

### No confirmation modal

Clicking the rotate button writes the new value immediately. There is no "are you sure?" prompt — the action is meant to be one-click for emergency use. This is by design but worth noting if a merchant clicks it accidentally.

## Related

- [[settings-general]] — hub.
- [[settings-staff]] — sibling mechanism: the **Force sign out** button there deletes session records server-side (audit-friendly), whereas this box invalidates cookies by rotation.
- [[merchant-roles]] — Administrator vs Moderator (both are affected by rotation; customers are not).
- [[settings-general-maintenance]] — sibling box under the same "Security and maintenance" header.

## Open questions

None.
