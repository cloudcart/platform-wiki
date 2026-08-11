---
type: feature
nav_path: "Settings → Cart and checkout → Marketing and consent"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Marketing checkbox", "I accept marketing", "hide_marketing", "Terms of Service page", "checkout_terms_page", "Additional consent pages", "checkout_other_pages", "GDPR app off", "SettingsCartPages"]
tags: [settings, cart, checkout, marketing, gdpr, consent, terms-of-service]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, abandoned reminder, payment/shipping defaults, limits, checkout fields, UI behavior, Google Maps).

# Cart and checkout — Marketing and consent

## Purpose

The box on the Cart and checkout page that controls the **storefront consent UI** at checkout — specifically the "I accept marketing" checkbox, the Terms of Service page link, and a list of additional consent pages (privacy policy, returns policy, etc.). This entire box is **only visible when CloudCart's GDPR app is NOT installed**. When the GDPR app is active, it provides its own consent UI and overrides everything in this box, so the screen hides it.

## Where to find it

Sidebar → Settings → **Cart and checkout** → box **Marketing and Terms of service** (`marketing`).

This is the **eleventh** box on the page, appearing only when CloudCart's GDPR app is NOT installed. With the GDPR app active, the box is hidden entirely — see the "GDPR app overrides this box" rule below.

## What the merchant can do here

- Toggle whether the "I accept marketing" checkbox appears at checkout.
- Pick a CMS page (from the store's pages) to act as the Terms of Service link.
- Add a list of additional consent pages (privacy policy, returns policy, etc.) shown alongside the Terms of Service link at checkout.

## Settings & fields

### Box: Marketing and Terms of service (`marketing`) — only when GDPR app is OFF

This entire box is hidden when CloudCart's GDPR app is installed and active — consent is handled by the GDPR app instead.

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Show "I accept marketing" checkbox** (`hide_marketing`) | Switch with inverted semantics: ON = checkbox IS shown at checkout. | Useful for marketing newsletter consent. |
| **Choose the static page which contents your Terms of Service** (`checkout_terms_page`) | Pick a CMS page that the "I agree to terms" checkbox links to. | Options come from the store's `Page` model. |
| **(embedded component) Additional consent pages** | A custom Vue component (`SettingsCartPages`) lets the merchant add multiple additional consent links (privacy policy, etc.) shown at checkout. | Saved into `checkout_other_pages` as a JSON array. The backend stores it as JSON. |

### "Additional consent pages" sub-module — UI shape (verified)

The marketing box embeds a small two-state module (`SettingsCartPages`):

1. **Empty state** — a centered text link *"+ Add page"* (purple, with plus-circle icon).
2. **Active state** — clicking *"+ Add page"* slides up the link and slides in a tags-mode multi-select dropdown labelled *"Additional pages"*. Options come from `meta.policies` (the merchant's CMS pages). The merchant can pick one or more pages.
3. Clearing all chosen pages slides the dropdown back down and re-shows the *"+ Add page"* link — the UI gracefully toggles between the two states based on whether `checkout_other_pages` has entries.

Both transitions use `Vue3SlideUpDown` with **180 ms** duration. The selected pages persist into the `checkout_other_pages` array; if the merchant clears all selections, the field is dropped from the save payload (kept blank in storage).

## Business rules

### GDPR app overrides this entire box

When the GDPR app is installed and active, the **Marketing and Terms of service** box is hidden from the Cart and checkout page entirely — that app provides its own consent UI (with finer-grained controls and audit logging). If the merchant uninstalls the GDPR app, the box reappears on next page load and the previously-saved settings (if any) take effect again.

So the merchant has two mutually-exclusive paths:

1. **GDPR app installed** — consent UI is handled by the GDPR app. This box is invisible.
2. **GDPR app NOT installed** — consent UI is handled by this box. The merchant configures the marketing checkbox + Terms of Service page + additional consent pages here.

### `hide_marketing` is inverted

The switch uses `trueValue: false, falseValue: true` — UI ON ("Show marketing checkbox") stores literal `false` in `hide_marketing`. A support agent looking at a raw API dump should mentally invert this key before reasoning about merchant intent. See the hub [[settings-cart]] for the cross-cutting list of inverted switches.

### `checkout_other_pages` is empty-array-dropped on save

The save handler drops `checkout_other_pages` from the payload entirely if the merchant has no consent pages selected (rather than sending `[]`). Practical effect: the stored value stays blank in storage rather than being explicitly set to an empty array. This keeps the storage clean for stores not using additional consent pages. See the hub [[settings-cart]] for the general save-handler rules.

### `meta.policies` source

The dropdown options for both Terms of Service (`checkout_terms_page`) and the additional consent pages multi-select come from `meta.policies` — the merchant's CMS Pages collection. The merchant creates the pages first in the CMS (Sidebar → Web pages → Pages or equivalent) and then picks them here. Pages deleted from the CMS after being selected here remain referenced in the setting but render as broken links on the storefront — the merchant should re-save this box after deleting referenced pages.

### Marketing consent vs newsletter subscribers

The "I accept marketing" checkbox at checkout is a **consent flag stored on the order**, separate from the newsletter-subscribers list. Customers who tick the checkbox at checkout are added to the marketing-eligible list (the mechanism depends on which marketing app the merchant has installed). Without the GDPR app, the merchant should ensure the marketing checkbox text and Terms of Service page satisfy local consent regulations (GDPR, ePrivacy, etc.) — CloudCart provides the UI but not legal compliance.

### Terms of Service link interaction with the checkout submit button

The Terms of Service checkbox at checkout typically gates the submit button — the customer cannot complete the order until it's ticked. The exact gating logic is implemented at the storefront-checkout level (not in this settings page). The merchant should test that the chosen page renders correctly and that the link works.

## Related

- [[settings-cart]] — hub.
- [[apps-gdpr-overview]] — the GDPR app whose presence overrides this entire box.
- [[apps-gdpr-settings]] — sibling GDPR-app configuration that replaces this box when the app is active.
- [[apps-gdpr-acceptance]] — the consent-recording behaviour that the GDPR app uses instead of `checkout_other_pages`.
- [[checkout-flow]] — end-to-end checkout sequence; the marketing checkbox + Terms of Service link appear at the final submit step.
- [[order]] — the order entity that stores the consent flag.
- [[marketing-subscribers]] — marketing-subscribers list that customers join via the checkbox.

## Open questions

_None._
