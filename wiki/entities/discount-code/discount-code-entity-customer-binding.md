---
type: entity
nav_path: "Entity → Discount Code → Customer binding"
aliases: ["Single-customer code", "Personal discount code", "DiscountToCustomer binding", "Code for one customer", "Персонален код за отстъпка", "Код за конкретен клиент"]
tags: [entity, marketing, discounts, codes, customers]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-code]]. See the hub for the other aspects (two-table model, usage limits, lifecycle, API access).

# Discount Code — customer binding

## Identity

This aspect covers how a Discount Code is restricted to a **specific customer** — the "issue Maria a personal 20% code" scenario. The critical fact: **there is NO `customer_email` column** on either the Container `discount_codes` table or the Code PRO `discounts_code_pro` table. Older wiki phrasing referenced a `customer_email` column for single-customer codes — no such column exists. Per-customer binding is implemented through other mechanisms, all of which are **customer-ID-based or group-based, never an email string**.

## Aliases

- **Single-customer code** / **Personal code** — a code that only one specific customer can redeem.
- **Registered-users-only code** — the `only_customer` (Code PRO) variant that excludes guest checkouts.

## Key Attributes

The four mechanisms for binding a code to a customer (or restricting who may redeem it):

| Mechanism | What it does | Scope |
|-----------|--------------|-------|
| `DiscountToCustomer` join table | Many-to-many association from a parent Discount to specific customer records, **by customer ID, not email**. The checkout flow matches the logged-in customer's ID. | Parent Discount (applies to all its codes). |
| `customer_groups[]` restriction | Limits redemption to a list of customer groups (entity-level, not email). | Parent Discount. |
| `only_customer` flag | When set, hides the code from guest checkouts entirely. | Code PRO code (per-code). |
| `maxused_user` cap | Caps redemptions per `customer_id`. | Code PRO at the per-code level; Container inherits from parent. See [[discount-code-entity-usage-limits]]. |

### The must-be-logged-in rule

For `DiscountToCustomer` binding, the customer must be **logged in** for the binding to apply. A guest entering the same email as a bound customer will **NOT** receive the discount unless they sign in. There is no email-string match column; the binding is always customer-ID-based.

### How a merchant issues a personal code

Merchants who want to issue *"a personal 20% off code for Maria"* must do one of:

1. Create a custom customer group, assign Maria to it, and bind the parent Discount to that group, OR
2. Bind the parent Discount to Maria's customer record via the `DiscountToCustomer` join, OR
3. Use a Code PRO discount with a unique code string distributed only to Maria + set `maxused_user = 1`.

## Where it appears

- [[marketing-discounts-code-pro]] — Code PRO management; exposes `only_customer` and `maxused_user` per code.
- [[marketing-discounts]] — the Discount edit form exposes the customer-picker that writes the `DiscountToCustomer` join and the customer-group restriction.
- [[customer]] — the customer records a code can be bound to.
- The cart's coupon field — where the logged-in / guest distinction is enforced at redemption.

## Related

- [[discount-code]] — hub.
- [[discount]] — parent Discount; carries the `DiscountToCustomer` join and customer-group restriction.
- [[customer]] — codes are bound to customer records by ID.
- [[checkout-flow]] — where the logged-in-vs-guest distinction is enforced.

## Open Questions

- ⏸️ The exact precedence when both a `DiscountToCustomer` binding AND a customer-group restriction (on the parent Discount) are set — does the cart check both, or does one take priority?
