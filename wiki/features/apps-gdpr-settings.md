---
type: feature
nav_path: "Apps → GDPR → Settings"
route_name: apps.gdpr.settings
route_path: /admin/apps/gdpr/settings
aliases: ["GDPR Settings", "GDPR config", "GDPR install settings"]
tags: [apps, gdpr, compliance, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 6
---
# GDPR → Settings

## Purpose

The **Settings** tab is the GDPR app's general configuration page — install-time setup (initial values entered when the app is first activated), and ongoing app-level options that don't belong to any of the specific tabs (Address / Cookies / Policy / Acceptance / Requests).

For the full GDPR feature set, see [[apps-gdpr-overview]].

## Where to find it

Sidebar → Apps → GDPR → **Settings tab**. Route: `/admin/apps/gdpr/settings`.

API endpoints:
- `GET /api/gdpr/settings/{form?}` — load settings (`form` parameter scopes to a specific section: address / cookies / cookies-consent / etc.).
- `POST /api/gdpr/settings/{form?}` — save settings.
- `GET /api/gdpr/install-settings` — load install-time settings (initial configuration wizard).
- `POST /api/gdpr/install-settings` — save install-time settings.
- `POST /api/gdpr/install` — execute install.
- `POST /api/gdpr/uninstall` — uninstall app.
- `GET /api/gdpr/active/{status?}` — toggle app active state.

## What the merchant can do here

### Install flow

When the merchant first installs GDPR, a wizard collects required configuration:
1. **Store address** ([[apps-gdpr-address]]) — legal entity details.
2. **Cookies** ([[apps-gdpr-cookies]]) — initial bar / wall + default cookie groups.
3. **Policy** ([[apps-gdpr-policy]]) — first Privacy Policy.
4. Confirm + activate.

### Ongoing settings adjustments

- General app behaviour (e.g., default consent state for new visitors).
- Email notification preferences for incoming Requests.
- Audit log retention preferences (verify).
- Storefront integration toggles (e.g., enforce consent before tracking scripts load).

### Uninstall

The merchant can uninstall the GDPR app via `POST /api/gdpr/uninstall`. However:
- Existing acceptance records persist (immutable audit).
- Cookie bar disappears from storefront.
- Pending Requests need to be handled BEFORE uninstall (verify warning).

### What the merchant CANNOT do here
- Uninstall while EU compliance is required and the storefront is still serving EU customers — would create immediate non-compliance.
- Skip the install wizard if it's required for compliance.

## Settings & fields

### Form-scoped settings (per `form` parameter)

The `{form}` parameter in the settings endpoint scopes the request to a specific section:
- `form=address` → store address (see [[apps-gdpr-address]]).
- `form=cookies` → cookie configuration (see [[apps-gdpr-cookies]]).
- `form=cookies-consent` → consent dialog text.
- (verify) other form names per tab.

This sectioned approach keeps the merchant's edits scoped — saving one section doesn't accidentally overwrite another. **Caveat:** when saving across ALL forms at once (no `form` parameter), the platform clears every policy mapping before re-creating from the submitted input. Always submit the complete mapping set when saving all forms — a partial submit loses data. Per-section saves and the all-forms save are atomic: if a save fails mid-way it rolls back entirely, so the merchant never ends up with a half-applied mapping set.

### Re-accept policies popup

- `show_policies_popup` — when ON, prompts existing logged-in customers to re-accept policies. The first time such a customer logs in with no acceptance record yet, the `policies_popup` cookie is set and the storefront surfaces the popup (see [[apps-gdpr-overview]]).
- `policies_popup_text` — the text shown in that popup.

### Active state toggle

`GET /api/gdpr/active/{status?}` flips the app's master active state. When inactive:
- Cookie bar / wall NOT shown.
- Acceptance log still readable (read-only).
- Requests still accessible.

This is a temporary pause mechanism, not a full uninstall.

## Business rules

### Install wizard enforces minimum config

The platform doesn't allow GDPR to activate without:
- Store address filled.
- At least one cookie group configured.
- At least one Privacy Policy active.

This is to prevent merchants from activating GDPR partially and shipping non-compliant.

### Uninstall warnings

Before uninstall, the platform should warn:
- Pending customer Requests remain unprocessed.
- The cookie bar will disappear.
- Tracking scripts may execute without consent (non-compliant for EU traffic).

Uninstall (`POST /api/gdpr/uninstall`) removes the app's active flag and stops the cookie bar from rendering, but it does NOT remove the acceptance log or customer Requests — those persist by design to preserve the audit trail across deactivation/reactivation. So if the merchant reinstalls later, old acceptance records are still there.

### Reinstall resets cookie groups + providers

Caveat to the above: reinstalling the GDPR app re-runs the seeder, which wipes cookie groups and per-cookie definitions before inserting the seed defaults. Any custom cookie groups or cookie definitions the merchant added are LOST and replaced with the 5 default groups. Acceptance log, customer Requests, and policies survive a reinstall; cookie definitions do not. Reinstall also recreates the 4 default policies (see [[apps-gdpr-policy]] for the seeded templates).

### Settings save regenerates storefront JS

Saving any settings — `POST /api/gdpr/settings/{form?}`, the cookie-bar / cookie-consent / cookie-group endpoints, or the active toggle (`GET /api/gdpr/active/{status}`) — rebuilds the storefront JavaScript bundle so the new consent / policy configuration takes effect on the next storefront page load.

### Per-storefront settings (NOT shared across stores)

All GDPR settings (cookie groups, policy mappings, address, popup text, acceptance log) are stored per storefront. **Multi-storefront merchants configure GDPR independently for each store** — editing cookie groups on Store A does NOT mirror to Store B, and the active toggle is per store with no global switch. Same per-site model as [[apps-gdpr-address]].

### No export / import, no compliance presets

- There is no settings export or import — the merchant cannot download their GDPR configuration as a file for backup or to replicate to another store. To replicate, recreate it manually in each store, or reinstall the app on the target store (which recreates the 4 default policies + 5 default cookie groups from scratch with default text).
- The app ships ONE set of defaults. **There is no "GDPR strict" / "CCPA mode" / "UK GDPR" preset toggle.** The seeded text is GDPR-oriented (references EU Regulation 2016/679); merchants in a non-EU jurisdiction (California CCPA, Brazil LGPD, etc.) must manually rewrite the policy text and adjust cookie group defaults.

### Out-of-date version warning

If the merchant's GDPR app subscription is expired or doesn't include updates, the Settings screen shows an `upgradeMessage` warning that the app version is out of date.

### Permission
Standard apps permission scope.

## Related

- [[apps-gdpr-overview]] — GDPR hub.
- [[apps-gdpr-address]] — store address sub-page.
- [[apps-gdpr-cookies]] — cookies sub-page.
- [[apps-gdpr-policy]] — policies sub-page.
- [[apps-gdpr-acceptance]] — acceptance log.
- [[apps-gdpr-requests]] — customer requests.

## Open questions

