---
type: concept
nav_path: "Concept → Product compatibility & fitment"
route_name: (none)
route_path: (none)
aliases: ["Product compatibility", "Fitment", "Sell by compatibility", "Automotive store", "Car parts store", "Vehicle fitment", "Device compatibility", "Автомобилен магазин", "Авточасти", "Съвместимост", "Brand and model", "Year make model"]
tags: [compatibility, fitment, brand-model, automotive, catalog, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---
# Product compatibility & fitment

## Definition

**Product compatibility (fitment)** is the pattern of selling products by *what they fit* rather than by what they are — the customer picks their device or vehicle and sees only the products that match it. Classic cases: a **car / moto parts** shop (pick make → model → see fitting parts), a **phone-accessories** shop (pick brand → model → see cases / screens / chargers), plus laptop & PC components, camera gear, printer consumables, eyewear. CloudCart's tool for this is the installable **[[brand-model]]** app, which adds a **two-level Brand → Model** taxonomy plus a storefront brand-then-model filter.

## Scope

- The **Brand → Model** catalogue — [[brand-model-brand]] (top level: Toyota, Apple) and [[brand-model-model]] (per-brand: Corolla, iPhone 15 Pro).
- **Tagging products** with one or more models on the product editor (multi-assign; the brand is derived from the chosen model) — see [[products-products]].
- A **storefront filter** (brand → then model) on category pages, plus dedicated `/brand/<handle>/` and `/model/<handle>/` SEO pages, and a Page Builder block ([[design-module-pb-brand-model]]) to surface the picker.
- Bulk load via [[apps-csv-import]] / [[apps-xml-import]] (verify field mapping).

## Contrasts

- **Compatibility (Brand-Model) vs versions (Variants).** Brand-Model answers *"what does this product FIT?"* — one accessory fits many models. [[products-variants-options|Variants]] answer *"which version of THIS product?"* — size / colour / capacity. They are orthogonal: a phone case can be tagged to 5 models **and** have 3 colour variants.
- **Two-level cap — the key correction.** Brand → Model is the **maximum depth**; there is **no third level**. Automotive granularity below the model (year / engine / trim) is *not* a Brand-Model feature — encode it via [[products-variants-options|variants]], a naming convention on the model (e.g. "Golf VII 2013–2020"), or product parameters. Brand-Model is a *compatibility taxonomy*, not a general multi-level parameter tree.
- **Compatibility vs manufacturer.** [[products-vendors|Vendors]] = who *made* the product (flat list, one per product). Brand-Model = what the product *fits* (hierarchical, multi-assign). A case made by an OEM can fit Apple models.
- **Compatibility vs multi-attribute filtering.** Filtering by colour / material / power = product **parameters** + [[apps-advanced-search]], not Brand-Model.

## Where it applies

- The model picker on the product editor — see [[products-products]].
- Storefront category filters + the brand / model SEO landing pages.
- The Page Builder brand-model block — see [[design-module-pb-brand-model]].

## Related

- [[brand-model]] — the app hub (the engine for this concept), with [[brand-model-brand]] and [[brand-model-model]].
- [[products-variants-options]] — version-level distinctions (the deeper-than-model need).
- [[products-vendors]] — manufacturer (a separate, flat axis).
- [[apps-advanced-search]] — multi-attribute storefront filtering.

## Open Questions

- Whether year / trim is ever modelled as a Brand-Model extension or only via variants / naming (verify).
- Exact CSV / XML field mapping for bulk brand-model import (verify).
