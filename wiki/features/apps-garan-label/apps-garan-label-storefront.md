---
type: feature
nav_path: "Apps → GARAN Label → what customers see"
route_name: apps.garan_label.settings
route_path: /admin/apps/garan_label/settings
aliases: ["GARAN on product page", "GARAN at checkout", "GARAN in email", "Your legal guarantee rights", "Legal guarantee notice", "GARAN badge", "Вашите права по законовата гаранция", "Законова гаранция за съответствие", "Етикет на страницата на продукта", "Гаранция за издръжливост GARAN"]
tags: [apps, compliance, storefront, checkout, emails, guarantee]
plan_gates: ["garan_label_quota"]
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-garan-label]]. See the hub for set-up and label display.

# GARAN Label — what customers see

## Purpose

Where the label and the legal guarantee notice appear for a customer. The app shows two official EU items: the **GARAN label**, per product, for the commercial guarantee of durability, and the **legal guarantee notice**, one for the store, for the legal guarantee of conformity.

## Where to find it

Nothing to place: both appear on their own once the app is active and a product has a record. **Display format** on the **Settings** tab ([[apps-garan-label]]) decides whether the label is a compact badge or shown in full.

## What the merchant can do here

- Choose the display format, and see the preview on the Settings tab.
- Limit a label to a validity period on the product's record ([[apps-garan-label-products]]).

## Settings & fields

| Place | What shows |
|---|---|
| **Product page** ([[product-detail]]) | The label, which switches with the variant. |
| **Checkout** ([[checkout]]) | A label on each line with a record, and once per order the notice link **Your legal guarantee rights** / *Вашите права по законовата гаранция*. |
| **Order confirmation email** ([[settings-emails]]) | A small badge per line linking to the full label, and a link to the notice page. |

The label carries three fields: the guarantee in years, the brand (the product's vendor) and the model identifier (SKU or barcode).

### Wording customers see

| Item | English | Bulgarian |
|---|---|---|
| Label title | GARAN durability guarantee | Гаранция за издръжливост GARAN |
| Open the full label | View the full GARAN guarantee label | Вижте пълния етикет за гаранция GARAN |
| Link on the label | Information about the commercial guarantee of durability | Информация за търговската гаранция за издръжливост |
| Notice title | Legal guarantee of conformity | Законова гаранция за съответствие |
| Link on the notice | Learn more about your legal guarantee rights | Научете повече за правата си по законовата гаранция |

## Business rules

- **A record shows when** it is active, inside its validity period if it has one, and within the record limit ([[apps-garan-label-quota]]).
- **Display format.** `nested` shows a compact badge that opens the full label on click or tap. `full` shows the label inline under the product.
- **The notice** exists in 24 EU languages, with English for the rest. At checkout it shows whenever the app is active, whatever is in the cart.
- **Before purchase.** The label and notice appear at checkout, and the email keeps a durable copy afterwards.
- **Headless storefronts.** A product on the [[headless-storefront-api|Storefront API]] has a `garanLabel` field with `years`, `months`, `labelImageUrl`, `infoUrl` and `alt`. It is null when the app is off or the product has no record that shows by the rules above.

## Related

- [[apps-garan-label]] — hub.
- [[product-detail]] — the storefront product page.
- [[checkout]] — the checkout page.
- [[settings-emails]] — customer emails.

## Open questions

None.
