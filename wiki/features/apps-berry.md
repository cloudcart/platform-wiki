---
type: feature
nav_path: "Apps → Berry"
route_name: apps.berry
route_path: /shipping/berry
aliases: ["Berry", "Berry courier"]
tags: [apps, shipping, deprecated, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 1
---
# Berry (DEPRECATED / NOT IN USE)

## Purpose

**This app is NOT in active use on the platform.** Merchants should NOT install or rely on it. The integration remains in the codebase but is not part of the actively supported shipping-provider set.

## Where to find it

The app may still appear in the App Store catalogue but is effectively inert. Merchants should use the regionally-appropriate active alternatives below.

## What the merchant can do here

- **DO NOT use.** Pick an active courier integration instead:
  - Bulgaria: [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-dpdbulgaria-speedy]].
  - Romania: [[apps-sameday]], [[apps-cargus]], [[apps-fancourier]], [[apps-dpdromania]].
  - Multi-country EU: [[apps-gls]], [[apps-sendcloud]], [[apps-dhl]], [[apps-dhlexpress]].

## Settings & fields

Not applicable — the integration is deprecated.

## Business rules

Deprecated. No SLA / support on this integration.

## How it works (verified against backend)

### Status
Berry remains in the CloudCart codebase but is not part of the actively supported shipping-provider set. Merchants who never installed it will not see it as a recommended option; merchants who configured it historically may still have residual data tied to it.

### What replaces Berry
Merchants should pick an active courier integration from the recommended list above (Econt, Speedy, BoxNow, DPD Bulgaria, Sameday, Cargus, Fan Courier, DPD Romania, GLS, Sendcloud, DHL, DHL Express). For historical orders that already used Berry, the data remains in the order record but no new waybills can be generated.

### Codebase footprint (deprecated)
The Berry module remains in the codebase under the theme templates with **legacy Smarty `.tpl` templates only** and the platform code. There is **NO modern Vue surface** under `vuejs-sitecp/src/CcModules/Shipping/Providers/` — Berry was never migrated to the modern admin UI. In the platform code Berry is registered with `active: 0` (`tracking_link` → `https://sandbox.berry.bg/bg/t/{$tracking_number}` — a SANDBOX URL, another sign the integration is not production-active). This confirms its deprecated status: any merchant who would try to install it would land on legacy Smarty pages, not the modern OmniShip experience.

Berry should NOT be promoted, recommended, or installed. Documenting this purely for historical / support-ticket completeness.

## Per-channel delivery pricing

Berry delivers to **address** and to **office** — each of its **2** delivery channels (to **address** and to **office**) is a separate rate card with its own enable toggle (`to_address` / `to_office`) and a **Delivery price calculation** type. The selectable types (the platform-standard set shared by the courier integrations):

- `calculator` — real-time Berry quote (automatic calculation of the delivery price).
- `calculator_fixed` — the Berry quote plus a fixed **processing fee** the merchant enters.
- `calculator_free` — the Berry quote, but **free to the customer above a minimum-order-value** threshold.
- `fixed_price` — a merchant rate table keyed by **cart subtotal** tiers (the courier quote is ignored).
- `fixed_weight` — a merchant rate table keyed by **weight** tiers.
- `price_and_weight` — a merchant rate table combining **both** subtotal and weight.

Each card also exposes a **fallback price** sub-switch (a rate table used when the chosen type yields no price) and **category-condition** sub-switches (different rates for chosen product categories). The rate-table mechanics are shared — see [[shipping-calc-rate-models]] and [[shipping-calc-carrier-integrations]].

## Related

- [[apps]] — App Store hub.
- [[shipping]] — shipping providers landing.
- [[apps-deprecated]] — deprecated apps hub.

## Open questions

_None — all questions answered above._
