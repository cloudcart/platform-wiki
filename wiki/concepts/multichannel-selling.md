---
type: concept
nav_path: "Concept → Multichannel & marketplace selling"
route_name: (none)
route_path: (none)
aliases: ["Multichannel selling", "Marketplace selling", "Sell on marketplaces", "Channel sync", "Product feeds", "Platform migration", "Многоканална продажба", "Маркетплейс", "OLX eMAG продажба", "Sell on OLX", "Sell on eMAG", "Google Shopping feed", "TikTok Shop"]
tags: [multichannel, marketplace, channels, feeds, migration, apps, integrations, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---
# Multichannel & marketplace selling

## Definition

**Multichannel & marketplace selling** is selling the store's catalogue **beyond the merchant's own storefront** — listing products on external marketplaces, pushing product feeds to shopping / ad engines, and migrating an existing store into CloudCart. Each channel is a separate app from the [[apps]] App Store; this page is the map of which app does what and how orders / data flow.

## Scope

- **Marketplaces (orders flow back into CloudCart):** [[apps-olx]] (OLX), [[apps-emag-sync]] (eMAG), [[apps-etsy]] (Etsy), [[apps-tiktok-shop]] (TikTok Shop) — list products on the marketplace and pull the resulting orders back.
- **Shopping feeds & ads (advertise only, no order sync):** [[apps-google-shopping]], [[apps-google-dynamic]] (dynamic remarketing), [[apps-tiktok-ads]] — send a product feed so the channel can advertise; the customer still buys on the CloudCart storefront.
- **Generic product feeds:** [[apps-xml-feed-generator]] (build an XML feed to point anywhere), [[apps-xml-sync]] (recurring supplier feed sync).
- **Platform migration (one-time import INTO CloudCart):** [[apps-woocommerce]], [[apps-magento]], [[apps-shopify]], plus [[apps-json-import]].
- **Sync engine:** [[apps-listing-engine]] keeps the storefront search / listing index in step as the catalogue changes.

## Contrasts

- **Marketplace vs feed/ads.** A marketplace ([[apps-olx]], [[apps-emag-sync]], [[apps-tiktok-shop]]) *sells* the product on the external site and pulls orders BACK. A feed/ads app ([[apps-google-shopping]], [[apps-tiktok-ads]]) only *advertises* — no order flows back from the ad platform.
- **Channel vs migration.** OLX / eMAG / TikTok Shop are *ongoing* channels; the WooCommerce / Magento / Shopify importers are *one-time* migrations into CloudCart (you leave the old platform behind).
- **Generic feed vs marketplace API.** [[apps-xml-feed-generator]] produces a generic feed file; a marketplace app speaks that marketplace's own API and round-trips orders.

## Where it applies

- Inventory / price kept consistent across channels — see [[inventory-tracking]].
- Orders pulled from a marketplace enter the normal [[order-processing-pipeline]].
- Product-data shape for feeds — see [[products]].

## Related

- [[apps]] — the App Store (install any channel).
- [[import-pipeline]] — the bulk-import mechanism migrations rely on.
- [[erp-integrations]] / [[fulfillment-and-warehouse]] — sibling integration categories.

## Open Questions

- Which marketplaces sync inventory bidirectionally vs one-way (verify per app).
- Whether marketplace orders carry a channel tag distinguishing them from storefront orders (verify).
