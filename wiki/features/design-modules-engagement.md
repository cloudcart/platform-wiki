---
type: feature
nav_path: "Design → Modules → Engagement"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Engagement modules", "Contact modules", "Newsletter module", "Mailchimp module", "Google Map module", "Contact information module", "Product review module", "Embedded form module", "Контактна форма", "Контакти", "Карта", "Бюлетин", "Ревюта"]
tags: [design, modules, engagement, contact, newsletter, reviews]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# Storefront Engagement Modules

## Purpose

The **engagement modules** are how the merchant **captures intent and stays in touch with shoppers** from the storefront: the contact form on the Contacts page, the contact-information block around it, the Google Map showing physical locations, the Mailchimp newsletter pop-up, the visual-builder subscribe forms embedded via the `cc_form` page-builder block, the product-review showcase rows, and the request-review CTA block.

They live across two tabs in the [[design-modules]] screen — **Contacts** (for `contactForm`, `contactInformation`, `googleMap`) and **User** (for `newsletter`) — plus the page-builder palette (for `cc_form`, `product_review`, `request_review`). The module catalogue is controlled by the **active theme** ([[design-themes]]) — switching themes can change which engagement-module instances appear or how they render. The module TYPES below are platform-wide.

This hub catalogues each engagement module; per-module detail pages live as siblings under this cluster.

## Where to find it

Sidebar → **Design** → **Modules**:

- **Contacts** tab — `contactInformation`, `googleMap` (and the implicit `contactForm` slot, which has no editable card).
- **User** tab — `newsletter` (Mailchimp pop-up).
- **Page-builder** (via [[marketing-landing-pages]] when editing a Dynamic page) — `cc_form`, `product_review`, `request_review` blocks.

Each card opens an edit panel with three buttons at the top: **Save module**, **Reset module** (confirmation: *"Are you sure you want to reset this module?"*), and **Cancel**. Saves regenerate the storefront cache automatically. Success messages: *"Module successfully edited"* / *"Module successfully reset"*.

## What the merchant can do here

On the Contacts and User tabs the merchant configures the storefront's customer-engagement surfaces — the **Contacts page** form + information + Google map, the **newsletter** pop-up that captures email subscribers via Mailchimp, and the page-builder blocks that embed custom subscribe forms and product-review showcases. Each module is configured independently per instance, save / reset is per-module, and the storefront cache refreshes automatically on save.

## Settings & fields

Each engagement module has its own detailed Settings & fields table on its per-module page (linked below). The hub catalogues which module covers what.

## Sub-pages (in this cluster)

- [[design-module-contact-form]] — render slot for the storefront `/contacts` form; has NO edit panel (recipient + GDPR live in [[settings-general]]).
- [[design-module-contact-information]] — prose + address block on `/contacts`; controls whether the contact form is visible.
- [[design-module-contact-google-map]] — Google Map embed with pin set, zoom, map type, and UI controls.
- [[design-module-newsletter]] — Mailchimp-backed newsletter pop-up + inline footer form; gated by [[apps-mailchimp]].
- [[design-module-cc-form]] — page-builder block that embeds a pre-built subscribe form from [[marketing-subscribers-subscribe-forms]].
- [[design-module-product-review]] — page-builder block showing a row / carousel of collected reviews; gated by [[apps-product-review]].
- [[design-module-request-review]] — page-builder block asking the logged-in customer to leave reviews on past purchases; gated by [[apps-product-review]].

## Module catalog (at a glance)

| Module | Tab | Type (map) | Configurable | Gating |
|--------|-----|------------|--------------|--------|
| `contactForm` | Contacts (implicit) | `contact.form` | No (system module; no edit panel) | None |
| `contactInformation` | Contacts | `contact.information` | Yes — `show_form`, `show_custom_information`, `page_text`, `custom_information` | None |
| `googleMap` | Contacts | `contact.googleMap` | Yes — pins, zoom, map controls | Platform Google key (custom optional) |
| `newsletter` | User | `mailchimp.newsletter` | Yes — `form`, `automatic`, `delay`, `status`, `title`, `description` | [[apps-mailchimp]] must be configured |
| `cc_form` | Page-builder | `extra.cc_form` | Yes — `form_id` | At least one form in [[marketing-subscribers-subscribe-forms]] + `subscriber_forms` plan feature |
| `product_review` | Page-builder | `extra.product_review` | Yes — 14 fields (filters, layout) | [[apps-product-review]] installed + enabled |
| `request_review` | Page-builder | `extra.request_review` | Yes — `title`, `description`, `color`, `enable_slider`, `per_row` | [[apps-product-review]] installed + enabled + customer logged in |

