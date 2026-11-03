---
type: feature
nav_path: "Apps → Yotpo"
route_name: apps.yotpo.overview
route_path: /admin/apps/yotpot
aliases: ["Yotpo", "Yotpo Reviews", "Yotpo UGC", "Yotpo Loyalty"]
tags: [apps, others, reviews, ugc, loyalty]
plan_gates: ["yotpo"]
created: 2026-05-22
updated: 2026-06-11
source_count: 4
---
# Yotpo (external review + UGC platform)

## Purpose

**Yotpo** integration — embed Yotpo's review + UGC (User-Generated Content) modules on storefront product pages. Yotpo is a leading external review-platform with:

- Reviews + Q&A module (alternative to CloudCart's native [[apps-product-review]]).
- Photo + video reviews.
- Email outreach campaigns soliciting reviews from past customers.
- Loyalty + rewards integration (NOT covered by this integration — see Business rules).
- Verified-buyer badges via Yotpo's order-import.

Used by merchants who want richer review UX than CloudCart's native offering, especially when running on multiple platforms (Yotpo can sync reviews across Shopify, WooCommerce, CloudCart).

## Where to find it

Sidebar → Apps → install → **Yotpo**. See [[apps-yotpo-settings]] for configuration.

## What the merchant can do here

- Configure the Yotpo App Key + App Secret.
- Activate to inject Yotpo's review module on storefront product pages, and a conversion-tracking pixel on the order-confirmation page.

### What the merchant CANNOT do here
- Manage Yotpo's review queue from CloudCart — that's done in Yotpo's own admin.
- Use without an active Yotpo subscription.

## Settings & fields

The integration injects Yotpo's JavaScript snippet (`//staticw2.yotpo.com/{app_key}/module.js`) plus per-product configuration so Yotpo's CDN-served module displays. Two storefront surfaces:

- **Product page review module** — the full reviews + Q&A widget on product detail pages.
- **Conversion-tracking pixel** — fires on the order-confirmation page, pushing order data (order, currency) to Yotpo for verified-buyer reviews + ROI tracking.

Settings keys (configured on [[apps-yotpo-settings]]):

- `app_key` — the Yotpo App Key. This is the only credential the live integration actually uses (both for the module script and the conversion pixel).
- `app_secret` — collected and stored, but **not used** by the current integration. It is kept for future Yotpo authenticated-API operations (review-import sync, programmatic review fetch) that CloudCart does not yet invoke. A merchant who has lost their App Secret can paste a placeholder; the integration works on `app_key` alone.
- `show_in_listing` — default **0** (off). When off, the star module does NOT appear on category cards / product listings, only on product detail pages. This conservative default keeps category-page load fast (Yotpo's module JS doesn't load on listings unless enabled). Turn it on to show the compact star average + count on listings.

> **Known UI bug (App Key / App Secret labels are swapped).** On the Yotpo settings screen the input that stores `app_key` is **labelled "App Secret"** and vice versa. The merchant must paste their real Yotpo App Key into the field labelled **"App Secret"** for the module to work, because the live integration reads `app_key`. See [[apps-yotpo-settings]].

## Business rules

### Configured check requires both App Key and App Secret

The integration is treated as configured only when **both** `app_key` and `app_secret` are set; either missing means "not configured". There is **no automated API health check** — the connection status is a placeholder that does not validate credentials against Yotpo. The merchant should rely on the configured-check (both fields filled) to know the integration is set up, not on any "connected" indicator.

### Graceful degradation

If the app is not installed, the review module renders nothing (silently). The conversion pixel additionally requires the app to be active and an `app_key` to be set. An uninstalled or misconfigured Yotpo therefore never breaks product or order-confirmation pages.

### Discount-aware price sent to Yotpo

The product module receives the **discounted price when a discount applies** (otherwise the catalog price). So Yotpo shows the actual customer-facing price, not an inflated catalog price.

### Replaces / supplements native reviews — no auto-conflict resolution

When Yotpo is active, the merchant typically disables CloudCart's native [[apps-product-review]] to avoid two review modules on the same page. The platform does **not** auto-mediate this: both can be enabled at once, and nothing checks whether the native reviews app is active when Yotpo is installed/activated (or vice versa). The merchant must disable one manually.

### Yotpo data lives on Yotpo's side

All reviews submitted via the Yotpo module are stored in Yotpo's database, NOT CloudCart. The merchant doesn't see them in [[customers-details-reviews]]. To migrate to CloudCart's native reviews, the merchant must export from Yotpo and import.

### Photo / video reviews handled entirely by Yotpo

CloudCart sends only the product anchor (`product_id`, `name`, `url`, `image-url`, `description`, `price`, `currency`) to Yotpo's module. Whether a displayed review carries photos or video depends on the merchant's Yotpo plan and the customer's submission in Yotpo's review-collection flow — CloudCart neither captures nor stores review media.

### Multi-language reviews handled by Yotpo's locale settings

CloudCart does not pass a language or locale to Yotpo. The module's display language is controlled inside the Yotpo admin (Yotpo auto-detects from the storefront browser locale or uses the merchant's Yotpo-side language config). Multi-language storefronts see whatever language Yotpo's module decides per page-load.

### Yotpo Loyalty + Rewards NOT included

This integration covers only the Reviews + Q&A module and conversion tracking. It does **NOT** include Yotpo Loyalty, SMSBump, or Yotpo Rewards — those are separate Yotpo products with no native CloudCart integration. A merchant who wants Loyalty must install Yotpo Loyalty's script via the storefront's custom-code area or use a different loyalty solution.

### GDPR cookie consent NOT gated

The Yotpo module script loads unconditionally on every product page where the module renders — there is no GDPR-consent guard around the script tag and no integration with [[apps-gdpr-overview]] cookie categories. Merchants who need strict cookie-consent compliance should configure Yotpo's own cookie controls on the Yotpo side, or block the module through a third-party consent-manager script.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `yotpo` | Access gate (install URL) | The install URL `/admin/apps/yotpo/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-yotpo-settings]] — settings sub-page.
- [[apps-product-review]] — alternative CloudCart-native reviews.
- [[products-products]] — products where Yotpo module appears.

## Open questions

- Note on slug: the live app key is `yotpo` (no typo). The wiki file slug `apps-yotpot.md` has a trailing "t"; the actual app and route group are `yotpo`.
