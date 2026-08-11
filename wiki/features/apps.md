---
type: feature
nav_path: "Apps"
route_name: apps.all
route_path: /admin/apps/:all?
aliases: []
tags: [apps, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 2
---
# Apps

## Purpose

Hub page for the **Apps** area of the CloudCart admin panel. Lists the screens that live under this section.

## Where to find it

Top-level sidebar entry **Apps** (with the grid `fal fa-th` icon). The page URL is `/admin/apps`.

## What the merchant can do here

- Browse the full App Store catalog and filter by **My apps** (installed) vs **All apps** (everything available for the store's country).
- Search apps by name, mapping, description text, or category (search supports Cyrillic-to-Latin substitution — typing `плагин` matches `plagin`).
- Filter by category and toggle a **Recommended** flag.
- View Featured apps in a hero swiper at the top.
- Click any app card to open its Overview / Install / Settings flow.

## Layout of the hub page

The page is rendered by `AppsList.vue` and has three main sections, top-to-bottom:

| Section | What it shows |
|---|---|
| **Breadcrumbs** | `Apps → My apps` (when on the My-apps tab) or just `Apps` (when on `All apps`). |
| **Featured** | Hero swiper with the merchant's curated featured apps. |
| **Searchbar + category filter** | Free-text search input + multi-select category picker. Includes a "Recommended" pseudo-category. |
| **Two tabs** | "My apps" (only installed) vs "All apps for &lt;Country&gt;" (everything filtered to the merchant's country). The "All apps" tab additionally shows the country flag from the store's country code. |
| **App grid** | Cards with logo, name, install/uninstall button, and category. |
| **Empty state** | a not-found error when search/filter yields zero matches; the query is also reported via Sentry for analytics. |

## Install / Uninstall sub-flow (per app card)

Every app card uses the same install / uninstall flow rendered by `Install.vue`:

1. **Required-apps gate** — when the app declares `required_apps`, the platform shows a "You're almost set!" card BEFORE the install button: the merchant must install each prerequisite first. Each row shows the dependency's name + an **Install App** button or "installed" label.
2. **Paid apps** — for `is_paid && !paid` apps the card shows the monthly / annual price + VAT note. Two side-by-side buttons: **Start N days trial** (when `is_allow_trial`) and **Buy**. Both emit a `buy` event that opens the billing flow.
3. **Free / already-paid apps** — single **Install** button. While the install POST is in flight, the button shows a spinner and is disabled.
4. **Install endpoint** — `POST` to `app.urls.install` (or fallback `/admin/api/<key>/install`). Success path: toast *"This application has been installed"* → set `is_installed = true` → call `goToSettings` → navigate to `apps.<key>.overview` (when the app isn't installed yet) or `apps.<key>.settings`.
5. **Request-app flow** — for apps with `request_app = true` (typically deprecated / unavailable ones), the install button is replaced by **Request**. Submits to `app.urls.request_app_url`. Success toast: *"Request submitted successfully. You will be contacted by a representative soon."* Error toast: *"You have already requested the app."* (or the response's error message).
6. **Uninstall** — for installed paid apps the card shows a red **Uninstall** button. Confirmation is NOT a modal — the click immediately fires `DELETE /admin/api/core/applications/{key}`. Success toast: *"This application has been removed successfully"*. If the response contains a `redirect`, the loader stays on and the router redirects.

After install/uninstall the navigation sidebar is updated via `$updateNavigationInstallUninstallApp` so the menu entry appears or disappears immediately. Sentry events are also fired (`installApp`).

## Settings & fields

Not applicable — this is a navigation hub, not a screen with its own settings. (Per-app settings live on each app's Settings sub-page.)

## Business rules

- The Apps sidebar entry is visible to a staff member only if their role grants the `apps` permission. The entry surfaces a "New" badge until the merchant first opens the page.
- **Permission gate** — the Apps API endpoints are gated by `hasApiPermission:apps`. A moderator needs the **Apps** (`apps`) permission grant from [[settings-staff]] to list, install, configure, or uninstall apps. Owners always pass. Each individual app's own settings page may additionally enforce a narrower permission (e.g., a shipping app's settings need `store.shipping`, an analytics app's settings need `reports.analytics_settings`). So a moderator with `apps` but missing the underlying area permission can browse the catalog but may be blocked from saving config inside a specific app.
- Search input value is preserved in the URL query (`?search=...`) so refreshing the page keeps the merchant's filter context.
- Selected categories are persisted in the URL as `?category=cat1,cat2`.
- The Recommended toggle filters to apps where `other.recommend = true`.
- Category filter and search compose with AND — both must match for an app to show.
- The grid is sorted: apps whose name matches the keyword come first, then alphabetical.

## Related

- [[erp-integrations]] — directory of ERP / accounting integrations (concept hub).
- [[fulfillment-and-warehouse]] — directory of fulfillment / warehouse / 3PL apps (concept hub).
- [[multichannel-selling]] — sell on marketplaces / feeds / migrate in (concept hub).
- [[b2b-wholesale]] — B2B & wholesale selling (concept hub).
- [[digital-products]] — digital / downloadable products (concept hub).
- [[food-restaurant-grocery]] — food / restaurant / grocery (concept hub).
- [[import-pipeline]] — the bulk-import mechanism behind the CSV / XML / JSON import apps (concept hub).
- [[shipping-provider-mechanism]] — the courier-integration mechanism behind the shipping / courier apps (concept hub).
- [[payment-provider-mechanism]] — the payment-integration mechanism behind the payment apps (concept hub).
- [[invoicing-and-accounting]] — the accounting-integration mechanism behind Szamlazz / SmartBill / FGO / Profisc (concept hub).
- [[multi-language]] — the translation mechanism behind the Multilang app (concept hub).
- [[apps-advanced-search]]
- [[apps-aftercare]]
- [[apps-algolia]]
- [[apps-algolia-settings]]
- [[apps-also]]
- [[apps-barsy]]
- [[apps-bgn2eur]]
- [[apps-blog-csv-import]]
- [[apps-bumpcart]]
- [[apps-bumpcart-settings]]
- [[apps-cart-rules]]
- [[apps-cart-rules-rules]]
- [[apps-click-to-call]]
- [[apps-cloudio-details]]
- [[apps-cloudio-history]]
- [[apps-cloudio-overview]]
- [[apps-cloudio-settings]]
- [[apps-colibri]]
- [[apps-csv-import]]
- [[apps-datalayer]]
- [[apps-deprecated]]
- [[apps-dexpress]]
- [[apps-disqus-comments]]
- [[apps-domain-redirect]]
- [[apps-domain-redirect-settings]]
- [[apps-drop-shipping]]
- [[apps-e-store-content]]
- [[apps-e-store-content-settings]]
- [[apps-elslogistic]]
- [[apps-emag-sync]]
- [[apps-etsy]]
- [[apps-evropat]]
- [[apps-facebook-comments]]
- [[apps-facebook-comments-settings]]
- [[apps-fast-order]]
- [[apps-fast-order-settings]]
- [[apps-fedex]]
- [[apps-fgo]]
- [[apps-fgo-settings]]
- [[apps-finaleinventory]]
- [[apps-flix-facts]]
- [[apps-flix-facts-settings]]
- [[apps-frisbo]]
- [[apps-frisbo-orders]]
- [[apps-frisbo-settings]]
- [[apps-gdpr-acceptance]]
- [[apps-gdpr-address]]
- [[apps-gdpr-cookies]]
- [[apps-gdpr-overview]]
- [[apps-gdpr-policy]]
- [[apps-gdpr-requests]]
- [[apps-gdpr-settings]]
- [[apps-gensoft]]
- [[apps-glovo]]
- [[apps-google-analytics]]
- [[apps-google-analytics-settings]]
- [[apps-google-connect]]
- [[apps-google-dynamic]]
- [[apps-google-dynamic-settings]]
- [[apps-google-search-console]]
- [[apps-google-search-console-settings]]
- [[apps-google-sheets]]
- [[apps-google-sheets-settings]]
- [[apps-google-sheets-tasks]]
- [[apps-google-shopping]]
- [[apps-google-shopping-attributes]]
- [[apps-google-shopping-products]]
- [[apps-google-shopping-settings]]
- [[apps-google-shopping-status]]
- [[apps-google-tags]]
- [[apps-google-tags-settings]]
- [[apps-google-workspace]]
- [[apps-grocery-store-overview-new]]
- [[apps-grocery-store-settings]]
- [[apps-imos3d]]
- [[apps-imos3d-settings]]
- [[apps-it4profit]]
- [[apps-json-import]]
- [[apps-lets-encrypt]]
- [[apps-listing-engine]]
- [[apps-live-chat]]
- [[apps-live-chat-settings]]
- [[apps-load-bee]]
- [[apps-load-bee-settings]]
- [[apps-magento]]
- [[apps-mailchimp]]
- [[apps-mailchimp-settings]]
- [[apps-mikmik]]
- [[apps-multilang]]
- [[apps-multilang-create-step]]
- [[apps-multilang-products]]
- [[apps-multilang-progress]]
- [[apps-multilang-settings]]
- [[apps-multilang-stores]]
- [[apps-n18-audit]]
- [[apps-n18-audit-settings]]
- [[apps-ntclogistics]]
- [[apps-olx]]
- [[apps-olx-adverts]]
- [[apps-olx-configuration]]
- [[apps-olx-history]]
- [[apps-olx-parameters]]
- [[apps-olx-parameters-values]]
- [[apps-olx-products]]
- [[apps-olx-settings]]
- [[apps-pick-and-pack]]
- [[apps-pick-and-pack-settings]]
- [[apps-pigeonexpress]]
- [[apps-private-store]]
- [[apps-private-store-settings]]
- [[apps-product-review]]
- [[apps-profisc]]
- [[apps-profisc-settings]]
- [[apps-request]]
- [[apps-rkeeper]]
- [[apps-seo-spinner]]
- [[apps-seo-spinner-settings]]
- [[apps-shipping-hours]]
- [[apps-shipping-hours-settings]]
- [[apps-shipping-hours-shipping-list]]
- [[apps-shopify]]
- [[apps-size-chart]]
- [[apps-size-chart-conditions]]
- [[apps-smart-bill]]
- [[apps-smart-bill-settings]]
- [[apps-smtp]]
- [[apps-smtp-settings]]
- [[apps-store-locations]]
- [[apps-store-locations-settings]]
- [[apps-stores]]
- [[apps-stores-settings]]
- [[apps-stores-sync]]
- [[apps-stores-sync-settings]]
- [[apps-suppliers]]
- [[apps-suppliers-overview]]
- [[apps-suppliers-supplier-products]]
- [[apps-szamlazz]]
- [[apps-szamlazz-orders-credit-note]]
- [[apps-szamlazz-orders-invoice]]
- [[apps-szamlazz-orders-receipt]]
- [[apps-szamlazz-settings]]
- [[apps-tcscourier]]
- [[apps-tiktok-ads]]
- [[apps-tiktok-ads-settings]]
- [[apps-tiktok-pixel]]
- [[apps-tiktok-pixel-settings]]
- [[apps-tiktok-shop]]
- [[apps-tiktok-shop-products]]
- [[apps-tiktok-shop-settings]]
- [[apps-ultracep]]
- [[apps-universum]]
- [[apps-up-cross-sell]]
- [[apps-vali-computers]]
- [[apps-versus-erp]]
- [[apps-video-slider-widget]]
- [[apps-woocommerce]]
- [[apps-xml-feed-generator]]
- [[apps-xml-feed-generator-features]]
- [[apps-xml-import-features]]
- [[apps-xml-import-overview]]
- [[apps-xml-import-settings]]
- [[apps-xml-import-status]]
- [[apps-xml-import-step2]]
- [[apps-xml-import-step3]]
- [[apps-xml-sync-features]]
- [[apps-xml-sync-overview]]
- [[apps-xml-sync-settings]]
- [[apps-xml-sync-status]]
- [[apps-xml-sync-step2]]
- [[apps-xml-sync-step3]]
- [[apps-yotpo-settings]]
- [[apps-yotpot]]
- [[apps-zeron]]
- [[apps-zopim]]
- [[apps-zopim-settings]]

- [[apps-ad-scout]]
- [[apps-brands-distribution]]
- [[apps-workflow]]

## Open questions

(none)
