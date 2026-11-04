---
type: entity
nav_path: "Entity → Discount Code → Customer binding"
aliases: ["Single-customer code", "Personal discount code", "Code for one customer", "Персонален код за отстъпка", "Код за конкретен клиент"]
tags: [entity, marketing, discounts, codes, customers]
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-code]]. See the hub for the other aspects (two-table model, usage limits, lifecycle, API access).

# Discount Code — customer binding

## Identity

This aspect covers how a Discount Code is restricted to a **specific customer** — the "issue Maria a personal 20% code" scenario. **There is NO `customer_email` column** on either the Container `discount_codes` table or the Code PRO `discounts_code_pro` table. Customer groups are checked.

## Aliases

- **Single-customer code** / **Personal code** — a code that only one specific customer can redeem.
- **Registered-users-only code** — the `only_customer` restriction, enforced for codes at entry.

## Key Attributes

What applies to a code at redemption:

| Mechanism | What it does | Scope |
|-----------|--------------|-------|
| `customer_groups[]` restriction | Checked for codes. Limits redemption to a list of customer groups. | The discount. |
| `only_customer` flag | Limits the code to registered customers, at entry: *"The code is valid only for registered users"*. | The discount or a Code PRO code. |
| `maxused_user` cap | Per-customer limit for logged-in customers. On Code PRO it counts across the whole campaign. See [[discount-code-entity-usage-limits]]. | The discount or a Code PRO code. |


### How a merchant issues a personal code

Merchants who want to issue *"a personal 20% off code for Maria"* create a customer group, assign Maria to it, and limit the discount to that group, because groups are checked.


## Where it appears

- [[marketing-discounts-code-pro]] — Code PRO management; exposes `only_customer` and `maxused_user` per code.
- [[marketing-discounts]] — the Discount edit form exposes the customer-group restriction and the customer picker.
- [[customer]] — the customer records and their groups.
- The cart's coupon field — where the logged-in / guest distinction is enforced at redemption.

## Related

- [[discount-code]] — hub.
- [[discount]] — carries the customer-group restriction and the customer list.
- [[customer]] — `maxused_user` counts per customer record.
- [[checkout-flow]] — where the logged-in-vs-guest distinction is enforced.

## Open Questions

None.
