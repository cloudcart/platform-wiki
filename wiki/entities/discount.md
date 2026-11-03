---
type: entity
nav_path: "Entity → Discount"
aliases: ["Discount", "Promo code", "Coupon", "Coupon code", "Promotion", "Sale", "Voucher", "Отстъпка", "Промо код", "Купон"]
tags: [marketing, discounts, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---

# Discount

## Identity

A **Discount** is a rule the merchant configures to reduce the price the customer pays. It is the central promotions object on the platform — every storefront price reduction, every coupon code at checkout, every "Buy 5, save 20%" tier, and every "Free shipping over 50 BGN" banner is a Discount in the database.

Each Discount carries:

- A **type** (`flat` / `percent` / `shipping` / `fixed` / `quantity` / `countdown` / `code-pro`) that defines HOW the rule applies. Plus the **Container** variant: `is_container = 1` on a `flat` or `percent`.
- A **target** (`all` / `product` / `category` / `vendor` / `category_vendor` / `selection` / `order_over` / `shipping`) that defines WHERE it applies.
- An optional **code** the customer must type.
- A set of **conditions** (date window, customer-group restriction, region restriction, usage caps).

At checkout, when the customer's cart matches a discount's target + conditions, the discount **attaches** to the cart (or to the specific lines it targets), and the totals are recomputed. When the order is placed, a per-order-discount row is written linking that specific order to the discount that applied — which is the audit row used by analytics and by the discount's `uses` counter.

CloudCart's Discounts are intentionally **single-condition** rules (one type, one target, one threshold) — for compositional rules with multiple triggers and actions, merchants use [[apps-cart-rules|Cart Rules]] instead. But Discounts cover the most common 80% of promotions, are simpler to configure, and have first-class support in the listing engine for "from X / now Y" price display on category pages.

## Aliases

- "Discount" — the canonical merchant-facing term in the UI and reports.
- "Promo code" / "Coupon" / "Coupon code" — typically used for code-gated discounts (the `code` field is non-null).
- "Promotion" / "Sale" — informal language ("our spring sale" is usually a Global discount).
- "Voucher" — used in some merchant communications for code-based discounts.
- Bulgarian: "Отстъпка" (the standard label), "Промо код" / "Купон" (for code-based).
- The "Discount code (PRO)" feature ([[marketing-discounts-code-pro]]) refers to a multi-code campaign where each code under the parent discount has its OWN terms — they share a parent Discount but each child code (a PRO code row) carries independent conditions.

## Key Attributes

The Discount entity is documented across five aspect pages. The high-level shape is:

- **Type** — one of 7 values: `flat`, `percent`, `shipping`, `fixed`, `quantity`, `countdown`, `code-pro` — plus the `is_container = 1` Container variant.
- **Target** — one of 8 values controlling where the rule applies.
- **Code** — optional string the customer types (case-insensitive); null = auto-apply.
- **Date window** — `date_start` / `date_end` (end nullable).
- **Usage caps** — `max_uses`, `maxused_user`, `only_customer`.
- **Restrictions** — `customer_groups[]`, `geo_zone_id`, `force_save`.
- **Lifecycle flag** — `active = yes | no`.
- **Display fields** — visual presentation (`color`, `text_color`, `position`, `countdown_minutes`, etc.).

For the full verbatim field catalogue, including validation strings and the cents-based amounts, see [[discount-entity-fields]].

## Sub-pages (in this cluster)

This entity is split into 5 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[discount-entity-fields]] — verbatim field set with validation strings (identity, type & target, code, usage caps, restrictions, display).
- [[discount-entity-lifecycle]] — states (`scheduled` / `active` / `expired` / `inactive`), 10-minute activation cooldown, per-product attachment regeneration, `uses` recompute, counted statuses, Code PRO sub-lifecycle.
- [[discount-entity-business-rules]] — one-per-store limits, plan-gating per type, save-time normalisation, force-save, container code consumption, cart code mutual-exclusion, currency caps, soft-delete cascade.
- [[discount-entity-stacking-evaluation]] — `code_apply` default-off rule, `apply_regular_price` max-of-two filter, Discounts-before-Cart-Rules ordering, stand-alone XOR Container codes per cart.
- [[discount-entity-webhooks-api]] — `discount.created` / `discount.updated` / `discount.deleted` webhooks, internal `DiscountStatusChange` event, JSON-API v2 endpoints + same-side-effects + 5-type allowlist (`percent` / `flat` / `fixed` / `shipping` / `code-pro`).

## Where it appears

- [[marketing-discounts]] — the master list and primary CRUD screen.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] / [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] — per-type editor screens.
- [[marketing-discounts-code-pro]] — multi-code campaign (PRO).
- [[marketing-discounts-code-pro-generator]] — bulk code generator for PRO.
- [[marketing-discounts-code-pro-export]] — export PRO codes for distribution.
- [[marketing-discounts-codes]] — Container codes list (mass-generated single-use codes).
- [[marketing-discounts-products]] — per-product price-override sub-page for Fixed discounts.
- [[orders-discount-add]] — apply a discount to an existing order from the admin (creates a per-order-discount row).
- [[orders-details]] — discount action row shows order-level discounts; line-level rows show product-level discounts.
- [[apps-cart-rules]] — companion engine for compositional rules; Cart Rules evaluate AFTER Discounts at checkout.
- [[marketing-segments]] — segment conditions can reference discount usage (e.g., "customers who used promo X").
- [[marketing-campaigns]] — campaigns can embed dynamic PRO codes in their messages.
- [[apps-up-cross-sell]] — cross-sell offers can reference discounts.
- [[products-banners-labels]] — banners and labels are discount-type rows but pure-visual (not price reductions).
- [[analytics-top-order-discounts]] / [[analytics-top-order-product-discounts]] — analytics dashboards aggregating discount usage.
- [[api-discounts]] — JSON-API v2 endpoint.

## Related

- [[discount-code]] — entity page for a Container child code.
- [[order]] — orders carry zero-or-more discounts via per-order-discount audit rows.
- [[customer]] — customer-group and per-customer-cap restrictions apply against this entity.
- [[customer-group]] — `customer_groups[]` restriction.
- [[geo-zone]] — `geo_zone_id` restriction.
- [[product]] — discount targets reference product IDs (and the product's per-variant fixed-discount rows).
- [[category]] — discount targets reference category IDs.
- [[vendor]] — discount targets reference vendor (brand) IDs.
- [[smart-collection]] — `selection`-target discounts reference smart-collection IDs.
- [[cart]] — discount evaluation happens against the cart at checkout.
- [[cart-rule]] — companion entity for compositional rules; Cart Rules evaluate AFTER Discounts.
- [[discount-stacking]] — concept page on stacking semantics.
- [[discount-stacking-code-apply]] — concept page on `code_apply`.
- [[discount-stacking-evaluation-order]] — concept page on Discounts-before-Cart-Rules ordering.
- [[checkout-flow]] — the storefront flow that applies discounts.
- [[settings-statuses]] — `discounts_used_statuses` setting determines which order statuses count toward `max_uses`.
- [[settings-hooks]] — `discount.*` webhooks.
- [[plan-gates]] — per-type plan-feature counters.
- [[json-api-v2]] — API concept (auth, rate-limit, same-side-effects).

## Open Questions

- ⏸️ **Auto-cleanup of expired Container codes** — see [[discount-entity-lifecycle]].
- ⏸️ **Bulk-export of Container codes format** — see [[discount-entity-business-rules]].
