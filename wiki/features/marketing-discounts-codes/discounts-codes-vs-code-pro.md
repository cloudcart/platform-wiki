---
type: feature
nav_path: "Marketing → Discounts → Container codes → vs Code PRO"
route_name: discounts-codes_list
route_path: /admin/marketing/discounts/codes
aliases: ["Container codes vs Code PRO", "Which coupon engine", "Shared pool vs per-code terms", "Контейнерни кодове или Code PRO", "Избор на купон механизъм"]
tags: [marketing, discounts, coupons, container, code-pro, comparison]
plan_gates: ["discount-container", "discount_global", "discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

# Container codes vs Code PRO — which engine to use

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, redemption, and parent-term inheritance.

## Purpose

CloudCart has two bulk-coupon engines, and merchants regularly ask which to use. This aspect lays out the difference: **Container codes** are a mass-generated, reusable, store-wide pool with only a percent per code; **Code PRO** codes each carry their own terms, restrictions, usage limits and date windows. The choice hinges on whether codes need more than their own percent.

## Where to find it

Container codes are one store-wide list at `/admin/marketing/discounts/codes` (see [[discounts-codes-list-view]]). Code PRO is a separate discount type — see [[marketing-discounts-code-pro]] and its generator [[marketing-discounts-code-pro-generator]].

## What the merchant can do here

- **Pick Container codes** when every code just needs a percent, shares one target and date window, and needs no usage limit.
- **Pick Code PRO** when codes need different targets or discount types, per-code restrictions, per-code usage limits, or custom code shapes.

## Settings & fields

This is a comparison aspect; the concrete fields are on each engine's own pages. The decision table:

| Dimension | Container codes | Code PRO |
|-----------|-----------------|----------|
| **Terms per code** | Its own percent only; target, dates and region come from the Container that wins at checkout (see [[discounts-codes-parent-terms]]). | Each code carries its **own** discount terms, regions, customer groups, and date windows. |
| **Redemptions per code** | No limit: reusable until turned off or deleted. | Configurable per code via `max_uses` and `maxused_user`. |
| **Code shape** | Hard-coded 10-char `[A-Z0-9]` (see [[discounts-codes-generator]]). | Length / range / random controls via [[marketing-discounts-code-pro-generator]]. |
| **Batch cap per request** | The admin modal has no upper limit; JSON-API v2 generate takes up to 1,000 per call. | The admin generator caps **both** modes — random (code count) and range (span) — at the `discount-code-pro-generator` plan-feature value (default 5,000). JSON-API v2 caps random mode at 5,000 per call; its *range* path has no count cap. |
| **CSV export** | Use the standard table-export of the codes listing. | Dedicated CSV export — see [[marketing-discounts-code-pro-export]]. |
| **Cart stacking** | Multiple Container codes can stack in one cart, up to the value of the winning Container (see [[discounts-codes-redemption]]). | Stand-alone code; entering one clears any Container codes in the cart. |

## Business rules

- **Different plan checks.** Creating a Container checks `discount-container` in the admin and `discount_global` through JSON-API v2 (see [[discounts-codes-parent-terms]]). Creating a Code PRO campaign checks `discount-code-pro` in the admin and `discount_coupon` through JSON-API v2, and the admin generator's volume is capped by `discount-code-pro-generator`.
- **Mutually exclusive in the cart.** A cart holds either Container codes or one stand-alone (Promo / Code PRO) code — never both at once. See [[discounts-codes-redemption]] for the array-vs-single mechanics.
- **Rule of thumb.** Only a percent per code, click-to-apply mailout → Container codes. Different targets or discount types per recipient, usage limits per code, or custom code shapes → Code PRO.

## Related

- [[marketing-discounts-codes]] — hub.
- [[marketing-discounts-code-pro]] — the per-code-terms engine.
- [[marketing-discounts-code-pro-generator]] — Code PRO bulk generator with shape controls.
- [[marketing-discounts-code-pro-export]] — Code PRO CSV export.

## Open questions

No outstanding questions.
