---
type: entity
nav_path: "Entity → Discount Code"
aliases: ["Discount Code", "Coupon code", "Promo code", "Code", "Voucher code", "Промо код", "Код за отстъпка", "Купон"]
tags: [entity, marketing, discounts, codes]
created: 2026-05-21
updated: 2026-06-10
source_count: 3
---
# Discount Code

## Identity

A **Discount Code** is a redeemable string the customer enters at checkout to activate a [[discount|Discount]] (e.g., "SUMMER20", "WELCOME10", "BLACKFRIDAY"). It is the customer-facing handle of a discount: the merchant runs an email campaign saying "use code SUMMER20", the customer types it into the cart's coupon field, and the platform attaches the corresponding Discount to the cart. Without the right code, the discount stays inactive — even if all other conditions match.

A single Discount can have **one** code (the classic case: discount + code = 1:1) or **many** codes ([[marketing-discounts-codes|Container codes]] sharing the parent's terms, or [[marketing-discounts-code-pro|Code PRO codes]] where each code carries its OWN terms — price, conditions, customer restriction). The Code carries the redeemable string itself, the per-code use cap, the running uses counter, the per-code expiry, and the customer restriction. The actual discount mechanics — what % off, on which products, the order-over threshold — live on the parent [[discount|Discount]] for Container codes, and on the Code itself for Code PRO.

**The single most important structural fact:** Container codes and Code PRO codes live in two SEPARATE tables with different field sets. The two are not interchangeable, and most "why doesn't this code field exist" confusion traces back to mixing them up. See [[discount-code-entity-tables]].

## Aliases

- **Discount Code** — the canonical merchant-facing term in the admin UI.
- **Coupon code** / **Promo code** / **Code** — informal merchant phrasing, often used interchangeably with "Discount Code".
- **Voucher code** — used in some merchant communications.
- **Промо код** / **Код за отстъпка** / **Купон** — Bulgarian terms used interchangeably.

## Key Attributes

This entity is split across an aspect subfolder because the field model, the customer-binding mechanics, the usage caps, and the lifecycle are each a distinct concept. At a glance:

- **Two backing tables.** Container codes (the classic [[marketing-discounts-codes]] feature) carry only `code`, `discount_id`, `type` + `value`, and `active`. Code PRO codes ([[marketing-discounts-code-pro]]) carry full per-code terms — `value` / `type_value`, `conditions`, `max_uses` / `uses`, `maxused_user`, `date_start` / `date_end`, barcode mode, `active`, `force_save`, `only_customer`. Container codes inherit every other restriction from their parent Discount. Full table breakdown on [[discount-code-entity-tables]].
- **No `customer_email` column on either table.** Per-customer binding is done through the `DiscountToCustomer` join (customer-ID-based), customer-group restriction, the `only_customer` guests-excluded flag (Code PRO), or the `maxused_user` per-customer cap — never an email string. See [[discount-code-entity-customer-binding]].
- **Usage caps stack.** Per-code `max_uses`, per-Discount overall `usage_limit`, per-customer `usage_limit_customer`, and (Code PRO) per-code per-customer caps all check independently at checkout. See [[discount-code-entity-usage-limits]].
- **Case-insensitive redemption.** Codes match regardless of case typed; the code is valid only while active, unexpired, and under its caps. See [[discount-code-entity-lifecycle]].

## Sub-pages (in this cluster)

This entity is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[discount-code-entity-tables]] — the two-table model (Container `discount_codes` vs Code PRO `discounts_code_pro`); the exact field set on each; which restrictions are inherited from the parent vs carried per-code.
- [[discount-code-entity-customer-binding]] — why no `customer_email` column exists; the four ways to bind a code to a specific customer (`DiscountToCustomer` join, customer-group, `only_customer`, `maxused_user`); the must-be-logged-in rule.
- [[discount-code-entity-usage-limits]] — `max_uses` / `uses` semantics; counted-status increments; Code PRO recompute-vs-increment behavior (cancelled orders auto-free Code PRO slots, not Container); the four interacting caps.
- [[discount-code-entity-lifecycle]] — the six states (generated → active → exhausted → expired → inactive → deleted); case-insensitive matching; coupon-field-only redemption (no auto-apply); deletion preserving order history.
- [[discount-code-entity-api]] — JSON-API v2 access via the two resources ([[api-discount-codes]] Container, [[api-discount-codes-pro]] Code PRO); the same-side-effects principle; where regular promo codes live instead.

## Where it appears

- [[marketing-discounts-codes]] — the management screen for Container codes (the classic multi-code mode where codes share parent terms).
- [[marketing-discounts-code-pro]] — the management screen for Code PRO codes (each code carries individual terms).
- [[marketing-discounts-code-pro-generator]] — bulk code generation for Code PRO.
- [[marketing-discounts-code-pro-export]] — bulk export of Code PRO codes (typically for distribution to partners).
- [[marketing-discounts]] — parent screen listing all discounts; the code-related columns surface here.
- Customer-facing surfaces:
  - The cart's "Coupon code" field — where the customer types the code.
  - Order confirmation emails and the order detail page — show which code was redeemed.

## Related

### Related entities

- [[discount]] — the parent Discount carries the mechanics (% off, target, conditions). Required parent.
- [[order]] — orders redeem codes; the order's discount snapshot preserves the historical code value.
- [[customer]] — codes can be bound to a specific customer; see [[discount-code-entity-customer-binding]].

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

- ⏸️ The exact merchant-visible error wording at checkout when a code is invalid vs expired vs exhausted vs not-for-this-customer — these are distinct messages but the precise text isn't fully documented (the storefront shows a generic "invalid code" for most failure modes; only `only_customer = 1 + guest`, `order_over threshold not met`, `code_apply + cart has discount` emit distinct messages). See [[discount-code-entity-lifecycle]].
