---
type: feature
nav_path: "Apps → OLX"
route_name: apps.olx.overview
route_path: /admin/apps/olx
aliases: ["OLX", "OLX marketplace", "OLX adverts", "OLX Bulgaria", "OLX Romania", "enable disable button", "app active toggle"]
tags: [apps, others, marketplace, adverts, sync]
plan_gates: ["olx", "olx_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# OLX (marketplace integration)

## Purpose

**OLX** integration — publishes the merchant's products as **adverts on OLX**, the dominant classified marketplace in the target markets. Customers who browse OLX see the merchant's products there and can buy or contact directly through OLX (clicks track back to the CloudCart store). Critical for merchants who want broader reach beyond their own storefront — OLX traffic is huge in target markets.

**Production currently supports only Bulgaria (olx.bg) and Romania (olx.ro).** Poland, Ukraine, Portugal, Kazakhstan, Belarus, Angola, and Mozambique exist in the codebase and appear in the country dropdown, but their API credentials are commented out — they cannot be connected today. See [[apps-olx-main-connection]] for the connection / authorization model.

This page is the **hub** for the OLX integration. It defines the app at a glance and points to the per-aspect sub-pages (below) plus the per-tab UI sub-pages. The Assistant should drill into the aspect that matches the question rather than read every page.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **OLX**. The app presents eight tabs, each with its own UI sub-page:

| Tab | Route name | UI sub-page |
|----------|------------|-------------|
| Overview | `apps.olx.overview` | (this hub) |
| Settings | `apps.olx.settings` | [[apps-olx-settings]] |
| Configuration | `apps.olx.configuration` | [[apps-olx-configuration]] |
| Adverts | `apps.olx.download` (path `/admin/apps/olx/adverts`) | [[apps-olx-adverts]] |
| Products | `apps.olx.products` | [[apps-olx-products]] |
| Parameters | `apps.olx.parameters` | [[apps-olx-parameters]] |
| Parameters → Values | `apps.olx.parameters.values` | [[apps-olx-parameters-values]] |
| History | `apps.olx.history` | [[apps-olx-history]] |

## Sub-pages (in this cluster)

The verified-behaviour detail is split into four aspect pages. The per-tab UI pages above describe each screen; these aspect pages describe the cross-tab mechanics.

- [[apps-olx-main-connection]] — the multi-country / per-endpoint credential model; the two-token OAuth flow (partner credentials + per-merchant user token); the CloudCart Socialite redirect; refresh-token lifetime and silent token-expiry gating.
- [[apps-olx-main-sync]] — the automatic stock / status / delete sync settings (`sync_quantity`, `sync_status`, `sync_delete`) that mirror CloudCart product state to OLX adverts; manual bulk price re-sync; how bulk publish loops product IDs one at a time.
- [[apps-olx-main-advert-format]] — how an advert is assembled: auto-built description (variants + properties + vendor + filtered text), 70-character title trim, per-category image cap, logo auto-attach (300×300 minimum), and the activate/deactivate command model.
- [[apps-olx-main-publishing]] — the OLX taxonomy-mapping requirement, the six background populate jobs + 30-day refresh interval, rejection handling surfaced in History, the absence of buyer-message integration, and the plan caps.

## What the merchant can do here

- **Connect** one or more OLX accounts (one per supported country) and authorize CloudCart against each — see [[apps-olx-settings]] + [[apps-olx-main-connection]].
- **Select products** to publish and map them to OLX categories / parameters — see [[apps-olx-products]], [[apps-olx-parameters]], [[apps-olx-parameters-values]].
- **Publish, sync, re-publish, and take down adverts** — see [[apps-olx-adverts]] + [[apps-olx-main-sync]].
- **Configure auto-sync** of stock, status, and deletions so adverts track CloudCart product state — see [[apps-olx-main-sync]].
- **Troubleshoot failed publishes** via the operation log — see [[apps-olx-history]] + [[apps-olx-main-publishing]].

### What the merchant CANNOT do here

- Use OLX without an active OLX seller account in the relevant country.
- Connect a country other than Bulgaria or Romania (others are codebase-only — see [[apps-olx-main-connection]]).
- Edit adverts at OLX's side directly for some changes — those must go through OLX's own portal.
- Receive OLX buyer messages inside CloudCart — there is no buyer-message integration (see [[apps-olx-main-publishing]]).

## Settings & fields

Connection-level fields (country / endpoint, shipping payer, OAuth authorization) live on [[apps-olx-settings]] and are explained in [[apps-olx-main-connection]]. Per-product mapping fields live on [[apps-olx-products]], [[apps-olx-parameters]], and [[apps-olx-parameters-values]]. App-wide sync toggles (`sync_quantity`, `sync_status`, `sync_delete`) live on [[apps-olx-configuration]] and are explained in [[apps-olx-main-sync]].

## Business rules

- **OLX has its own product taxonomy.** CloudCart products MUST be mapped to OLX categories + parameters before publishing, or OLX rejects the advert — see [[apps-olx-main-publishing]].
- **OAuth-based authentication with a 1-month refresh-token lifetime.** If the merchant takes no OLX action for over a month, the token expires and they must re-authorize — see [[apps-olx-main-connection]].
- **Adverts have a limited life on the marketplace** (typically 30–60 days depending on country / paid promotion). The merchant must re-publish to keep them live — see [[apps-olx-adverts]].
- **Auto-sync mirrors product state.** With the sync settings on, stock-out / inactive / deleted products auto-deactivate or remove their adverts — see [[apps-olx-main-sync]].
- **History tracks every API operation** — the first place to look for why a product failed to publish — see [[apps-olx-history]].

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `olx` | Access gate (install URL) | The install URL `/admin/apps/olx/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |
| `olx_total_products` | Numeric (global cap) | App-specific cross-task cap on products published to OLX. When the cap is hit, additional adverts cannot be published. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[multichannel-selling]] — multichannel / marketplace concept hub.
- [[apps]] — App Store.
- [[apps-olx-settings]] — settings / connection tab.
- [[apps-olx-configuration]] — configuration tab (sync toggles).
- [[apps-olx-adverts]] — adverts list.
- [[apps-olx-products]] — product selection.
- [[apps-olx-parameters]] — parameter mapping.
- [[apps-olx-parameters-values]] — value mapping.
- [[apps-olx-history]] — operation log.
- [[apps-olx-main-connection]] — multi-country + OAuth connection model.
- [[apps-olx-main-sync]] — stock / status / delete / price sync.
- [[apps-olx-main-advert-format]] — advert assembly + lifecycle commands.
- [[apps-olx-main-publishing]] — taxonomy mapping, populate jobs, rejections, caps.
- [[products-products]] — source products.
- [[products-property]] — properties mapped to OLX parameters.

## Open questions

None.
