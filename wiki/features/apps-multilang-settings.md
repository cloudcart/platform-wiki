---
type: feature
nav_path: "Apps → Multilang → Settings (Features)"
route_name: apps.multilang.settings
route_path: /admin/apps/multilang/settings
aliases: ["Multilang Settings", "Multilang Features", "Multi-language features"]
tags: [apps, administration, multilang, settings]
plan_gates: [multilang_product_copy, multilang_product_translate]
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---
# Multilang → Settings

## Purpose

The **Settings** tab (the "Features" component) is a **quota dashboard**, not a configuration screen. It shows the merchant how much of their two Multilang plan quotas — product **copy** and product **translate** — they have left, and lets them buy more. It does **not** hold the translate toggles, price transform, or per-field options that earlier wiki drafts placed here; those all live on the per-sister Configuration modal — see [[apps-multilang-stores-config-modal]].

For the full Multilang feature set, see [[apps-multilang]].

## Where to find it

Sidebar → Apps → Multilang → **Settings tab**. Route: `/admin/apps/multilang/settings`. The tab renders two cards side by side: one for the `multilang_product_copy` quota, one for the `multilang_product_translate` quota.

## What the merchant can do here

- **Read remaining quota** for copying products to sister sites (`multilang_product_copy`) and for translating products (`multilang_product_translate`).
- **Buy additional packs** of either quota when a balance runs low, via the "Buy an additional package" link on each card.

Everything else about *how* a sister site is fed (which fields translate, price markup, manual-vs-automatic copy, cascade delete, URL rewriting) is configured per sister site on the Configuration modal — see [[apps-multilang-stores-config-modal]]. There is no store-wide master settings surface for those toggles.

### What the merchant CANNOT do here

- Set any translate / copy field toggle — those are per-sister; see [[apps-multilang-stores-config-modal]].
- Disable Multilang entirely — that is the parent app's deactivate / uninstall flow.
- See a per-character price or a per-toggle cost estimate — only the remaining quota balance (see Business rules).

## Settings & fields

The tab renders exactly **two cards**, each a quota progress widget:

| Card | Quota key | Shows |
|---|---|---|
| **Copy** | `multilang_product_copy` | `<used> / <total>` products. Description: "Copying products in the language versions". |
| **Translate** | `multilang_product_translate` | `<used> / <total>` symbols. Description: "Translation of newly added products after copying". |

Each card has:
- A **header** with the `<used> / <total>` counter.
- A **progress bar** filling to `used / total`.
- **Help text** below the bar: *"You have {N} products left to copy"* (copy) or *"You have {N} characters to translate"* (translate).
- A **"Buy an additional package"** link.

## Business rules

### The tab is quota-display only — no behaviour toggles live here

The component renders only the two quota cards above. The translate field toggles (`translate.title`, `translate.description`, `translate.category`, `translate.variety`, `translate.meta`, `translate.product_tags`, `translate.properties`, `translate.tabs`, `translate.alt_tags`), the price transform, the `method` (manual / automatic) and `delete` cascade settings are all on the per-sister Configuration modal — see [[apps-multilang-stores-config-modal]]. They are stored per `site_id`, so each sister site has its own independent config.

### "Buy an additional package" opens the PlanFeature modal

The link opens the platform's `PlanFeature` modal with the matching `mapping` — `multilang_product_copy` or `multilang_product_translate`. The merchant picks a pack tier and pays through the standard plan-feature checkout. On success, the `handleAfterPay` callback updates the card's `total` + `remaining` locally, so the new balance shows immediately without a page reload.

### Pack pricing model: 1 unit = N symbols

Pricing is structured as plan-feature packs, not a visible per-character rate. Each pack has a `price` (in cents) and a `value` (count of symbols / products included); the implied per-unit price is `(price/100) / value`. Every translated symbol decrements the remaining `multilang_product_translate` balance by 1; every copied product decrements `multilang_product_copy`. CloudCart's wholesale cost (Google's $20 / 1M characters) is internal accounting the merchant never sees — see [[apps-multilang-main-translation-engine]].

### Quota gates each per-sister save, not this tab

The merchant cannot run out of quota *here* — this tab only displays and tops up the balance. The gates fire when the merchant enables copy / translate on a sister: that save returns HTTP 402 with a buy-quota message when the relevant quota is exhausted. The 402 flow and the two gated toggles are documented on [[apps-multilang-stores-config-modal]]; the copy-vs-translate sync mechanics on [[apps-multilang-main-translation-engine]].

### Permission

Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang hub.
- [[apps-multilang-stores-config-modal]] — where the per-sister translate / price / method / delete toggles actually live.
- [[apps-multilang-main-translation-engine]] — copy-vs-translate sync, quota gating, symbol cost accounting.
- [[apps-multilang-stores]] — sister-site management.
- [[apps-multilang-products]] — per-product translation status + manual re-sync.
- [[apps-multilang-progress]] — sync progress + actual quota consumption.
- [[plan-gates]] — `multilang_product_copy` + `multilang_product_translate` quotas.

## Open questions

None — per-field toggle behaviour is documented on [[apps-multilang-stores-config-modal]].
