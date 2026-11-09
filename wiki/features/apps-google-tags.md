---
type: feature
nav_path: "Apps → Google Tag Manager"
route_name: apps.google_tags.overview
route_path: /admin/apps/google_tags
aliases: ["Google Tags", "Google Tag Manager", "GTM", "Tag Manager", "Гугъл Таг Мениджър"]
tags: [apps, google, tag-manager, tracking]
plan_gates: ["google_tags"]
created: 2026-05-22
updated: 2026-11-09
source_count: 7
---
# Google Tag Manager (GTM)

## Purpose

**Google Tag Manager** integration — injects a GTM container into the storefront so the merchant can manage ALL tracking scripts (Google Ads, Facebook Pixel, TikTok Pixel, Hotjar, custom JavaScript, etc.) through the GTM UI WITHOUT touching CloudCart's storefront theme. The benefit: marketers add / remove / change tags via GTM's web interface; developers aren't needed.

Pairs well with [[apps-google-analytics]] (GA emit) and [[apps-google-dynamic]] (dynamic remarketing tags).

## Where to find it

Sidebar → Apps → install → **Google Tag Manager**. See [[apps-google-tags-settings]] for configuration.

## What the merchant can do here

- Configure the GTM container ID (`GTM-XXXXXXX` format).
- Inject the GTM container snippet into all storefront pages.
- Use GTM's web UI to add tracking tags without redeploying CloudCart.

### What the merchant CANNOT do here
- Manage tag firing rules from this page — that's done in GTM's web UI (tagmanager.google.com).
- Use without a Google account + GTM container.

## Settings & fields

The Manager exposes:
- the configured check — credential / container-ID validity check.

The integration injects the standard GTM snippet (head + body initialization) on every storefront page.

## Business rules

### What the data layer carries

Every storefront page pushes one `cc_page_data` object: the page type and its context (the product, the listed products, the cart, the checkout, or on the thank-you page the order with its `js_events` once-per-order flag). The storefront pushes no `{event: …, ecommerce: …}` object, so a GTM tag waiting for a GA4-style `purchase` or `add_to_cart` event with an `ecommerce` block never fires. GA4-named events go to Google only through [[apps-google-analytics]] and [[apps-google-dynamic]]; see [[apps-google-analytics-purchase-event]].

### One container per store

Typically one GTM container per CloudCart store. Multi-store merchants use one container per store OR one shared container with conditional tag firing.

### Cookie consent integration

With [[apps-gdpr-overview]] active, the container itself loads only once the Performance cookie group counts as accepted: "yes" until the visitor answers, so only a refusal keeps GTM off. The Google Consent Mode group does not delay the container; the tags inside it follow whatever consent settings the merchant gives them in GTM.

### No OpenAI / ChatGPT pixel

CloudCart has no built-in OpenAI or ChatGPT pixel. A merchant who needs one adds it as their own tag in their GTM container.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `google_tags` | Access gate (install URL) | The install URL `/admin/apps/google_tags/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-google-tags-settings]] — settings sub-page.
- [[apps-google-analytics]] — analytics measurement (often paired with GTM).
- [[apps-google-dynamic]] — dynamic remarketing tags.
- [[apps-datalayer]] — sister CloudCart app for data layer customisation.
- [[apps-facebook-comments]] / [[apps-tiktok-pixel]] — other tracking integrations that may be managed via GTM.
- [[apps-gdpr-overview]] — consent gates GTM tags.

## How it works (verified against backend)

### Single required setting: `code`

The integration requires only the `code` field. The merchant pastes the GTM Container ID (`GTM-XXXXXXX`) into the `code` field. That's it.

### Minimal integration

The integration is bare-bones — just an app key and a configured-check. **All GTM logic lives in storefront templates** that consume the `code` setting and inject the GTM snippet at storefront-render time.

This is a SIMPLE pass-through integration: CloudCart provides the container ID; GTM handles everything else (tags, triggers, variables, data layer pushes) on the customer side via the container's web UI.

### Validation: GTM ID format enforced

The merchant's input is validated by the regex `/GTM-[0-9A-Z]{5,}/i` (case-insensitive). Pasting an invalid format triggers: *"The Google Tag ID is invalid"*. Pasting nothing while the app is active triggers: *"Please add your Google Tag ID"*.

### Single settings field

Per the platform code's `$only` allowlist, the ONLY saveable setting is `code` — the merchant cannot configure anything else from this page. Multi-container support, server-side GTM URLs, or data layer toggles are NOT present in the current implementation.

### Standard data-layer push: `cc_page_data` blob

Each storefront page emits ONE primary push on load: `dataLayer.push({cc_page_data: cc_page_data})`. The object varies by route (product / category / cart / checkout / checkout-return / etc.) and carries the relevant context (product details, line items, totals, customer state). On the thank-you page no further purchase push follows: CloudCart's own analytics records the order separately, and that is not a data-layer event. Customer details come in `cc_customer_data`, loaded by a second script.

### Preview mode works because injection is plain HTML

The integration adds the standard GTM `<script>` to `<head>` and `<noscript>` to `<body>` using the merchant's container ID. GTM's Preview Mode operates by appending a query parameter to the page URL and reading container state — this works normally on a CloudCart storefront because no special wrapper interferes with GTM's standard bootstrap. There is no CloudCart-specific Preview Mode setting; the merchant uses GTM's UI directly.

### GTM bootstrap rides the shared apps JS file (CDN), not per-request

Like GA, the GTM container ID is compiled into the shared `cc_applications_config.js` file on S3/CDN, and the storefront page references that file from `<head>`. The shared loader checks the configured GTM code and dynamically loads the `google_tags` storefront loader. Practical implication: saving a new GTM container ID requires the JS file to **regenerate** before the new container is picked up by browsers. The Google Tags manager implements the `AppJsRegenerate` contract — saving the settings page triggers the regenerate automatically.

### Crawler / admin-preview detection blocks GTM bootstrap

The apps loader does NOT load the `google_tags` snippet when the request is from a crawler (`cc_settings.isCr` is true) or when the storefront is being previewed by a CloudCart admin (`cpadm` flag). Bots therefore do not trip GTM tags; admin previews do not pollute pixel/conversion counts.

### Cookie consent: GTM consent triggers are merchant-configured in GTM, but Consent Mode v2 is emitted by GDPR app

If [[apps-gdpr-overview]] is installed with the "Google Consent Mode" cookie group active, the storefront emits the `gtag('consent', ...)` signals BEFORE GTM bootstraps. GTM tags configured by the merchant in tagmanager.google.com can either:
1. Wait on the GDPR consent state (using Consent Mode tags inside GTM).
2. Ignore consent (fires unconditionally).

The choice is up to the merchant inside GTM — CloudCart only emits the upstream signals.

### The data layer does not depend on an app

The `cc_page_data` push and the customer script are part of every storefront page. [[apps-datalayer]] is installed on new stores by default, and its install state does not switch them off. A GTM-only setup still gets no GA4 events: the merchant builds tags and variables on `cc_page_data`.

### Two tabs: Overview + Settings (no auth state)

Like Google Analytics, the Vue Index uses `ApplicationSettings` with `:tabs="true"` and the router exposes exactly two routes — Overview + Settings. No OAuth state, no conditional tabs, no install-only stub.

## Open questions

(None currently outstanding for this page.)
