---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → UpSell List → Fields & validation"
route_name: admin.up_sell.list
route_path: /admin/marketing-new/up-sell
aliases: ["UpSell fields", "UpSell validation", "UpSell bundle exclusion", "UpSell chain re-anchor", "UpSell offer title", "Валидация на UpSell оферта"]
tags: [marketing, upsell, list, validation, fields]
plan_gates: ["upsells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-up-sell-list]]. See the hub for the other aspects (table, actions, storefront firing, plan budget).

# UpSell List — offer fields & validation

## Purpose

This aspect documents the **fields** that define an UpSell offer and the **validation rules** the platform enforces when the offer is saved. One rule is load-bearing and easy to trip over: **bundles cannot be a trigger or an offer**.

## Where to find it

The offer fields are edited in the edit modal of [[marketing-up-sell-diagram]] (opened from the UpSell List). The validation runs server-side on the create / edit request behind `/admin/marketing-new/up-sell`.

## What the merchant can do here

The merchant fills the offer fields per node — internal title, customer-facing offer title, trigger variant, offer variant, an optional active-from / active-to window, popup colors, and an optional confetti effect. Each field is validated on save; failures return an inline error message.

## Settings & fields

### Validation

- **Internal title** (`up_sell.name`): required, 2-191 chars.
- **Offer title** (`up_sell.offer_title`): required, 2-191 chars.
- **Trigger variant** (`up_sell.trigger_variant_id`): required, must exist in `products_variants`, **must NOT be a bundle** — *"Bundles is not supported. Please, select product"*.
- **Offer variant** (`up_sell.offer_variant_id`): same as trigger — required, exists, not a bundle.
- **Active from / active to**: must match the site's date format; `active_from` cannot be in the past; `active_to` cannot be before today.
- **Colors** (`background`, `text_color`, `button_background`, `button_text_color`): must each be a valid hex color.
- **Confetti popup effect** (`popup_effect`): optional, must be one of the supported effect keys.

## Business rules

### Bundles cannot be an UpSell trigger or offer

The UpSell request registers a custom `not_bundle` validation rule that loads the picked variant and rejects if its product is a bundle-type product. So the merchant cannot pick a bundle as the variant being replaced, **nor** as the variant offered as the upgrade. The error message is *"Bundles is not supported. Please, select product."* Cross-Sell's product autocomplete excludes bundles too (see [[marketing-cross-sell]]).

If a previously valid variant is later converted to a bundle, the existing UpSell record continues to live in the database, but storefront-side it will not match — the offer / trigger checks include the visible scope, which excludes invalid records.

### Event picker is implicit

Unlike Cross-Sell (which has six selectable events), UpSell has a hard-coded trigger: *"customer added a specific product variant to cart"*. There is no event field on the UpSell record — the model focuses entirely on the trigger-variant / offer-variant pair. Any `event` shown in the diagram for an UpSell node comes from a Cross-Sell parent (if any).

## Related

- [[marketing-up-sell-list]] — hub.
- [[marketing-up-sell-diagram]] — the edit modal these fields live in.
- [[upsell-list-actions]] — create / edit actions that submit this form.
- [[marketing-cross-sell]] — Cross-Sell engine; also excludes bundles and uses selectable events.
- [[products-products]] — products picked as trigger / offer variants.

## Open questions

No outstanding questions.
