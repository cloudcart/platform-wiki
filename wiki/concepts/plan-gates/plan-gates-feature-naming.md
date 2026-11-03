---
type: concept
nav_path: "Concept → Plan gates → Feature naming & configuration"
aliases: ["Plan feature naming", "Plan feature mapping conventions", "Feature key prefixes", "Plan feature prefixes", "Where plan gates are configured", "Who configures plan gates", "Конвенции за имена на функции", "Конфигуриране на лимити"]
tags: [billing, plans, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-gates]]. See the hub for the other aspects (restriction shapes, enforcement points, LTA contracts, trial / catalogs).

# Plan gates — feature naming & configuration

## Definition

The ~200 plan-feature mappings follow **consistent naming prefixes**, so the feature key in an HTTP 402 payload (`info.key` — see [[plan-gates-enforcement-points]]) usually tells you what category of gate fired. And separately: the merchant does **not** configure plan gates directly — they are catalog-defined by CloudCart staff. The merchant's only levers are which plan to be on and which feature packs to add.

## Scope

What this covers:

- The plan-feature mapping naming conventions (the prefix families).
- Where — and by whom — plan gates are configured (catalog-defined, not merchant-editable).
- The merchant's actual levers: plan choice, feature packs, services, app subscriptions.

What it does NOT cover:

- The three restriction shapes a mapping can take — see [[plan-gates-restriction-shapes]].
- Where the gate runs and what it returns — see [[plan-gates-enforcement-points]].
- The full catalog of which packs exist per feature — see [[plan-features]].
- LTA-contract negotiated values — see [[plan-gates-lta-contracts]].

## Contrasts

- **Naming convention vs. restriction shape**: the prefix (`discount_*`, `*_report`) tells you the feature *category*; the restriction shape (boolean / numeric — see [[plan-gates-restriction-shapes]]) tells you how it's *enforced*. A `*_report` feature is usually boolean; a `discount_*` feature is usually numeric. The two classifications are orthogonal.
- **Catalog-defined gates vs. merchant-editable settings**: ordinary store settings ([[settings-cart]], notifications, etc.) are merchant-editable; plan-gate values are NOT — they're set by CloudCart staff in the plan catalog and (for LTA merchants) negotiated in the contract.

## Where it applies

### Plan-feature naming conventions

Plan-feature mappings follow consistent prefixes:

- **Entity counters**: bare noun — `products`, `customers`, `vendors`, `categories`, `administrators`.
- **App-specific**: app-key prefix — `mailchimp`, `cloudio_ai`, `viber_messages`, `xml_sync_limit`, `multi-warehouse`.
- **Per-discount-type**: `discount_*` — `discount_global`, `discount_coupon`, `discount_fixed`, `discount_quantity`.
- **Per-cart-rule sub-feature**: `cart_rules_*` — `cart_rules_total`, `cart_rules_range`, `cart_rules_conditions`, `cart_rules_actions`.
- **Per-ERP-app product cap**: `<erp>_total_products` — `gensoft_total_products`, `microinvest_total_products`, `colibri_total_products`, `etsy_total_products`.
- **Boolean toggles**: descriptive — `ssl_certificate`, `storefront_builder`, `subscriber_forms`, `abandoned_notification`, `authorize_payment`, `support_meetings`.
- **Reports**: `*_report` — `sale_report`, `product_report`, `payment_report`, `customer_report`.

These prefixes map directly to the categories listed on the [[plan-gates]] hub's "Where it applies" section (numeric quotas, boolean features, service / consumable quotas).

### Where the merchant configures plan gates

The merchant does NOT directly configure plan gates — they're catalog-defined by CloudCart staff. The merchant's choice is which plan to be on ([[plans]] → [[plans-purchase]]) and which feature packs to add ([[plan-features]]). Some features are also tied to one-off **services** ([[plan-services]]) or **app subscriptions** ([[plan-apps]]). The pack-vs-upgrade trade-off is covered on [[plan-vs-feature-pack]].

For LTA-contract merchants, the gate values are negotiated as part of the contract — still not directly editable in the admin UI. See [[plan-gates-lta-contracts]].

## Related

- [[plan-gates]] — hub.
- [[plan-feature]] — the Plan-Feature entity catalog these mappings live in.
- [[plan-features]] — the feature-pack upsell screen; one of the merchant's levers.
- [[plans]] / [[plans-purchase]] — the plan-choice lever.
- [[plan-services]] / [[plan-apps]] — paid services / app subscriptions tied to some features.
- [[plan-vs-feature-pack]] — the pack-vs-upgrade decision.
- [[discount-stacking]] — explains the `discount_global` vs. `discount_coupon` counter split.

## Open Questions

None.
