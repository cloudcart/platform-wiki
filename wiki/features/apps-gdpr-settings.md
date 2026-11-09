---
type: feature
nav_path: "Apps → GDPR → Consent sections"
route_name: apps.gdpr.settings
route_path: /admin/apps/gdpr/settings
aliases: ["GDPR Settings", "Consent sections", "GDPR config", "GDPR install settings", "Policy at checkout", "Completing an order", "Закачане на политика към чекаута", "GDPR uninstall reinstall", "GDPR app expired", "Age confirmation checkbox", "18+ потвърждение"]
tags: [apps, gdpr, compliance, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-11-09
source_count: 7
---
# GDPR → Consent sections (Settings)

## Purpose

The **Consent sections** tab (route `apps.gdpr.settings`) decides which policies each storefront form asks the customer to accept, and whether each is required. It is where a policy is attached to the checkout. For the whole app, see [[apps-gdpr-overview]].

## Where to find it

Sidebar → Apps → GDPR → **Consent sections** tab, `/admin/apps/gdpr/settings`. The tab and box names here are the admin's English labels; its Bulgarian labels are kept in the admin's translations, not in the code.

## What the merchant can do here

One box per storefront form:

| Box | Form on the storefront |
|---|---|
| **Completing an order** | The checkout, and the fast-order panel. |
| **User Registration** | The registration form. |
| **Contact Form** | The contact form. |
| **Subscribers - subscription forms** | Subscription forms and popups. |
| **Request for consent for registered users after login** | The re-acceptance popup; this box also has its on/off switch and text. |

In each box: pick a policy in the dropdown (any page on the **Policies** tab), tick **Required** or leave it unticked for optional, remove a row, or **Add policy** for another row. The box summary lists the attached policies with a **Required** or **Optional** badge.

### What the customer sees

Each attached, active policy is one checkbox reading **I accept** / **Приемам** followed by the policy's name, which links to the policy page. The words before the name are fixed; the merchant controls only the policy's name. There is no free-text consent line. A required box must be ticked or the form, the order included, is not submitted; optional ones come first. Details: [[apps-gdpr-policy-forms]].

### An age confirmation

The platform has no age check: no age gate, no date-of-birth check, no such app. The only native way to ask for a confirmation is a page such as "I confirm I am 18 or older" attached as **Required** to **Completing an order** (and **User Registration**). The customer must tick it and the acceptance is logged; nothing is verified.

## Settings & fields

### Saving a box

Saving one box replaces only that form's attachments. A save without a form named replaces every attachment, so it must carry the complete set. A failed save rolls back.

### Re-accept policies popup

- `show_policies_popup` — when ON, a signed-in customer without an acceptance record is asked to accept the box's policies after signing in, or to sign out (see [[apps-gdpr-overview-consent-logging]]).
- `policies_popup_text` — the popup's text.

## Business rules

### When the app is switched off or lapses

Switched off (**Disable**), or unpaid, the storefront treats the app as absent at once:

- no cookie bar, wall or dialog, and no consent check: the built-in tracking apps run unchecked ([[apps-gdpr-overview-script-gating]]);
- no GDPR checkboxes on the checkout, registration, contact and subscription forms, and no re-acceptance popup;
- the native **Marketing and Terms of service** box of Settings → Cart and checkout takes over again, with what was saved in it ([[settings-cart-marketing-consent]]).

An unpaid app is then marked not installed by the unpaid-apps check, with an Important alert. Nothing is deleted. The policies are ordinary store pages, so they stay published either way.

### Uninstall and reinstall

- **Uninstall** deletes the app's settings: the bar or wall choice and texts, the cookie policy page, the re-acceptance popup and its text, and which policy is the marketing policy. It keeps the cookie groups and cookie entries, the policy attachments, the acceptance log, the requests and the policy pages.
- **Reinstall**, after an uninstall or a lapse, brings the kept data back as it was. Nothing is re-seeded: the starter policies and groups are created only on the very first install ([[apps-gdpr-policy-seeding]]). The bar mode, the bar and consent texts and the cookie policy page return to the install defaults; after an uninstall the marketing policy must be designated again ([[apps-gdpr-policy-editor]]).
- A reinstall, by hand or by a late payment after the app was marked not installed, leaves the app **switched off**: nothing shows on the storefront until the merchant presses **Enable**. A payment made before that mark simply keeps the app as it was.

### Settings save regenerates storefront JS

Saving any GDPR settings, or switching the app on or off, rebuilds the storefront's apps file: signed-in visitors see it on the next page load, guests within up to 20 minutes (cached page copy, [[storefront-arch-caching-invalidation]]).

### Per-storefront settings (NOT shared across stores)

All GDPR settings are per store. **Multi-storefront merchants configure GDPR independently for each store**; the switch is per store. There is no settings export or import, and no "CCPA" or "UK GDPR" preset: the seeded texts are GDPR-oriented.

### Out-of-date version warning

On a one-time purchase without updates, the screen shows a warning that the app version does not include updates ([[apps-gdpr-cookies-consent-mode]]).

### Permission

Standard apps permission scope.

## Related

- [[apps-gdpr-overview]] — GDPR hub.
- [[apps-gdpr-address]] — store address sub-page.
- [[apps-gdpr-cookies]] — cookies sub-page.
- [[apps-gdpr-policy]] — policies sub-page.
- [[apps-gdpr-acceptance]] — acceptance log.
- [[apps-gdpr-requests]] — customer requests.
- [[apps-gdpr-policy-forms]] — how attached policies render and record.
- [[settings-cart-marketing-consent]] — the native box used while the app is off.

## Open questions

None.
