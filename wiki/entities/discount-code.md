---
type: entity
nav_path: "Entity → Discount Code"
aliases: ["Discount Code", "Coupon code", "Promo code", "Code", "Voucher code", "Промо код", "Код за отстъпка", "Купон"]
tags: [entity, marketing, discounts, codes]
created: 2026-05-21
updated: 2026-11-04
source_count: 3
---
# Discount Code

## Identity

A **Discount Code** is a redeemable string the customer enters at checkout to activate a [[discount|Discount]] (e.g., "SUMMER20", "WELCOME10", "BLACKFRIDAY"). It is the customer-facing handle of a discount: the merchant runs an email campaign saying "use code SUMMER20", the customer types it into the cart's coupon field, and the platform attaches the corresponding Discount to the cart. Without the right code, the discount stays inactive — even if all other conditions match.

A Discount can have **one** code of its own (the classic case: discount + code = 1:1), or it can use many codes: [[marketing-discounts-codes|Container codes]], one store-wide pool attached to no particular Container, or [[marketing-discounts-code-pro|Code PRO codes]], where each code carries its OWN terms — price, conditions, customer restriction. A Code PRO code carries its use cap, uses counter and expiry itself. A Container code carries only the string, its value, its type and an active flag; the rest comes from the Container discount it lands on.

**The single most important structural fact:** Container codes and Code PRO codes live in two SEPARATE tables with different field sets. The two are not interchangeable, and most "why doesn't this code field exist" confusion traces back to mixing them up. See [[discount-code-entity-tables]].

## Aliases

- **Discount Code** — the canonical merchant-facing term in the admin UI.
- **Coupon code** / **Promo code** / **Code** — informal merchant phrasing, often used interchangeably with "Discount Code".
- **Voucher code** — used in some merchant communications.
- **Промо код** / **Код за отстъпка** / **Купон** — Bulgarian terms used interchangeably.

## Key Attributes

This entity is split across an aspect subfolder because the field model, the customer-binding mechanics, the usage caps, and the lifecycle are each a distinct concept. At a glance:

- **Two backing tables.** Container codes (the classic [[marketing-discounts-codes]] feature) carry only `code`, `type` + `value`, and `active`. Code PRO codes ([[marketing-discounts-code-pro]]) carry full per-code terms — `value` / `type_value`, `conditions`, `max_uses` / `uses`, `maxused_user`, `date_start` / `date_end`, barcode mode, `active`, `force_save`, `only_customer`. Full table breakdown on [[discount-code-entity-tables]].
- **No `customer_email` column on either table.** To limit a code to one person, put them in a customer group. See [[discount-code-entity-customer-binding]].
- **Usage caps stack.** `max_uses` and `maxused_user` on the discount, and the same pair on each Code PRO code, check independently. See [[discount-code-entity-usage-limits]].
- **Case-insensitive redemption.** Codes match regardless of case typed; the code is valid only while active, unexpired, and under its caps. See [[discount-code-entity-lifecycle]].

## Sub-pages (in this cluster)

This entity is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[discount-code-entity-tables]] — the two-table model (Container `discount_codes` vs Code PRO `discounts_code_pro`); the exact field set on each.
- [[discount-code-entity-customer-binding]] — why no `customer_email` column exists; which customer restrictions a code actually checks (customer groups, `only_customer`, `maxused_user`); how to issue a personal code.
- [[discount-code-entity-usage-limits]] — `max_uses` / `uses` semantics; counted statuses; cancelled orders free a use on the discount; a Container code has no counter; the interacting caps.
- [[discount-code-entity-lifecycle]] — the six states (generated → active → exhausted → expired → inactive → deleted); case-insensitive matching; coupon field and discount link (no auto-apply); deletion preserving order history.
- [[discount-code-entity-api]] — JSON-API v2 access via the two resources ([[api-discount-codes]] Container, [[api-discount-codes-pro]] Code PRO); where regular promo codes live instead.

## Where it appears

- [[marketing-discounts-codes]] — the management screen for Container codes (the store-wide pool).
- [[marketing-discounts-code-pro]] — the management screen for Code PRO codes (each code carries individual terms).
- [[marketing-discounts-code-pro-generator]] — bulk code generation for Code PRO.
- [[marketing-discounts-code-pro-export]] — bulk export of Code PRO codes (typically for distribution to partners).
- [[marketing-discounts]] — parent screen listing all discounts; the code-related columns surface here.
- Customer-facing surfaces:
  - The cart's "Coupon code" field — where the customer types the code. A discount link (`/cart/discount:<CODE>`) also puts a code in the cart.
  - Order confirmation emails and the order detail page — show which code was redeemed.

## Related

### Related entities

- [[discount]] — the Discount carries the mechanics (% off, target, conditions).
- [[order]] — orders redeem codes; the order's discount snapshot preserves the historical code value.
- [[customer]] — who may use a code; see [[discount-code-entity-customer-binding]].

### Cross-cutting concepts

- [[discount-stacking]] — how a code-gated discount interacts with other discounts (auto-applied or other coupon codes) in the same cart.
- [[checkout-flow]] — where the customer enters the code and how the cart engine validates it.
- [[notification-delivery]] — codes are typically distributed via [[campaign|Campaigns]] (email, SMS, Viber); the campaign carries the code string in the message body.

### Settings & feature pages

- [[marketing-discounts-codes]] — Container code management.
- [[marketing-discounts-code-pro]] — Code PRO management.
- [[marketing-discounts-code-pro-generator]] — bulk generator.
- [[marketing-discounts-code-pro-export]] — bulk export.

## Open Questions

None.
