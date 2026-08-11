---
type: entity
nav_path: "Entity → Discount Code → Lifecycle & redemption"
aliases: ["Code lifecycle", "Code states", "Code redemption", "Case-insensitive code matching", "Coupon field redemption", "Жизнен цикъл на код", "Осребряване на код"]
tags: [entity, marketing, discounts, codes]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-code]]. See the hub for the other aspects (two-table model, customer binding, usage limits, API access).

# Discount Code — lifecycle & redemption

## Identity

This aspect covers a Discount Code's lifecycle (the six states it moves through), how it is matched and redeemed at checkout, and what happens to order history when the code is deleted. The defining behavioral rules: codes match **case-insensitively**, they redeem only through the **coupon field** (never auto-apply), and deleting a code **preserves** the historical snapshot on past orders.

## Aliases

- **Code states** — generated / active / exhausted / expired / inactive / deleted.
- **Code redemption** — the customer typing the code into the cart's coupon field.
- **Code-gated discount** — a discount that requires a code to activate (vs an auto-applying discount).

## Key Attributes

### Lifecycle states

A Discount Code moves through these states:

1. **Generated** — the merchant creates the code, either manually (typed a memorable string like "SUMMER20") or via the [[marketing-discounts-code-pro-generator|Code PRO Generator]] (bulk-generated random codes). At create, the uses counter is `0`.
2. **Active** — `active = yes`, parent Discount is also `active = yes`, the per-code end date is in the future (or `null`), and the uses counter is under `max_uses` (or `max_uses = null`). The code is valid at checkout — customers entering it see the discount attach to their cart.
3. **Exhausted** — the uses counter has reached `max_uses`. The code stops working at checkout — the customer sees a "code is no longer valid" / "usage limit reached" message. Whether the counter can drop back down depends on code type — see [[discount-code-entity-usage-limits]].
4. **Expired** — the per-code end date is in the past. The code stops working at checkout regardless of the uses counter. The row stays in the database for audit and reporting.
5. **Inactive** — `active = no`. The code is manually disabled even if not exhausted / expired. Useful when the merchant wants to retract a code prematurely.
6. **Deleted** — hard-deleted. Historical orders that used the code retain their per-order discount snapshot (the code string is preserved in the order row).

### Case-insensitive matching at checkout

When a customer types a code at checkout, the platform normalizes both the typed value and the stored code before comparing. So `BLACK-FRIDAY`, `Black-Friday`, and `black-friday` all match the same code. There is no per-store opt-in to case-sensitive matching. The merchant should communicate codes in uppercase for clarity, but the cart accepts any case.

### Uniqueness scope

- **Container codes**: uniqueness is enforced **within** the parent Discount's code list, not across the entire store. Two different Discounts can each have a code called `SUMMER20`. In practice, merchants usually keep codes globally unique to avoid confusion, but the platform does not enforce it.
- **Code PRO codes**: the `code` string is **unique store-wide** (enforced at the DB level).

### Codes redeem via the coupon field — no auto-apply

A Discount with a code attached does NOT auto-apply on cart-match — the customer MUST type the code into the coupon field. Discounts without codes (e.g., a global 10% off campaign) auto-apply on cart-match. The presence of a code is what makes a discount "code-gated".

### Deletion behavior

- **Deleted codes free up for re-use immediately.** Codes are hard-deleted — there is no soft-delete or cooldown window. The same code string can be reused (under any parent Discount) immediately after deletion. The uniqueness check sees only the live rows.
- **Deletion preserves order history.** When the merchant deletes a Discount Code (or even the entire parent Discount), orders that previously used the code retain their per-order discount snapshot — the historical code string, the historical price applied, and the historical conditions are all preserved in the order row. The merchant can safely delete obsolete codes without breaking the audit trail.

## Where it appears

- [[marketing-discounts-codes]] — Container code management; the per-row `active` toggle.
- [[marketing-discounts-code-pro]] — Code PRO management; per-code `active`, `date_start` / `date_end`.
- [[marketing-discounts-code-pro-generator]] — bulk generation (the Generated state).
- The cart's "Coupon code" field — where the customer redeems the code.
- Order confirmation emails + the order detail page — show which code was redeemed (preserved even after deletion).

## Related

- [[discount-code]] — hub.
- [[discount]] — parent Discount; its own `active` flag and dates gate the code.
- [[order]] — preserves the historical code snapshot after deletion.
- [[checkout-flow]] — where the customer enters the code and the cart engine validates it.

## Open Questions

- ⏸️ The exact merchant-visible error wording at checkout when a code is invalid vs expired vs exhausted vs not-for-this-customer — these are distinct messages but the precise text isn't fully documented (the storefront shows a generic "invalid code" for most failure modes; only `only_customer = 1 + guest`, `order_over threshold not met`, `code_apply + cart has discount` emit distinct messages).
