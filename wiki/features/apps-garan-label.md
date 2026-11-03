---
type: feature
nav_path: "Apps → GARAN Label"
route_name: apps.garan_label.overview
route_path: /admin/apps/garan_label
aliases: ["GARAN Label", "GARAN", "EU durability label", "Commercial guarantee of durability", "Durability guarantee", "Directive 2024/825", "Guarantee label", "Етикет GARAN", "ГАРАН", "Гаранция за издръжливост", "Търговска гаранция за издръжливост", "Етикет за гаранция", "Законова гаранция"]
tags: [apps, compliance, products, guarantee, eu-regulation]
plan_gates: ["garan_label_quota"]
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

# GARAN Label

## Purpose

**GARAN Label**: *"Renders the official EU harmonised GARAN label for a commercial guarantee of durability (Directive (EU) 2024/825)."* A merchant who sells products with a manufacturer's durability guarantee longer than the statutory 2 years records it per product, and the app shows the official label on the storefront, at checkout and in the order confirmation. Legal basis: Directive (EU) 2024/825 and Implementing Regulation (EU) 2025/1960, applying from 27 September 2026.

## Where to find it

Sidebar → **Apps → GARAN Label**. Permission `apps`.

| Tab | Path | Route name | When |
|---|---|---|---|
| Overview | `/admin/apps/garan_label` | `apps.garan_label.overview` | Always |
| **Plan & prices** | `/admin/apps/garan_label/plan` | `apps.garan_label.plan` | Always, also during set-up |
| Settings | `/admin/apps/garan_label/settings` | `apps.garan_label.settings` | Always |
| Products | `/admin/apps/garan_label/products` | `apps.garan_label.products` | After set-up |
| Bulk generation | `/admin/apps/garan_label/bulk` | `apps.garan_label.bulk` | After set-up |

## Sub-pages (in this cluster)

- [[apps-garan-label-products]] — records per product, bulk generation, printing A4 sheets, imports.
- [[apps-garan-label-quota]] — the free 10 records, the tiers, what happens at the limit or after a lapse.
- [[apps-garan-label-storefront]] — the label on the product page, at checkout and in the email; the legal guarantee notice.

## What the merchant can do here

- Complete set-up: declare eligibility and choose how the label is shown.
- Record guarantees per product, or for many at once by category and vendor.
- Print labels on an A4 sheet.
- See the record limit and change plan.

## Settings & fields

### Set-up (Settings tab)

*"Welcome — set up GARAN Label"*. *"Confirm the guarantee qualifies for GARAN and choose how the label is shown on your storefront."*

**GARAN eligibility.** *"Confirm the commercial guarantee meets the GARAN criteria. This is your declaration — it is recorded but not verified by us; you are responsible for its accuracy."* Four switches, on by default:

| Switch | Key |
|---|---|
| The guarantee is given by the manufacturer | `eligibility_manufacturer` |
| It is free of charge | `eligibility_free` |
| It covers the whole product under normal use | `eligibility_whole_product` |
| It is expressed in years and is longer than 2 years | `eligibility_years` |

The first save, **Save & activate**, ends set-up (`onboarding_step` becomes 1). The switches are recorded, and do not block the save. Only then do the on/off switch, **Products** and **Bulk generation** appear.

### Label display

| Field | Key | Options |
|---|---|---|
| **Display format** | `display_type` | `nested`, the default: *"Compact badge; expands to the full label on click / tap (EU-recommended online)."* `full`: *"Full label rendered inline under the product."* |
| **Default model identifier** | `default_model_source` | `sku`, the default, or `barcode`. What prints as the label's model identifier. |

## Business rules

- **App Store badge.** The card and intro show **Free for the first 10 products** instead of "Free" (verify) ([[apps-garan-label-quota]]).
- **The label is only for a commercial guarantee of durability** over 2 years, in whole or half years, given by the manufacturer. The statutory 2-year guarantee is covered by the legal notice ([[apps-garan-label-storefront]]).
- **Records live in the app.** Guarantees are managed on the app's **Products** tab.
- In the administration category.

## Related

- [[apps]] — App Store.
- [[products-editor]] — the product's vendor, SKU and barcode, which the label needs.
- [[checkout]] — where the label and notice appear before purchase.
- [[aftercare-withdrawals-admin]] — the EU withdrawal flow, a related consumer-law app.

## Open questions

- None.
