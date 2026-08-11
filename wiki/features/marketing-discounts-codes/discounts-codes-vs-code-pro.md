---
type: feature
nav_path: "Marketing → Discounts → Container codes → vs Code PRO"
route_name: discounts-codes_list
route_path: /admin/marketing-new/discounts/codes
aliases: ["Container codes vs Code PRO", "Which coupon engine", "Single-use vs multi-code engine", "Контейнерни кодове или Code PRO", "Избор на купон механизъм"]
tags: [marketing, discounts, coupons, container, code-pro, comparison]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Container codes vs Code PRO — which engine to use

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, redemption, and parent-term inheritance.

## Purpose

CloudCart has two bulk-coupon engines, and merchants regularly ask which to use. This aspect lays out the difference: **Container codes** are identical-terms, mass-generated, single-use coupons; **Code PRO** codes each carry their own terms, restrictions, and date windows. The choice hinges on whether every code in the campaign shares the same discount or needs to differ.

## Where to find it

Container codes live under a Container discount at `/admin/marketing-new/discounts/codes` (see [[discounts-codes-list-view]]). Code PRO is a separate discount type — see [[marketing-discounts-code-pro]] and its generator [[marketing-discounts-code-pro-generator]].

## What the merchant can do here

- **Pick Container codes** when the whole batch shares one discount level and each code redeems once.
- **Pick Code PRO** when codes need different discount levels, per-code restrictions, per-code usage limits, or custom code shapes.

## Settings & fields

This is a comparison aspect; the concrete fields are on each engine's own pages. The decision table:

| Dimension | Container codes | Code PRO |
|-----------|-----------------|----------|
| **Terms per code** | Identical — inherited from the parent Container (see [[discounts-codes-parent-terms]]). | Each code carries its **own** discount terms, regions, customer groups, and date windows. |
| **Redemptions per code** | Single-use (one code, one order). | Configurable per code via `max_uses` and `maxused_user`. |
| **Code shape** | Hard-coded 10-char `[A-Z0-9]` (see [[discounts-codes-generator]]). | Prefix / suffix / length / range / random controls via [[marketing-discounts-code-pro-generator]]. |
| **Batch cap per request** | 1,000 on the **legacy** generator; the modern Vue modal has no upper cap. | The admin generator caps **both** modes — random (code count) and range (span) — at the `discount-code-pro-generator` plan-feature value (default 5,000). Only the JSON-API v2 *range* path has no count cap. |
| **CSV export** | Use the standard table-export of the codes listing. | Dedicated CSV export — see [[marketing-discounts-code-pro-export]]. |
| **Cart stacking** | Multiple Container codes can stack in one cart, up to the parent's cap (see [[discounts-codes-redemption]]). | Stand-alone code; entering one clears any Container codes in the cart. |

## Business rules

- **Same plan feature for the parent, different per-code limits.** Both engines are code-based discounts gated by `discount_coupon` for creating the parent (see [[discounts-codes-parent-terms]]). Code PRO additionally gates generation volume on `discount-code-pro-generator`.
- **Mutually exclusive in the cart.** A cart holds either Container codes or one stand-alone (Promo / Code PRO) code — never both at once. See [[discounts-codes-redemption]] for the array-vs-single mechanics.
- **Rule of thumb.** Same discount for everyone, click-to-apply mailout → Container codes. Different discounts per recipient, multi-use codes, or custom code shapes → Code PRO.

## Related

- [[marketing-discounts-codes]] — hub.
- [[marketing-discounts-code-pro]] — the per-code-terms engine.
- [[marketing-discounts-code-pro-generator]] — Code PRO bulk generator with shape controls.
- [[marketing-discounts-code-pro-export]] — Code PRO CSV export.

## Open questions

No outstanding questions.