## Business rules

### Reset module

Clicking **Reset module** wipes the merchant's saved settings for THAT instance and restores the theme's shipped defaults. Confirmation prompt: *"Are you sure you want to reset this module?"*. Success message: *"Module successfully reset"*. There is no undo — for the `googleMap` module in particular, reset wipes ALL configured pins.

### Cache invalidation

Both **Save** and **Reset** regenerate the storefront cache for the site. The merchant doesn't need to manually clear cache — the next storefront request sees the new settings.

### Plan gating & app dependencies

| Module | Requirement |
|--------|-------------|
| `newsletter` | Plan-free, but requires the Mailchimp app ([[apps-mailchimp]]) installed and configured. Without it, the panel shows *"Configure app first"*. |
| `cc_form` | At least one form in [[marketing-subscribers-subscribe-forms]] + the `subscriber_forms` plan feature. |
| `product_review` / `request_review` | The [[apps-product-review]] app installed and active; the app's own plan-gating applies. |
| `googleMap` | Platform-provided Maps embed key — no merchant setup unless they want a custom key. |
| `contactForm` / `contactInformation` | No app required; uses platform-built-in contact email routing. |

### Localization

Module text fields are stored as a single string per instance — NOT per-language by default. For multi-language storefronts, the merchant needs the multi-language app to enter per-language copy — see [[multi-language]].

### Behavior worth knowing

- **Mailchimp uninstall** hides the `newsletter` edit panel, but saved settings are preserved — re-installing restores access.
- **Product Review modules** appear or disappear dynamically depending on whether the app is installed and enabled.
- **Contact email recipient** is store-wide (`site_email` in [[settings-general]]) — there is no per-module recipient override.
- **`cc_form`** references a form ID from [[marketing-subscribers-subscribe-forms]] — deleting that form leaves the module pointing at a missing ID.
- **Settings are keyed by instance name** — switching themes orphans the saved settings for instances the new theme doesn't ship; switching back re-exposes them.

## Related

- [[design-modules]] — parent module editor (lists ALL modules and the full module-type catalogue).
- [[design-modules-products]] — sibling category page (product detail, related, showcase, last viewed, bundles).
- [[design-modules-navigation]] — sibling category page (header / footer / menu / navigation links).
- [[design-modules-content]] — sibling category page (text, banner, carousel, slider).
- [[design-modules-utility]] — sibling category page (filters, social icons, footer text, layout).
- [[design-themes]] — theme picker that controls which engagement-module instances appear on this screen.
- [[design]] — parent Design pillar.
- [[apps-mailchimp]] — Mailchimp integration; powers the `newsletter` pop-up.
- [[marketing-subscribers-subscribe-forms]] — visual-builder subscribe forms surfaced via `cc_form`.
- [[apps-product-review]] — Product Review app; powers `product_review` and `request_review`.
- [[apps-store-locations]] — multi-store data overlay for `googleMap`.
- [[marketing-landing-pages]] — Dynamic pages use the page-builder, which exposes `cc_form`, `product_review`, and `request_review` blocks.
- [[settings-general]] — store-information settings (address, contact-email recipient) used as defaults by `contactInformation` and the `contactForm` submit pipeline.

## Open questions

- 📡 **Contact email recipient.** Controlled under [[settings-general]] (`site_email` setting). GraphQL-resolvable: query the merchant's general settings to read the `site_email` value.
- 📡 **Per-language module text.** With `multylang`, text fields accept per-language entries via the language switcher. GraphQL-resolvable: query whether the `multylang` app is installed.
- 📡 **Per-instance Mailchimp list.** Mailchimp app stores one list per store — multiple newsletter modules all target the same list. GraphQL-resolvable: query whether Mailchimp is installed and which list it targets.
