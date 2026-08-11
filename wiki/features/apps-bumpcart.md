---
type: feature
nav_path: "Apps → Bump Cart"
route_name: apps.bumper_offer.overview
route_path: /admin/apps/bumpcart
aliases: ["Bumpcart", "Bump Cart", "Bumper Offer", "Cart upsell module"]
tags: [apps, marketing, conversion, cart, upsell]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 7
---
# Bump Cart (cart-upsell module)

## Purpose

**Bump Cart** (internal name: Bumper Offer) — adds a **goal-based motivation module** to the storefront's cart page. The module shows the customer how close they are to a target (e.g., "Spend 10 BGN more to get free shipping") and may auto-add bumper products if the customer's cart is below a threshold. Used to:

- Increase average order value via goal-gamification (free shipping at X, discount at Y).
- Encourage discovery of specific add-on products (the bumper offer).
- Push customers across a free-shipping threshold (high-conversion lever).

The module can target FOUR goal types: amount cart, total cart, free shipping, discount.

## Where to find it

Sidebar → Apps → install → **Bump Cart**. Two sub-pages:

| Sub-page | Route name | Route path |
|----------|------------|------------|
| Overview / Index | `apps.bumper_offer.overview` | `/admin/apps/bumpcart` |
| Settings ([[apps-bumpcart-settings]]) | `apps.bumper_offer.settings` | `/admin/apps/bumpcart/settings` |

(Note: the route name uses `bumper_offer` while the URL path uses `bumpcart` — the route name is the historical/internal app key; the URL is the merchant-facing slug.)

## What the merchant can do here

### Stats card
Recent activity:
- **Added products** count + sum value (e.g., "5 / 50.00 BGN" — 5 products auto-added totalling 50 BGN).
- Per-period analytics (date-range picker).
- Link to detailed reports.

### Settings — goal configuration

| Goal type | What it does |
|-----------|--------------|
| **amount_cart** | Triggers when cart total is below a minimum threshold (`checkout_min_price`). |
| **total_cart** | Targets a specific cart total amount (`total_cart_amount`). Module shows progress toward this target. |
| **free_shipping** | Targets the free-shipping threshold — encourages customer to add more to qualify. |
| **discount** | Targets a configured discount (the customer adds enough to unlock the discount). |

### Per-goal fields

When the merchant picks a goal type, additional fields appear:
- **Title** — module headline shown to customers.
- **Total cart amount** (for total_cart) — the target value.
- **Shipping discount ID** (for free_shipping) — references a free-shipping discount in [[marketing-discounts]].
- **Discount ID** (for discount) — references the target discount.
- **Bumper products** — products to auto-add when the goal applies.

### What the merchant CANNOT do here
- Run multiple bump cart modules simultaneously (single module per store).
- Run on pages other than cart (cart-only module).

## Settings & fields

Goal type (one of `amount_cart` / `total_cart` / `free_shipping` / `discount`), plus per-goal fields (above) and the bumper-product selection controls (see *How it works*). Standard apps permission scope.

## Business rules

- **One goal per instance.** The merchant picks ONE goal type, sets its target + bumper products; the customer sees progress + suggested products at cart. No multi-goal chaining or fallback.
- **Bumper products are SUGGESTED, never auto-added.** The module lists them with their own "Add to cart" affordance; the customer chooses to add. An optional custom **button** (status / name / url) can be configured for a call-to-action.
- **Discounts must exist first.** For `free_shipping` and `discount` goals, the module references an existing discount from [[marketing-discounts]] — create the discount before referencing it here.

## Related

- [[apps]] — App Store.
- [[apps-bumpcart-settings]] — settings sub-page.
- [[marketing-discounts]] — discounts referenced by free_shipping / discount goals.
- [[settings-cart]] — cart configuration that interacts with the module.
- [[products-products]] — bumper products picked from catalog.

## How it works (verified against backend)

### Goal threshold logic

Each goal fires the module when the cart is still below its target, and each requires its own field:

| Goal | Fires while cart is below… | Required field |
|---|---|---|
| **amount_cart** | the storewide minimum-order threshold (`checkout_min_price`) | none — gated by `checkout_min_price` |
| **total_cart** | the configured target (`total_cart_amount`) | `total_cart_amount` |
| **free_shipping** | the `order_over` threshold of a `shipping`-type discount | `shipping_discount_id` |
| **discount** | the `order_over` threshold of a `percent` / `flat` discount | `discount_id` |

The referenced discount type is enforced: `free_shipping` needs a `shipping` discount; `discount` needs a `percent` or `flat` discount (not `shipping`). Each goal shows a translatable condition label (e.g., "Spend X more for free shipping").

### Empty / 0 silently disables the module

If a goal is picked but its required field is unset, the module simply does not render (it saves fine). In particular, when `checkout_min_price` defaults to 0 the `amount_cart` goal never fires; the settings UI warns *"You didn't set a Minimum amount for an order"* but still lets the merchant save. Because `amount_cart` reads `checkout_min_price` live, changing the storewide minimum later adjusts the module automatically — no re-save needed.

Amount comparisons are exact (no float-rounding early-trigger), so a 0.99 remainder shows "Add 0.99 more". For `free_shipping`, the gap is measured against the **pre-shipping subtotal**, not the full cart total.

### Bumper product selection

The merchant chooses how products are picked via `filter_group`:
- **`related`** — scope by category / vendor / tag matching the cart's products (uses the Related Products module settings).
- **`product`** — explicit product list (`filter_group_value`).
- **`category` / `vendor` / `tag`** — products from the specified categories / vendors / tags.
- **`all`** — any product in the catalog.

Suggestions are then filtered by:
- **Max price** — `max_price = remaining_gap + (remaining_gap × percent / 100)`, where `percent` is the "Price uplift" setting (default 0). A 20% uplift on a 10 gap caps suggestions at 12 — slightly over the gap, the upsell sweet spot. At `percent = 0` the cap equals the exact gap.
- **Show products** — optional `new` / `featured` / `sale` flag filter (OR logic).
- **Sort by** — `price-high` (default), `price-low`, `date`, `rating`, `comments`, `orders`.

Products already in the cart are always excluded.

### Revenue attribution & stats

Each time a bumper product is added, a stat row is recorded (cart, product, amount, goal text), recorded only ONCE per cart+product pair — re-adding the same product isn't double-counted. On order completion those rows are tagged with the order so the module's revenue can be attributed. Three metrics are tracked over a date range (default last 30 days): **Added products**, **Purchased products**, and **Average amount** (store-wide AOV, with an "increased by" figure for bumper-attributed revenue as a percentage of non-bumper revenue). Note the stats view is **not currently reachable in the UI** (only `apps.bumper_offer.overview` and `apps.bumper_offer.settings` routes exist); the data is collected but surfaces only via maintenance tooling. The `bumpoffer:clear-doublicates` command exists to prune any duplicate stat rows.

### Storefront placement — cart AND checkout

The module renders into `#bumper-offer-modal` and reloads against the cart and checkout DOM targets `.cc-cart-products`, `.js-checkout-summary`, `.js-checkout-authorize`, `.js-checkout-shipping`, `.js-checkout-shipping-address`, and `.js-checkout-payment`. So it appears throughout the checkout flow, re-fetching as the cart total changes (item added/removed, discount applied) to keep progress toward the goal current.

## Open questions

All previously-flagged questions resolved. See body sections.
