---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → Cross-Sell List → Validation"
route_name: admin.cross_sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross-Sell validation", "Cross-Sell required fields", "Cross-Sell offer field rules", "Cross-Sell products limit", "Cross-Sell discount type validation"]
tags: [marketing, cross-sell, validation, fields]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-cross-sell-list]]. See the hub for the other aspects (grid & metrics, actions, plan budget).

# Cross-Sell List — validation & required fields

## Purpose

This aspect documents the **required-field set** the platform enforces when a merchant creates or edits a Cross-Sell offer from the diagram editor. Although the offer is built inside the diagram (see [[marketing-up-sell-diagram]]), the validation is what gates a successful save and what produces the error messages a merchant sees — so it is documented here against the list cluster.

## Where to find it

The validation runs server-side on the Cross-Sell store / update endpoint reached when the merchant saves the offer in the editor (opened from the Cross-Sell List at `/admin/marketing-new/cross-sell`). Errors surface inline on the modal fields.

## What the merchant can do here

The merchant fills in the offer fields in the diagram side-panel; on save, each field below must pass validation or the save is rejected with the named error message. There are no partial saves — targets, actions, and meta are wired in a single DB transaction (see [[cross-sell-list-plan-budget]]).

## Settings & fields

### Required-field set (create / edit)

| Field | Key | Rule | Error mapping |
|---|---|---|---|
| Internal title | `cross_sell.name` | Required, 2-191 chars. | `global.error.validation.internal_title.*` |
| Offer title | `cross_sell.offer_title` | Required, 2-191 chars. | `cross_sell.error.validation.offer_title.*` |
| Type | `cross_sell.type` | Required, one of `simple`, `extended`. | `global.error.validation.type.in` |
| Event | `cross_sell.event` | Required, one of the 6 supported events. | Custom error lists all 6 events by translated name. |
| Targets | `cross_sell.targets.*.*.type` | Required, one of `product`, `category`, `vendor`, `selection`, `cart`, `shipping`, `payment`. | Error enumerates the allowed types. |
| Actions | `cross_sell.actions.0.*.type` | Required for the first action group; type must be one of the same set as targets. | — |
| Products limit | `cross_sell.products_limit` | Required, integer, **min 1, max 10**. Caps how many products one popup surfaces. | — |
| Max user views | `cross_sell.max_user_views` | Integer, min 0. `0` means unlimited. | — |
| Discount type | `cross_sell.discount_type` | One of `fixed`, `percent`, `shipping`, `free_product`. | Custom rule enforces a non-empty value when type is `fixed` or `percent`. |
| Active from / to | — | Must match the site's date format; `active_to` must be on/after today. | — |

The 6 supported events are `add_to_cart`, `cart`, `checkout`, `checkout_select_payment`, `checkout_select_shipping`, `return_page` — see [[marketing-cross-sell]] for what each fires on.

## Business rules

### Targets accept extra types beyond the model constant

Even though the platform code lists only `product`, `category`, `vendor`, `selection`, the request validator **also** accepts `cart`, `shipping`, `payment` as target types. These are used for cart-event triggers (e.g. "cart total > X", "shipping method = courier Y", "payment method = card") where the trigger is the cart's state, not a product/category. Without these extra types, the cart-flow events (`cart`, `checkout`, `checkout_select_payment`, `checkout_select_shipping`) couldn't have target conditions wired at all.

### Discount type conditionally required

`discount_type` accepts four values, but the custom rule makes a non-empty value mandatory only when the discount is `fixed` or `percent` (`shipping` and `free_product` carry the discount semantics implicitly). The discount itself integrates with [[marketing-discounts]] via the `discount_percent` / `discount_type` fields.

### Products limit is platform-wide, not plan-tiered

The `products_limit` 1-10 cap is enforced by the validator's `min:1|max:10` rule and is the same for every store — it is not a plan-tier setting. (Contrast with the *number of offers* a store may have, which IS plan-gated — see [[cross-sell-list-plan-budget]].)

### Active window

`active_from` / `active_to` must parse against the store's configured date format, and `active_to` cannot be in the past (must be on or after today). An offer outside its active window does not fire even when its Active toggle is on.

## Related

- [[marketing-cross-sell-list]] — hub.
- [[marketing-cross-sell]] — the engine; full semantics of events, targets, actions, and discount behaviour.
- [[marketing-discounts]] — discount records attached via `discount_percent` / `discount_type`.
- [[products-products]] / [[products-categories]] / [[products-vendors]] / [[products-smart-collections]] — record types accepted as `product` / `category` / `vendor` / `selection` targets and actions.

## Open questions

No outstanding questions.
